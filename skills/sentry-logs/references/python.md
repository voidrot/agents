# Python

## Confirmed support and paths

Current Python docs confirm Structured Logs in `sentry-sdk` 2.35.0+ and now state that direct SDK logging is enabled by default. Use `sentry_sdk.logger.trace/debug/info/warning/error/fatal` after `sentry_sdk.init`; `{attribute_name}` placeholders create structured message parameters, and `attributes={...}` adds searchable fields. Do not retain legacy blanket advice that `enable_logs=True` is always required.

| Path/library | Structured Logs status | Current configuration boundary |
|---|---|---|
| Native `sentry_sdk.logger` | Confirmed | Current page says enabled by default after init. |
| Standard-library `logging` | Confirmed | Configure `LoggingIntegration(capture_sentry_logs=True)`. `sentry_logs_level` controls Logs; `level` controls breadcrumbs; `event_level` controls error events. The older `enable_logs` behavior is documented as deprecated for this integration. |
| Loguru | Confirmed | Configure `LoguruIntegration(capture_sentry_logs=True)`; it exposes separate Logs, breadcrumb, and event thresholds. |

No other Python logging bridge is named on the current Python Logs page.

## Data and threshold policy

The current direct Logs page says attribute values should be primitive strings, numbers, or booleans; serialize a complex value only if it is safe and genuinely searchable. It specifically demonstrates joining list values because arrays are not stored as attributes. Prefer omission or a small derived field over serializing objects/payloads.

For both bridges, the library's own logger level must allow a record before Sentry thresholds apply. Default bridge behavior can send `INFO+` to Logs and breadcrumbs and `ERROR+` as events; configure all three intentionally to prevent volume and duplicate semantics. Extra fields from stdlib `logging` become top-level searchable attributes, so allowlist them and never forward arbitrary request dictionaries.

Use `before_send_log` for local filtering/redaction. `ignore_logger` affects breadcrumbs/events, not necessarily Structured Logs; use the current integration page's Logs-specific controls rather than assuming one ignore path covers every output.

## Initialization, lifecycle, and validation

Initialize before modules emit records, especially when integrations are auto-enabled. Preserve existing handlers and avoid adding both stdlib and Loguru routes to the same record. The cited Logs/integration pages do not promise a universal Python flush behavior; follow separately verified SDK/framework shutdown guidance and report worker/serverless termination risk.

With authorization, issue one controlled `INFO` record through the selected path with primitive fields. Verify its attributes and confirm whether bridge settings also created a breadcrumb or error event; an event alone is not Logs success. Redact logger names/messages in evidence if they contain user input.

## Canonical official docs

- [Python Logs](https://docs.sentry.io/platforms/python/logs/)
- [Standard library logging integration](https://docs.sentry.io/platforms/python/integrations/logging/)
- [Loguru integration](https://docs.sentry.io/platforms/python/integrations/loguru/)
