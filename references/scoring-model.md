# Scoring model

## Engineering Health

Rate each applicable dimension from 0 to 5:

| Maturity | Meaning |
|---:|---|
| 0 | Absent, or the critical responsibility is completely unknown. |
| 1 | Ad hoc and dependent on individual memory or manual intervention. |
| 2 | Partly defined, mostly through documentation or convention. |
| 3 | Explicitly defined and used on primary paths. |
| 4 | Reliably enforced by code, review, or repeatable process. |
| 5 | Continuously enforced by automated checks, CI, or platform controls. |

For each rating, cite evidence and explain why it is not one level higher or lower. An `unknown` dimension is not zero: keep it unscored, lower confidence, and disclose the coverage gap. A genuinely `not_applicable` dimension is removed and its weight redistributed proportionally.

`weighted score = maturity / 5 × effective weight`

| Dimension | Weight | Primary question |
|---|---:|---|
| Architecture & Boundaries | 15 | Are responsibilities and dependency directions clear and enforceable? |
| Domain & Data Ownership | 12 | Is each core fact governed by an identifiable owner and write policy? |
| Contracts & Type Safety | 10 | Are interactions, errors, side effects, and state transitions explicit? |
| Verification & Testing | 15 | Can critical behavior and business invariants be demonstrated? |
| Change Isolation | 10 | Is the impact of an ordinary change predictable? |
| Observability | 8 | Can a failure's input, stage, state, and outcome be reconstructed? |
| Release & Recoverability | 10 | Can change be released, traced, rolled back, restored, or replayed safely? |
| Knowledge Externalization | 8 | Does retained project evidence replace author or chat memory? |
| Security & Configuration | 7 | Are access, secrets, input, dependencies, and environments controlled? |
| Technical Debt & Dependencies | 5 | Is debt visible, bounded, owned, and retired deliberately? |

| Score | Classification |
|---:|---|
| 90–100 | `ROBUST` |
| 80–89 | `MAINTAINABLE` |
| 70–79 | `MAINTAINABLE_WITH_DEBT` |
| 55–69 | `CONTROLLED_VIBE` |
| 40–54 | `VIBE_RISK` |
| 20–39 | `VIBE_SLOP` |
| 0–19 | `STRUCTURALLY_UNSAFE` |

Classification describes capability only. It never cancels a critical gate.

## Dimension inspection prompts

- **Architecture & Boundaries:** dependency cycles, cross-layer calls, business rules in transport handlers, boundaryless shared modules, architecture tests, documented-versus-real topology.
- **Domain & Data Ownership:** authoritative sources, writers, lifecycle, state transitions, invariant enforcement, bypass paths.
- **Contracts & Type Safety:** validated input/output, error taxonomy, versioning, compatibility, contract tests, critical uses of unvalidated dynamic structures.
- **Verification & Testing:** invariant coverage, appropriate test levels, reproducibility, gate enforcement, controlled test data, regression evidence, real integration debt.
- **Change Isolation:** change-coupling, hotspots, extension points, unrelated co-change, regression patterns. Without history, label structural inference and reduce confidence.
- **Observability:** structured signals, correlation, stage/outcome reconstruction, redaction, actionable alerts and runbooks.
- **Release & Recoverability:** environment isolation, approvals, traceability, health checks, flags, migration compatibility, backup, rollback, replay, idempotency, exercises.
- **Knowledge Externalization:** purpose, run/verify path, data flow, decisions and rationale, operational knowledge, rules moving from prose into enforcement.
- **Security & Configuration:** credentials, authorization boundaries, input validation, environment separation, dependency/supply-chain checks, least privilege.
- **Technical Debt & Dependencies:** repeated workaround patterns, duplication, dead code, oversized responsibility, obsolete dependencies, debt ownership and exit criteria.

## Vibe Slop Risk

Rate each signal from 0 (no supported systemic risk) to 5 (severe, repeated, confirmed risk):

1. Patch Accumulation
2. Architecture Drift
3. Knowledge Dependency
4. Change Blast Radius
5. Verification Gap
6. Model Inconsistency
7. Unbounded Agent Freedom

Use equal weights in version 0.1:

`base risk = sum(signal / 5 × 100 / 7)`

Apply one evidence-backed responsibility mismatch factor:

| Factor | Use when |
|---:|---|
| 0.7 | Disposable experiment or one-shot low-criticality work |
| 0.9 | MVP or bounded internal tool with consciously accepted controls |
| 1.0 | Responsibility is unknown or governance broadly matches current duty |
| 1.15 | Active or production responsibility has material control gaps |
| 1.3 | High-criticality production duty lacks important baseline controls |
| 1.5 | Critical responsibility lacks foundational ownership, verification, or recovery controls |

Use factors above 1 only when actual responsibility is evidenced. Record the chosen factor and rationale. `risk = min(100, base risk × factor)`, rounded to the nearest integer.

| Risk | Level |
|---:|---|
| 0–19 | `LOW` |
| 20–39 | `CONTROLLED` |
| 40–59 | `MATERIAL` |
| 60–79 | `HIGH` |
| 80–100 | `SEVERE` |
