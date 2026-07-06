---
name: python-project-structure
description: Organize Python packages, modules, public APIs, imports, and project layout.
---

# Python Project Structure

## When to use

- starting or reorganizing a Python project or package layout
- deciding between src layout, package modules, namespace packages, or app folders
- reviewing import boundaries, public APIs, __all__, or module ownership

## Workflow

1. Identify distribution boundaries, runtime entry points, and test/import needs.
2. Choose a layout that makes imports predictable and packaging explicit.
3. Keep public APIs small and documented; hide implementation modules by convention.
4. Separate application composition from domain logic and infrastructure adapters.
5. Update tests, packaging metadata, and imports together when moving modules.

## Constraints

- Prefer simple package boundaries over framework-shaped directories when no framework requires them.
- Avoid utils dumping grounds; name modules by responsibility.
- Move layout variants and import examples to references.

## References

- [moved layout variants and examples](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
