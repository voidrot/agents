---
name: go-testing
description: Write, review, organize, and debug Go tests, including table tests, integration tests, race checks, fuzzing, and examples.
license: MIT
compatibility: Go projects using the standard testing package.
metadata:
  owner: voidrot
---

# Go Testing

Use this skill to write tests as executable specifications. Prefer behavior-focused tests that constrain the public contract over tests that mirror implementation details.

## Workflow

1. Identify the behavior, API boundary, and observable outcomes under test.
2. Start with the smallest reliable test: unit test, table-driven test, integration test, fuzz test, or example.
3. Name table cases and run each with `t.Run`.
4. Cover happy paths, edge cases, and important error paths.
5. Keep tests deterministic and independently runnable; isolate filesystem, clock, network, and environment dependencies.
6. Use `t.Parallel()` only when shared state, environment variables, temp directories, and ports are safe.
7. Run `go test ./...`; add `go test -race ./...` for concurrency-sensitive code when possible.

## Checklist

- Test files are co-located with code and named `_test.go`.
- Same-package tests are used for white-box coverage; `_test` package tests are used for public API behavior.
- Table-driven tests include a `name` field and clear expected values.
- Assertions report enough context to debug failures.
- Integration tests are separated with build tags such as `//go:build integration` when they need external services.
- Tests do not depend on order, global state, current time, or real network access unless explicitly isolated.
- Examples double as documentation when API usage matters.

## Debugging Failed Tests

1. Reproduce the failure with a focused `go test` command.
2. Make flakes deterministic before changing production code.
3. Change one hypothesis at a time.
4. Use `go-troubleshooting` when the failure points to a deeper bug, race, deadlock, or panic.

## References

- For HTTP handler tests, read `references/http-testing.md`.
- For integration test isolation and build tags, read `references/integration-testing.md`.
- For helper functions and fixtures, read `references/helpers.md`.
- For mocks and test doubles, read `references/mocking.md`.
