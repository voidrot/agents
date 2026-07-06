---
name: pytest-coverage
description: Use when running pytest with coverage, finding uncovered Python lines or branches, and adding targeted tests until a requested coverage threshold is met.
---

# Pytest Coverage

Use this skill when the task is to measure Python test coverage, inspect uncovered lines, and close coverage gaps with focused tests.

## Workflow

1. Confirm the target package/module, desired threshold, and whether branch coverage is required.
2. Run pytest with coverage for the smallest meaningful scope, for example `pytest --cov=<module> --cov-report=term-missing --cov-report=annotate:cov_annotate`.
3. Inspect uncovered files in the terminal report or `cov_annotate`; lines prefixed with `!` are missing line coverage.
4. Add focused tests for behavior, edge cases, and error paths instead of tests that only execute code.
5. Repeat coverage and relevant test runs until the target is met or remaining gaps need a product/design decision.

## Constraints

- Do not chase 100% coverage with brittle tests when the user requested a lower threshold.
- Prefer behavior assertions over implementation-only coverage.
- Keep generated coverage artifacts out of commits unless the project explicitly tracks them.

## Expected output

- Coverage command and scope used.
- Coverage before/after, including remaining uncovered lines if any.
- Tests added or changed, and any gaps intentionally left uncovered.
