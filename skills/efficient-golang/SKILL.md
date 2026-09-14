---
name: efficient-golang
description: Implement, review, debug, or refactor idiomatic Go code and package boundaries; use when a task involves Go errors, interfaces, context, goroutines, standard-library choices, project organization, testing, benchmarks, or profiling.
---

# Efficient Go

Use this skill for Go-specific implementation and review work. Keep the existing observable contract unless the request changes it. This skill owns Go package design, errors, interfaces, contexts, goroutine lifecycles, standard-library selection, Go tests, and measured performance work.

Do not use it as a substitute for security review, telemetry-specific work, dependency upgrades, CI configuration, or generic testing strategy. For a focused regression or unit-test decision that is not Go-specific, use `efficient-testing`; use the relevant Sentry skill for Sentry work.

## Workflow

1. **Establish the Go contract and toolchain.** Read `go.mod`, the changed package and callers, nearby tests, and repository instructions. Identify the module's declared Go version, supported commands, package naming and test conventions, public API, error behavior, cancellation behavior, and concurrency assumptions. Reproduce a reported failure with the narrowest relevant `go test` command before changing it when practical. Do not use an API merely because it exists in the locally installed Go toolchain if the module's declared version does not support it.

2. **Choose the smallest package boundary.** Keep code with the package that owns its behavior and data. Keep `main` packages limited to process startup, configuration, dependency wiring, and exit behavior; put reusable application behavior in ordinary packages. Use `internal` only to enforce repository-private imports. Add a new package, exported identifier, module, workspace, or architectural layer only when it creates a stable boundary that current callers need; otherwise extend the existing package. Avoid import cycles by moving shared domain-neutral types to the narrowest package that can own them, not to a catch-all utility package.

3. **Shape APIs around concrete use.** Start with concrete types and functions. Define a small interface at the consuming boundary only when the consumer needs substitutable behavior, such as a real external dependency and a test double. Keep interfaces behavior-oriented and no wider than the methods used; do not create one for every type or expose implementation details through one. Make zero-value usability, constructors, and nil semantics explicit where callers can observe them. Keep exported APIs deliberate because compatibility is a package contract.

4. **Propagate context deliberately.** Accept `context.Context` as the first parameter for operations that perform request, job, or caller-scoped I/O, blocking work, or child work. Pass the received context through to compatible calls; derive a child only to add a justified deadline, cancellation boundary, or value. Call each derived cancel function when its work is finished, including error paths. Do not store contexts in structs, replace a supplied context with `context.Background`, use a nil context, or use context values as optional function parameters. At a process root, choose `Background` or a signal-aware context according to the application's existing lifecycle.

5. **Preserve useful error semantics.** Return ordinary failures as `error`; reserve panic for unrecoverable programmer or process invariants, not expected input or operational outcomes. Check every returned error. Add a short operation-specific message only where it helps diagnose the failing layer, and wrap a cause with `%w` when callers must retain `errors.Is`, `errors.As`, or unwrapping behavior. Use sentinels for stable conditions callers branch on and typed errors only when callers need structured information. Join errors only when independent failures all matter. At an application boundary, map errors to the required response or exit result and log or report them once according to local policy; do not lose the chain or create duplicate handling. Preserve existing recovery behavior, and recover only at an intentional request, worker, or process boundary.

6. **Make every goroutine owned and stoppable.** Before adding `go`, name its owner, input source, result/error path, cancellation signal, and the event that proves it has exited. Prefer synchronous code until concurrency improves a stated latency, throughput, or isolation requirement. Bound fan-out and queues from a real resource limit or workload requirement. The sender that owns a channel is responsible for closing it; receivers must not close a channel they do not own. Ensure blocking sends, receives, timer waits, and external calls can finish when the owner cancels. Protect shared mutable state with the simplest appropriate synchronization, keep locks out of blocking I/O, and wait for owned workers before their dependencies are released. Do not add fire-and-forget work unless its independent lifecycle, shutdown, error handling, and backpressure are explicit.

7. **Prefer the standard library without forcing it.** Use existing project dependencies when they already fit. Otherwise prefer a standard-library facility that meets the requirement, such as `net/http` and `httptest` for HTTP, `errors` for error inspection, `log/slog` for structured logging, and `testing` for tests and benchmarks. Add a dependency only for a capability the standard library and existing dependencies cannot provide, after checking its compatibility, maintenance, license, and operational cost. Keep dependency-specific APIs behind the narrowest useful boundary when replacement is plausible; do not add wrappers merely to anticipate replacement.

8. **Write Go-focused evidence.** Place `_test.go` files with the package they exercise. Test the observable contract with deterministic inputs; use a same-package test only when access to unexported behavior is necessary, otherwise favor the public API. For I/O, time, randomness, processes, or external services, inject a narrow dependency or controlled input rather than sleeping, relying on order, or contacting production. Read [conditional Go testing](references/testing.md) when adding or reviewing Go tests, benchmarks, fuzz targets, or concurrent-code validation.

9. **Measure before performance changes.** Define the user-relevant metric and a representative workload. Add or run a focused benchmark only when performance is requested or a measured bottleneck warrants it. Capture a baseline, inspect profiles when benchmark results do not identify the cause, change one factor, then rerun the same benchmark under comparable conditions. Keep an optimization only when it improves the stated metric without weakening correctness, readability, cancellation, or error behavior. Do not add pooling, unsafe code, concurrency, caching, or tuning based on intuition alone.

10. **Verify proportionately and handle failures.** Format changed Go files with `gofmt`. Run the narrowest supported tests that prove the changed contract; expand to dependent packages or `go test ./...` when shared code, repository policy, or the changed boundary requires it. Run `go test -race` for affected concurrent or shared-state code when feasible. Run a benchmark and profile only for performance claims. If a check fails, preserve its output and classify it as a product defect, incorrect expectation, race, hang/leak, toolchain/version mismatch, or unavailable prerequisite. Change the identified cause before rerunning; do not hide failures with retries, sleeps, swallowed errors, broad recoveries, or weakened assertions. If validation cannot run, report the exact command, blocker, and unverified risk.

## Review checkpoints

- Does each package expose only a purposeful API and avoid cycles or speculative layers?
- Do contexts reach blocking and child operations, with cancellation released and respected?
- Can callers inspect errors that need inspection, while process boundaries present and record them once?
- Can every goroutine stop, communicate failure, and be waited on before teardown?
- Does each added dependency earn a capability the standard library and current dependencies lack?
- Do tests cover the changed public behavior deterministically, including material error or cancellation behavior?
- Does any performance claim have a comparable benchmark or profile rather than intuition?

## Completion evidence

Report the package/API boundary changed, context and goroutine ownership decisions where applicable, error behavior preserved or changed, exact formatting/test/race/benchmark/profile commands and results, and every skipped or blocked check with its reason. State whether a performance result is measured, inconclusive, or not evaluated.
