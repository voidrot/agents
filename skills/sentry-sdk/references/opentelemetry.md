# SDK-relevant OpenTelemetry interoperability

Use only when an application already uses OpenTelemetry and the task is to make its tracing coexist with an official Sentry SDK. This is **not** guidance for building a generic OTel pipeline, Collector/exporter deployment, multi-project routing, or product administration.

1. Inventory existing tracer providers, SDK auto-instrumentation, propagators, exporters, resource attributes, and runtime startup order. Identify exactly one owner for trace-provider initialization.
2. Read the selected Sentry platform's current OTel section before changing anything. Choose either its documented interoperability path or native Sentry tracing; do not invent a universal exporter/collector configuration from another language.
3. Do not run competing tracing providers, duplicate auto-instrumentation, or two independent exports for the same spans unless the current official platform docs explicitly require and explain it. Resolve propagation, sampling, and resource/release/environment fields consistently.
4. Validate locally for duplicate spans and preserved context. With authorization, verify one controlled error is linked to the intended trace. Remove diagnostics afterward.

The legacy exporter workflow included collector installation, project creation, and remote configuration; those are out of scope and require separate explicit authorization. Current platform docs: [Node](https://docs.sentry.io/platforms/javascript/guides/node/), [Python](https://docs.sentry.io/platforms/python/), [Go](https://docs.sentry.io/platforms/go/), and [JavaScript](https://docs.sentry.io/platforms/javascript/).