---
name: async-python-patterns
description: "Use for Python asyncio and concurrency: async/await, event loops, tasks, cancellation, timeouts, async I/O, and non-blocking APIs."
---

# Async Python Patterns

Use this skill for in-process async/concurrent Python design with `asyncio`, async libraries, and non-blocking I/O.

## When to Use

- Building async APIs, clients, scrapers, WebSocket handlers, or high-concurrency services
- Coordinating many concurrent I/O operations
- Choosing sync vs async for an I/O-heavy call path
- Managing tasks, timeouts, cancellation, async context managers, or async iterators
- Debugging blocked event loops or mixed sync/async code

## Boundaries

- Use `python-background-jobs` for queue/worker systems that run outside the request process.
- Use `django-celery` for Django-specific Celery integration.
- Use `python-testing-patterns` for testing async code with pytest.

## Decision Guide

| Workload | Prefer |
| --- | --- |
| Many concurrent network/DB calls | `asyncio` and async-native clients |
| CPU-bound computation | multiprocessing or explicit executor offload |
| Simple scripts/few connections | sync code for simplicity |
| Request work that must survive process restarts | background job queue |

Stay fully sync or fully async within a call path when possible. Hidden blocking inside async code can stall every task on the event loop.

## Workflow

1. Confirm the workload is I/O-bound and benefits from concurrency.
2. Use async-native libraries throughout the path.
3. Bound concurrency with semaphores, pools, or queue sizes.
4. Add timeouts and cancellation cleanup.
5. Offload unavoidable blocking work with `asyncio.to_thread()` or an executor.
6. Test with `python-testing-patterns` and monitor for event-loop blocking.

## Key Rules

- Always `await` coroutines or schedule them deliberately.
- Prefer `asyncio.run()` at process boundaries, not deep in library code.
- Do not call blocking APIs such as `time.sleep()` or sync HTTP clients in async functions.
- Treat cancellation as normal control flow and re-raise `CancelledError` after cleanup.

## References

- [Detailed async examples](references/details.md) — gather, tasks, error handling, timeouts, async context managers, queues, semaphores, locks, WebSockets, and blocking-code offload.
