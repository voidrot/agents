# Unsupported or undocumented runtime boundary

This is a documentation boundary, not a capability matrix. The Python and Go Application Metrics pages are now covered by their [Python](python.md) and [Go](go.md) runtime references. For the following targets, current official **runtime-specific Application Metrics/custom-metrics documentation is not established by this skill**:

| Runtime | Required action |
|---|---|
| Android / Kotlin / Java | Stop at current documentation review. |
| .NET | Stop at current documentation review. |
| PHP | Stop at current documentation review. |
| Ruby | Stop at current documentation review. |
| Unity | Stop at current documentation review. |
| Kotlin Multiplatform | Stop at current documentation review. |

Also apply this rule to Browser JavaScript, React, Next.js, Bun, Deno, Cloudflare, React Router Framework mode, and React Native unless a current page for that exact runtime has been reviewed. Node.js/TanStack Start documentation does not establish runtime parity.

## Strict rule

Use the [Sentry platform index](https://docs.sentry.io/platforms/) to locate a current, exact runtime page. Until one is established, do **not** port `Sentry.metrics`, `enableMetrics`, `beforeSendMetric`, metric type names, units, initialization, buffering, trace correlation, or flush behavior from another SDK, a legacy skill, or an OTel example. Do not make a package/configuration change or remote test call.

This no-porting rule is especially important for Go: its documented API is `sentry.NewMeter(ctx)` followed by meter methods, not the JavaScript/Dart `Sentry.metrics` namespace. Follow [Go](go.md) only for Go-specific implementation.

“Current runtime-specific docs are not established by this skill” is **not proof that the SDK lacks the capability**. It only means this skill cannot safely prescribe implementation. Report the documentation gap and request or perform a fresh official documentation review before implementation.
