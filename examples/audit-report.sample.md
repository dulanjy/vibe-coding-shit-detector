# Project Engineering Audit — Fictional Example

> This report is an abbreviated example for the fictional `Acme Catalog API`. Paths and revisions do not refer to a real repository.

## Audit Scope

- Project: Acme Catalog API
- Audited revision: `0123456789abcdef0123456789abcdef01234567`
- Working tree state: clean
- Included evidence: application source, database migrations, tests, Git history, CI workflow, deployment manifest
- Exclusions: managed backup configuration and production alert routing were inaccessible

## Executive Summary

- Detected Type: `BACKEND_SERVICE`
- Lifecycle Stage: `PRODUCTION`
- Criticality: `MEDIUM`
- Engineering Health: `67/100`
- Engineering Classification: `CONTROLLED_VIBE`
- Vibe Slop Risk: `39/100` — `CONTROLLED`
- Evidence Confidence: `78/100`
- Production Readiness: `CONDITIONAL`
- Critical Findings: 0
- Next Highest-Leverage Improvement: enforce catalog write invariants through one service boundary and an integration test

The service has clear API contracts, readable module boundaries, and CI execution. Its largest constraint is that catalog writes enter through both the service layer and an administrative import path, while only the service path has invariant coverage. Backup evidence is inaccessible, so disaster recovery is not assessed as present or absent.

## Classification Basis

| Field | Value | Source | Evidence | Assumptions |
|---|---|---|---|---|
| Type | `BACKEND_SERVICE` | repository-inferred | `src/api/main.py:1-35`, `deploy/service.yaml:1-40` | None |
| Stage | `PRODUCTION` | user-stated + repository-supported | user statement; deployment workflow on `main` | Current workflow remains active |
| Criticality | `MEDIUM` | user-stated | catalog outage disrupts sales but does not process payment | No regulated data is stored |

## Critical Gates

No confirmed blocking gate was triggered. Recovery evidence remains incomplete; this contributes to `CONDITIONAL`, not to a fabricated failure.

## Dimension Scores

| Dimension | Maturity | Weight | Score | Confidence | Rationale |
|---|---:|---:|---:|---:|---|
| Architecture & Boundaries | 4 | 15 | 12.0 | 85 | Primary layering is explicit; CI does not enforce dependencies. |
| Domain & Data Ownership | 3 | 12 | 7.2 | 80 | Ownership is defined, but the importer bypasses one write boundary. |
| Contracts & Type Safety | 4 | 10 | 8.0 | 90 | API and database contracts are typed and validated. |
| Verification & Testing | 3 | 15 | 9.0 | 80 | Critical reads are covered; import-path invariants are not. |
| Change Isolation | 3 | 10 | 6.0 | 75 | History is available; several schema changes co-change with both writers. |
| Observability | 3 | 8 | 4.8 | 70 | Structured logs exist; business correlation is incomplete. |
| Release & Recoverability | 3 | 10 | 6.0 | 55 | Releases are traceable; managed backup evidence is inaccessible. |
| Knowledge Externalization | 4 | 8 | 6.4 | 85 | Setup, data flow, and operating notes are retained in the repository. |
| Security & Configuration | 3 | 7 | 4.2 | 70 | Secrets are externalized; dependency scanning is advisory. |
| Technical Debt & Dependencies | 3 | 5 | 3.0 | 75 | Debt is recorded, but the import bypass has no exit date. |

Total: `66.6`, rounded to `67`.

## Vibe Slop Signals

| Signal | Rating | Evidence |
|---|---:|---|
| Patch Accumulation | 2 | Two retained import compatibility paths |
| Architecture Drift | 1 | One bounded write-path exception |
| Knowledge Dependency | 2 | Backup ownership exists outside accessible evidence |
| Change Blast Radius | 2 | Schema changes touch both writers and related tests |
| Verification Gap | 3 | Import invariants are untested |
| Model Inconsistency | 1 | A legacy field name is translated at the import boundary |
| Unbounded Agent Freedom | 1 | Repository instructions require review, but no architecture gate exists |

Base risk: `34.3`. Production mismatch factor: `1.15`. Final risk: `39`.

## Repository Amnesia Test

- Repository Self-Sufficiency: `MEDIUM`
- A newcomer can locate the service entry point, schema, local run path, tests, and deployment workflow.
- The repository does not contain enough evidence to verify backup ownership, restore testing, or alert routing.

## Controlled Change Test

- Simulated change: add `material_origin` to `Product`
- Predicted modules: product model, API schema, migration, service writer, importer, contract tests, integration tests
- Boundaries crossed: API → domain → persistence; administrative import → persistence
- Unknown dependencies: downstream analytics export ownership
- Verification plan available: partially
- Estimated Blast Radius: `MEDIUM`

## Finding VS-DATA-001 — Administrative import bypasses the catalog write service

- Dimension: Domain & Data Ownership
- Severity / Status / Confidence / Evidence: medium / confirmed / high / E3
- Evidence: `src/importer/catalog_import.py:52-91` writes repository records directly; `src/catalog/service.py:40-88` contains the canonical validation path.
- Impact: import-created products can bypass the `material_origin` and uniqueness invariants.
- Recommendation: route imports through the canonical write service and add an integration test covering an invalid import.
- Acceptance: all catalog writers use the canonical boundary; CI rejects invalid imported records.

## Missing Evidence and Limitations

| Domain | Status | Effect | Resolution |
|---|---|---|---|
| Managed backups | unknown | Recovery maturity and readiness cannot be fully assessed | Provide backup policy and a recent restore exercise record |
| Alert routing | unknown | On-call response cannot be verified | Provide alert configuration and linked runbook |

## Next Highest-Leverage Improvement

- Action: consolidate catalog writes behind one invariant-enforcing boundary and verify the import path in CI.
- Why first: it closes the largest ownership and verification gap while reducing change blast radius.
- Effort: medium
- Acceptance: no direct importer writes; one integration test proves invalid import rejection; CI runs the test.
