---
name: python-resource-management
description: Manage Python files, connections, locks, streams, and cleanup lifecycles safely.
---

# Python Resource Management

## When to use

- writing or reviewing context managers and cleanup code
- managing files, sockets, database sessions, async clients, locks, or streams
- debugging resource leaks, double-close bugs, or cancellation cleanup

## Workflow

1. Identify who owns acquisition, lifetime, and release of each resource.
2. Prefer with/async with and contextlib helpers for deterministic cleanup.
3. Keep cleanup idempotent and exception-safe.
4. Handle cancellation and partial initialization explicitly in async code.
5. Test both normal completion and failure during acquisition/use/release.

## Constraints

- Do not rely on garbage collection for critical cleanup.
- Avoid sharing mutable resource handles across unrelated lifetimes.
- Move extended sync/async examples to references.

## References

- [resource-management examples](references/details.md)
- [moved lifecycle guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
