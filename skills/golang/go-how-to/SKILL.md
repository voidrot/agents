---
name: go-how-to
description: Choose the right focused Go skill before coding, reviewing, testing, debugging, or restructuring Go projects.
license: MIT
compatibility: Go projects using standard Go tooling.
metadata:
  owner: voidrot
---

# Go Skill Routing

Use this skill only as a router. Once the task is classified, follow the most specific Go skill and return here only if the work crosses boundaries.

## Workflow

1. Classify the request: layout, style, naming, errors, tests, safety, or troubleshooting.
2. Pick one primary skill; add secondary skills only for real cross-cutting concerns.
3. Resolve overlaps by risk: active failures → troubleshooting; preventive correctness → safety; error API/logging semantics → error handling.
4. Run the relevant Go command when possible: `go test ./...`, `go test -race ./...`, `go vet ./...`, or project-specific checks.

## Routing Table

| Intent | Use | Also consider |
| --- | --- | --- |
| Create or reorganize a Go repo | `go-project-layout` | `go-naming`, `go-testing` |
| Improve readability and control flow | `go-code-style` | `go-naming` |
| Choose package, type, function, or test names | `go-naming` | `go-code-style` |
| Create, wrap, inspect, or log errors | `go-error-handling` | `go-safety` |
| Write, review, or debug tests | `go-testing` | `go-troubleshooting` for failures |
| Prevent panics or subtle correctness bugs | `go-safety` | `go-error-handling` |
| Diagnose crashes, flakes, races, hangs, or wrong output | `go-troubleshooting` | `go-safety`, `go-testing` |

## Boundaries

- This skill routes work; it is not a Go handbook and should not duplicate focused skill checklists.
- When a specialized skill exists, follow that skill after choosing it.
- For specialized Go domains not yet imported here, use ordinary project investigation and official Go documentation until a local skill is added.

## References

- For the broader Go skill catalog and activation cues, read `references/by-category.md`.
- For overlap between similar Go skills, read `references/disambiguation.md`.
- For project-level skill trigger guidance, read `references/project-config.md`.
