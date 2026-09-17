# Critical gates

Apply gates after scoring and before the executive conclusion. A gate requires a trigger, applicability, evidence, severity, readiness impact, and clearance condition. Never emit a vague gate warning.

| Gate ID | Trigger | Default severity | Readiness impact | Typical applicability | Clearance condition |
|---|---|---|---|---|---|
| `CG-DATA-OWNERSHIP` | Core durable data has no identifiable authority, or independent writers can bypass the same invariant. | critical | `BLOCKED` | Data systems, production services, AI agents | Establish authoritative ownership and enforce write paths/invariants. |
| `CG-NO-EXEC-VERIFY` | No executable evidence can verify any critical behavior. | high | `BLOCKED` | Systems carrying production responsibility | Add reproducible verification for critical behavior and make results inspectable. |
| `CG-DESTRUCTIVE-MIGRATION` | A destructive production migration lacks a verified backup, forward-compatible path, rollback, or recovery plan. | critical | `BLOCKED` | Persistent production systems | Demonstrate a safe migration and tested recovery path. |
| `CG-LIVE-CREDENTIAL` | A credential in repository history or current content appears valid or plausibly usable. | critical | `BLOCKED` | All projects | Revoke/rotate, remove exposure where feasible, and add prevention. Never test the credential. |
| `CG-AUTH-BYPASS` | An evidenced path bypasses required authentication or authorization. | critical | `BLOCKED` | Systems with access control | Close the bypass and demonstrate access-control regression coverage. |
| `CG-UNTRACEABLE-RELEASE` | A deployed production version cannot be tied to a source revision and build artifact. | high | `BLOCKED` | Production systems | Establish verifiable source-build-release provenance. |
| `CG-OPAQUE-CRITICAL-FAILURE` | A critical workflow cannot identify failure stage or terminal outcome. | high | `CONDITIONAL` or `BLOCKED` | High-criticality workflows | Add evidence that terminal status and failure stage are observable. |
| `CG-DOC-EXEC-CONFLICT` | A documented safety or governance rule conflicts with executable behavior. | varies | depends on affected responsibility | All projects | Reconcile behavior and documentation; enforce the intended rule where required. |

## Gate decision rules

- Confirm applicability from project classification and real responsibility.
- Use `confirmed` only with direct evidence. A suspected credential or bypass can be a high-priority finding without activating a confirmed gate.
- Security-sensitive validation must remain non-invasive. Do not authenticate with found secrets, exploit endpoints, or change access state.
- Multiple gates do not average together. The most restrictive applicable confirmed impact controls readiness.
- `READY` requires no blocking gate, adequate evidence for the project's responsibility, and no unmitigated critical finding.
- `CONDITIONAL` must name every condition and its acceptance evidence.
- Use `NOT_ASSESSED` when production responsibility or operational evidence is insufficient to reach a defensible decision.
