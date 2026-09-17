#!/usr/bin/env python3
"""Summarize file hotspots and co-change pairs from local Git history.

The script is read-only and does not inspect commit messages or file contents.
Co-change is a lead for human inspection, not proof of architectural coupling.
"""

from __future__ import annotations

import argparse
import itertools
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath


DEFAULT_EXCLUDES = {
    ".git", ".venv", "venv", "node_modules", "vendor", "dist", "build",
    "target", "coverage", ".next", ".nuxt", ".cache", "__pycache__",
}


def git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or "git command failed"
        raise RuntimeError(message)
    return completed.stdout


def excluded(path: str, excludes: set[str]) -> bool:
    return any(part.lower() in excludes for part in PurePosixPath(path).parts)


def parse_history(raw: str, excludes: set[str]) -> list[tuple[str, list[str]]]:
    commits: list[tuple[str, list[str]]] = []
    for block in raw.split("\x1e"):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        commit = lines[0]
        paths = sorted({line.replace("\\", "/") for line in lines[1:] if not excluded(line.replace("\\", "/"), excludes)})
        commits.append((commit, paths))
    return commits


def analyze(commits: list[tuple[str, list[str]]], top: int, pair_file_limit: int) -> dict:
    file_changes: Counter[str] = Counter()
    pair_changes: Counter[tuple[str, str]] = Counter()
    skipped_large_commits = 0

    for _, paths in commits:
        file_changes.update(paths)
        if len(paths) > pair_file_limit:
            skipped_large_commits += 1
            continue
        pair_changes.update(itertools.combinations(paths, 2))

    hotspots = [
        {"path": path, "commits_changed": count}
        for path, count in file_changes.most_common(top)
    ]
    pairs = []
    for (left, right), together in pair_changes.most_common(top * 4):
        union = file_changes[left] + file_changes[right] - together
        jaccard = together / union if union else 0.0
        pairs.append({
            "left": left,
            "right": right,
            "commits_together": together,
            "jaccard": round(jaccard, 4),
        })
    pairs.sort(key=lambda item: (item["jaccard"], item["commits_together"], item["left"], item["right"]), reverse=True)

    return {
        "commit_count": len(commits),
        "unique_file_count": len(file_changes),
        "skipped_large_commits_for_pairs": skipped_large_commits,
        "hotspots": hotspots,
        "cochange_pairs": pairs[:top],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Git worktree or repository root")
    parser.add_argument("--max-commits", type=int, default=300, help="Maximum commits to inspect")
    parser.add_argument("--since", help="Optional Git date expression, such as '12 months ago'")
    parser.add_argument("--top", type=int, default=30, help="Number of hotspots and pairs to return")
    parser.add_argument("--pair-file-limit", type=int, default=100, help="Skip pair expansion for commits changing more files")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory name to exclude; repeatable")
    parser.add_argument("--json-output", help="Optional output path; stdout is used when omitted")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if args.max_commits < 1 or args.top < 1 or args.pair_file_limit < 2:
        print("error: numeric limits must be positive", file=sys.stderr)
        return 2

    try:
        repository_root = Path(git(root, "rev-parse", "--show-toplevel").strip()).resolve()
        revision = git(repository_root, "rev-parse", "HEAD").strip()
        command = [
            "log", f"--max-count={args.max_commits}", "--no-renames",
            "--format=%x1e%H", "--name-only",
        ]
        if args.since:
            command.append(f"--since={args.since}")
        raw = git(repository_root, *command)
    except RuntimeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    excludes = {item.lower() for item in DEFAULT_EXCLUDES}
    excludes.update(item.lower() for item in args.exclude)
    commits = parse_history(raw, excludes)
    metrics = analyze(commits, args.top, args.pair_file_limit)
    result = {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository_root": str(repository_root),
        "revision": revision,
        "history_window": {"max_commits": args.max_commits, "since": args.since},
        **metrics,
        "limitations": [
            "Co-change is a candidate signal and does not prove architectural coupling.",
            "Renames are not followed; generated and excluded directories are omitted.",
            "Large commits are counted as hotspots but may be skipped for pair expansion.",
        ],
    }
    if len(commits) < 2:
        result["limitations"].append("Fewer than two commits were available; coupling evidence is insufficient.")

    encoded = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.json_output:
        output = Path(args.json_output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    else:
        sys.stdout.write(encoded)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
