# Scopes, enrichment, and filtering

Read the current platform enrichment/scope and options pages before choosing APIs. Scope lifetime and concurrency isolation are SDK/framework-specific.

## Scope policy

- **Global scope:** immutable deployment-wide metadata only. Do not place user, request, job, or mutable state here.
- **Request/current scope:** use the documented request-, hub-, isolate-, or task-local scope for a request/job/user session, and ensure it is cleared/popped at its boundary.
- **Event scope:** use for one capture/callback when data must not outlive that event.
- In concurrent servers, workers, async tasks, and mobile isolates, prove isolation using the platform's documented mechanism. Never share mutable scope data merely because it worked in a single request.

## Choose bounded fields

| Field | Use | Do not use |
|---|---|---|
| Tags | Small stable, low-cardinality query/filter dimensions | IDs, emails, raw URLs, messages, secrets |
| Contexts | Bounded structured diagnostic state | Raw request objects, bodies, headers, arbitrary user input |
| Extras | Small exceptional debugging details | PII, credentials, high-volume/unbounded data |
| Breadcrumbs | Scrubbed, bounded lead-up context | Error-event replacement, raw network/auth/body data |

Explicitly set scope data can bypass automatic-collection assumptions; apply the same allowlist and privacy policy to it.

## Filtering

Use the exact platform's pre-send and breadcrumb filtering callbacks only after consulting its current docs. They are defense in depth, not a reason to collect sensitive material. Filter/drop or redact locally at the earliest practical boundary; prevent sensitive data at the call site too. Keep callbacks deterministic, bounded, exception-safe, and unable to affect application control flow. Do not rely on a product-side rule as the only protection.

## Sources

- [Go scopes](https://docs.sentry.io/platforms/go/enriching-events/scopes/)
- [Go options](https://docs.sentry.io/platforms/go/configuration/options/)
- [Python options](https://docs.sentry.io/platforms/python/configuration/options/)
- [JavaScript enriching events](https://docs.sentry.io/platforms/javascript/enriching-events/)
- [JavaScript options](https://docs.sentry.io/platforms/javascript/configuration/options/)
