# Python

**Use for:** Python services, workers, scripts, and supported web/task frameworks.

1. Inspect packaging/lock files, Python version, ASGI/WSGI/process entry points, web/task framework, logging, existing SDK initialization, and OpenTelemetry. Use the current Python guide for the supported package, integrations, and init placement.
2. Initialize once at startup before framework/task execution. Enable only documented framework integrations; ensure worker and web processes each follow their documented lifecycle. Preserve native framework error handling and avoid duplicate manual capture.
3. Resolve existing OTel ownership before enabling Sentry tracing; see [OpenTelemetry](opentelemetry.md). Set sampling and data filtering deliberately. Add build metadata only if reliably produced. Python normally has no source-map upload step; if native/packaged artifacts are involved, use current platform documentation and match them to the shipped build.
4. Run repository tests/type/lint and exercise startup. With authorization, emit a controlled non-sensitive exception in the relevant process and inspect event/trace association.

Legacy material noted separate process lifecycles and OTel interaction; current docs control implementation details. Docs: <https://docs.sentry.io/platforms/python/>.