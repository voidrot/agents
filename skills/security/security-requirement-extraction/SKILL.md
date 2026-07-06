---
name: security-requirement-extraction
description: Use when turning threat models, audits, compliance obligations, incidents, or architecture reviews into specific, testable security requirements and acceptance criteria.
---

# Security Requirement Extraction

Use this skill as the activation and routing layer for security requirement extraction work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Collect inputs: threats, assets, regulations, policies, architecture boundaries, existing controls, and product constraints.
2. Translate each risk or obligation into an actionable requirement with actor, system behavior, condition, and measurable outcome.
3. Attach priority, rationale, owner, verification method, and traceability back to the source threat or obligation.
4. Remove vague requirements; split broad controls into testable acceptance criteria.
5. Return a requirement matrix with assumptions, dependencies, and open questions.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for extraction templates and example requirement matrices.
- references/quick-reference.md for the original process summary.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
