---
name: cqrs-implementation
description: Use when separating command/write models from query/read models, implementing CQRS handlers, designing eventual-consistency boundaries, or pairing CQRS with event sourcing.
---

# CQRS Implementation

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Separating write-side commands from read-side queries
- Building independent read models for reporting, search, or dashboards
- Defining command/query handlers and projection handoffs
- Deciding whether CQRS is worth the operational complexity

## Quick Workflow

1. Confirm the domain has distinct write and read pressures.
2. Define commands, command handlers, queries, and query handlers separately.
3. Choose consistency expectations and projection lag budgets.
4. Design read models around actual query shapes.
5. Add idempotency, event versioning, and rebuild paths before scaling out.

## Reference Routing

- Detailed templates and examples: [references/details.md](references/details.md)
- Original source guidance: [references/full-guidance.md](references/full-guidance.md)

## Boundaries

- Use `projection-patterns` for projection-specific implementation details.
- Use `event-store-design` for event persistence and stream storage decisions.

## Expected Output

- Command/query boundary proposal
- Read-model and projection design
- Consistency and rebuild notes
- Implementation risks and verification checks
