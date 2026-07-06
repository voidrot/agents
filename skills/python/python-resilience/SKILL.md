---
name: python-resilience
description: Add Python timeouts, retries, backoff, idempotency, and graceful degradation.
---

# Python Resilience

## When to use

- handling transient network, database, queue, or service failures
- adding retry and timeout policy with tenacity or client-native APIs
- reviewing fault tolerance, idempotency, circuit breaking, or fallback behavior

## Workflow

1. Classify the failure as transient, permanent, overload, or caller error.
2. Set explicit timeouts before adding retries.
3. Retry only idempotent or safely repeatable operations.
4. Use bounded exponential backoff with jitter and observability.
5. Test exhausted retries, cancellation, and fallback behavior.

## Constraints

- Never add infinite retries or unbounded waits.
- Do not retry validation/authentication errors unless the API explicitly says they are transient.
- Keep tenacity and HTTP client recipes in references.

## References

- [resilience examples](references/details.md)
- [moved retry and timeout guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
