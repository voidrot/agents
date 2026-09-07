# Android

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Android Capturing Errors](https://docs.sentry.io/platforms/android/usage/) **confirms** manual exception/message capture. Read [Android platform documentation](https://docs.sentry.io/platforms/android/) for the installed SDK's current automatic Java/Kotlin crash, ANR, and NDK support. **Verify docs:** exact defaults, startup-crash persistence/flush behavior, ANR variants, NDK enablement, and which callbacks process managed versus native events; do not preserve legacy timing/default claims without confirmation.

## Layer and ownership decisions

Map Java/Kotlin exceptions, ANRs/app exits, and NDK/native crashes separately. Let the documented uncaught/native handler own a true crash and preserve the original Android handler/termination behavior. Manually capture only an unexpected handled `Throwable`. Do not catch a fatal exception merely to send it, and do not manually report before rethrowing to an automatic crash owner.

Initialize in the documented Application/startup location before failures of interest. Keep Activity/Fragment/UI fallback behavior separate from capture ownership. Event-local or current execution context should contain only stable screen/feature/operation values; do not attach Intent extras, Bundle dumps, view text, screenshots, user input, headers, or device identifiers without explicit approved policy.

Managed and NDK layers can have different filtering, scope synchronization, persistence, and symbolication behavior. Treat cross-layer parity as **unconfirmed** until the exact Android/NDK pages establish it. Logs and breadcrumbs do not replace crash/error events.

## Lifecycle and validation

A native crash may be persisted and reported on a later launch where current docs confirm it; this is not guaranteed delivery. Process kills, OOMs, battery/OS termination, offline state, and disabled restart can prevent observation. Do not force a crash without explicit crash-test authorization. Prefer one handled synthetic exception, then separately validate native/ANR paths only when required and authorized. Confirm one event, correct managed/native mechanism, preserved app behavior, safe context, and readable frames. ProGuard/R8 mappings and native debug symbols may be prerequisites; upload is outside scope.
