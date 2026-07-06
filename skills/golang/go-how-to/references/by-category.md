# Go skills — local catalog by category

This repository currently includes 8 local Go skills. Skills marked ⭐️ are recommended for most Go projects. Topics not listed as headings below are not currently loadable local skills; handle them with manual guidance, general Go knowledge, or external documentation.

---

## Code Quality

### `go-code-style` ⭐️ ⚙️

Go code formatting, conventions, and project-level style consistency — gofmt, goimports, line length, var declarations, blank lines, comment heuristics.

Use when: the user asks about formatting rules, style review, or project coding standards. Not for naming conventions (→ `go-naming`). Linter configuration and documentation standards are manual/external checks in this repo.

---

### `go-error-handling` ⭐️ ⚙️

Go error handling best practices — error creation, wrapping with fmt.Errorf and errors.Is/As, sentinel errors, custom error types, panic recovery.

Use when: writing or reviewing error propagation, wrapping, logging, or recovery patterns. For preventing panics → `go-safety`. Structured-error libraries such as samber/oops require manual/external guidance.

---

### `go-naming` ⭐️ ⚙️

Go naming conventions across all identifier types — packages, constructors, structs, interfaces, constants, errors, receivers, acronyms, test functions. Covers MixedCaps rules, Get-prefix, and utils/helpers anti-patterns.

Use when: naming a new type, function, package, or constant. Not for broader formatting (→ `go-code-style`).

---

### `go-safety` ⭐️

Defensive Go coding — prevents panics, silent data corruption, and runtime bugs. Nil safety, append aliasing, map concurrent access, float comparison, zero-value design, numeric overflow.

Use when: writing or reviewing code that could silently produce wrong results or panic. Not for external threats; security review is a manual/external check in this repo. For error handling idioms → `go-error-handling`.

---

## Architecture & Design

Concurrency, context propagation, data structures, database access, dependency injection, design patterns, and modernization are not currently local skills in this repo. Cover them with manual Go guidance or external references, and pair with `go-safety`, `go-error-handling`, or `go-testing` when those local skills apply.

---

## QA & Performance

### `go-testing` ⭐️ 🧠 ⚙️

Production-ready Go tests — table-driven tests, fuzzing, fixtures, goroutine leak detection (goleak), snapshot testing, code coverage, integration tests, parallel tests.

Use when: writing or reviewing tests. Testify-specific APIs and performance measurement are manual/external checks in this repo.

---

### `go-troubleshooting` ⭐️ 🧠

Systematic Go debugging — common pitfalls, test-driven debugging, pprof capture, Delve debugger, race detection, GODEBUG tracing, production debugging.

Use when: debugging a panic, unexpected output, or hard-to-reproduce bug. Profile interpretation and optimization patterns require manual/external guidance.

---

## Project Setup

### `go-project-layout`

Go project structure and workspace setup — cmd/internal/pkg conventions, monorepo layout, CLI project structure, and when to keep things flat.

Use when: starting a new project or restructuring an existing one. Architectural patterns, CLI frameworks, dependency management, API frameworks, and library-specific topics are manual/external guidance unless one of the local skills above directly applies.
