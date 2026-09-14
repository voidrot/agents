---
name: efficient-testing
description: Decide, write, update, and run focused unit or regression tests for changed behavior in any language; use for targeted tests of a code change or confirmed bug, not E2E-only work, coverage maximization, framework setup, fuzz/property testing, or broad suite refactors unless focused unit/regression testing is also needed.
---

# Efficient Testing

Use this skill to produce the smallest reliable unit or regression evidence for a code change. A test is an executable statement of an observable contract, not a branch-coverage exercise.

Do not use this skill as the primary workflow for E2E-only work, installing or configuring a test framework, maximizing coverage, fuzz or property testing, or a broad test-suite refactor. If one of those tasks also changes behavior that needs a focused unit or regression test, use this workflow for that portion.

## Workflow

1. **Establish the change and its contract.** Read the requirement, issue or defect report, changed code, and the closest relevant tests. Identify the public input, observable result or effect, and one scenario that proves the intended behavior. Inspect local test documentation, configuration, scripts, and nearby tests to learn the supported runner, test location, naming, and prerequisites. Do not reproduce an elaborate existing pattern merely because it exists.
2. **Decide whether to add a test.**
   - For new or changed behavior, start with the happy path focused on one behavior. Stop there unless another case is justified below.
   - For a pure refactor with no changed observable contract, normally update tests only when a change to the supported public interface breaks an existing test; run the relevant existing tests instead of inventing new coverage.
   - Add one edge or failure scenario only when an explicit requirement, production contract, or confirmed/surfaced defect calls for it. Do not add speculative inputs, permutations, or hypothetical failures.
   - For a confirmed defect, add the smallest discriminating regression test that reproduces the reported behavior. When practical, retain evidence that it fails before the fix and passes after it. If a pre-fix run is impossible, record why rather than claiming it failed.
3. **Choose the smallest proving level.** Prefer a direct unit test of the public contract. Move to a component, database, or service-dependent test only when the behavior cannot be established at a lower level. Do not test test-framework behavior, mocks, fixtures, helpers, or test utilities solely for their own sake. Add input or entry-point contract validation only when the public boundary genuinely requires it; otherwise prefer a self-contained setup.
4. **Write a discriminating test.** Give the test a scenario-and-outcome name. Arrange only the inputs and dependencies necessary for the case, perform one meaningful action, then assert independent observable outcomes. Use fixed expected values or an independently known result; do not calculate expected output with the production algorithm. Keep it isolated from test order, clocks, network availability, shared state, and unrelated implementation details. Use the runner's native helpers, lifecycle hooks, and temporary-resource facilities for setup and deterministic cleanup when available. For concurrent tests, synchronize on an explicit condition or completion signal; do not use sleeps as synchronization. Assert public results rather than private calls, fields, or intermediate steps unless the public contract explicitly exposes them.
5. **Make prerequisites explicit and safe.** Record the exact targeted command used and, when discoverable, the runner and version source. Record required configuration, local databases or services, ports, OS or network constraints, and test-data setup. Use isolated disposable data and safe cleanup. Never require real credentials or an external production service. Read [framework runner notes](references/framework-runners.md) for a verified local-runner selection process and [database and service test notes](references/database-and-service-tests.md) before tests that need infrastructure.
6. **Run proportionately.** First run the narrowest supported target that reaches the new or changed test. Rerun it after a relevant code or test change. Run a broader relevant group only when required by project policy or when shared code, configuration, dependencies, or the changed boundary makes it necessary. Treat coverage as a diagnostic signal: use it to investigate an unexpected gap, never as a quota or a reason to exercise every branch.
7. **Diagnose failures before expanding scope.** Determine whether a failure is a product defect, an incorrect expectation, an unstable/order-dependent test, a runner/configuration issue, or unavailable infrastructure. Preserve the failure output and relevant setup facts. Fix the identified cause; do not weaken assertions, add retries, or broaden scenarios to make a failure disappear. If prerequisites cannot be met safely, report the test as blocked with the missing requirement and the smallest next action.

## Completion evidence

Report only evidence actually obtained:

- the behavior and scenario covered, and why any edge or failure case was justified;
- test file or location and the public contract asserted;
- targeted command, runner/version evidence when known, and pass/fail result;
- prerequisite and isolation details for any database or service dependency;
- for a defect, pre-fix failure evidence when obtained and the post-fix pass result; or the reason pre-fix proof was not practical;
- relevant limits, skipped checks, baseline failures, or blocked infrastructure.

Stop when the changed contract has focused evidence and any required regression is covered. Do not add cases merely to increase count or coverage.
