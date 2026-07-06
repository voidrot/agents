---
name: threat-mitigation-mapping
description: Use when converting identified threats into preventive, detective, corrective, and compensating controls; prioritizing remediation; validating coverage; or building a risk treatment roadmap.
---

# Threat Mitigation Mapping

Use this skill as the activation and routing layer for threat mitigation mapping work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. List threats with affected assets, attacker paths, likelihood, impact, and current controls.
2. Map each threat to layered controls across application, data, identity, infrastructure, endpoint, monitoring, and process layers.
3. Classify controls as preventive, detective, corrective, or compensating and note ownership and verification method.
4. Score residual risk, implementation effort, dependencies, and expected effectiveness.
5. Produce a prioritized roadmap with gaps, quick wins, long-term controls, and validation tests.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for mitigation templates, control mappings, and roadmap examples.
- references/quick-reference.md for the original control category overview.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
