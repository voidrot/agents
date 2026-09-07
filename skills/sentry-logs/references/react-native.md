# React Native

## Confirmed support and paths

Current React Native docs confirm Sentry Structured Logs in `@sentry/react-native` 7.0.0+ and require `enableLogs: true` in `Sentry.init`. Initialize in the actual app entry path before relevant calls. Use `Sentry.logger.trace/debug/info/warn/error/fatal`, optional `Sentry.logger.fmt` parameterization, and direct structured attributes.

| Path/library | Structured Logs status | Current boundary |
|---|---|---|
| Direct `Sentry.logger` | Confirmed | Preferred for intentional application records. |
| Console logging | Confirmed | Current integration page says Console capture is enabled by default when Logs are enabled; since SDK 8.14.0, `enableAutoConsoleLogs` can disable it. It instruments documented `console.*` methods. |
| Consola | Confirmed in SDK 10.12.0+ | Add the documented Sentry Consola reporter and select levels as needed. |

No other React Native logging-library adapter is named on the current Logs page. Ordinary native platform logs are not automatically equivalent to JavaScript Console Structured Logs; do not infer Android Timber/Logcat support into React Native.

## Mobile safety and lifecycle

- Inventory SDK version and default Console capture before adding an integration. Otherwise direct calls and auto-Console can duplicate records or unexpectedly ship existing console output.
- Prefer direct logging. If Console/Consola capture is authorized, allowlist levels and use `beforeSendLog`; development console traffic and dependency messages can be noisy or sensitive.
- Current docs say only string, number, and boolean attribute values are supported for the documented scope behavior. Avoid navigation params, device/user objects, errors, request data, tokens, and payloads. Clear user/session state at logout.
- The React Native page explicitly warns that logs can be lost when a crash terminates the app before the SDK sends them. App backgrounding, force-stop, offline state, and abrupt native termination are delivery risks; no universal flush guarantee is documented here.

## Authorized validation

With authorization, emit one controlled `info` record after init on each in-scope platform/build mode. Use a synthetic correlation value and bounded `platform`/`path` fields. Confirm one Logs record and whether its origin is direct, Console, or Consola; detect direct-plus-auto-Console duplicates. Do not force a crash or modify mobile/cloud settings just to test delivery without separate authorization.

## Canonical official docs

- [React Native Logs](https://docs.sentry.io/platforms/react-native/logs/)
- [React Native Console logging integration](https://docs.sentry.io/platforms/react-native/integrations/console-logging/)
- [React Native Consola integration](https://docs.sentry.io/platforms/react-native/integrations/consola/)
