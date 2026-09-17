# Software Engineering Health Audit

An evidence-based Codex skill for assessing whether a software project can be understood, changed, verified, operated, and recovered without relying on chat history or one author's memory.

It keeps four conclusions separate:

- **Engineering Health** — the maturity of ten engineering capabilities.
- **Vibe Slop Risk** — the mismatch between actual responsibility and governance.
- **Evidence Confidence** — how well the conclusions are supported.
- **Production Readiness** — `NOT_ASSESSED`, `BLOCKED`, `CONDITIONAL`, or `READY`.

The default mode is read-only. The skill does not refactor code, install dependencies, change infrastructure, or turn recommendations into claimed fixes.

## Why this is different

The audit classifies the project before scoring it, distinguishes `UNKNOWN` from `FAIL`, and lets critical security, data, verification, or recovery gates override averages. File counts, TODOs, dynamic types, framework choices, and test counts are treated as inspection leads rather than verdicts.

Two practical tests anchor the assessment:

1. **Repository Amnesia Test:** could a capable newcomer take over using retained project evidence alone?
2. **Controlled Change Test:** can an ordinary change be traced to predictable owners, boundaries, verification, and recovery?

## Install

Clone the repository into your Codex skills directory:

```bash
git clone https://github.com/dulanjy/software-engineering-health-audit.git ~/.codex/skills/software-engineering-health-audit
```

On Windows PowerShell:

```powershell
git clone https://github.com/dulanjy/software-engineering-health-audit.git "$env:USERPROFILE\.codex\skills\software-engineering-health-audit"
```

Restart or refresh Codex skill discovery after installation.

## Use

Invoke the skill explicitly:

```text
Use $software-engineering-health-audit to perform a read-only audit of this repository.
```

By default, the deliverables are:

- `audit-report.md` for people
- `audit-result.json` for automation, validated against the bundled JSON Schema

The skill may also be discovered automatically for repository engineering-health, takeover-readiness, architecture-drift, governance-gap, and Vibe Slop audit requests.

## Optional read-only helpers

Create a content-free inventory of repository paths and file metadata:

```bash
python scripts/repository_inventory.py /path/to/repository
```

Summarize local Git hotspots and file co-change pairs:

```bash
python scripts/git_change_coupling.py /path/to/repository --max-commits 300
```

The helper outputs are discovery evidence, not automatic findings. Both scripts use only the Python standard library and do not execute repository code.

## Scope and limitations

- Version `0.1` is a repository-grounded audit framework, not a universal static analyzer.
- Production readiness requires accessible operational and release evidence; otherwise it remains `NOT_ASSESSED`.
- Generic dependency graphs across every language are intentionally out of scope. Use project-native analyzers when available and authorized.
- Initial weights and thresholds should be calibrated against varied real repositories and independent reviewers before organization-wide benchmarking.

## License

[MIT](LICENSE)
