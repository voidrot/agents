# Go

## Confirmed support and paths

Current Go docs confirm Structured Logs in `sentry-go` 0.33.0+ and state Logs are enabled by default after `sentry.Init`. Create `sentry.NewLogger(ctx)` and emit through its level entries; use `SetAttributes` for persistent logger attributes or typed per-entry attributes. Current docs limit attribute values to `int`, `string`, `bool`, and `float`.

| Path/library | Structured Logs status | Current boundary |
|---|---|---|
| Native `sentry.Logger` | Confirmed, 0.33.0+ | Create with the operation/request `context.Context` for correct correlation and isolation. It also implements `io.Writer`, but docs recommend native/supported integrations when context changes. |
| `log/slog` | Confirmed, SDK 0.34.0+ | `sentry-go/slog` handler; `Option.LogLevel` selects records. Context attribute extraction is explicit. |
| Zap | Confirmed | `sentry-go/zap` Core; select `Option.Level`, attach Sentry context as documented, and honor its sync/flush timeout behavior. The current rendered page confirms support but does not state a version gate; do not guess one. |
| Logrus | Confirmed, SDK 0.34.0+ | Use the **log hook** for Structured Logs. The separate event hook is error events, not Logs. Flush the hook before `logger.Fatal`/`os.Exit` as documented. |
| Zerolog | **Not supported for Structured Logs** | Current page explicitly says it sends error events and may add breadcrumbs, not Structured Logs, due to `io.Writer`/context limitations. Do not use it for this task. |

No other Go library is named as a Structured Logs bridge on the current Go Logs page.

## Context, lifecycle, and safety

- Initialize before constructing adapters. Pass the request/operation context when creating native, slog, or Zap routes; do not reuse a background-context logger when per-request correlation/isolation is required.
- Configure one Logs route and distinguish Logrus log hooks from event hooks. Fatal APIs may exit before deferred work; follow the exact adapter's exit/flush guidance.
- The Go Logs page shows `defer sentry.Flush(2 * time.Second)` before termination, and adapter pages document their own flush/close behavior. Treat every timeout as a bounded attempt, never a delivery guarantee.
- Use stable typed attributes, not full structs, errors, HTTP requests, headers, bodies, or user-provided strings. Expect sensitive-data scrubbing through Sentry server-side rules. Apply `BeforeSendLog`/adapter replacement filtering for privacy only when the user explicitly requests it, as optional defense in depth.

## Authorized validation

After authorization, create one request-scoped controlled `info` record with a synthetic ID and primitive attributes. Verify the expected trace/context only if tracing already exists; do not add tracing for this task. Confirm one Logs entry and, for Logrus, that event hooks did not create an unintended event. For short-lived tests, invoke the documented bounded flush and report its return/observation without promising arrival.

## Canonical official docs

- [Go Logs](https://docs.sentry.io/platforms/go/logs/)
- [slog](https://docs.sentry.io/platforms/go/logs/slog/)
- [Zap](https://docs.sentry.io/platforms/go/logs/zap/)
- [Logrus](https://docs.sentry.io/platforms/go/logs/logrus/)
- [Zerolog (events only)](https://docs.sentry.io/platforms/go/logs/zerolog/)
