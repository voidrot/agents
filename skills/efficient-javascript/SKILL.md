---
name: efficient-javascript
description: Plan, implement, debug, refactor, and test ES6+ JavaScript runtime code; use for module semantics, asynchronous or event-loop behavior, browser or server runtime boundaries, performance measurement, project organization, and focused JavaScript tests—not TypeScript types, React, or generic web work.
---

# Efficient JavaScript

Use this skill for behavior in JavaScript that depends on the language or its executing runtime. Keep the existing observable contract: values and errors, side effects, ordering, module initialization, and supported runtime behavior.

Do not use it for TypeScript type-system design or diagnostics; use `efficient-typescript`. Do not use it for React rendering, component state, or React testing; use `efficient-react`. For semantic HTML, CSS, accessibility, responsive layout, or browser UI integration, use `efficient-web-development`. Use `efficient-testing` alongside this skill when the change needs its focused test-selection workflow.

## Workflow

1. **Identify the actual execution contract before editing.** Read the entry point, changed module, direct callers, closest tests, package manifest and lockfile, build configuration, and supported start/test commands. Record:
   - browser, server, worker, CLI, or test runtime;
   - exact runtime and version source, module format (ESM or CommonJS), package `type`, and any bundler or transpiler boundary;
   - public inputs and outputs; error, cancellation, and cleanup owners; and observable initialization or import side effects.

   Do not infer Node, Bun, Deno, edge, browser, or test-environment behavior from another runtime. If the runtime or module mode is unknown, stop before changing import order, module syntax, global APIs, or lifecycle code; obtain the start command or configuration that establishes it.

2. **State the smallest behavioral change.** Describe the input, result, side effects, error behavior, and ordering that must remain or change. For a defect, first reproduce the reported symptom with a deterministic command or focused test, then reduce it to the smallest case. Keep refactoring separate from a behavior change unless the same small edit is necessary to make the contract explicit. Do not introduce an abstraction, package, compatibility layer, or configuration flag without a demonstrated caller or runtime need.

3. **Apply JavaScript semantics deliberately.** Preserve distinctions the contract observes: absent property versus `undefined` versus `null`, truthy/falsy values, object identity and mutation, and synchronous throw versus rejected promise. Use strict equality when the intended comparison is exact; use a nullish check or default only when `null` and `undefined` are the values to replace. Do not replace a loop, callback, function form, or object update merely for modern syntax when it could change `this`, evaluation order, holes, getters, mutation, or error timing.

4. **Preserve the module boundary.** Follow the repository's established ESM or CommonJS convention for the affected package. Keep exports, import evaluation side effects, circular-dependency behavior, and public file paths stable unless the requirement changes them. Do not mix `require` and `import`, alter extension or package-export resolution, or move initialization across imports on assumption. When an import fails, inspect the selected runtime's module mode, package metadata, resolved artifact, and build output before changing source or configuration.

5. **Make asynchronous ownership explicit.** Classify each path as a returned promise, callback, event listener, timer, stream, or intentionally detached task.
   - Return or `await` work whose completion affects the caller's result. Handle a deliberately detached task at its launch point, including a defined error and cancellation owner.
   - Catch an error only at a boundary that can recover, translate it to a documented result, or report it before preserving propagation. Preserve the original error and causal information when wrapping; never convert a failure to success by logging and continuing.
   - Clean up listeners, timers, streams, and per-request resources on the completion, cancellation, and failure paths that own them. Do not use a timer as a synchronization guarantee: promise jobs, timer tasks, I/O, and rendering callbacks have distinct scheduling rules.
   - Treat an unhandled rejection, callback error, or test timeout as missing async ownership. Locate the producer and consumer before adding retries, suppression, or a catch-all handler.

