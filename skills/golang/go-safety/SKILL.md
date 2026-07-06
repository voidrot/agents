---
name: go-safety
description: Prevent Go panics, aliasing bugs, concurrent map access, leaks, numeric truncation, and unsafe zero values.
license: MIT
compatibility: Go projects using standard Go runtime semantics.
metadata:
  owner: voidrot
---

# Go Safety

Use this skill for preventive correctness review and defensive coding. It applies before or during implementation, or after troubleshooting identifies a concrete safety pitfall.

## Workflow

1. Check nil behavior first: interfaces, maps, slices, channels, receivers, and returned values.
2. Review slices and maps for aliasing, defensive copies, unexpected mutation, and concurrent access.
3. Check resource lifetime: `defer` in loops, unclosed files/rows/bodies, missing context cancellation.
4. Validate numeric conversions, division, and floating-point comparisons.
5. Prefer compile-time safety: concrete types, generics, and comma-ok assertions over unchecked casts.
6. Verify with focused tests, `go test ./...`, and `go test -race ./...` for concurrency-sensitive changes.

## Checklist

- Typed nil pointers are not returned as non-empty interfaces; return explicit `nil` when appropriate.
- Maps are initialized before writes.
- Nil slices are acceptable only when their JSON/API behavior is intentional.
- Exported slices and maps are defensively copied when callers must not mutate internals.
- Appending to a subslice cannot unexpectedly mutate shared backing arrays.
- Maps are not read and written concurrently without synchronization.
- `defer` inside loops does not accumulate resources until function exit.
- Integer narrowing checks bounds before conversion.
- Float equality uses an epsilon or a decimal/big-number type when exactness matters.

## Related Skills

- Use `go-troubleshooting` when a failure is active and the suspected safety issue still needs proof.
- Use `go-error-handling` for error propagation, inspection, logging semantics, and panic/recover boundaries.
- Use `go-testing` to lock safety fixes with regression tests.

## References

- For nil interfaces, receivers, maps, slices, and channels, read `references/nil-safety.md`.
- For slice aliasing, map concurrency, range pitfalls, and defensive copies, read `references/slice-map-safety.md`.
