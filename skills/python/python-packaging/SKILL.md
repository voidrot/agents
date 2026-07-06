---
name: python-packaging
description: Package Python projects with pyproject.toml, build metadata, wheels, and releases.
---

# Python Packaging

## When to use

- creating or modernizing Python packages, libraries, or CLI distributions
- choosing pyproject.toml metadata, build backends, entry points, or package data
- checking install/build/publish workflows before release

## Workflow

1. Identify whether the project is an app, library, plugin, or CLI.
2. Use pyproject.toml as the source of build-system and project metadata.
3. Keep runtime, optional, development, and build dependencies separate.
4. Build wheels/sdists in a clean environment and test installation before publishing.
5. Publish with non-interactive, token-based tooling only when the user asks for release execution.

## Constraints

- Follow PyPA packaging specs over backend-specific folklore.
- Do not add setup.py unless the selected backend or compatibility need requires it.
- Keep metadata examples, release checklists, and backend matrices in references.

## References

- [packaging examples](references/details.md)
- [advanced packaging patterns](references/advanced-patterns.md)
- [moved workflow guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
