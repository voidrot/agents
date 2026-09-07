# Platform patterns

These are tracing decision points, not setup instructions. Verify exact APIs, startup ordering, integrations, lifecycle behavior, and supported frameworks in current platform documentation before changing code.

| Platform | Trace-specific decisions and hazards |
|---|---|
| Browser / JavaScript | Preserve one page-load/navigation/router root; avoid duplicate router roots. Allowlist propagation targets narrowly and configure receiving CORS/proxies for tracing headers. Exclude noisy client requests deliberately; dynamic URLs and user input must not become names/attributes. See [JS tracing](https://docs.sentry.io/platforms/javascript/tracing/), [instrumentation](https://docs.sentry.io/platforms/javascript/tracing/instrumentation/), and [distributed tracing](https://docs.sentry.io/platforms/javascript/tracing/distributed-tracing/). |
| Node | Initialize the documented tracing/OTel path before instrumented modules when required by current docs. Preserve async context through callbacks, workers, queues, and streams; avoid a second OTel provider/instrumentation set. See [Node OTel](https://docs.sentry.io/platforms/javascript/guides/node/opentelemetry/). |
| Python | Let documented framework/integration coverage own request, DB, HTTP, and task spans. Preserve context across async tasks, executors, Celery-like consumers, and streaming responses; finish custom work on cancellation. See [Python tracing](https://docs.sentry.io/platforms/python/tracing/). |
| Go | Use request context consistently through handlers, outbound clients, goroutines, and workers. Do not detach child work accidentally; bound long-lived goroutines and finish manually managed spans on every exit. |
| Cloudflare / edge | Start/continue context at the fetch/worker entry, propagate only through approved outbound fetches, and finish before runtime termination. Treat wait-until/background work as a separate documented lifecycle decision. |
| Android | Keep app/navigation/network roots aligned with supported instrumentation. Bound coroutine, thread, WorkManager/job, and lifecycle spans; avoid view/item identifiers and user content in names. |
| Flutter | Align route, HTTP, isolate, and background-task context with supported integrations. Do not keep UI spans open across unrelated navigation or app lifecycle transitions. |
| React and web frameworks | Let the framework/router integration create navigation/request roots. Do not layer manual route roots over it; add child spans only for material uninstrumented work and stable route naming. |
| React Native | Coordinate native and JS lifecycle/navigation/network instrumentation. Verify context behavior across the bridge and background transitions; do not assume browser semantics. |

For platforms without a focused link above, navigate from [Sentry platform documentation](https://docs.sentry.io/platforms/) and use its current tracing page. This skill intentionally does not duplicate generic `sentry-sdk` setup guidance.
