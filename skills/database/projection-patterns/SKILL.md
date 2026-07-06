---
name: projection-patterns
description: Use when building projections, materialized views, read models, search indexes, or dashboards from event streams in CQRS/event-sourced systems.
---

# Projection Patterns

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Creating read models from domain events
- Rebuilding materialized views or search indexes
- Designing projection checkpoints, lag monitoring, and replay behavior
- Choosing inline, live, catch-up, or persistent projection patterns

## Quick Workflow

1. Start from query/read-model requirements, not from event structure alone.
2. Pick projection mode: inline for stronger consistency, async for scale, catch-up for rebuilds.
3. Make handlers idempotent and order-aware.
4. Store checkpoints with enough metadata to resume safely.
5. Add lag/error monitoring and a documented rebuild path.

## Reference Routing

- Detailed templates and examples: [references/details.md](references/details.md)
- Original source guidance: [references/full-guidance.md](references/full-guidance.md)

## Boundaries

- Use `event-store-design` for event storage and subscription infrastructure.
- Use `cqrs-implementation` for broader command/query separation.

## Expected Output

- Projection type and handler design
- Read-model schema or index shape
- Checkpoint, idempotency, and replay plan
- Monitoring and rebuild guidance
