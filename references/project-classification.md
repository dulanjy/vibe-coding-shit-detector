# Project classification

Classify the responsibility the project actually carries, not the label that makes it look best. Record the evidence and source of every classification.

## Project type

Choose one primary type and optional secondary types:

| Type | Distinguishing responsibility |
|---|---|
| `PROTOTYPE` | Tests a concept; disposal is acceptable and continued operation is not promised. |
| `SCRIPT` | Bounded automation with a narrow invocation and output. |
| `LIBRARY` | Publishes a reusable API and compatibility contract. |
| `CLI` | Provides an operator-facing command interface and local execution contract. |
| `INTERNAL_TOOL` | Supports a bounded internal workflow and known users. |
| `WEB_APPLICATION` | Serves interactive users through a browser-facing application. |
| `DATA_PIPELINE` | Moves or transforms durable data with correctness and replay concerns. |
| `AI_AGENT` | Chooses or executes actions with model-driven variability and tool permissions. |
| `BACKEND_SERVICE` | Exposes a network contract and owns operational availability or data. |
| `DISTRIBUTED_SYSTEM` | Coordinates independently deployed components and failure domains. |

## Lifecycle stage

| Stage | Evidence to look for |
|---|---|
| `EXPERIMENT` | Explicitly disposable exploration, no continuing users or operating duty. |
| `MVP` | Narrow validated scope, early users, accepted temporary constraints. |
| `ACTIVE_DEVELOPMENT` | Ongoing feature work and a maintained compatibility surface. |
| `PRODUCTION` | Real users, durable data, service obligations, or recurring operations. |
| `MATURE` | Stable responsibility, controlled evolution, established operations. |
| `LEGACY` | Continuing responsibility with constrained change or replacement trajectory. |

Do not classify a system as experimental merely because its engineering controls are weak. Production responsibility is established by actual users, data, deployment, or business dependence.

## Criticality

| Level | Consequence of failure |
|---|---|
| `LOW` | Easy to repeat or discard; little user, financial, privacy, or operational impact. |
| `MEDIUM` | Material workflow disruption, limited data loss, or recoverable customer impact. |
| `HIGH` | Significant customer, financial, privacy, integrity, or availability impact. |
| `CRITICAL` | Safety, regulated, irreversible financial, identity, or organization-wide impact. |

Increase criticality only with evidence. If consequences are unclear, mark `UNKNOWN` and state which facts would resolve it.

## Applicability adjustments

The ten health dimensions remain visible, but a responsibility can be not applicable. For example, a local one-shot CLI may not need a production deployment platform. Mark that dimension `not_applicable`, explain why, and redistribute its weight proportionally across applicable dimensions. Never silently award full points for missing responsibility.

When several plausible classifications materially change the audit, show the alternatives and their consequences. Otherwise choose the best-supported classification and continue with a labeled assumption.
