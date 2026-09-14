---
name: efficient-rust
description: Implement, review, debug, or test Rust code when ownership, borrowing, lifetimes, Result and error boundaries, traits/modules, Cargo layout, async/concurrency, unsafe code, or Rust-specific performance behavior affects the change.
---

# Efficient Rust

Use this skill for a bounded Rust change or review where Rust semantics affect correctness, safety, maintainability, or validation. It owns Rust-specific decisions about ownership, errors, API boundaries, Cargo organization, asynchronous/concurrent work, performance, `unsafe`, and tests.

Do not use it for generic coding process, product design, deployment, or non-Rust framework configuration. Use the relevant Sentry skill for Sentry instrumentation; do not infer Sentry behavior from language patterns. Use `efficient-testing` when a changed contract needs its focused test-selection workflow.

## Workflow

1. **Establish the local contract.** Read the request, the affected public API and callers, nearby tests, and the closest `Cargo.toml`. Inspect the workspace root, member manifests, lockfile policy, toolchain file, enabled features, profiles, lint configuration, and existing runtime/test conventions when present. Identify observable behavior, error behavior, feature combinations, blocking or cancellation boundaries, and safety invariants before editing. Preserve them unless the request explicitly changes them.
2. **Choose the smallest Rust-shaped design.** Keep code in the existing crate and module unless a distinct compilation, visibility, dependency, or ownership boundary requires another crate. Prefer a direct function, struct, or enum over a new abstraction. Keep items private by default; expose the narrowest stable interface required by callers. Add a trait only when multiple real implementations, a consumer-owned dependency seam, or a generic algorithm needs it. Do not create a trait, feature, crate, or dependency for a hypothetical future use.
3. **Make ownership explicit.** Start with borrowed inputs when the callee need not retain or mutate them; accept owned values when the operation consumes, stores, transfers, or must outlive the caller. Return a borrow only when the result is demonstrably tied to an input and that relationship makes the caller simpler. Otherwise return an owned value. Let inference express local lifetimes; add named lifetimes only to express a real relationship between references. Do not add `'static`, `Box::leak`, `Rc<RefCell<_>>`, `Arc<Mutex<_>>`, or a clone merely to silence the borrow checker without documenting the changed ownership, lifetime, or synchronization cost.
4. **Design the error boundary.** Identify who can recover from each failure and what context they need. Use `Result` for expected fallible operations and reserve `panic!`, `unwrap`, `expect`, and assertions for established programmer-invariant failures or tests. Preserve sources with `Error::source` and error wrapping; add stable, actionable context at the layer that knows the operation and relevant safe identifiers. Keep library error types specific enough for callers to distinguish supported recovery cases; translate them at application, protocol, or CLI boundaries without exposing internal details. Do not discard errors, stringify away their source chain, or use one opaque catch-all error where callers need a decision.
5. **Set module and trait boundaries.** Group code by a cohesive responsibility, not by a speculative architectural layer. Keep representation and invariants private behind constructors and methods when callers must not violate them. Put behavior with the data or module that owns its invariants. Prefer concrete parameters and return types until polymorphism is required. When a trait is needed, make its ownership, error type, `Send`/`Sync` expectations, object-safety needs, and feature visibility intentional; avoid public traits that force downstream implementations unless that extension point is the contract.
6. **Handle async and concurrency as lifecycle work.** Select the project’s existing runtime and current installed documentation; do not add or mix runtimes casually. For every spawned task, channel, lock, or shared resource, name its owner, stop signal, completion/error observation, capacity or backpressure rule, and shutdown behavior. Treat task cancellation and a dropped future as normal outcomes: make partial work, resource cleanup, and externally visible state safe when polling stops. Bound task creation and queues where input can grow. Do not hold a synchronous or asynchronous lock across `.await` unless the awaited operation cannot re-enter or contend for that state and the wait is demonstrably safe; prefer extracting data, narrowing the critical section, or message passing. Keep blocking work out of async execution paths using the runtime’s documented mechanism, and propagate task failures rather than silently detaching them.
7. **Treat `unsafe` as a proof obligation.** Use safe Rust first. Before writing or accepting `unsafe`, state the safe alternative considered and the concrete reason it cannot meet the required contract or measured constraint. Minimize the unsafe region; keep it in a small, reviewed helper behind a safe API that enforces its preconditions. Document each block with a `SAFETY:` comment naming the invariants that make it sound, including validity, initialization, bounds, alignment, aliasing/mutability, ownership/drop, layout, and thread-safety assumptions that apply. Do not make callers uphold undocumented invariants, rely on tests to prove absence of undefined behavior, or broaden an unsafe block for convenience.
8. **Optimize only against evidence.** First establish the correct behavior and a representative baseline with the project’s supported benchmark, profiler, trace, or targeted measurement. Identify the measured bottleneck and its workload, then change one relevant cost at a time. Prefer algorithmic or allocation/data-movement improvements that preserve the public contract over micro-optimizations or unsafe code. Remeasure the same workload and check that latency, throughput, allocation, memory, and cancellation behavior relevant to the claim did not regress. Revert an optimization that lacks a material measured benefit or makes the ownership/error/safety story less clear.
9. **Add proportionate Rust tests.** Test behavior through the smallest stable boundary: unit tests for isolated logic and crate-level integration tests for public behavior or cross-module wiring. Cover an error variant or recovery path only when it is contractual or addresses a confirmed defect; assert the meaningful variant, source, state transition, or output rather than incidental formatting. Exercise cancellation, shutdown, ordering, and concurrent interleavings when the change creates those guarantees; use deterministic coordination and bounded timeouts instead of sleeps where the existing test stack supports them. Test each materially supported feature combination affected by the change, not an automatic feature matrix. Keep test-only helpers and feature gates out of the production API unless they serve a real production boundary. When deciding Rust test layout, failure assertions, async test execution, property tests, or benchmark evidence, read the conditional [Rust testing reference](references/testing.md).
10. **Validate in increasing scope and report limits.** Run the narrowest applicable checks first, then rerun checks affected by later changes. Use repository commands when documented; otherwise, from the relevant workspace or package root, select applicable commands such as:

    ```sh
    cargo fmt --check
    cargo check --all-targets
    cargo test
    cargo clippy --all-targets --all-features -- -D warnings
    ```

    Run `cargo test --doc` when doctests are part of the crate contract, and use `cargo test --features <affected-feature>` when a changed optional feature is not in the default set. Run a supported benchmark or profiler only for a performance claim. For unsafe-sensitive changes, run the project-supported interpreter or sanitizer check when available; report unavailable toolchain components rather than claiming that ordinary tests establish soundness. Classify a failed command as a code defect, test expectation, feature/configuration issue, toolchain problem, or unavailable prerequisite before changing code or expanding scope. Do not weaken assertions, remove lints, add retries, or disable features merely to obtain green output.

