# JVM Java and Kotlin

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Java Capturing Errors](https://docs.sentry.io/platforms/java/usage/) **confirms** manual exception/message capture and explains events versus Issues and breadcrumbs. JVM Kotlin applications using the Java SDK share this documentation/API surface, but framework and Kotlin-specific behavior must be checked on the exact [Java platform/integration page](https://docs.sentry.io/platforms/java/). Automatic capture is integration-specific; a general Java usage page does not prove Spring, servlet, coroutine, or executor behavior.

## Decision and boundary order

Use a documented framework integration for unhandled exceptions that reach it. Manually capture the original `Throwable` only when application code catches and intentionally consumes an unexpected actionable failure. Preserve `cause` and suppressed exceptions; do not replace the throwable with its message. Avoid duplicate manual capture plus rethrow into servlet/filter/controller/global handlers.

Place integrations, servlet filters, Spring advice, uncaught handlers, or executor/task wrappers exactly where the current integration page requires relative to routing and application handlers. **Verify docs:** Spring Boot generation/version, servlet/Jakarta namespace, logging integration behavior, Kotlin coroutine context, thread pools, and uncaught-thread support. Do not infer Android behavior from JVM Java; use the Android reference.

Keep request/job context thread/coroutine-local. Do not leave identity or request values on a process-global scope across pooled threads. Logs and breadcrumbs are context, not captured exceptions.

## Lifecycle and validation

Short-lived JVMs, executors, abrupt halt/exit, shutdown hooks, and asynchronous transports may lose events. Use only current documented close/flush behavior, without blocking request handling or promising delivery. With authorization, use one synthetic caused exception; verify one event, cause/suppressed data as supported, safe scope isolation, unchanged framework response/rethrow behavior, and expected-error filtering. Obfuscated/native frames can require matching mapping/debug symbols; their upload is outside scope.
