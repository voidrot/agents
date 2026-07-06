---
name: python-code-style
description: Apply Python formatting, linting, naming, import, and docstring conventions.
---

# Python Code Style

## When to use

- writing or reviewing Python code for style, readability, naming, imports, or comments
- configuring Black, Ruff, isort-compatible import rules, mypy, or pyright
- deciding how much style change is appropriate in a feature or cleanup patch

## Workflow

1. Detect the project’s existing formatter/linter/type-checker configuration first.
2. Make the smallest style change that improves readability or satisfies configured tools.
3. Keep behavioral refactors separate from pure formatting unless the user asks for both.
4. Use automated formatters for mechanical layout; reserve manual judgment for names, comments, and structure.
5. Run the project’s configured checks after edits.

## Constraints

- PEP 8 is guidance; project configuration wins when it is explicit.
- Avoid churn-only rewrites in unrelated files.
- Move command matrices, config examples, and detailed style tables to references.

## References

- [moved style and tool guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
