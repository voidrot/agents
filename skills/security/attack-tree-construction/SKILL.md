---
name: attack-tree-construction
description: Use when building or reviewing attack trees to map attacker goals, OR/AND paths, defense gaps, likelihood, cost, detection, and risk communication for security architecture or penetration-test planning.
---

# Attack Tree Construction

Use this skill as the activation and routing layer for attack tree construction work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Define the root attacker goal, target asset, assumed attacker capability, and scope boundaries.
2. Break the goal into OR/AND subgoals until leaf actions are concrete enough to assess.
3. Annotate leaves with preconditions, cost, skill, time, likelihood, detection, impact, and existing controls.
4. Identify least-resistance paths, missing mitigations, and defense-in-depth gaps.
5. Return the tree plus prioritized remediation and assumptions that need validation.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for templates and worked examples.
- references/quick-reference.md for the original compact guidance and node attribute tables.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
