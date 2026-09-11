# Flutter and Dart

## Confirmed support and path

Current Flutter docs confirm Sentry Structured Logs in `sentry_flutter` 9.0.0+ and state they are enabled by default in 9.28.0+. Supported versions below 9.28.0 require `options.enableLogs = true` in `SentryFlutter.init`. After initialization, use the documented `Sentry.logger` levels. The current page uses `Sentry.logger.fmt` with `%s` placeholders for parameterized messages and `SentryAttribute` typed values for additional fields.

**Named adapter status:** the current Flutter Logs page names no Dart/Flutter logging-framework bridge. Therefore use the direct SDK logger for Structured Logs. Do not carry forward legacy `sentry_logging`/Dart `logging` bridge claims unless a current `docs.sentry.io` Flutter Logs or integration page explicitly confirms that bridge at implementation time.

## Initialization, data, and lifecycle

- Initialize `SentryFlutter` before `runApp`/first log through the documented startup path. Check installed version before adding the opt-in switch; avoid asserting one default for every 9.x release.
- Use typed, stable `SentryAttribute.string/int/double/bool` values shown by current docs. Do not pass widget state, exceptions, routes with user parameters, payloads, tokens, or arbitrary maps.
- Keep operation/session scope narrow and clear user state on logout. Keep bounded level filtering separate from privacy scrubbing. Expect sensitive-data scrubbing through Sentry server-side rules; apply the page's `beforeSendLog` callback for privacy only when the user explicitly requests it, as optional defense in depth.
- The current page explicitly warns that logs can be lost when a crash terminates the app before send. It does not document a framework adapter or universal manual flush guarantee. Do not add speculative app-lifecycle flushes or claim next-restart delivery.

## Authorized validation

With authorization, emit one non-sensitive direct `info` log after initialization in a safe build, using a synthetic correlation value and bounded platform/build-mode attributes. Verify one record and expected typed attributes. Exercise background/crash behavior only if specifically authorized; never deliberately crash a user or production session merely to validate Logs.

## Canonical official docs

- [Flutter Logs](https://docs.sentry.io/platforms/dart/guides/flutter/logs/)
