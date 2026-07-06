---
name: python-configuration
description: Design typed, environment-driven Python configuration and settings loading.
---

# Python Configuration

## When to use

- externalizing runtime configuration from code into environment variables or config files
- using pydantic-settings or similar typed settings models
- reviewing secret handling, configuration precedence, or environment-specific behavior

## Workflow

1. Inventory all configuration inputs and their precedence.
2. Keep secrets out of source control and logs.
3. Represent settings with explicit types, defaults, and validation boundaries.
4. Initialize settings at the application edge; pass typed settings inward.
5. Test representative environments and failure cases.

## Constraints

- Do not read environment variables deep inside business logic when dependency injection is practical.
- Document precedence where multiple sources are supported.
- Keep expanded pydantic-settings examples in references.

## References

- [worked pydantic-settings examples](references/details.md)
- [moved configuration guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
