---
name: python-testing-patterns
description: "Use for Python pytest tests, fixtures, mocks, parametrization, coverage, TDD, async tests, and CI test setup."
---

# Python Testing Patterns

Use this skill to design or repair Python tests with pytest. It is the canonical Python testing skill; the retired `python-testing` content has been merged here.

## When to Use

- Writing unit, integration, API, database, or async tests
- Setting up pytest, fixtures, markers, coverage, or CI test runs
- Applying TDD or improving test design and isolation
- Mocking external dependencies, time, files, network calls, or queues
- Debugging brittle, slow, or unclear Python tests

## Boundary

- Use `async-python-patterns` for async/concurrency architecture; use this skill only for testing async code.
- Use `django-celery` for Django-specific Celery task testing.
- Use `python-background-jobs` for queue/worker architecture and job lifecycle design.

## Workflow

1. Identify the behavior under test and choose the smallest useful test type.
2. Prefer clear AAA structure: arrange, act, assert.
3. Isolate external systems with fixtures, fakes, `monkeypatch`, or `unittest.mock`.
4. Cover success, failure, edge, and retry/idempotency paths.
5. Keep tests deterministic: control time, randomness, environment, and I/O.
6. Run the focused test first, then the relevant suite and coverage gate.

## Key Rules

- Test behavior, not implementation details.
- Keep one primary behavior per test.
- Use descriptive names such as `test_create_user_with_duplicate_email_raises_conflict`.
- Prefer `tmp_path`, fixtures, and `pytest.raises(..., match=...)` over manual cleanup or broad exception checks.
- Mark slow/integration tests so fast unit tests stay fast.
- Treat coverage as a signal; require high coverage for critical paths.

## References

- [Detailed pytest patterns](references/details.md) — basic pytest, fixtures, parametrization, mocking, exceptions, and test design.
- [Advanced patterns](references/advanced-patterns.md) — async testing, monkeypatching, temporary files, property-based tests, database tests, CI, and configuration.
