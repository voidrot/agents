# Rust

## Confirmed support and paths

The current [Rust Logs page](https://docs.sentry.io/platforms/rust/logs/) confirms direct Sentry logging macros, a `tracing` integration, and a `log` integration using `SentryLogger`. `tracing` fields become Structured Log attributes. Do not claim a universal field mapping for the `log` adapter where the documentation does not establish one.

The documented filtering can create Logs plus events or breadcrumbs depending on level and filter configuration. Define an explicit output policy and test it so one source record does not unintentionally produce duplicate Logs, breadcrumbs, or events. Logs remain distinct from explicit error capture.

## Lifecycle, privacy, and validation

- Initialize and install only the selected integration before relevant records are emitted; do not stack direct, `tracing`, and `log` routes without an intentional deduplication policy.
- Use bounded `tracing` fields/attributes and avoid intentionally emitting credentials, PII, request bodies, and untrusted blobs. Expect sensitive-data scrubbing through Sentry server-side rules. Use documented client-side filtering for privacy only when the user explicitly requests it, as optional defense in depth.
- Follow exact current SDK shutdown guidance. Crash, abrupt termination, filtering, or transport failure can prevent delivery; no flush is a delivery guarantee.
- With authorization, emit one synthetic record through the selected route. Verify attributes for `tracing`, then check the configured Logs/event/breadcrumb outputs and duplicate count.

## Canonical official docs

- [Rust Logs](https://docs.sentry.io/platforms/rust/logs/)
