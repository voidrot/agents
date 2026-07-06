---
name: design-system-patterns
description: Use when creating or evolving design systems: design tokens, theme architecture, component APIs, documentation, governance, multi-brand support, and design-to-code workflows.
---

# Design System Patterns

Use this skill for focused design work in this task family. Keep the active guidance concise, and open supporting references only when their detail is needed.

## When to use

- Defining token hierarchies, theme architecture, or multi-brand UI foundations.
- Building component libraries with consistent APIs, variants, accessibility, and documentation.
- Reviewing design-system scalability, governance, contribution flow, or design-to-code handoff.

## Workflow

1. Identify consumers, platforms, brand requirements, existing components, and ownership model.
2. Separate primitive, semantic, and component-level tokens and document their intended use.
3. Define component API, theming, accessibility, versioning, and documentation patterns.
4. Check adoption risks: breaking changes, duplicated patterns, token drift, and governance gaps.
5. Return a phased implementation or refactor plan with validation criteria.

## Constraints

- Do not create token or component abstractions without clear reuse and ownership.
- Keep accessibility and interaction states part of component contracts, not optional polish.
- Prefer incremental migration paths over disruptive design-system rewrites.

## References

Read only the sections needed for the task:

- [references/design-tokens.md](references/design-tokens.md) — Token taxonomy, naming, semantics, and scaling guidance.
- [references/theming-architecture.md](references/theming-architecture.md) — Theme switching, multi-brand architecture, and runtime patterns.
- [references/component-architecture.md](references/component-architecture.md) — Component API, composition, and library architecture patterns.
- [references/details.md](references/details.md) — Additional design-system details and examples.
- [references/full-guidance.md](references/full-guidance.md) — Source guidance preserved from the original skill.

## Output

Return design-system recommendations, token/component changes, governance notes, migration steps, and validation criteria.
