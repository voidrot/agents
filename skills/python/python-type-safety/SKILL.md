---
name: python-type-safety
description: Add Python annotations, generics, protocols, narrowing, and type-checker configuration.
---

# Python Type Safety

## When to use

- typing new or existing Python APIs
- designing generic classes, protocols, typed dicts, or callable signatures
- configuring or resolving mypy, pyright, or pydantic typing issues

## Workflow

1. Type public boundaries first: inputs, outputs, exceptions, and protocols.
2. Use concrete runtime behavior to choose between classes, Protocols, TypedDicts, and dataclasses/models.
3. Tighten optional and union handling with explicit narrowing.
4. Introduce strict checker settings incrementally by package or error class.
5. Keep runtime validation separate from static typing guarantees.

## Constraints

- Do not add Any to silence errors without documenting why.
- Prefer modern built-in generics and typing syntax supported by the project Python version.
- Move generics/protocol examples and checker matrices to references.

## References

- [typing examples](references/details.md)
- [moved type-safety guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
