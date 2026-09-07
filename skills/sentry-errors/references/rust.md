# Rust

An exception/error event is one captured occurrence. Sentry Logs and breadcrumbs are separate signals and are not substitutes; an Issue is server-side grouping of events, and Issue triage is outside this skill.

## Official status

[Rust Capturing Errors](https://docs.sentry.io/platforms/rust/usage/) is the current official general capture guide. It **confirms manual event/error reporting only to the extent shown on that page**; re-check it for the installed crate and enabled integrations before choosing exact traits, macros, or APIs. [Rust platform documentation](https://docs.sentry.io/platforms/rust/) governs panic integration and framework support. Do not infer error-chain, async, or panic behavior from another SDK.

## Decision and ordering

Use a current documented panic integration for unhandled panics only if it preserves the application's existing panic hook/unwind/abort behavior. Manually report an actionable handled error at the layer that consumes it. Preserve source/error chains and backtraces where supported; do not replace the error with formatted text. Do not manually capture immediately before a panic that an installed panic owner also reports.

Initialize the guard/client and framework layers in the exact current documented lifetime/order. **Verify docs:** panic hook chaining, `panic=abort`, Tokio/task panic handling, thread-local scope, framework middleware, and which error types/chains produce exception events. Keep task/request context isolated across async executors.

Logs and breadcrumbs do not replace error events. Avoid request bodies, headers, debug dumps, secrets, IDs, and arbitrary `Debug` output in context.

## Lifecycle and validation

Guard drop, runtime shutdown, abort, signal termination, and process exit differ. Use documented shutdown behavior without changing panic strategy or promising delivery. With authorization, prefer one handled synthetic chained error. A controlled panic needs separate authorization. Confirm one event, chain/backtrace, task isolation, unchanged `Result`/panic behavior, and filtering. Native debug symbols may be required for readable optimized frames; upload is outside scope.
