---
name: saga-orchestration
description: Use when implementing sagas for distributed transactions, compensating actions, cross-service workflows, long-running business processes, or debugging stuck saga states.
---

# Saga Orchestration

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Coordinating multi-service transactions without two-phase commit
- Designing compensations for partially completed workflows
- Building order, booking, approval, or fulfillment processes
- Debugging stuck, duplicated, or incorrectly compensated saga executions

## Quick Workflow

1. Map service ownership, ordered steps, and the success event for each step.
2. Define idempotent action commands and reverse-order compensation commands.
3. Choose orchestration or choreography based on visibility, coupling, and failure handling needs.
4. Persist saga state transitions with correlation IDs and per-step timeouts.
5. Test failure injection at every step, including duplicate delivery and compensation retries.

## Reference Routing

- Detailed concepts and templates: [references/details.md](references/details.md)
- Advanced implementation patterns: [references/advanced-patterns.md](references/advanced-patterns.md)
- Original source guidance: [references/full-guidance.md](references/full-guidance.md)

## Boundaries

- Use `event-store-design` if saga state must be event-sourced.
- Use `cqrs-implementation` when saga completion feeds read-model updates.

## Expected Output

- Saga state machine or choreography map
- Action and compensation command definitions
- Timeout, retry, DLQ, and monitoring plan
- Failure-mode test checklist
