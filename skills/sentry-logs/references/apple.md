# Apple

## Confirmed support and path

The current [Apple Logs page](https://docs.sentry.io/platforms/apple/logs/) confirms Structured Logs through the direct `SentrySDK.logger` route after SDK initialization. It names no external logging-library adapter; do not infer support for Swift third-party logging libraries from other Sentry platforms.

Use Logs for standalone searchable structured records, not as a replacement for breadcrumbs or error events. Keep exception capture explicit when issue grouping or a stack trace is required.

## Data, lifecycle, and validation

- Keep messages stable and attributes bounded; exclude secrets, PII, request/response bodies, and user-controlled blobs before calling the logger.
- Expect sensitive-data scrubbing through Sentry server-side rules. Use the page's pre-send filtering hook for privacy only when the user explicitly requests it, as optional defense in depth.
- The page warns that a crash can occur before logs are delivered. Follow only documented lifecycle behavior; no flush or retry is a delivery guarantee.
- With authorization, emit one non-sensitive direct record after initialization and verify one Logs record, its level and attributes, and that it did not instead appear only as a breadcrumb or event.

## Canonical official docs

- [Apple Logs](https://docs.sentry.io/platforms/apple/logs/)
