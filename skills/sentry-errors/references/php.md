# PHP

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[PHP Capturing Errors](https://docs.sentry.io/platforms/php/usage/) **confirms** manual capture of a `Throwable` and current last-error capture guidance. Use [PHP integrations](https://docs.sentry.io/platforms/php/integrations/) for framework-specific automatic behavior. Do not infer Laravel/Symfony or worker behavior from the general page.

## Decision and ordering

Let a documented framework error/exception integration own unhandled throwables. Manually capture the original `Throwable` only when application code catches and consumes an unexpected actionable error. Preserve `getPrevious()` chains; do not convert to a string. Use last-error handling only as current docs direct for PHP errors not represented by a caught throwable, and avoid overlap with shutdown/framework handlers.

Register/init in the current framework bootstrap order. Place exception listeners/middleware relative to application handlers exactly as the integration page requires, preserving the existing HTTP response, exception propagation, and PHP error handler chain. **Verify docs:** fatal/shutdown behavior, long-running workers, fibers/coroutines, framework status-code filtering, and whether a logging integration emits events.

Keep request/job data request-local, especially in long-running workers. Do not attach superglobals, request bodies/files, cookies, sessions, headers, SQL parameters, or serialized objects. Logs and breadcrumbs are not exception events.

## Lifecycle and validation

Request shutdown, fatal errors, worker recycling, signal termination, and process exit have different opportunities to send. Follow exact integration flush/close guidance; no shutdown callback guarantees delivery. With authorization, use one caught synthetic throwable with a previous cause. Confirm one event, chain/stack, unchanged response/throw behavior, worker scope reset, filtering, and no shutdown duplicate. Native extension frames may require symbols outside this skill.
