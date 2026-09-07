# Unity

## Confirmed support and paths

The current [Unity Logs page](https://docs.sentry.io/platforms/unity/logs/) confirms the direct `SentrySdk.Logger` route and built-in Unity `Debug`/`LogType` forwarding. It names no external logging-library adapter; do not infer support for Unity third-party loggers.

Forwarding can send Logs or breadcrumbs. `AddBreadcrumbsWithStructuredLogs` can send both, so select and configure one intentional output policy, then validate duplicate behavior. A breadcrumb or error event is not evidence that a standalone Structured Log arrived.

## Lifecycle, privacy, and validation

- Initialize before direct or Unity Debug output is emitted. Respect the documented asynchronous delivery behavior and synchronous handler boundaries; delivery is not guaranteed during crash, quit, or abrupt termination.
- Keep messages and attributes stable and low-cardinality. Exclude secrets, PII, bodies, and user-provided blobs at source; use documented filtering defensively.
- With authorization, emit one non-sensitive direct or forwarded record in a safe build. Verify its Logs result, level, fields, and whether the chosen setting also created a breadcrumb; do not deliberately crash a user or production session.

## Canonical official docs

- [Unity Logs](https://docs.sentry.io/platforms/unity/logs/)
