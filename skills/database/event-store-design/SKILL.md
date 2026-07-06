---
name: event-store-design
description: Use when designing event stores for event-sourced systems, choosing storage technology, modeling streams, or implementing append-only event persistence and subscriptions.
---

# Event Store Design

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Designing append-only event persistence
- Choosing between EventStoreDB, PostgreSQL, Kafka, DynamoDB, or framework-specific stores
- Modeling streams, global positions, optimistic concurrency, and subscriptions
- Planning event schema versioning, idempotency, retention, and replay

## Quick Workflow

1. Identify aggregate streams, event ordering requirements, and read patterns.
2. Choose storage based on stream reads, global ordering, subscriptions, and operations constraints.
3. Define event envelope fields: id, stream id, version, type, payload, metadata, correlation, causation.
4. Enforce append-only writes with optimistic concurrency and idempotency keys.
5. Plan subscriptions, replay, retention, and migration/versioning before production use.

## Reference Routing

- Detailed templates and examples: [references/details.md](references/details.md)
- Original source guidance: [references/full-guidance.md](references/full-guidance.md)

## Boundaries

- Use `projection-patterns` for read-model rebuilds and checkpointing.
- Use `cqrs-implementation` for command/query application boundaries.

## Expected Output

- Event store schema or technology recommendation
- Stream and event envelope design
- Concurrency/idempotency strategy
- Replay, subscription, and operational caveats
