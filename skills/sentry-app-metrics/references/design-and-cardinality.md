# Metric design and cardinality

Application Metrics are direct SDK-emitted quantitative telemetry. Design the metric contract before choosing an API: owner, question, type, stable name, unit, allowed attributes, maximum rate, and drop policy. The current Sentry runtime pages describe the three types as counts for events, gauges for current values, and distributions for value ranges ([Node](https://docs.sentry.io/platforms/javascript/guides/node/metrics/), [iOS](https://docs.sentry.io/platforms/apple/guides/ios/metrics/), [Dart](https://docs.sentry.io/platforms/dart/metrics/)).

## Type choice

| Type | Use when | Avoid when |
|---|---|---|
| Count | An owned outcome happened a known number of times | Modeling unique people/items or state snapshots |
| Gauge | A periodically observed level can rise or fall | Recording a latency/size population where a range matters |
| Distribution | Each numeric observation contributes to a range, such as duration or size | Counting occurrences or representing a current level |

A count is not a unique-user/set metric. Do not derive distinct-user analytics by attaching user identifiers.

## Names and units

- Use lowercase, dot-delimited, domain-owned names such as `checkout.completed`, `queue.depth`, and `image.decode.duration`.
- Name the business or system concept, not a deployment, account, user, raw route, or temporary experiment value.
- Preserve meaning: changing type, unit, denominator, ownership, or outcome semantics requires a deliberate new name/version rather than reusing history.
- Select the unit that matches the numeric value and use the chosen runtime's documented representation. Consult Sentry's official [units specification](https://develop.sentry.dev/sdk/foundations/data-model/attributes/#units); do not invent a unit string or assume another SDK accepts one.

## Attributes and cardinality

Attributes create series dimensions. Allow only a short, documented allowlist with finite values: for example `outcome` (`success|failure`), a finite `operation`, or an approved region set. A route **template** can be allowed only when bounded and scrubbed.

Never emit identifiers; raw URLs, raw paths, or query strings; emails; user input; tokens; headers; request/response bodies; timestamps; random values; or an unbounded exception/message value. These are privacy risks and can create unbounded series. Treat values arriving from telemetry, users, or the application as untrusted; reject unknown values instead of normalizing them into new labels.

Before merge, calculate the plausible upper bound of `metric name × attribute combinations`. Review scope/global attributes too: inherited user or request data is not automatically safe for metrics. Keep request and user context out unless the documented SDK behavior is inspected and an explicit bounded policy allows it.

## Volume, filtering, and aggregation expectations

- Establish an emission budget before adding a hot-path metric: expected steady rate, burst rate, owner, and what is dropped first. Do not emit one metric per request or user without an explicit, bounded volume policy.
- Prefer a count at the once-only business outcome over multiple attempt-side counts. Prefer a cadence-controlled gauge over emitting every state mutation.
- Application metrics are aggregated quantitative telemetry, not an event ledger. Do not depend on an individual point appearing, immediate visibility, exact delivery, or a flush as a delivery guarantee.
- If a current runtime page documents a pre-send metric callback, it may drop known noise or unsafe attributes before transmission. It is defense in depth, not permission to construct unsafe metrics at call sites.
- Do not claim a universal sampling, buffer-size, envelope-size, aggregation-window, or filtering default. Verify the exact runtime's current documentation.

## Privacy review

Perform a call-site review and a pre-send review. Ensure the numeric value itself does not encode sensitive information (for example, an account balance tied to an identity). Evidence must identify only the contract and aggregate result—not raw payloads, credentials, or captured user data.
