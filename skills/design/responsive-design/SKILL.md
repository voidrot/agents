---
name: responsive-design
description: Use when implementing adaptive interfaces with mobile-first layout, container queries, fluid typography, responsive media, CSS Grid/Flexbox, or component-level breakpoint strategy.
---

# Responsive Design

Use this skill for focused design work in this task family. Keep the active guidance concise, and open supporting references only when their detail is needed.

## When to use

- Designing or fixing layouts across mobile, tablet, desktop, and embedded contexts.
- Choosing breakpoint, container-query, fluid type, responsive image, or adaptive navigation patterns.
- Reviewing responsive behavior for component libraries, dashboards, forms, tables, or content-heavy pages.

## Workflow

1. Identify target viewports, content constraints, input modes, and container boundaries.
2. Start from content and task priority, then choose mobile-first layout and progressive enhancement.
3. Use container queries for component-local behavior and breakpoints for page/system-level shifts.
4. Check typography, spacing, media, navigation, tables, forms, touch targets, zoom, and overflow states.
5. Provide implementation notes and validation cases for the most important viewport ranges.

## Constraints

- Do not rely on device-specific breakpoints when content- or container-driven thresholds are clearer.
- Avoid fixed heights/widths that break zoom, localization, dynamic type, or reflow.
- Preserve accessibility: touch targets, focus order, reduced motion, text scaling, and readable line lengths.

## References

Read only the sections needed for the task:

- [references/details.md](references/details.md) — Responsive design fundamentals and implementation details.
- [references/breakpoint-strategies.md](references/breakpoint-strategies.md) — Breakpoint selection and system strategy.
- [references/container-queries.md](references/container-queries.md) — Component-level responsiveness with container queries.
- [references/fluid-layouts.md](references/fluid-layouts.md) — Fluid typography, spacing, media, and layout techniques.
- [references/full-guidance.md](references/full-guidance.md) — Source guidance preserved from the original skill.

## Output

Return responsive layout recommendations, CSS/component changes where useful, and viewport/container validation cases.
