---
name: python-anti-patterns
description: Review Python code for common anti-patterns and safer refactoring paths.
---

# Python Anti-Patterns

## When to use

- reviewing Python code for brittle, slow, or hard-to-maintain patterns
- debugging issues that may come from mutable defaults, broad exceptions, hidden side effects, or unsafe imports
- preparing a refactor plan and needing a concise checklist before edits

## Workflow

1. Classify the smell first: correctness, maintainability, performance, security, or API design.
2. Confirm the behavior with tests or a minimal reproduction before refactoring.
3. Replace one anti-pattern at a time with the smallest idiomatic alternative.
4. Preserve public APIs unless the user explicitly accepts a breaking change.
5. Verify with the project test suite and the relevant linters/type checkers.

## Constraints

- Prefer Python language/library guidance over style folklore.
- Do not apply blanket rewrites when a local exception is intentional and documented.
- Route large examples and smell catalogs to the references instead of expanding this file.

## References

- [moved anti-pattern checklist and examples](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
