# Browser JavaScript and React

## Confirmed support and paths

The current browser and React Logs pages confirm Sentry Structured Logs for JavaScript SDK 9.41.0+. Logs are enabled by default in 10.71.0+; older supported versions require `enableLogs: true`. After `Sentry.init`, use `Sentry.logger.trace/debug/info/warn/error/fatal`; pass structured attributes as the second argument and use `Sentry.logger.fmt` as the documented tagged template for parameterized messages.

| Path/library | Browser JS | React | Notes |
|---|---:|---:|---|
| Direct `Sentry.logger` | Confirmed | Confirmed | Preferred for intentional records. |
| Console via `consoleLoggingIntegration` | Confirmed | Confirmed | Select explicit console levels; multiple-argument searchable parsing requires JS SDK 10.13.0+. Ordinary console output is not a Sentry Log without this forwarding behavior. |
| Consola via `createConsolaReporter` | Confirmed | Confirmed | Current page requires JS SDK 10.12.0+. |

No other browser/React logging library is named on the current Logs pages. In particular, do not list server logger bridges here.

## Browser install and lifecycle boundaries

The current generic JavaScript Logs page explicitly says logging is supported through CDN bundles and the Loader Script and links to the current loader documentation. This supersedes legacy claims that Loader Script support is absent. Verify the exact loader/project feature configuration before suggesting it; changing a loader or Sentry project setting needs authorization. Package builds should import the matching SDK (`@sentry/browser` or `@sentry/react`) and initialize before app logging.

Page close, navigation, offline state, ad blockers, and abrupt termination can prevent buffered client telemetry from arriving. The Logs pages do not promise a universal browser flush; do not add blocking unload workarounds or claim delivery.

## Safe implementation and validation

- Prefer direct calls over broad console interception. If console capture is selected, allowlist levels and filter third-party noise locally with `beforeSendLog`.
- Use stable templates and documented values; current JS shared attributes accept strings, numbers, booleans, or arrays of these, but explicit per-log data should follow the exact installed SDK types. Never pass DOM objects, errors, auth state, URLs with query strings, or payloads.
- Keep session/operation attributes on the narrowest scope and clear user state at logout.
- With authorization, trigger one record after init, verify it in Logs by a synthetic correlation value, and check that console capture did not duplicate a direct call.

## Canonical official docs

- [Browser JavaScript Logs](https://docs.sentry.io/platforms/javascript/logs/)
- [React Logs](https://docs.sentry.io/platforms/javascript/guides/react/logs/)
- [JavaScript Loader Script](https://docs.sentry.io/platforms/javascript/install/loader/)
