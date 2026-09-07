# .NET

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[.NET Capturing Errors](https://docs.sentry.io/platforms/dotnet/usage/) **confirms** manual exception/message capture. Use [.NET platform guides](https://docs.sentry.io/platforms/dotnet/) for the exact ASP.NET Core, desktop, MAUI, Unity, logging, or other integration. Automatic unhandled capture and middleware behavior are integration-specific; the general usage page does not confirm every host/runtime path.

## Decision and ordering

Prefer documented host/framework automatic capture for exceptions that remain unhandled. Manually capture the original `Exception` only when code catches and consumes an unexpected actionable failure. Preserve `InnerException` and aggregate exception structure; do not report only `Message`. Avoid manual capture plus rethrow into ASP.NET exception middleware, host handlers, or logging integrations that also create events.

Place SDK host/middleware integration exactly where the selected current guide requires relative to routing and custom exception handlers. **Verify docs:** ASP.NET Core middleware order, background services/tasks, unobserved task exceptions, desktop dispatcher handlers, MAUI native bridges, and logging-provider event behavior. Keep request/activity/async context isolated; never static/global user or request fields.

Logs and breadcrumbs are not substitutes for captured exceptions. Keep only bounded route templates, component, operation class, and outcome context—no claims, headers, bodies, connection strings, or serialized request/exception objects.

## Lifecycle and validation

Short-lived console apps, host shutdown, background services, fail-fast, and native termination can bypass async completion. Follow current close/flush guidance without changing exit behavior or promising delivery. With authorization, use one synthetic exception with an inner cause; verify one event, chain/stack, scope isolation, original response/rethrow behavior, and filtering. PDB/native symbols may be prerequisites for readable frames; upload is outside scope.
