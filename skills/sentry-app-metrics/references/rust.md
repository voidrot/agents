# Rust Application Metrics

## Established current documentation

The official [Sentry Rust Application Metrics page](https://docs.sentry.io/platforms/rust/metrics/) documents support in Rust SDK **0.48.0+**. Re-check that page and the installed SDK version before implementation. In the top-level `sentry` crate, the `metrics` feature is enabled by default; metrics are enabled by default, and `ClientOptions::enable_metrics(false)` disables them. These facts do not establish parity with another SDK.

## Direct API and metric contract

Use the Rust-specific `sentry::metrics` API. Its builder/capture style creates counters, gauges, and distributions; use the exact current signatures and builder methods from the official page:

```rust
sentry::metrics::counter("checkout.completed", 1).capture();
sentry::metrics::gauge("workers.active", 12.0).capture();
sentry::metrics::distribution("checkout.duration", 18.4)
    .unit(sentry::protocol::Unit::Millisecond)
    .capture();
```

Counters are unitless. Gauges and distributions can use `sentry::protocol::Unit`; choose a semantically correct standard unit from the [official units specification](https://develop.sentry.dev/sdk/foundations/data-model/attributes/#units). Use `.attribute()` for explicitly allowed filtering/grouping attributes. Keep names stable and semantic, and define a small bounded allowlist of attribute keys and values before emission. Do not use IDs, raw paths or query strings, emails, user input, headers, bodies, tokens, or credentials. Review name × attribute cardinality and hot-path volume; filtering cannot make per-request or per-user telemetry safe.

The Rust page documents `ClientOptions::before_send_metric`; returning `None` drops a metric. Use it only as deterministic defense in depth for known noisy names or attributes outside the contract, not as permission to forward arbitrary input. Metrics associate with the current trace/span when applicable. Do not enable tracing solely to emit metrics or claim a Rust OpenTelemetry metrics bridge.

## Context, privacy, lifecycle, and validation

Default attributes can include environment, release, and server, and can include configured user identifiers when `send_default_pii` is enabled. Treat these automatic or user attributes as sensitive: inspect the active configuration and obtain the required privacy/cardinality review before enabling or relying on them. Do not add user or request identifiers, or other sensitive context, merely because the SDK can attach them.

The Rust metrics page does not establish a separate metric flush API or a metric-delivery guarantee. Do not port a flush, close, buffering, or shutdown procedure from another SDK. The `sentry::init` guard's documented event-flush behavior is insufficient evidence for metric delivery. Buffered telemetry can be lost; a flush or timeout would not guarantee delivery.

Run local Rust build/test/lint and focused tests for once-only placement, bounded attributes, and filtering before sending telemetry. Only with separate explicit authorization for remote traffic, emit one non-sensitive, low-volume controlled metric in a safe environment and verify only the agreed name, type, unit, allowed attributes, and time window. Do not retain or report raw telemetry; remove temporary probes. A missing result is not proof of delivery failure.
