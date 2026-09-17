# Report and finding contract

Use [../assets/audit-report-template.md](../assets/audit-report-template.md) for the human report and validate machine output against [../assets/audit-result.schema.json](../assets/audit-result.schema.json).

## Stable finding shape

```yaml
id: VS-ARCH-003
title: Retrieval layer imports ingestion internals
dimension: architecture_boundaries
severity: high
status: confirmed
confidence: high
evidence_level: E3
evidence:
  - path: src/retrieval/service.py
    lines: 8-12
    observation: Imports an ingestion-internal parser.
expected:
  - Retrieval depends only on normalized or indexed-data interfaces.
impact:
  - Reverse dependency and increased change coupling.
recommendation:
  action: Introduce an explicit retrieval data interface.
  effort: medium
  expected_effect:
    - Prevent ingestion implementation changes from leaking into retrieval.
acceptance:
  - No retrieval module imports ingestion internals.
  - An architecture check rejects future violations.
```

Do not promise a numeric score improvement for a proposed change unless it is recomputed by a later audit. Use stable IDs with a dimension prefix when possible.

Allowed finding statuses: `confirmed`, `probable`, `unknown`, `not_applicable`, `resolved`.

Recommended severity meanings:

- `critical`: plausible severe security, irreversible data, safety, or release-blocking consequence.
- `high`: material reliability, integrity, maintainability, or operating risk needing prompt action.
- `medium`: bounded but meaningful weakness that increases cost or failure likelihood.
- `low`: localized improvement with limited near-term consequence.

## Required report contents

- Audited scope, timestamp, branch/SHA, dirty-state note, and exclusions.
- Classification and the evidence source for each field.
- Four separate headline conclusions.
- Critical gates before dimension details.
- All dimension ratings, effective weights, scores, confidence, and rationales.
- All seven Vibe Slop signals and mismatch factor.
- Repository Amnesia Test and Controlled Change Test.
- Findings with reproducible evidence.
- Missing evidence and limitations.
- One highest-leverage improvement and no more than five roadmap items.

## Consistency checks

Before delivery:

1. Recalculate totals from raw ratings and effective weights.
2. Ensure health classification and risk level match the published ranges.
3. Ensure every confirmed gate has evidence and a clearance condition.
4. Ensure `UNKNOWN` areas lower confidence rather than health automatically.
5. Ensure report and JSON contain the same headline values and finding IDs.
6. Ensure no secret values or unnecessary personal data appear in either output.
