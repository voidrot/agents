# Kotlin Multiplatform

## Confirmed support and path

The current [Kotlin Multiplatform Logs page](https://docs.sentry.io/platforms/kotlin/guides/kotlin-multiplatform/logs/) confirms Structured Logs through the direct `Sentry.logger` route after initialization. A log message is required. The page names no external logging adapter; in particular, do not infer Android Timber or Logcat support for Kotlin Multiplatform.

Logs are standalone searchable records, not breadcrumbs or error events. Keep explicit exception capture for failures requiring issue grouping or a stack trace.

## Data, lifecycle, and validation

- Use stable required messages and bounded attributes; exclude secrets, PII, headers, bodies, and untrusted user data before logging.
- Use the documented `beforeSend` filtering as defense in depth, not as the primary privacy boundary.
- The page warns that a crash can occur before send. Follow only documented lifecycle behavior; no flush or retry guarantees delivery.
- With authorization, emit one non-sensitive direct record after initialization and verify one Logs record with its message, level, and attributes—not only a breadcrumb or event.

## Canonical official docs

- [Kotlin Multiplatform Logs](https://docs.sentry.io/platforms/kotlin/guides/kotlin-multiplatform/logs/)
