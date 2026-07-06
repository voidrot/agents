---
name: uv-package-manager
description: Use uv for Python projects, dependencies, lockfiles, virtualenvs, tools, and scripts.
---

# uv Package Manager

## When to use

- setting up or maintaining Python projects with uv
- managing dependencies, lockfiles, Python versions, virtual environments, tools, or scripts
- migrating from pip, pip-tools, poetry, or ad hoc virtualenv workflows to uv

## Workflow

1. Detect whether the repo is a uv project, workspace, script, or tool-only use case.
2. Use pyproject.toml and uv.lock as the source of dependency state when present.
3. Choose uv add/remove/sync/lock/run for project workflows instead of mixing package managers.
4. Keep CI commands frozen/locked when reproducibility matters.
5. Use non-interactive flags and avoid commands that prompt.

## Constraints

- Do not hand-edit uv.lock.
- Do not mix pip install into a uv-managed environment unless debugging and explicitly isolated.
- Move command matrices and migration recipes to references.

## References

- [uv command recipes and workflows](references/advanced-patterns.md)
- [moved uv guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
