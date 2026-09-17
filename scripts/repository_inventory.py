#!/usr/bin/env python3
"""Create a deterministic, content-free repository inventory.

The script reads file metadata and path names only. It never imports repository
code or reads file contents, which makes it suitable for an audit discovery pass.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


DEFAULT_EXCLUDES = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".venv",
    "venv",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    "coverage",
    ".next",
    ".nuxt",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    "__pycache__",
}

CATEGORY_PATTERNS = {
    "documentation": {
        "readme.md", "contributing.md", "architecture.md", "security.md",
        "runbook.md", "agents.md", "changelog.md",
    },
    "manifests": {
        "package.json", "pyproject.toml", "requirements.txt", "poetry.lock",
        "uv.lock", "cargo.toml", "cargo.lock", "go.mod", "go.sum",
        "pom.xml", "build.gradle", "build.gradle.kts", "composer.json",
        "gemfile", "mix.exs", "pubspec.yaml",
    },
    "containers": {
        "dockerfile", "compose.yaml", "compose.yml", "docker-compose.yaml",
        "docker-compose.yml",
    },
    "infrastructure": {
        "terraform.tf", "serverless.yml", "serverless.yaml", "pulumi.yaml",
        "helmfile.yaml", "helmfile.yml", "fly.toml", "vercel.json",
        "netlify.toml",
    },
}

EXTENSION_LANGUAGES = {
    ".py": "Python", ".pyi": "Python", ".js": "JavaScript",
    ".jsx": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".java": "Java",
    ".kt": "Kotlin", ".kts": "Kotlin", ".go": "Go", ".rs": "Rust",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".fs": "F#",
    ".cpp": "C++", ".cc": "C++", ".cxx": "C++", ".c": "C",
    ".h": "C/C++ Header", ".hpp": "C/C++ Header", ".swift": "Swift",
    ".scala": "Scala", ".ex": "Elixir", ".exs": "Elixir",
    ".vue": "Vue", ".svelte": "Svelte", ".sql": "SQL",
    ".sh": "Shell", ".ps1": "PowerShell",
}


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def bounded_sorted(values: Iterable[str], limit: int) -> list[str]:
    return sorted(set(values))[:limit]


def classify_path(relative: str, name: str) -> set[str]:
    lower = relative.lower()
    lower_name = name.lower()
    parts = set(Path(lower).parts)
    categories: set[str] = set()

    for category, candidates in CATEGORY_PATTERNS.items():
        if lower_name in candidates:
            categories.add(category)

    if lower.startswith(".github/workflows/") or lower_name in {
        ".gitlab-ci.yml", "azure-pipelines.yml", "jenkinsfile", "circle.yml"
    }:
        categories.add("ci")
    if any(part in {"test", "tests", "spec", "specs", "__tests__"} for part in parts) or lower_name.startswith("test_") or lower_name.endswith(("_test.py", ".spec.ts", ".test.ts", ".spec.js", ".test.js")):
        categories.add("tests")
    if any(part in {"migration", "migrations", "alembic", "flyway", "liquibase"} for part in parts):
        categories.add("migrations")
    if any(part in {"deploy", "deployment", "k8s", "kubernetes", "helm", "terraform", "infra", "infrastructure"} for part in parts):
        categories.add("infrastructure")
    if any(part in {"docs", "doc", "adr", "adrs", "runbooks"} for part in parts) or Path(lower).suffix in {".md", ".rst", ".adoc"}:
        categories.add("documentation")
    if lower_name.startswith(".env") or lower_name in {"secrets.yaml", "secrets.yml", "credentials.json"}:
        categories.add("sensitive_name_candidates")
    return categories


def inventory(root: Path, excludes: set[str], sample_limit: int) -> dict:
    extension_counts: Counter[str] = Counter()
    language_counts: Counter[str] = Counter()
    category_paths: dict[str, list[str]] = defaultdict(list)
    top_level_counts: Counter[str] = Counter()
    file_count = 0
    total_bytes = 0
    inaccessible: list[str] = []

    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d.lower() not in excludes)
        current_path = Path(current)
        for filename in sorted(files):
            path = current_path / filename
            try:
                if path.is_symlink():
                    continue
                stat = path.stat()
            except OSError:
                inaccessible.append(relative_posix(path, root))
                continue

            relative = relative_posix(path, root)
            file_count += 1
            total_bytes += stat.st_size
            extension = path.suffix.lower() or "[no extension]"
            extension_counts[extension] += 1
            language = EXTENSION_LANGUAGES.get(path.suffix.lower())
            if language:
                language_counts[language] += 1
            top_level_counts[relative.split("/", 1)[0]] += 1
            for category in classify_path(relative, filename):
                category_paths[category].append(relative)

    return {
        "schema_version": "0.1",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "root": str(root),
        "method": "path and file metadata only; repository contents were not read",
        "excluded_directory_names": sorted(excludes),
        "summary": {
            "file_count": file_count,
            "total_bytes": total_bytes,
            "inaccessible_file_count": len(inaccessible),
        },
        "languages_by_file_count": dict(language_counts.most_common()),
        "extensions_by_file_count": dict(extension_counts.most_common(30)),
        "top_level_entries_by_file_count": dict(top_level_counts.most_common()),
        "evidence_candidates": {
            key: bounded_sorted(paths, sample_limit)
            for key, paths in sorted(category_paths.items())
        },
        "inaccessible_paths": bounded_sorted(inaccessible, sample_limit),
        "limitations": [
            "Path classification identifies inspection candidates, not findings.",
            "Generated directories are excluded by name and may contain relevant custom code.",
            "Language counts are based on filename extensions only.",
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--exclude", action="append", default=[], help="Additional directory name to exclude; repeatable")
    parser.add_argument("--sample-limit", type=int, default=200, help="Maximum paths retained per category")
    parser.add_argument("--json-output", help="Optional output path; stdout is used when omitted")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"error: repository root is not a directory: {root}", file=sys.stderr)
        return 2
    if args.sample_limit < 1:
        print("error: --sample-limit must be positive", file=sys.stderr)
        return 2

    excludes = {item.lower() for item in DEFAULT_EXCLUDES}
    excludes.update(item.lower() for item in args.exclude)
    result = inventory(root, excludes, args.sample_limit)
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
