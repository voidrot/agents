---
name: go-project-layout
description: Structure Go repositories, cmd/internal/pkg layouts, modules, workspaces, tests, and right-sized project boundaries.
license: MIT
compatibility: Go projects using modules and standard Go tooling.
metadata:
  owner: voidrot
---

# Go Project Layout

Use this skill to right-size a Go repository structure. Keep small projects simple; add layers only when the codebase has real boundaries that need them.

## Workflow

1. Determine the project type: CLI, service, library, worker, monorepo, or small script.
2. Ask or infer the architecture constraint before creating layers; avoid clean/hexagonal/DDD scaffolding unless the project needs it.
3. Choose the module path to match the repository URL, all lowercase, with hyphens for multi-word repository names.
4. Put executable entrypoints in `cmd/<name>/` and keep `main` packages thin.
5. Put private application code in `internal/`; use `pkg/` only for code intended for external importers.
6. Co-locate `_test.go` files with the code under test and use `testdata/` for fixtures.
7. For multi-module repos, use `go.work` deliberately and keep module boundaries explicit.

## Layout Guide

| Project type | Typical layout |
| --- | --- |
| Small CLI or script | `main.go` or `cmd/<name>/main.go`, minimal `internal/` |
| CLI application | `cmd/<name>/`, `internal/`, optional `pkg/` for public libraries |
| Service or worker | `cmd/<service>/`, `internal/`, optional `api/`, `web/`, `migrations/` |
| Library | package directory at module root or `pkg/<name>/`, plus `internal/` for private helpers |
| Monorepo | `go.work` plus separate modules with clear ownership |

## Checks

- `cmd/` contains wiring and process setup, not business logic.
- Package names are lowercase, short, singular, and match directories; use `go-naming` for naming disputes.
- Config comes from environment, flags, or config files according to the app's needs; avoid hidden global state.
- Run `go test ./...` and `go vet ./...` after structural changes when possible.

## Constraints

- Do not add abstraction layers just to match a template.
- Do not use `pkg/` as a dumping ground; prefer `internal/` unless external consumers are intended.

## References

- For concrete directory trees and anti-patterns, read `references/directory-layouts.md`.
- For application config placement, read `references/config.md`.
- For test file layout, read `references/testing-layout.md`.
- For multi-module setup, read `references/workspaces.md`.
