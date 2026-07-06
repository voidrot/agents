---
name: e2e-testing-patterns
description: Use when designing or maintaining end-to-end browser tests, user journeys, selectors, test data, CI execution, debugging, and flaky-test reduction.
---

# E2E Testing Patterns

Use when designing or maintaining end-to-end browser tests, user journeys, selectors, test data, CI execution, debugging, and flaky-test reduction.

## Workflow

1. Confirm the framework, package manager, runtime versions, and constraints before applying patterns.
2. Open only the supporting reference that matches the task; avoid loading the whole reference set by default.
3. Prefer the smallest idiomatic change that preserves existing architecture and public behavior.
4. Validate with the project’s relevant type checks, tests, linting, build, or browser checks.

## Supporting Material

- Read `references/full-guidance.md` for the migrated long-form guidance, examples, and checklists from the source skill.
- Read `references/details.md` for additional details guidance.

Keep this `SKILL.md` as the concise activation and routing entry point; put long examples, matrices, and reusable snippets in `references/`.
