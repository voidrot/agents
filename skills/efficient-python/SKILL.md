---
name: efficient-python
description: Implement, review, debug, and validate maintainable Python changes involving Pythonic APIs, typing, exceptions and resource lifetimes, asyncio boundaries, standard-library choices, profiling, package layout, tooling, or Python tests. Use when a Python task needs language-specific design or diagnosis; not for generic implementation, non-Python work, or Sentry instrumentation.
---

# Efficient Python

Use this skill for Python-specific engineering decisions. Preserve the local public contract—results, exceptions, ordering, side effects, import behavior, and supported Python versions—unless the request intentionally changes it. Prefer direct, idiomatic code that the repository's configured formatter, linter, type checker, and test runner support.

This skill does not choose product behavior, redesign an architecture, or configure third-party observability. Use `efficient-testing` for the focused test-design workflow; use the applicable Sentry skill for Sentry work. Do not add a dependency, tool, framework, or abstraction merely to make a Python change look uniform.

## Ordered workflow

1. **Establish the Python contract.** Read the request, affected modules, call sites, nearby tests, and project configuration before editing. Identify supported Python versions; package/build backend; configured formatter, linter, type checker, test runner, and dependency/lockfile workflow; and whether code runs in a CLI, web request, worker, subprocess, or async loop. Record observable inputs, outputs, raised exceptions, cleanup obligations, concurrency ownership, and performance claim, if any.
   - Treat an undocumented behavior as an assumption, not a compatibility promise. Inspect callers before changing an exception type, return shape, import-time effect, or ordering.
   - For a defect, first obtain a deterministic symptom or minimal reproduction. If that is impossible, state the missing condition and avoid guessing through unrelated edits.

2. **Choose the smallest conventional design.** Keep a change inside its existing module and public boundary unless a concrete dependency direction, reuse need, or packaging constraint requires movement. Prefer the standard library when it fully meets the stated need and matches the supported Python versions. Use a small function, class, dataclass, or module with one clear responsibility rather than a speculative protocol, registry, base class, or helper layer.
   - Keep import-time work minimal and deterministic. Put I/O, environment reads, process startup, and dependency construction at an explicit entry point or injected boundary when callers need control.
   - Use names that expose units, ownership, and failure meaning. Preserve local naming and import conventions rather than imposing a personal style.
   - When code is duplicated, first identify the differing policy and callers. Extract only a stable shared behavior; leave coincidental similarity alone.

3. **Make types express the supported interface.** Type public functions, methods, returned values, and stateful data where the project uses typing or the boundary is non-obvious. Use concrete built-in collection types when their semantics are required; use abstract collection interfaces for accepted inputs only when callers genuinely need alternatives. Model absence explicitly with an optional type, and model distinct valid states with a clear type or small value object.
   - Narrow uncertain values at the boundary with validation or runtime checks; type annotations do not validate untrusted input at runtime. Keep parsing, validation, and conversion errors actionable and close to the input boundary.
   - Prefer precise unions, protocols, generics, overloads, or type guards only when they make a real caller contract clearer. Do not hide uncertainty behind broad `Any`, untyped dictionaries, blanket casts, or suppression comments. If an unavoidable suppression is supported by the configured checker, keep it local and document the concrete limitation.
   - Do not expose mutable internal collections or mutable defaults. Create per-call mutable values and return an immutable or copied view when ownership requires it.

4. **Define failure and resource ownership.** Raise or translate exceptions only at a boundary that can add useful domain context. Preserve the original cause when translating; do not catch broad exceptions merely to log, return a sentinel, or continue. Let expected outcomes be normal return values only when the local API already models them that way.
   - Use context managers for files, locks, database sessions, network responses, temporary resources, and other acquire/release pairs. Put cleanup that must run on both success and failure in `finally` or the context manager exit path. Make ownership clear: a function either closes a resource it creates, documents transfer to its caller, or returns a context-managed abstraction.
   - Do not retain handles, iterators, generators, tasks, or callbacks beyond the lifetime their source permits. Close generators and streams when stopping early; do not rely on garbage collection for prompt cleanup.
   - Preserve interruption and cancellation. Perform necessary bounded cleanup, then propagate them unless the documented boundary intentionally converts them. Never use a bare `except` or silently discard an exception.

