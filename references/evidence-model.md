# Evidence and confidence model

## Evidence levels

| Level | Meaning | Examples |
|---|---|---|
| `E4` | Automatically executed or platform-enforced evidence | Required CI gate, architecture test, reproducible test result, protected deployment rule |
| `E3` | Code or configuration evidence | Schema, type, dependency rule, state machine, migration or rollback implementation |
| `E2` | Repository documentation evidence | ADR, architecture document, runbook, data ownership record |
| `E1` | Naming or weak signal | Filename, comment, TODO, directory layout, keyword match |
| `E0` | No accessible evidence | Assumption, unavailable external system, inaccessible history |

Documentation cannot receive the same maturity credit as automated enforcement. When documentation conflicts with executable behavior, prefer executable evidence, record drift, and reduce consistency confidence.

## Claim discipline

- `confirmed`: directly supported by consistent E3/E4 evidence, or multiple mutually supporting lower-level sources.
- `probable`: supported by incomplete or indirect evidence; name the missing confirmation.
- `unknown`: evidence is inaccessible or insufficient.
- `not_applicable`: the responsibility genuinely does not apply to the classified project.
- `resolved`: historical finding with current evidence demonstrating closure.

Never convert inaccessible evidence into a confirmed negative. Keyword matches, file size, test counts, framework choice, and directory names can select inspection targets but cannot create findings by themselves.

## Evidence Confidence

Score each factor from 0 to 100, then calculate the weighted mean:

| Factor | Weight | Question |
|---|---:|---|
| Repository Coverage | 30% | Were the important source, configuration, docs, and generated-code boundaries inspected? |
| Executable Evidence Coverage | 25% | Were critical claims supported by tests, gates, or repeatable commands? |
| Git History Availability | 15% | Was enough history available to assess change coupling and drift? |
| CI/Release Evidence Availability | 15% | Were gate and release behaviors visible rather than merely described? |
| Infrastructure/Operations Evidence | 10% | Were runtime, recovery, and operating controls accessible? |
| Evidence Consistency | 5% | Did code, docs, tests, and configuration agree? |

Round the final score to the nearest integer and retain factor scores in the JSON result.

| Score | Interpretation |
|---:|---|
| 85–100 | High confidence; suitable for a formal engineering review. |
| 65–84 | Moderate confidence; useful for governance decisions with named verification gaps. |
| 40–64 | Limited confidence; use as triage only. |
| 0–39 | Insufficient evidence; do not issue a definitive overall verdict. |

## Evidence references

Prefer precise, reproducible references:

- repository path and line or narrow range;
- command plus exit code and relevant result summary;
- commit range plus changed-path observation;
- configuration key without secret value;
- explicit missing domain and why it could not be inspected.

Do not paste credentials, tokens, personal data, or large source excerpts into the report.
