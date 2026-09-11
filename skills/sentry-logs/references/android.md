# Android (Kotlin/Java)

## Confirmed support and paths

Current Android docs confirm Sentry Structured Logs in `sentry-android` 8.12.0+, using `Sentry.logger()` after `SentryAndroid.init`. The page currently requires `options.logs.enabled = true` (or the documented manifest metadata). For advanced structured entries, use the documented `log(level, SentryLogParameters, message, parameters...)` path with `SentryAttributes`; do not transplant syntax from JavaScript/Dart.

Officially documented bridges are exactly:

| Path | Structured Logs status | Key setup boundary |
|---|---|---|
| Direct `Sentry.logger()` | Confirmed | Initialize in the application startup path and enable Logs before calls. |
| Timber (`sentry-android-timber`) | Confirmed from Android SDK 8.17.0+ | Auto-install may occur when the Gradle plugin discovers Timber; otherwise add/configure `SentryTimberIntegration`. `minLogsLevel` controls Logs separately from `minBreadcrumbLevel` and `minEventLevel`. Ensure Timber itself is planted/configured as its docs require. |
| Logcat (`android.util.Log`) | Confirmed from Android SDK 8.17.0+ | Requires current Sentry Android Gradle plugin Logcat bytecode instrumentation. `minLevel` gates captured calls; it may include matching calls from bundled libraries inside the app package. |

Do not call Timber breadcrumbs/events or uninstrumented Logcat output Structured Logs. No other Android logging library is named by the current Logs page.

## Safe implementation and validation

- Inspect Gradle plugin, SDK, Timber dependency, manifest, and application initialization before selecting a path. Avoid duplicate Timber/Logcat/manual capture.
- Prefer direct calls for a small set of intentional records. If broad Logcat capture is authorized, start with a restrictive level because third-party output may be included. Use local pre-send privacy filtering only when the user explicitly requests it, as optional defense in depth alongside expected server-side Sentry rules.
- Use typed, stable attributes and review scope attributes for user/request data. Avoid intentionally attaching secrets and payloads. Expect sensitive-data scrubbing through Sentry server-side rules; apply the Android Logs `beforeSend` callback to drop or modify records for privacy only when the user explicitly requests it, as optional defense in depth.
- Android docs warn that buffered logs can be lost when the app crashes before send. Do not claim guaranteed delivery or invent a flush-on-background strategy.
- With authorization, emit one non-sensitive `info` test after init, exercise the selected direct/Timber/Logcat route, and verify one Logs record, expected attributes/level, and no unintended event duplication.

## Canonical official docs

- [Android Logs](https://docs.sentry.io/platforms/android/logs/)
- [Timber integration](https://docs.sentry.io/platforms/android/integrations/timber/)
- [Logcat integration](https://docs.sentry.io/platforms/android/integrations/logcat/)
