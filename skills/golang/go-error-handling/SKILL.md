---
name: go-error-handling
description: Design and review Go error creation, wrapping, inspection, panic boundaries, and structured logging semantics.
license: MIT
compatibility: Go projects using standard errors, fmt, and log/slog.
metadata:
  owner: voidrot
---

# Go Error Handling

Use this skill when the task is about error meaning, propagation, inspection, or logging. Every error should be checked, handled once, or returned with useful context.

## Workflow

1. Check every returned error; do not discard errors with `_` unless there is an explicit documented reason.
2. Add context while propagating errors with `fmt.Errorf("operation: %w", err)`.
3. Inspect wrapped chains with `errors.Is` for sentinels and `errors.As` for typed errors.
4. Apply the single-handling rule: log an error or return it, not both.
5. Use sentinels for expected comparable conditions and custom error types when callers need structured data.
6. Reserve `panic` for programmer errors or unrecoverable initialization failures; recover only at process or goroutine boundaries where you can log and contain the failure.
7. Translate internal errors before showing user-facing messages.

## Checklist

- Error strings are lowercase and have no trailing punctuation.
- Wrapping context describes the failed operation, not the caller's hoped-for action.
- `%w` is used when callers should be able to inspect the chain; `%v` is used only when intentionally hiding the chain at a boundary.
- Logs use stable, low-cardinality messages with IDs and dynamic values as structured attributes.
- Expected absence or validation failures have clear sentinel or typed errors when callers branch on them.
- Tests cover important error paths, not only the happy path.

## Related Skills

- Use `go-safety` for preventing panics, nil-interface traps, defensive copies, and resource-lifetime hazards.
- Use `go-troubleshooting` when errors are evidence in an active failure whose root cause is not yet known.
- Use `go-naming` for `ErrNotFound`, `PathError`, and error message naming conventions.

## References

- For sentinel errors, custom error types, and message construction, read `references/error-creation.md`.
- For `%w`, `%v`, `errors.Is`, `errors.As`, and joined errors, read `references/error-wrapping.md`.
- For single handling, panic/recover, and structured logging patterns, read `references/error-handling.md`.
