---
name: python-observability
description: Add Python structured logging, metrics, tracing, and production diagnostics.
---

# Python Observability

## When to use

- instrumenting Python services with logs, metrics, traces, or correlation IDs
- reviewing observability for APIs, workers, background jobs, or libraries
- debugging production behavior where signals are missing or too noisy

## Workflow

1. Start from the operational question: what must an operator diagnose?
2. Add structured logs at boundaries and important state transitions.
3. Expose low-cardinality metrics for rates, errors, latency, saturation, and queues.
4. Propagate trace/correlation context across async tasks and service boundaries.
5. Verify signals locally without leaking secrets or high-cardinality user data.

## Constraints

- Prefer standard logging plus project-approved processors/exporters.
- Do not log credentials, tokens, PII, or unbounded payloads.
- Keep metrics/tracing setup examples in references.

## References

- [observability examples](references/details.md)
- [moved instrumentation guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
