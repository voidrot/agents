---
name: stride-analysis-patterns
description: Use when applying STRIDE threat modeling to systems, features, diagrams, APIs, data flows, or architecture reviews to identify spoofing, tampering, repudiation, information disclosure, denial of service, and elevation-of-privilege risks.
---

# Stride Analysis Patterns

Use this skill as the activation and routing layer for stride analysis patterns work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Define the feature, assets, actors, trust boundaries, data stores, processes, and data flows.
2. Walk each element through STRIDE categories and record credible threats, not generic possibilities.
3. Tie each threat to evidence: affected flow, attacker capability, preconditions, impact, and existing controls.
4. Prioritize by risk and map mitigations, tests, owners, and unresolved assumptions.
5. Return a concise threat table and escalation items for high-risk gaps.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for STRIDE templates and examples.
- references/quick-reference.md for the original category overview.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
