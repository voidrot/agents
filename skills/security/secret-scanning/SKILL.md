---
name: secret-scanning
description: Use when enabling, configuring, or troubleshooting secret scanning, push protection, custom secret patterns, alert triage, remediation, or pre-commit checks for leaked credentials in repositories and CI/CD workflows.
---

# Secret Scanning

Use this skill as the activation and routing layer for secret scanning work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Identify the platform scope: repository, organization, enterprise, local pre-commit workflow, or CI/CD pipeline.
2. Enable or verify secret scanning and push protection according to the platform plan and repository visibility.
3. Configure custom patterns and exclusions cautiously; avoid suppressing real secret locations without documented risk acceptance.
4. Triage alerts by validating exposure, rotating/revoking credentials, removing history exposure when appropriate, and documenting dismissal reasons.
5. Add prevention controls such as secret managers, environment protections, pre-commit scans, and developer guidance.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/full-guidance.md for detailed setup, commands, and decision tables.
- references/alerts-and-remediation.md for alert handling.
- references/custom-patterns.md for custom detector design.
- references/push-protection.md for blocked-push workflows.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
