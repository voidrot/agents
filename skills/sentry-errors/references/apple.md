# Apple platforms

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

- [Apple Capturing Errors](https://docs.sentry.io/platforms/apple/usage/) **confirms** current manual exception/message usage for the Apple SDK family.
- [iOS Capturing Errors](https://docs.sentry.io/platforms/apple/guides/ios/usage/) is the exact iOS guide.
- Use the selected guide under [Apple platforms](https://docs.sentry.io/platforms/apple/) for macOS, tvOS, watchOS, Swift/Objective-C, and integration-specific automatic crash behavior.

Automatic crash, app-hang/watchdog/OOM, and Swift concurrency coverage is platform/version-sensitive. **Verify docs:** which crash mechanisms are supported, what is persisted until next launch, event-processor/filter reach across native crash events, and lifecycle APIs. Do not state that every OS termination or Swift error is capturable.

## Decision and ordering

Let the documented native crash handler own uncaught fatal faults and preserve OS termination/previous handlers. Capture manually only an unexpected handled error/exception that will not reach that owner. Do not catch/rethrow fatal native exceptions merely for telemetry. Preserve Swift underlying errors and Objective-C exception information where the SDK supports them; do not stringify.

Initialize at the current application lifecycle point before faults of interest. Use event-local context; avoid view contents, screenshots, URLs, request data, device advertising IDs, contacts, or user-entered text. Native scope synchronization and background-thread behavior must be verified for the installed SDK.

## Lifecycle and validation

Native crash reports may need a subsequent launch to transmit when current docs say so. Watchdog termination, OOM, jetsam, force quit, offline state, and background suspension have distinct observability limits. Never promise a flush or crash event. Prefer an authorized handled synthetic error; hard-crash tests require separate authorization and a safe test device/build. Confirm one event, native/managed mechanism, preserved app behavior, safe context, and readable frames. Matching dSYMs are a prerequisite for symbolicated native frames; upload/admin is outside scope.
