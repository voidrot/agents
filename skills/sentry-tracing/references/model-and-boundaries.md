# Model and boundaries

Read current [tracing terminology](https://docs.sentry.io/concepts/key-terms/tracing/) before selecting APIs. The current conceptual model uses **spans**, including a root/service span and child spans. **Transaction** is legacy or SDK-version-specific vocabulary/API; use it only where the selected current platform documentation does. Do not translate terminology into a different SDK's API.

## Choose boundaries in order

1. Locate every execution entry: inbound request/router action, RPC handler, queue consumer, scheduled job, CLI command, serverless invocation, or mobile/browser root lifecycle.
2. At each entry/service boundary, preserve automatic root creation or create exactly one meaningful root if the current SDK requires it. If inbound propagation is valid, continue its context rather than creating a disconnected root.
3. Let supported automatic instrumentation create dependency spans. Add a manual child only around a material uninstrumented operation: a domain workflow, external call wrapper, queue handoff, significant computation, or other latency worth locating.
4. Do not create spans for every function, loop iteration, getter, logging action, or already-instrumented dependency. Aggregate/bound repeated work when a span is genuinely needed.

## Name and describe spans safely

- Name roots from stable route templates, operation names, or bounded task classes; name children from stable domain operations or dependency actions.
- Use a stable operation/category consistent with the current platform's semantic conventions. Never invent universal `op`/attribute keys; consult the selected SDK docs.
- Add only scrubbed, low-cardinality attributes useful for one trace: bounded booleans, enums, counts, or resource class. Exclude identifiers, raw URLs/query strings, payloads, secrets, user data, and unbounded error text.
- Prefer a stable template such as `GET /orders/:id` over a concrete path. This protects data and keeps aggregation/span metrics useful; see [span metrics](https://docs.sentry.io/concepts/key-terms/tracing/span-metrics/).

## Outcome and completion

- Mark a span's status/outcome according to the current SDK only when the operation's outcome is known. A failed span represents a failed timed operation; it is not an error event.
- Keep exception/error capture separate. Do not add duplicate error reporting solely because a span failed; follow the application's authorized error-capture policy.
- Prefer documented callback/context-manager/decorator forms that finish automatically on synchronous and asynchronous completion. For manually managed spans, finish exactly once on normal return, thrown/rejected error, cancellation, timeout, and stream/response completion as applicable.
- Ensure async work retains the active parent context. Do not defer completion beyond the process/request lifecycle without a documented background/streaming design.
