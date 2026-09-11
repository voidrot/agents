# Privacy, sampling, and lifecycle

Consult the installed SDK's current options, data-management, tracing/OTel coexistence, and lifecycle pages before changing these controls. Do not transplant exact behavior across SDKs.

## Privacy and collection

Prefer granular, documented data-collection controls over legacy broad PII switches. Review every newly enabled category, default change, integration, and explicit scope field. Explicit scope data can still be sent independently of automatic collection settings, so avoid intentionally attaching secrets, credentials, cookies, authorization headers, bodies, PII, or high-cardinality identifiers. Expect sensitive-data scrubbing through Sentry server-side rules; authorized Sentry administrator action may be needed to confirm or configure them. Use a local allowlist for privacy only when the user explicitly requests it, as optional defense in depth.

### Confirmed Go facts

The current Go options documentation describes `DataCollection` as granular automatic-data control and marks `SendDefaultPII` deprecated. `DataCollection` takes precedence when both are configured. Explicit data set on a scope (for example, with `Scope.SetUser`) is sent regardless of `DataCollection`; exclude sensitive data at the source and expect Sentry server-side scrubbing rules. Add client-side privacy filtering only when the user explicitly requests it, as optional defense in depth.

## Sampling versus filtering

Keep these decisions separate:

- **Error-event sampling** controls which error events are sent; it is not trace sampling.
- **Trace sampling** decides tracing capture and belongs to a deliberate tracing/OTel policy. For topology, propagation, or tracing implementation, use the `sentry-tracing` skill.
- **Filtering** for expected-error/noise handling deterministically drops known unwanted events and is not a volume policy substitute. For privacy/data scrubbing, use local drop/redaction only when the user explicitly requests it, as optional defense in depth alongside expected server-side Sentry rules.

Where OpenTelemetry owns instrumentation or sampling, follow the current documented coexistence path; do not install a competing provider or independently resample the same telemetry.

### Confirmed Go facts

Go documents `SampleRate` for error events separately from `TracesSampleRate` and `TracesSampler`. `TracesSampler` overrides `TracesSampleRate`; treat the two trace controls as mutually exclusive in the proposed configuration and use one deliberate trace-sampling owner. The exact semantics for all other SDKs must be read from their current pages.

## Lifecycle

Inspect short-lived processes, CLI jobs, serverless completion, workers, mobile termination, and shutdown order. Add draining/flush only as documented for the selected platform, bounded by its timeout/cancellation behavior, and keep normal completion/control flow intact. A flush/drain call is an attempt, not delivery evidence; abrupt termination can lose buffered telemetry.

### Confirmed Go fact

Go documents `Flush` as waiting up to its timeout for buffered events and returning whether the attempt completed before the timeout. It does not guarantee delivery.

## Sources

- [Go options](https://docs.sentry.io/platforms/go/configuration/options/)
- [Go data management](https://docs.sentry.io/platforms/go/data-management/)
- [Go draining](https://docs.sentry.io/platforms/go/configuration/draining/)
- [Python sensitive data](https://docs.sentry.io/platforms/python/data-management/sensitive-data/)
- [Python options](https://docs.sentry.io/platforms/python/configuration/options/)
- [JavaScript options](https://docs.sentry.io/platforms/javascript/configuration/options/)
- [Node OpenTelemetry](https://docs.sentry.io/platforms/javascript/guides/node/opentelemetry/)