6. **Put failure boundaries in the correct runtime layer.** In a browser, handle expected failures at the interaction, request, or application boundary that can update user-visible state; treat global handlers as last-resort observation, not recovery. In a server, preserve request or job isolation and let the framework's documented outer error boundary produce the existing response or retry behavior. Do not store request data in process-global mutable state. Verify framework middleware order, startup order, permissions, shutdown, and termination against the selected runtime and installed framework; server runtimes are not interchangeable. For Sentry-specific initialization or capture ownership, use `sentry-sdk` or `sentry-errors` rather than duplicating their setup here.

7. **Organize only around an observed boundary.** Put a cohesive public operation and its private helpers near the existing feature or domain boundary. Keep I/O adapters at the edges and pass dependencies or data through explicit parameters where the surrounding code already does so. Prefer a direct module and named operation over barrels, registries, base classes, or utility layers created for a single caller. Do not rearrange unrelated files while fixing an execution defect.

8. **Measure before optimizing.** Define a representative scenario, input size, runtime, and user-meaningful metric such as elapsed time, latency distribution, memory growth, or event-loop delay. Capture a baseline using the runtime's supported profiler or timing facility, change one suspected cost, then rerun the same scenario under comparable conditions. Inspect the hot path before caching, batching, parallelizing, or replacing an algorithm. Retain the measurement command, environment, sample limits, and result; do not claim a speedup from a different workload or a single noisy timing. If results are inconclusive, remove the speculative optimization and report the limit.

9. **Add JavaScript-specific focused evidence.** Test the public contract in the runtime it needs: a pure module directly; a server operation with controlled I/O; a browser behavior in a browser-capable environment only when DOM behavior is part of the contract. Await promises and assert rejection or result explicitly; do not let a test finish before asynchronous work settles. Isolate global state, environment variables, module caches, timers, network calls, and listeners, restoring them after each test. Use fake time only when time scheduling is the contract, and deliberately flush the task queues that the test depends on. Prefer a real small collaborator or boundary injection over a mock that repeats production logic.

10. **Verify the delivered artifact.** Run the narrowest existing lint, test, build, or start command that reaches the changed path, then rerun it after a material edit. Verify production-like output when bundling, module resolution, source mapping, or runtime startup is affected. For a browser/server difference, run the affected runtime rather than accepting a test-environment result as equivalence. Run a broader existing check only when shared modules, build configuration, or the changed entry boundary warrants it. Do not install a runner, dependency, polyfill, or benchmark tool merely to validate a narrow change.

## Failure handling

- **The symptom cannot be reproduced:** preserve the supplied inputs, runtime version, command, logs, and timing; minimize one variable at a time. Do not code to an unverified theory. Report the missing reproducer and the next smallest observation that can distinguish the leading hypotheses.
- **Module behavior differs after a change:** restore the known-good module boundary, then compare package metadata, runtime command, generated artifact, and import order. Do not "fix" it by mixing module systems or changing every import.
- **An async change times out or duplicates work:** trace completion, cancellation, and error ownership across every promise and callback. Remove temporary instrumentation after identifying the owner; do not add arbitrary delays or retries.
- **A runtime-specific API is unavailable:** retain the supported runtime behavior and verify the target's current documentation and installed version. Do not silently substitute a browser, Node, Bun, Deno, or edge API.
- **A performance result regresses or varies:** retain the baseline and profiler evidence, undo the unsupported optimization, and investigate workload, allocation, I/O, or scheduling separately before retrying.

## Completion evidence

Report only evidence obtained:

- runtime, module mode, entry point, and contract inspected;
- changed behavior and preserved side effects, ordering, and error ownership;
- focused test or reproduction and exact command/result, including test-environment limits;
- performance baseline and comparison when optimization was requested; or why measurement was not reached;
- commands skipped or blocked, their exact prerequisite or failure, and remaining runtime-specific risk.

Stop when the requested JavaScript behavior has direct evidence in its target runtime. Do not broaden the change into TypeScript, React, UI, framework setup, or a general code cleanup.
