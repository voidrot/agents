---
name: python-patterns
description: "Use for Python language idioms: typing, context managers, comprehensions, generators, dataclasses, decorators, errors, imports, and tooling."
origin: ECC
---

# Python Patterns

Use this skill for idiomatic Python code style and language-level patterns. It is not the structural design-pattern skill.

## When to Use

- Writing or reviewing everyday Python code
- Choosing Pythonic idioms for control flow, errors, resources, and data containers
- Applying type hints, protocols, dataclasses, generators, decorators, or context managers
- Cleaning up imports, package exports, tooling configuration, or common anti-patterns
- Refactoring code for readability without changing architecture

## Boundary with `python-design-patterns`

Use `python-patterns` for language mechanics and idioms inside functions, modules, and classes.
Use `python-design-patterns` for component boundaries, layering, abstraction decisions, dependency injection, composition vs inheritance, and coupling.

Examples:

- `python-patterns`: replace mutable defaults, add `Path`, use `dataclass`, simplify comprehensions, add precise exceptions.
- `python-design-patterns`: split a God class, introduce a service/repository boundary, decide whether a factory or strategy abstraction is justified.

## Workflow

1. Prefer readable, explicit code over clever compactness.
2. Add modern type hints where they clarify contracts.
3. Use context managers for resource lifetime.
4. Use comprehensions and generators only when they remain easy to read.
5. Choose dataclasses/named tuples for simple data carriers; use classes when behavior or invariants matter.
6. Keep imports explicit and tooling-driven (`ruff`, formatter, type checker, tests).

## Key Rules

- Use EAFP when it expresses normal Python control flow; avoid broad `except` blocks.
- Chain exceptions with `raise ... from ...` when translating errors.
- Avoid mutable default arguments and wildcard imports.
- Keep concurrency-specific choices in `async-python-patterns` or `python-background-jobs`.
- Keep architectural refactors in `python-design-patterns`.

## References

- [Detailed idiom reference](references/details.md) — examples for typing, errors, context managers, comprehensions, dataclasses, decorators, package organization, tooling, performance basics, and anti-patterns.
