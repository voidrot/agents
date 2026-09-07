# Elixir

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Elixir Capturing Errors](https://docs.sentry.io/platforms/elixir/usage/) is the current official general capture page. It **confirms only the capture behavior explicitly shown there**. Read [Elixir platform documentation](https://docs.sentry.io/platforms/elixir/) and the exact framework/integration page before selecting APIs. **Verify docs:** automatic OTP process crashes, Logger integration semantics, Plug/Phoenix boundary behavior, linked-process/supervisor metadata, and SDK delivery lifecycle. Do not infer Erlang/OTP behavior from Ruby or another server SDK.

## Decision and ordering

Preserve OTP supervision and crash semantics. Do not rescue a process exit merely to report it. Use documented automatic integration ownership for unhandled crashes where confirmed; manually report an unexpected handled exception only at the consuming boundary. Preserve exception, stacktrace, and cause/exit context as the exact API supports. Logger output, breadcrumbs, and messages are not substitutes for an exception event.

Place Plug/Phoenix middleware or error handling in current documented order while preserving response rendering and supervision/restart behavior. Avoid a manual capture followed by re-raise into the integration. Keep process/request/job context local; do not put assigns, params, socket state, messages, headers, bodies, tokens, or whole structs in event data.

## Lifecycle and validation

BEAM process termination, supervisor restart, application shutdown, release stop, and forced VM exit differ. Follow only documented client lifecycle behavior; no flush guarantees delivery. With authorization, use one handled synthetic exception in a test process and separately test supervision only if required. Confirm one event, stack/cause where supported, process isolation, unchanged restart/response behavior, and expected-error filtering.
