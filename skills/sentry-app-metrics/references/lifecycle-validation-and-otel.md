# Lifecycle, validation, and OpenTelemetry boundary

## Placement and once-only outcomes

Choose one authoritative owner for each metric. Place a count after its semantic outcome is known, including an explicit bounded `outcome` where success and failure must be compared. Do not count at both request entry and completion, on both client and server, or once per retry unless the contract explicitly says attempts are the measure.

For a timed distribution, start timing immediately around the owned operation and record exactly once when it resolves, rejects, times out, or is cancelled—according to the documented contract. Use `finally`/defer-style cleanup where appropriate, but do not fabricate a success value on an unknown outcome. Clean up timers/listeners on all exit paths.

For a gauge, nominate one component and a bounded interval/cadence. It represents an observation, not every mutation. Avoid lifecycle hooks that can run repeatedly or concurrently without a guard.

## Buffering and process lifecycle

Sentry's current documented JavaScript Application Metrics pages say metrics are buffered and sent periodically and provide an immediate flush snippet ([Node](https://docs.sentry.io/platforms/javascript/guides/node/metrics/), [TanStack Start](https://docs.sentry.io/platforms/javascript/guides/tanstackstart-react/metrics/)). The iOS page documents a blocking flush that waits for pending data or timeout ([iOS](https://docs.sentry.io/platforms/apple/guides/ios/metrics/)).

Use a flush/close/timer API only when the selected runtime's current page documents it, and only at its appropriate short-lived or shutdown boundary. It can time out, process termination can interrupt it, and network/backend processing can still fail: no metric path has a delivery guarantee. The current Dart/Flutter, Python, Go, and Rust metrics pages reviewed for this skill do not establish a metrics flush procedure; do not port one from JavaScript or Apple, or between those runtimes.

## Controlled validation and troubleshooting

1. Inspect the actual runtime, installed SDK version, initialization point, feature enablement, current official page, metric contract, and pre-send filter. Do not modify packages/configuration or transmit data without explicit authorization.
2. Run local-only checks first: compile/type-check/lint, focused tests of once-only outcome logic and allowed attributes, and a startup path that does not send telemetry where possible.
3. With separate explicit authorization for remote test traffic, emit one low-volume, non-sensitive metric in a safe environment. Use a stable test name only if the owner accepts its retention; do not use IDs or payload fragments as a marker.
4. Verify the agreed time window and only the expected type, name, unit, and safe attributes. Check duplicate placement, filter drops, initialization, runtime/version mismatch, and lifecycle termination before changing code.
5. Remove temporary probes; report aggregate evidence, time window, and uncertainty without raw telemetry.

A missing result is not evidence of a backend defect. Check authorization scope, local filtering, correct SDK initialization/runtime, asynchronous buffering, process lifetime, network policy, and documentation-supported feature availability. Do not add a blind flush, a second SDK initialization, credentials, debug payload logging, or product setting change as a workaround.

## SDK, OTel, and tracing boundary

Application metrics in this skill are direct Sentry SDK calls. Do not claim an automatic SDK-to-OpenTelemetry metrics bridge, an OTel Collector route, or shared buffering/flush behavior without current runtime-specific Sentry documentation. Generic OTel/Collector configuration is outside scope.

Trace correlation is also runtime-specific. The iOS metrics page exposes a trace identifier to its documented pre-send callback ([iOS](https://docs.sentry.io/platforms/apple/guides/ios/metrics/)); that does not prove correlation for other SDKs. Do not enable tracing merely to emit application metrics. For custom data that belongs to a sampled trace, use the tracing skill: Sentry's JavaScript [span-metrics page](https://docs.sentry.io/platforms/javascript/tracing/span-metrics/) distinguishes it from standalone application metrics.
