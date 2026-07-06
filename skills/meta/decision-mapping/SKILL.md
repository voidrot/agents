---
name: decision-mapping
description: Use when a loose idea has multiple unresolved decisions that must be mapped, sequenced, and resolved across one or more focused sessions.
disable-model-invocation: true
---

# Decision Mapping

Create and maintain a compact Markdown decision map for a planning effort with many unknowns. The map is the canonical artifact and should stay small enough to load in every follow-up session.

## Scope Boundaries

- Use this skill to sequence unresolved decisions, not to perform the whole implementation.
- Use `grilling` for conversational pressure-testing of one decision.
- Use `domain-modeling` when terminology or ADRs crystallize while resolving decisions.
- Use `handoff` only for session transfer; this skill owns the decision map itself.

## Workflow

1. If no map exists, interview just enough to identify the decision frontier, write the map, and stop.
2. If a map exists, load the whole map, choose the requested ticket or first unblocked open ticket, mark it `in-progress`, and save before working.
3. Resolve exactly one ticket using research, prototyping, grilling, or domain modeling as needed.
4. Record the answer, mark the ticket `resolved`, and add any newly discovered blocked tickets.
5. End with copy-paste next steps for one-session or parallel follow-up.

## Constraints

- Never resolve more than one ticket per session.
- Keep assets linked from the map, not duplicated inside it.
- Expect other agents may edit the map; claim tickets before work.

## Supporting Material

- Read `references/decision-map-workflow.md` for the full ticket schema, status rules, handoff text, and examples.
