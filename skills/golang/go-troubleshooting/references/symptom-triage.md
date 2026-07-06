# Symptom Triage

Use this file after the failure is captured but before broad investigation.

| Symptom | First checks |
| --- | --- |
| Compile failure | Run `go build ./...` or the focused package test; inspect the reported file, line, type mismatch, or missing module. |
| Wrong output | Add a focused failing test; trace inputs, state mutation, and error handling. |
| Panic | Capture the full stack with `GOTRACEBACK=all`; inspect nil values, bounds, type assertions, and goroutine ownership. |
| Race or flake | Run a focused `go test -race`; isolate shared state, timing assumptions, and cleanup order. |
| Hang or deadlock | Inspect goroutine stacks, blocked channels, locks, WaitGroups, and missing context cancellation. |
| High CPU | Reproduce first, then use CPU profiles or benchmarks to identify hot paths. |
| Memory growth | Reproduce first, then compare heap profiles and check retained references, caches, goroutines, and unclosed resources. |

Prefer the official Go tools first: `go test`, the race detector, pprof profiles, execution traces, and runtime diagnostics. Use Delve when interactive source-level inspection is necessary.
