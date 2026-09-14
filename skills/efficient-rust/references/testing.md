# Conditional Rust testing reference

Read this only when a Rust change needs test design beyond the normal focused validation workflow. Use the repository's existing test runner, runtime, property-test support, and benchmark tooling; do not introduce a testing dependency or tool merely to follow this reference. Use `efficient-testing` for generic test-selection and regression workflow.

## Choose the boundary

- Put isolated private logic in a nearby `#[cfg(test)]` module. Keep integration tests in the crate's `tests/` directory when they must exercise the public API or cross-module wiring; each top-level integration-test file is a separate crate.
- For a `Result`, assert the contractual error variant and relevant source, state, or recovery effect. Do not assert rendered error text unless that text is the interface.
- Test a panic only when panicking is the contract for a programmer-invariant violation. Prefer a fallible API's error assertion otherwise; constrain an expected panic message only when it is stable and meaningful.

## Respect async runtime boundaries

Run async tests with the runtime and test configuration already used by the project. Do not nest, mix, or add runtimes for a test. Await spawned work and assert its result; make cancellation, shutdown, and timeout behavior explicit. Prefer the project's deterministic synchronization or time controls to wall-clock sleeps.

## Use generative and performance evidence selectively

Add property tests only for invariant-rich behavior where many generated inputs add evidence, such as round trips, ordering, parser totality, or bounds preservation. Keep generators within the supported input domain and retain a direct regression example for a known failure.

For a performance claim, use the project's supported benchmark or measurement harness with a representative workload. Record the baseline, post-change result, and material trade-off; do not treat a unit-test duration or an unmeasured benchmark as performance evidence.
