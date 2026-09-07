# Python Application Metrics

## Established current documentation

The official [Sentry Python Application Metrics page](https://docs.sentry.io/platforms/python/metrics/) documents Application Metrics in Sentry Python SDK **2.44.0+**. Metrics are enabled by default after SDK initialization. Re-check that page and the installed SDK version before implementation; these claims do not establish parity with another SDK.

## Direct path and metric contract

Use the Python-specific `sentry_sdk.metrics` namespace, selecting the method that matches the contract:

```python
import sentry_sdk

# Bounded names and attributes only; these are not request or user data.
sentry_sdk.metrics.count(
    "checkout.completed", 1, attributes={"outcome": "success"}
)
sentry_sdk.metrics.gauge(
    "workers.active", 12, attributes={"pool": "billing"}
)
sentry_sdk.metrics.distribution(
    "checkout.duration", 18.4,
    unit="millisecond",
    attributes={"operation": "charge"},
)
```

The page documents `count` for occurrences, `gauge` for a current sampled value, and `distribution` for observations where percentiles matter. Use the exact documented Python signature and unit representation; choose a semantically correct standard unit from the [official units specification](https://develop.sentry.dev/sdk/foundations/data-model/attributes/#units), not an invented string.

Names must be stable, lowercase, and semantic. Define a small allowlist of bounded attributes before emission. Do not use identifiers, raw paths or query strings, emails, user input, headers, bodies, tokens, or credentials as a name or attribute. Review name × attribute cardinality and hot-path volume before sending; filtering cannot make per-request or per-user telemetry safe.

## Attributes, filtering, and context

The page documents per-call attributes and `before_send_metric`; its callback returns the metric to send or `None` to discard it. Use that callback only as deterministic defense in depth, such as dropping a known noisy metric family or rejecting an attribute outside the allowlist. Do not turn arbitrary input into attributes or rely on a callback to sanitize an unsafe call site.

Python also documents `sentry_sdk.set_attribute` for shared attributes in stream mode, scoped through the isolation scope for the current request or session. The SDK may automatically attach configured environment, release, SDK, server, and current-scope user attributes. Inspect the active scope and initialization before adding shared context: do not allow user identity or other personal/sensitive context onto metrics without explicit authorization and a privacy/cardinality review.

## Lifecycle, tracing, and safe validation

The current page documents metric emission, filtering, and context, but does **not** establish a Python metrics flush procedure. Do not transplant JavaScript, Dart, Apple, Go, or OpenTelemetry buffering/flush APIs. A flush or timeout would not guarantee delivery in any case.

The metric object exposed to Python's filter can contain trace and span identifiers; this does not authorize automatic correlation claims or enabling tracing solely for metrics. Keep tracing and OTel configuration separate unless current Python-specific Sentry documentation establishes the behavior.

Run local lint/type/test and once-only placement checks first. Only with separate explicit authorization for remote telemetry, emit one non-sensitive, low-volume metric in a safe environment and verify only its agreed name, type, unit, allowed attributes, and time window. Do not retain or report raw telemetry; remove temporary probes. A missing result is not proof of delivery failure.
