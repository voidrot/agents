---
name: tailwind-design-system
description: Use when building or refactoring Tailwind CSS v4 design systems, including CSS-first tokens, themes, component variants, responsive patterns, and accessibility conventions.
---

# Tailwind Design System

Use this skill for focused design work in this task family. Keep the active guidance concise, and open supporting references only when their detail is needed.

## When to use

- Creating Tailwind v4 design tokens, theme variables, component APIs, or multi-theme foundations.
- Migrating Tailwind design-system patterns while preserving accessibility and responsive behavior.
- Standardizing utility usage, variants, documentation, and reusable UI patterns.

## Workflow

1. Confirm Tailwind version and project styling architecture before recommending v4-only patterns.
2. Map existing colors, typography, spacing, states, and responsive rules to design tokens.
3. Define component variants and composition rules that avoid duplicated utility sprawl.
4. Check accessibility, dark mode, content scanning, and build-tool constraints.
5. Provide implementation steps and verification commands appropriate to the project.

## Constraints

- Do not use deprecated Tailwind v3 assumptions for a v4 system without calling out the version boundary.
- Do not preserve references to missing local files or pseudo-paths such as Tailwind directives as file links.
- Prefer semantic CSS variables and component contracts over hard-coded utility clusters.

## References

Read only the sections needed for the task:

- [references/details.md](references/details.md) — Core Tailwind design-system workflow and setup details.
- [references/advanced-patterns.md](references/advanced-patterns.md) — Advanced variants, theming, composition, and scaling patterns.
- [references/full-guidance.md](references/full-guidance.md) — Source guidance and examples preserved from the original skill.

## Output

Return Tailwind-specific design-system changes, token/component guidance, migration caveats, and a short validation checklist.
