# Dart and Flutter Application Metrics

Read the current official page for the actual target: [Dart](https://docs.sentry.io/platforms/dart/metrics/) or [Flutter](https://docs.sentry.io/platforms/dart/guides/flutter/metrics/). Both currently state support in SDK version **9.11.0+**, no setup beyond SDK initialization, and three types: `count`, `gauge`, and `distribution`.

## Direct implementation boundary

Use the current target page's examples for exact Dart signatures, imports, unit representation, and attribute parameter/type. The documented types are:

| Type | Use |
|---|---|
| `count` | Events such as orders, clicks, and API calls |
| `gauge` | Current values such as queue depth and connections |
| `distribution` | Value ranges such as response time and payload size |

Do not use legacy `increment`, `set`, option names, limits, or unit APIs merely because an old reference or another SDK used them.

## Enablement and filtering

The current pages document `options.enableMetrics = false` to disable metrics and `options.beforeSendMetric` to filter or modify metrics before sending; return `null` to drop. Use it to enforce the metric contract and volume/cardinality policy, such as dropping known noisy names or attributes outside a bounded allowlist. It is not default privacy scrubbing: call sites must already use fixed names and non-sensitive attributes, with expected sensitive-data scrubbing through Sentry server-side rules. Never emit user IDs, emails, raw URLs/query strings, input, headers, bodies, credentials, or per-request/per-user telemetry without an explicit bounded volume policy.

## Attributes and trace boundary

The pages establish that metrics can be searched by individual attributes, so apply the cardinality contract from [design and cardinality](design-and-cardinality.md). The pages should be re-read before asserting inherited attributes or trace correlation; do not infer automatic correlation from another SDK and do not enable tracing just for a metric.

## Delivery and validation

The Dart/Flutter pages reviewed for this skill do not establish a flush procedure. Do not port JavaScript or Cocoa flush behavior. Metrics remain telemetry with no delivery guarantee. Run local compile/lint and tests for outcome placement and filter policy first. With explicit, separate authorization for remote test traffic, emit one safe low-volume metric and verify the expected type, name, unit, and allowed attributes without retaining raw telemetry.
