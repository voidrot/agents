---
name: python-error-handling
description: Design Python validation, exception, retry boundary, and partial-failure behavior.
---

# Python Error Handling

## When to use

- creating or reviewing exception hierarchies and error boundaries
- deciding when to raise, wrap, log, retry, or return validation results
- handling batch/partial failures or framework API errors

## Workflow

1. Define the caller contract before choosing exception types.
2. Keep domain errors distinct from transport/framework errors.
3. Catch exceptions only where recovery, translation, cleanup, or context enrichment happens.
4. Log once at the boundary that has enough context; preserve tracebacks with exception chaining.
5. Test success, expected failure, and unexpected failure paths.

## Constraints

- Avoid bare except and broad suppression.
- Use ExceptionGroup only when callers can act on grouped failures.
- Keep hierarchy examples and validation recipes in references.

## References

- [detailed error patterns](references/details.md)
- [moved examples and checklists](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
