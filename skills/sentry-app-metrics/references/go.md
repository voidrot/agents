# Go Application Metrics

## Established current documentation

The official [Sentry Go Application Metrics page](https://docs.sentry.io/platforms/go/metrics/) documents Application Metrics in Sentry Go SDK **0.42.0+**. Re-check that page and the installed SDK version before implementation.

**Go does not use the JavaScript/Dart `Sentry.metrics` API.** The documented Go path constructs a meter with `sentry.NewMeter(ctx)` and records through its `Count`, `Gauge`, and `Distribution` methods. Do not port method names, initialization options, unit strings, callbacks, context behavior, or lifecycle behavior from JavaScript, Dart, or another SDK.

## Direct path, context, and metric contract

Create the meter with the relevant Go `context.Context`; use `WithCtx` when the documented current request context should link a metric to its current span. For example, use fixed names and bounded attributes only:

```go
meter := sentry.NewMeter(context.Background())

meter.Count("checkout.completed", 1,
    sentry.WithAttributes(attribute.String("outcome", "success")),
)
meter.Gauge("workers.active", 12.0,
    sentry.WithAttributes(attribute.String("pool", "billing")),
)
meter.Distribution("checkout.duration", 18.4,
    sentry.WithUnit(sentry.UnitMillisecond),
    sentry.WithAttributes(attribute.String("operation", "charge")),
)
```

The Go page documents `Count` for increments, `Gauge` for values that can rise or fall, and `Distribution` for value distributions. It documents `WithUnit` for gauges and distributions, using Go unit constants such as `sentry.UnitMillisecond` and `sentry.UnitByte`; use the exact Go representation and a semantically correct standard unit from the [official units specification](https://develop.sentry.dev/sdk/foundations/data-model/attributes/#units). Do not invent unit strings or infer that units apply to `Count`.

Names must be stable, lowercase, and semantic. Attribute keys and values must be an explicit, small bounded allowlist. Exclude IDs, raw URLs, paths/query strings, emails, user input, headers, bodies, credentials, and tokens. Review name × attribute cardinality and emission volume, especially on request paths. The page's trace-linking example is not permission to attach raw request paths or arbitrary request context.

## Filtering, lifecycle, and safe validation

The page documents `ClientOptions.BeforeSendMetric`, which receives `*sentry.Metric` and returns a modified metric or `nil` to drop it. Use it as deterministic defense in depth for known noisy names or attributes outside the contract. Do not use filtering to forward arbitrary input, to make unsafe source attributes acceptable, or to permit unbounded per-request/per-user telemetry.

The current Go metrics page does **not** establish a metrics flush procedure. Do not transplant a flush/close call from JavaScript, Dart, Apple, Python, or OTel. Buffered telemetry can be lost; even a documented flush or timeout would not guarantee delivery.

`NewMeter(ctx)` and `WithCtx` provide the page's documented trace-linking path, but do not enable tracing solely to emit metrics or claim an OTel metrics bridge, shared exporter, or shared lifecycle. Keep tracing and OTel configuration separate unless current Go-specific Sentry documentation establishes it.

Run local Go build/test and focused tests for once-only placement, bounded attributes, and filtering before sending telemetry. Only with separate explicit authorization for remote traffic, emit one non-sensitive, low-volume controlled metric in a safe environment and verify only the agreed name, type, unit, allowed attributes, and time window. Do not retain or report raw telemetry; remove temporary probes. A missing result is not proof of a delivery failure.
