# Python

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Python Capturing Errors](https://docs.sentry.io/platforms/python/usage/) **confirms** manual `capture_exception` inside an `except` block (with the current exception explicit or omitted) and distinguishes message capture and breadcrumbs from error events. [Python integrations](https://docs.sentry.io/platforms/python/integrations/) documents integration-specific automatic behavior; do not claim a framework, worker, or task runner is automatic until its exact integration page confirms it.

## Decision and ordering

Prefer the documented integration owner for an unhandled web/task failure. Manually capture the original exception only when application code catches and consumes an unexpected actionable failure. If it is re-raised into an integration, choose manual or automatic ownership—not both. Preserve `raise ... from ...` cause/context chains; do not report only `str(exc)`.

Initialize at the current integration's documented startup point before framework/app imports where required. Put Sentry integration around the framework's normal exception boundary while retaining later application error rendering/logging. **Verify docs:** ASGI/WSGI middleware order, Django/Flask/FastAPI behavior, Celery/RQ/asyncio coverage, and fork/preload handling for installed versions.

Use request/task-local scope, never module-global user/request state. Add route template, operation class, attempt bucket, or bounded outcome; never request/response bodies, headers, local-variable dumps, arbitrary object serialization, or exception custom fields without an allowlist.

## Lifecycle and validation

Async tasks, background threads, process pools, forks, workers, CLI exit, and forced exit can bypass send completion. Follow the exact integration/runtime shutdown guidance and do not claim flush guarantees delivery. With authorization, capture one synthetic exception inside `except`; assert original exception/cause, one event, scoped context, unchanged return/re-raise behavior, and expected-error filtering. Debug symbols/source maps are generally not the Python path, but native-extension frames may need their own platform symbol prerequisites.
