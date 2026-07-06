---
name: go-troubleshooting
description: Diagnose Go failures with evidence-first reproduction, tracing, race, pprof, and testing workflows.
license: MIT
compatibility: Go projects using standard Go diagnostics and testing tools.
metadata:
  owner: voidrot
---

# Go Troubleshooting

Use this skill for Go-specific root-cause debugging. It starts after something is failing or suspicious and ends when the failure mechanism is explained, fixed, and covered where practical.

## Workflow

1. Capture the exact symptom: error, panic stack, failing assertion, hang, race report, profile clue, or production signal.
2. Reproduce with the smallest reliable `go test`, `go test -race`, `go build`, benchmark, or project command.
3. Classify the failure and choose the relevant reference before collecting more data.
4. Test one hypothesis at a time; trace callers, data flow, goroutines, and resource lifetime only as far as needed.
5. Fix the root cause, not the first visible symptom.
6. Add or update a regression test when feasible, then rerun focused and broader checks.

## Rules

- Reproduce before fixing; change one thing at a time.
- Prefer evidence from tests, race detector reports, logs, traces, or profiles over intuition.
- Use `go-safety` when the work is preventive hardening or a known nil/slice/map/resource-lifetime pitfall.
- Use `go-error-handling` when the issue is error semantics, wrapping, inspection, panic boundaries, or logging.
- Use `go-testing` to make the bug reproducible and prevent regressions.

## References

- For the full debugging process, read `references/methodology.md`.
- For symptom-to-tool triage, read `references/symptom-triage.md`.
- For compile failures, read `references/compilation.md`.
- For common Go bug patterns, read `references/common-go-bugs.md`.
- For race, deadlock, and goroutine issues, read `references/concurrency-debug.md`.
- For diagnostic commands and Delve/GODEBUG usage, read `references/diagnostic-tools.md`.
- For pprof and production symptoms, read `references/pprof.md`, `references/performance-debug.md`, and `references/production-debug.md`.
- For test-driven debugging, read `references/testing-debug.md`.
- For review-time bug flags, read `references/code-review-flags.md`.
