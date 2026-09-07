# JavaScript Application Metrics

## Established current documentation

The current official [Node.js](https://docs.sentry.io/platforms/javascript/guides/node/metrics/) and [TanStack Start React](https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/metrics/) Application Metrics pages establish the following:

- Application Metrics are supported in Sentry JavaScript SDKs **10.25.0+**.
- No metrics-specific setup is required beyond SDK initialization; metrics are enabled by default.
- The direct API uses `Sentry.metrics.count`, `Sentry.metrics.gauge`, and `Sentry.metrics.distribution`—not legacy `increment`.
- `enableMetrics: false` disables collection. `beforeSendMetric` can filter or modify a metric and returns `null` to drop it.
- Metrics are buffered and sent periodically; those pages document an immediate flush snippet for the relevant short-lived lifecycle.

These are version/default/lifecycle claims for the linked pages, not a promise that every JavaScript deployment/runtime has the same initialization or shutdown behavior. Re-check the page and installed SDK version before changing code.

## Direct path

After authorization and only in a documented runtime, select the direct method matching the contract:

```ts
// Values and attributes shown are bounded examples, not user/request data.
Sentry.metrics.count("checkout.completed", 1, {
  attributes: { outcome: "success" },
});
Sentry.metrics.gauge("queue.depth", 12, {
  attributes: { queue: "billing" },
});
Sentry.metrics.distribution("image.decode.duration", 18.4, {
  unit: "millisecond",
  attributes: { source: "cache" },
});
```

Use the current page for exact signatures, supported unit spelling, initialization location, hook shape, and flush call. Keep a `beforeSendMetric` policy narrow: drop a known internal metric family or a metric that fails an attribute allowlist. Do not transform arbitrary input into labels or add process/request/user context without a cardinality review.

## Routing: documented does not mean parity

The linked **Node.js** and **TanStack Start React** pages are the runtime-specific evidence used here. They do not establish code/configuration parity for Browser JavaScript, React, Next.js, Bun, Deno, Cloudflare, React Router Framework mode, or React Native. For those targets, find and read the current official runtime-specific Application Metrics page before proposing `Sentry.metrics`, `enableMetrics`, `beforeSendMetric`, units, or flush behavior. If no current page is established, stop at documentation review.

The generic JavaScript page might be available from the platform navigation, but do not use it to override a runtime-specific page. The platform index is [Sentry platforms](https://docs.sentry.io/platforms/).

## Trace boundary

Application metrics are direct quantitative telemetry and are not inferred from Logs or span metrics. The official [JavaScript span-metrics guide](https://docs.sentry.io/platforms/javascript/tracing/span-metrics/) says standalone business counters, success/failure rates, and aggregates independent of trace sampling should use Application Metrics; span metrics require tracing and enrich existing traces.
