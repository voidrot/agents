# Competing clusters — local-skill disambiguation

This repository currently has these local Go skills: `go-how-to`, `go-project-layout`, `go-code-style`, `go-naming`, `go-error-handling`, `go-testing`, `go-safety`, and `go-troubleshooting`.

Topics outside that list are still useful Go concerns, but they are not currently loadable local skills in this repo. Treat them as manual guidance, external documentation checks, or future skill candidates.

---

## 1. Debugging, performance, and observability

| Situation | Local routing |
| --- | --- |
| Panic, crash, deadlock, flaky behavior, unexpected output | Start with `go-troubleshooting`. |
| Nil panic, integer overflow, append aliasing, concurrent map write, zero-value hazards | Pair `go-troubleshooting` with `go-safety`. |
| Benchmark regressions, pprof, tracing, production metrics, allocation tuning | Use manual/external performance and observability guidance; pair with `go-troubleshooting` when there is an active bug. |

Examples:

- "The process crashes after 10 minutes under load" → `go-troubleshooting`; add `go-safety` if the evidence points to nil, aliasing, races, or other defensive-coding issues.
- "My benchmark regressed by 20%" → run manual benchmark/profile analysis; this repo has no separate local benchmark or performance skill.
- "Add Prometheus metrics and OpenTelemetry tracing" → use project-specific observability guidance; this repo has no separate local observability skill.

---

## 2. Error handling and runtime safety

| Skill | Unique territory |
| --- | --- |
| `go-error-handling` | Idiomatic error flow: creation, wrapping, `errors.Is`/`errors.As`, sentinel errors, custom error types, panic/recover boundaries. |
| `go-safety` | Preventing bad runtime states: nil checks, zero-value design, integer overflow guards, append aliasing, map concurrency hazards. |
| `go-troubleshooting` | Finding the root cause of a current failure before applying a fix. |

Examples:

- "How should I wrap errors so callers can match them?" → `go-error-handling`.
- "My service panics on nil pointer dereference" → `go-troubleshooting` to diagnose, then `go-safety` to make recurrence less likely.
- "I want structured errors with a third-party error builder" → use external library docs plus `go-error-handling` principles.

---

## 3. Style and naming

| Skill | Unique territory |
| --- | --- |
| `go-code-style` | Formatting conventions, declaration layout, comment placement, clarity-oriented control flow. |
| `go-naming` | Identifier naming rules: MixedCaps, package names, constructors, interfaces, receivers, errors, test names. |

Lint configuration and documentation standards are manual/external checks in this repo.

Examples:

- "How do I name my constructor?" → `go-naming`.
- "When should I add a blank line between declarations?" → `go-code-style`.
- "How do I configure golangci-lint?" → manual linter guidance; no separate local lint skill exists.
- "How should I write package-level godoc?" → manual documentation guidance; no separate local documentation skill exists.

---

## 4. Testing and testify

| Situation | Local routing |
| --- | --- |
| Test strategy, table-driven tests, fixtures, fuzzing, parallel tests, coverage | `go-testing` |
| Test names | `go-naming` plus `go-testing` |
| Test code readability | `go-code-style` plus `go-testing` |
| Testify assertions, mocks, suites, argument matchers | Use testify documentation; keep `go-testing` for overall test design. |

Examples:

- "How do I write a table-driven test in Go?" → `go-testing`.
- "How do I assert a mock was called with specific args?" → external/testify docs plus `go-testing` for test structure.
- "How do I detect goroutine leaks in tests?" → `go-testing`.

---

## 5. Project layout, CLI shape, and configuration

| Situation | Local routing |
| --- | --- |
| Starting a new Go project, deciding cmd/internal/pkg layout, monorepos, workspaces | `go-project-layout` |
| CLI exit codes, signal handling, terminal I/O, Cobra command trees, Viper configuration | Manual/project-specific CLI guidance; pair with `go-project-layout` when directory structure is involved. |
| go.mod strategy, version pinning, replace directives, dependency upgrades | Manual dependency-management guidance. |

Examples:

- "Where should my main package live?" → `go-project-layout`.
- "How do I add shell completion to a Cobra command?" → external Cobra docs/manual guidance.
- "Upgrade a dependency and update go.mod" → manual dependency-management workflow.

---

## 6. Architecture, concurrency, context, and type design

These topics are not currently split into local skills here. Use general Go design judgment and external references, then add local skills where they overlap:

- Use `go-safety` for race-prone or panic-prone patterns.
- Use `go-error-handling` for cancellation/error propagation semantics.
- Use `go-code-style` and `go-naming` for readable APIs and type names.
- Use `go-testing` for proving behavior.
- Use `go-project-layout` if the design changes package/module structure.

Examples:

- "How do I cancel a goroutine from outside?" → manual concurrency/context guidance, plus `go-safety` if leak/race risk is high.
- "Should my method take a value or pointer receiver?" → manual type-design guidance; use `go-naming` for receiver names and `go-code-style` for clarity.
- "How do I implement the functional options pattern?" → manual design-pattern guidance, then `go-testing` for behavior coverage.

---

## 7. Security and package discovery

Security review, vulnerability scanning, pkg.go.dev lookup, library selection, and module version research are manual/external checks in this repo.

Use local skills for adjacent concerns:

- `go-safety` for runtime correctness bugs that are not attacker-driven.
- `go-error-handling` for safe error propagation and boundary behavior.
- `go-troubleshooting` when a vulnerability report or dependency issue is causing a concrete failure.
- `go-testing` for regression tests around fixes.

Examples:

- "Is this SQL query safe from injection?" → manual security review; add `go-testing` for regression coverage.
- "What versions of a module exist?" → pkg.go.dev or other external package lookup.
- "Which logging library should I adopt?" → manual library evaluation.

---

## 8. samber and other library-specific guidance

This repo does not currently include local skills for samber/lo, samber/mo, samber/oops, samber/ro, samber/do, Cobra, Viper, gRPC, GraphQL, Swagger, Wire, Dig, or Fx.

When those libraries appear:

1. Use the library's official docs or source examples.
2. Apply `go-error-handling`, `go-safety`, `go-testing`, `go-code-style`, and `go-naming` where the library usage touches those concerns.
3. Treat repeated usage as a future candidate for a dedicated local skill.
