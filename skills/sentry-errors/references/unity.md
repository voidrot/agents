# Unity

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Unity Capturing Errors](https://docs.sentry.io/platforms/unity/usage/) is the current official general usage guide and **confirms manual capture only as shown there**. Automatic Unity/managed/native crash ownership is **unconfirmed by this general page**; use [Unity platform documentation](https://docs.sentry.io/platforms/unity/) for the installed package, engine version, target backend, and automatic behavior. **Verify docs:** Unity log integration semantics, managed exception hooks, IL2CPP/Mono differences, mobile/desktop/console native crash support, and shutdown/persistence.

## Decision and ordering

Map managed C# exceptions, Unity log callbacks, engine/native crashes, and platform SDK crashes separately. A Unity error log is not automatically equivalent to a captured exception event unless the exact integration docs say it creates one. Prefer a documented unhandled owner; manually capture the original handled `Exception` only when consumed. Do not duplicate a managed exception through logging callback, manual call, and native crash bridge.

Initialize through the documented Unity lifecycle and preserve existing log handlers, exception propagation, frame loop, and crash behavior. Keep scene/feature/operation context stable and event-local. Never attach player names, chat, save data, transforms/object dumps, network payloads, device identifiers, screenshots, or log buffers.

## Lifecycle and validation

Editor, development player, IL2CPP build, mobile, desktop, and console targets are materially different. Domain reload, app pause/quit, hard crash, and offline caching can lose events. Validate the actual target build; do not promise flush. With authorization, prefer one handled synthetic managed exception. Native hard-crash tests require separate authorization. Confirm one event, correct layer, no log/manual/native duplicate, unchanged game behavior, and readable managed/native frames. IL2CPP symbols and native debug symbols may be prerequisites; upload is outside scope.
