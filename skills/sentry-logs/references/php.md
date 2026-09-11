# PHP

## Confirmed support and paths

Current PHP documentation confirms the direct SDK logger route for Structured Logs after initialization. It also documents the Monolog integration's `LogsHandler` as a Structured Logs route. `BreadcrumbHandler` sends breadcrumbs only, not standalone Sentry Logs; configure one intentional output path and keep explicit error capture for failures that need error events.

| Path | Structured Logs status |
|---|---|
| Direct PHP SDK logger | Confirmed on the Logs page |
| Monolog `LogsHandler` | Confirmed on the Monolog integration page |
| Monolog `BreadcrumbHandler` | Breadcrumbs only; not a Logs bridge |

No PHP framework integration beyond Monolog is established by these cited docs.

## Lifecycle, privacy, and validation

- For long-running CLI processes, use the PHP documentation's flush strategy at the appropriate controlled lifecycle boundary. Buffered work can still be lost; do not claim delivery is guaranteed.
- Use stable, low-cardinality fields and avoid intentionally logging credentials, PII, headers, and raw bodies. Expect sensitive-data scrubbing through Sentry server-side rules. Use documented local filtering for privacy only if the user explicitly requests it, as optional defense in depth.
- With authorization, send one synthetic direct or Monolog `LogsHandler` record and verify it is one Logs record with the expected fields—not merely a breadcrumb or event. Do not enable both handlers for the same source unless their outputs are deliberately separated.

## Canonical official docs

- [PHP Logs](https://docs.sentry.io/platforms/php/logs/)
- [Monolog integration](https://docs.sentry.io/platforms/php/integrations/monolog/)
