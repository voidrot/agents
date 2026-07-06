---
name: ruff-recursive-fix
description: Use when running Ruff iteratively on Python code, applying safe fixes, reviewing unsafe fixes, formatting, and resolving remaining lint findings with minimal manual edits.
---

# Ruff Recursive Fix

Use this skill to clean Python code with Ruff in controlled passes while preserving behavior.

## Workflow

1. Determine the target path, Ruff runner (`uv run ruff`, `ruff`, or `python -m ruff`), and any rule selections or ignores.
2. Run a baseline `ruff check` for the selected scope and classify findings as safe-fixable, unsafe-fixable, or manual.
3. Apply safe fixes with `ruff check --fix`, then run `ruff format` and review the diff.
4. Apply unsafe fixes only when permitted; review behavior-sensitive changes before continuing.
5. Fix remaining findings manually or ask the user when multiple valid choices or suppressions exist.
6. Repeat check/format cycles until Ruff is clean, blocked by a decision, or no progress is possible.

## Constraints

- Prefer project Ruff configuration from `pyproject.toml`, `ruff.toml`, or equivalent when present.
- Use narrow `# noqa: <RULE>` suppressions only with a clear rationale.
- Do not silently accept unsafe fixes that may alter behavior.
- Keep edits scoped to the requested target unless the lint finding requires a small adjacent change.

## References

- Read `references/full-guidance.md` for command construction, loop details, suppression policy, and output contract.

## Expected output

- Scope and Ruff options used.
- Number of iterations and categories of fixes applied.
- Manual fixes, suppressions with rationale, remaining findings, and checks run.
