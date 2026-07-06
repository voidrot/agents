---
name: temporal-python-testing
description: Use when testing Temporal Python workflows or activities with pytest, time-skipping, mocked activities, replay testing, local test servers, or CI coverage for workflow determinism.
---

# Temporal Python Testing

Use this skill for Temporal Python SDK tests where workflow determinism, activity isolation, time-skipping, or worker/test-environment setup matters.

## Workflow

1. Identify the test type: workflow unit/time-skipping, activity unit, integration with mocked activities, replay determinism, or local end-to-end setup.
2. Verify Temporal SDK and pytest async tooling versions before copying version-sensitive APIs.
3. Build tests around Temporal's testing environment and workers; isolate external systems behind activities or test doubles.
4. Cover timer, retry, signal, query, cancellation, and failure paths that affect workflow behavior.
5. Run focused pytest tests and replay checks before changing deployed workflow code.

## Constraints

- Preserve workflow determinism; do not add nondeterministic calls to workflow code just to simplify tests.
- Prefer integration-style workflow tests for orchestration logic and activity tests for external I/O behavior.
- Keep local server or Docker setup optional unless the test explicitly needs it.

## References

- Read `references/unit-testing.md` for workflow and activity unit tests.
- Read `references/integration-testing.md` for mocked activities, signals, queries, and coverage strategy.
- Read `references/replay-testing.md` before deploying workflow changes or validating determinism.
- Read `references/local-setup.md` for local Temporal server and pytest setup.
- Read `references/full-guidance.md` for the original overview and quick-start examples.

## Expected output

- Chosen Temporal test strategy and why.
- Test cases added or recommended, including determinism/replay coverage when relevant.
- Commands run and any SDK/version assumptions.
