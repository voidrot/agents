---
name: error-handling
description: Use when designing cross-language error models, retry policy, failure boundaries, API/user messages, or reviewing code for swallowed, leaky, or inconsistent errors.
origin: ECC
---

# Error Handling Patterns

Use this skill to design how failures move through a system: typed/domain errors, wrapping, logging, retryability, user-facing messages, API envelopes, and operational visibility.

## Scope Boundaries

- Use `error-handling` for system-level error taxonomy, failure boundaries, retry policy, and message separation.
- Use `api-design` for the client-visible HTTP error contract and status-code semantics.
- Use `backend-patterns` for where handlers, middleware, services, and repositories are wired.
- Use language-specific skills such as `go-error-handling` or `python-error-handling` for idioms, syntax, and library details.

## Workflow

1. Classify expected domain failures, validation failures, authorization failures, transient dependency failures, and programmer bugs.
2. Decide which layer creates, wraps, logs, translates, retries, or surfaces each class.
3. Keep developer diagnostics in logs/traces and user-facing messages safe, stable, and actionable.
4. Ensure retries are bounded, jittered, idempotency-safe, and limited to retriable failures.
5. Verify every catch/except branch handles, translates, logs, or rethrows; no silent swallowing.

## Constraints

- Never expose stack traces, SQL/provider errors, secrets, or internal topology to users.
- Do not retry client errors or non-idempotent writes unless an idempotency key or equivalent guard exists.
- Error codes become contracts once clients depend on them.

## Supporting Material

- Read `references/cross-language-error-patterns.md` for TypeScript, Python, Go, React boundary, retry, user-message, and checklist examples.
- Review references and assets with candidate material merged from `error-handling-patterns` when the request overlaps that source's specialized workflow.
  - `references/error-handling-patterns-merge-notes.md`
  - `references/details.md`
