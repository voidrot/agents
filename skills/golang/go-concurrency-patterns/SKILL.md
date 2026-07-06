---
name: go-concurrency-patterns
description: Use when designing, implementing, reviewing, or debugging concurrent Go code with goroutines, channels, select, sync primitives, worker pools, cancellation, or graceful shutdown.
---

# Go Concurrency Patterns

Use this skill for production Go concurrency work where goroutine lifetime, cancellation, synchronization, or shared state correctness matters.

## Workflow

1. Identify the concurrency boundary: task ownership, cancellation source, error propagation, and result collection.
2. Choose the simplest primitive that fits: sequential code, `context.Context`, `sync` primitives, channels, worker pools, or pipelines.
3. Make goroutine exit paths explicit and testable; avoid relying on sleeps or unbounded background work.
4. Check for data races, channel close ownership, leaked goroutines, blocked sends/receives, and lost errors.
5. Verify with focused tests and, when relevant, `go test -race`.

## Constraints

- Prefer no concurrency unless it improves latency, throughput, isolation, or cancellation behavior.
- The sender owns channel closure; receivers should not close channels they do not own.
- Propagate cancellation with `context.Context` and ensure every goroutine can observe shutdown.
- Use `go-testing`, `go-safety`, and `go-troubleshooting` for adjacent test, panic/race, or debugging work.

## References

- Read `references/details.md` for worked concurrency patterns, worker pools, pipelines, rate limiting, and race debugging.
- Read `references/full-guidance.md` for the original candidate guidance and examples.

## Expected output

- The selected concurrency pattern and why it is needed.
- Key ownership decisions for goroutines, channels, cancellation, and errors.
- Tests/checks run, especially race or leak checks, or a reason they were not run.