5. **Make synchronous and asynchronous boundaries explicit.** Keep code synchronous unless concurrent waiting or an async caller contract requires asynchronous execution. An async function is an API commitment, not a performance decoration.
   - In a coroutine, await async operations and avoid blocking I/O or long CPU work on the event-loop thread. Move blocking or CPU-bound work only through a project-supported boundary, and define its timeout, cancellation, error propagation, and resource ownership.
   - Give every created task an owner that awaits, collects, or deliberately supervises its result before the enclosing operation ends. Prefer structured task lifetimes when the supported Python version and project conventions provide them. Do not create background work that can outlive request, test, loop, or process shutdown without an explicit lifecycle contract.
   - Use async context managers for async resources. On timeout, cancellation, partial startup, or one concurrent failure, clean up all acquired resources and retain the primary failure rather than masking it with cleanup noise.
   - Do not cross a process, thread, or event-loop boundary with loop-bound objects, mutable shared state, or context-local assumptions without an explicit synchronization and lifetime design.

6. **Keep package and tooling behavior reproducible.** Follow `pyproject.toml` and the repository's selected package manager and build backend. Keep importable source in the established package layout; avoid `sys.path` mutation, source-tree-only imports, and implicit current-directory behavior. Use explicit package data and entry-point configuration when distribution needs them.
   - Change dependency declarations, lockfiles, extras, console entry points, build settings, or supported Python markers only when the requested behavior requires it. Use the repository's normal resolver/lock command; do not hand-edit generated lock state or install a global dependency as a workaround.
   - Exercise the built artifact or installed package in a clean, disposable environment when changing package discovery, entry points, package data, or build configuration. An import that works only from the checkout is not sufficient evidence.

7. **Measure before optimizing.** Define the representative workload, input size/distribution, environment, and user-relevant metric before changing code for speed or memory. Establish a baseline, change one candidate cause, and rerun the same workload. Use the standard library's timing, CPU profiling, or allocation-tracing tools when they answer the question; use a project-approved profiler only when its extra detail matters.
   - Separate CPU time, blocking/wait time, allocation growth, peak memory, and I/O latency. Inspect the measured hot path or allocation source before caching, parallelizing, pooling, or changing algorithms.
   - Keep a performance change only when the measurement is repeatable enough to distinguish it from noise and the added complexity is justified. Do not turn a one-off local timing into a permanent threshold without a stable workload and a stated regression risk.

8. **Validate at the affected boundary.** Use `efficient-testing` to select focused regression or behavior coverage. For Python-specific risks, exercise the observable exception contract, resource closure, import/package behavior, and async completion or cancellation path that changed. Use temporary paths, clocks, environments, and fakes supplied by the test framework or standard library; restore patched global state and do not require network access, real credentials, or production services.
   - Run the narrowest configured formatter, linter, type checker, test target, build, or installed-artifact check that reaches the changed boundary. Expand only when shared configuration, public interfaces, packaging, or the failure diagnosis makes a broader check relevant.
   - A passing type checker does not prove runtime validation, resource cleanup, cancellation behavior, or package installation. A passing test does not prove a performance claim without its recorded workload and measurement.

9. **Diagnose failures with evidence.** Classify a failure before changing another variable: product behavior, test expectation, static configuration, interpreter/version mismatch, dependency/build environment, resource leak, task lifecycle, or measurement setup. Preserve the smallest traceback, command, inputs, and environment facts needed to reproduce it; redact secrets.

| Signal | First response | Do not |
| --- | --- | --- |
| Type error | Check the runtime contract, narrow at the boundary, then revise the inaccurate annotation or implementation. | Add a broad cast, `Any`, or global suppression. |
| Unclosed resource or pending task | Identify the owner and exit path; add deterministic cleanup and a focused lifecycle check. | Rely on finalization, sleep, or test-order luck. |
| Async hang or cancellation failure | Minimize the task graph; inspect awaiting, timeout, cancellation, and shutdown paths. | Add retries or swallow cancellation. |
| Import/build-only failure | Reproduce from the built or cleanly installed artifact and inspect package configuration. | Patch `sys.path` or assume checkout imports prove packaging. |
| Performance regression | Reproduce the baseline workload and inspect measured hot paths or allocations. | Optimize from intuition or retain an unrepeatable benchmark. |

## Completion evidence

Report the contract preserved or intentionally changed; affected sync/async, exception, resource, typing, and packaging decisions; exact configured checks and their results; workload and before/after measurement for any performance claim; skipped or blocked validation; and remaining version, lifecycle, or environment risks. Stop when the requested Python behavior has proportionate evidence. Do not claim checks that did not run or guarantees that the selected Python/runtime boundary cannot provide.
