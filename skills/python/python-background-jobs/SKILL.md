---
name: python-background-jobs
description: "Use for Python queue/worker systems: background jobs, retries, idempotency, job status, dead-letter queues, and worker operations."
---

# Python Background Jobs & Task Queues

Use this skill to design queue-backed work that runs outside the request/response cycle and can be retried, monitored, and recovered.

## When to Use

- Offloading slow or unreliable work from an API request
- Sending emails, webhooks, notifications, reports, exports, or media processing jobs
- Designing job status polling, retries, idempotency, and dead-letter handling
- Choosing between Celery, RQ, Dramatiq, or cloud-native queues
- Operating workers and monitoring queue backlog

## Boundaries

- Use `async-python-patterns` for in-process `asyncio` concurrency and non-blocking I/O.
- Use `django-celery` for Django settings, app discovery, ORM-safe Celery tasks, Beat, and Django task tests.
- Use this skill for framework-neutral queue/worker design.

## Workflow

1. Decide whether the work must outlive the request process; if yes, enqueue it.
2. Persist a job record when clients need status or results.
3. Make tasks idempotent before enabling retries.
4. Set retry policy, timeouts, acknowledgment behavior, and dead-letter handling.
5. Expose status and observability: logs, metrics, queue depth, and failure records.
6. Test both task behavior and enqueue/status integration.

## Key Rules

- Return a job ID immediately for long-running user-visible work.
- Assume at-least-once delivery; duplicate execution must be safe.
- Retry only transient errors; do not retry validation or permanent failures.
- Use idempotency keys for external side effects.
- Monitor queue depth and worker failures before production rollout.

## References

- [Detailed job patterns](references/details.md) — DLQ, status polling, task chaining, alternative queues, and worked examples.
