---
name: go-code-style
description: Review Go readability, declarations, control flow, comments, and idiomatic clarity beyond gofmt.
license: MIT
compatibility: Go projects using gofmt and standard Go idioms.
metadata:
  owner: voidrot
---

# Go Code Style

Use this skill for judgment-based style that formatters do not cover. `gofmt` handles whitespace; this skill handles clarity.

## Workflow

1. Run or preserve `gofmt`/`gofmt -s`; do not hand-format Go code.
2. Review control flow first: handle errors and edge cases early, keep the happy path shallow.
3. Check declarations: use `:=` for initialized values and `var` when the useful zero value is intentional.
4. Break long lines at semantic boundaries, especially calls or signatures with many arguments.
5. Prefer explicit field names in composite literals.
6. Keep comments focused on why, invariants, exported API contracts, or surprising behavior.
7. If style and naming overlap, apply `go-naming` for identifier choices.

## Checklist

- Errors and guard clauses return early; unnecessary `else` blocks are removed after `return`, `break`, or `continue`.
- Complex boolean expressions are extracted into named booleans when the names improve understanding.
- Slices and maps are initialized intentionally; preallocation is used when expected size is known.
- Long function parameter lists are questioned, not merely wrapped; consider an options struct when the API is getting wide.
- Composite literals for structs use field names.
- Comments do not restate obvious code; they document constraints, tradeoffs, or exported behavior.
- Code remains boring and explicit over clever or compressed.

## Constraints

- Do not fight `gofmt`.
- Do not enforce a rigid line length when a readable exception is better, but treat lines over roughly 120 characters as a review prompt.
- Do not use this skill for linter configuration; use project tooling or add a dedicated lint skill when needed.

## References

- For detailed examples of complex conditions, loops, comments, imports, and API boundaries, read `references/details.md`.
