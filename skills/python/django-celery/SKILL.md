---
name: django-celery
description: "Use for Django Celery integration: app setup, settings, shared_task design, Beat schedules, retries, canvas, monitoring, and task tests."
origin: ECC
---

# Django + Celery Async Task Patterns

Use this skill for Celery inside Django projects. It specializes the framework-neutral `python-background-jobs` guidance for Django settings, app discovery, ORM boundaries, and Django test behavior.

## When to Use

- Adding Celery workers, queues, or scheduled tasks to a Django app
- Configuring Redis/RabbitMQ brokers, result backends, Beat, or worker options
- Writing `@shared_task` functions that interact safely with Django models
- Designing retries, idempotency, canvas workflows, and dead-letter records
- Testing Celery tasks with Django and pytest
- Debugging task failures, queue backlogs, or Beat duplication

## Boundaries

- Use `python-background-jobs` for queue/worker concepts not specific to Django.
- Use `async-python-patterns` for in-process asyncio code, not Celery workers.
- Use `python-testing-patterns` for general pytest fixtures, mocks, and coverage.

## Workflow

1. Add a Django Celery app entrypoint and import it from the project package.
2. Configure broker, result backend, serializers, time limits, acks, prefetch, and Beat in Django settings.
3. Put tasks in app-level `tasks.py` modules and pass IDs, not ORM model instances.
4. Make each task idempotent before adding retries or late acknowledgments.
5. Route long/priority work to named queues and run Beat as a single process.
6. Test task functions synchronously and integration paths with eager settings when appropriate.
7. Monitor workers, queues, failures, and scheduled-task duplication.

## Key Rules

- Pass primary keys or primitive payloads to tasks; fetch fresh ORM state inside the task.
- Never call `.apply()` or `.get()` from production request handlers.
- Set `CELERY_TASK_ACKS_LATE` only for idempotent tasks.
- Use soft time limits for cleanup before hard worker termination.
- Run Celery Beat on one node only unless using a scheduler designed for coordination.

## References

- [Detailed Django Celery patterns](references/details.md) — setup, settings, tasks, retries, Beat, canvas, DLQ, testing, monitoring, and production checklist.

## Related Skills

- [python-background-jobs](../python-background-jobs/SKILL.md) — framework-neutral queue/worker design.
- [python-testing-patterns](../python-testing-patterns/SKILL.md) — pytest configuration, fixtures, and mocks.