## Rust decision rules

| Situation | Default | Escalate when |
| --- | --- | --- |
| Borrow checker conflict | Clarify which component owns the value and shorten the borrow or restructure control flow. | Cloning is needed to preserve independent ownership or measured contention/lifetime constraints justify shared ownership. |
| Public error | Use a typed, source-preserving error that exposes supported recovery decisions. | A boundary intentionally maps internal detail to a user, wire, or domain error. |
| New abstraction | Use a concrete type or function. | Multiple current implementations or a consumer-owned substitution seam require a trait. |
| Async work | Keep work in the existing runtime and make task ownership and shutdown observable. | A different execution model is required and compatibility, cancellation, and blocking effects have been verified. |
| Shared mutable state | Prefer ownership transfer or narrow synchronization. | Shared state is necessary and lock ordering, contention, and `.await` interactions are explicit. |
| `unsafe` | Reject it in favor of safe Rust. | A measured or required capability cannot be met safely and its invariants can be locally enforced and reviewed. |
| Performance change | Preserve the simple implementation. | A representative measurement identifies a material bottleneck and validates the improvement. |

## Completion evidence

Report only facts established by the work:

- the changed Rust boundary and the ownership, error, trait/module, async, or safety decision;
- affected crate, feature, workspace, and public-API compatibility considerations;
- task ownership, cancellation, backpressure, and error-observation behavior for concurrent work;
- the invariant and safe wrapper for any `unsafe` code, plus limits of the review;
- baseline and post-change measurement, workload, and trade-offs for any performance claim;
- exact validation commands and results, plus skipped, blocked, or pre-existing failures and their causes.

Stop when the requested Rust contract is implemented or reviewed, its Rust-specific risks have proportionate evidence, and unsupported claims are marked as limits.
