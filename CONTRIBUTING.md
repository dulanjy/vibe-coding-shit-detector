# Contributing

Contributions should improve audit reliability, evidence discipline, portability, or usability without turning the default audit into a remediation agent.

## Useful contributions

- A reproducible false positive or false negative.
- A case where `UNKNOWN` was incorrectly treated as failure.
- Inconsistent scoring from equivalent evidence.
- A project classification that changes a gate unexpectedly.
- A helper-script portability or performance issue.
- A sample or acceptance criterion that makes a finding easier to verify.

Avoid adding generic best-practice lists, framework preferences, or keyword-only findings. New hard gates require a concrete failure consequence, a narrow applicability rule, evidence requirements, and a clearance condition.

## Before opening a pull request

1. Keep the audited-repository boundary read-only by default.
2. Put shared routing and constraints in `SKILL.md`; put conditional detail in `references/`.
3. Add or update an observable behavior test when changing scripts or the output contract.
4. Do not commit real credentials, private repository content, or customer audit evidence.
5. Run:

   ```bash
   python -m pip install -r requirements-dev.txt
   python -m unittest discover -s tests -v
   ```

6. If Codex's skill validator is available, also run `quick_validate.py` against the repository root.

## Pull request notes

Explain:

- the failure or limitation being addressed;
- the smallest representative example;
- why the change improves evidence quality rather than preferred wording;
- any compatibility or scoring impact.

Changes to weights, thresholds, or gates should include calibration evidence or remain explicitly experimental.
