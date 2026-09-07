# Go

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

- [Go Capturing Errors](https://docs.sentry.io/platforms/go/usage/) **confirms** manual capture of values implementing `error`, error-chain unwrapping, and asynchronous transport by default.
- [Handling Panics](https://docs.sentry.io/platforms/go/usage/panics/) **confirms** documented panic recovery paths, context-aware recovery, and the need to account for asynchronous delivery before termination.
- [Concurrency](https://docs.sentry.io/platforms/go/usage/concurrency/) is the authority for goroutine-safe hub/scope handling.

## Decision and ordering

Ordinary returned errors are not panics: capture a returned error only at the layer that decides it is unexpected/actionable and handles it. Preserve `%w`, unwrap/join, and causal structure. For a panic, install the exact documented recovery owner at the outer boundary of each goroutine/request/job where recovery is intended. Recovery changes panic behavior by definition; preserve the application's existing repanic/termination policy and never add recovery merely for telemetry.

Do not combine manual capture, panic recovery, and an HTTP/framework integration for the same panic. **Verify docs:** the selected router/framework middleware order and whether it creates request-local context. Clone/use the documented goroutine-aware context rather than mutating shared global scope.

A message is not a replacement for an `error`; breadcrumbs and Logs do not create exception events. Avoid expected sentinel/domain errors unless policy marks them actionable.

## Lifecycle and validation

The usage guide states capture is asynchronous by default. Follow current documented flush/sync transport guidance only where compatible with existing behavior. `os.Exit` bypasses deferred functions, so deferred recovery/flush cannot run; never rewrite exit behavior solely to report telemetry. A flush timeout is not delivery proof.

With authorization, use one synthetic wrapped error or controlled panic in a test harness, not production. Confirm one event, chain order and stack, goroutine/request isolation, preserved recovery/return behavior, and bounded context. Native Go frame readability can depend on matching build/debug information; artifact administration is outside scope.
