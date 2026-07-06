---
name: python-design-patterns
description: "Use for Python component design: layering, abstraction choices, dependency injection, composition vs inheritance, SRP, and coupling refactors."
---

# Python Design Patterns

Use this skill when code structure, boundaries, or abstractions are the problem. It complements `python-patterns`, which covers language idioms inside code.

## When to Use

- Designing a service, component, or module boundary
- Refactoring God classes, tangled functions, or mixed I/O/business logic
- Deciding whether duplication deserves an abstraction
- Choosing composition, inheritance, protocols, factories, strategies, or dependency injection
- Reviewing coupling, layer violations, or hard-to-test structure

## Boundary with `python-patterns`

Use `python-design-patterns` for architecture inside a Python codebase: responsibilities, dependencies, layering, seams, and abstraction cost.
Use `python-patterns` for Pythonic implementation details: typing, dataclasses, comprehensions, context managers, imports, exceptions, and local anti-patterns.

## Workflow

1. Name the current responsibility boundaries and reasons each unit changes.
2. Separate I/O, framework, data access, and business logic before adding patterns.
3. Prefer the simplest design that supports current requirements.
4. Use composition and constructor injection to make dependencies visible and testable.
5. Apply the rule of three before abstracting, unless duplicated logic is already causing bugs.
6. Add tests around each seam before or during structural refactors.

## Key Rules

- Complexity must buy clarity, testability, or extensibility.
- Do not add factories, registries, or base classes just to look patterned.
- Keep dependency direction explicit, for example API → service → repository.
- Avoid leaking persistence/framework types across layer boundaries.
- If dependency injection creates huge constructors, split responsibilities first.

## References

- [Detailed design patterns](references/details.md) — KISS, SRP, layering, composition, rule of three, DI, and anti-pattern examples.

## Related Skills

- [python-patterns](../python-patterns/SKILL.md) — Python language idioms and local implementation patterns.
- [python-testing-patterns](../python-testing-patterns/SKILL.md) — Test seams, layers, and injected dependencies.
- [python-project-structure](../python-project-structure/SKILL.md) — Package and project layout that supports clear boundaries.
