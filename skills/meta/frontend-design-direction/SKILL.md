---
name: frontend-design-direction
description: Use when a web UI needs visual direction, hierarchy, tone, layout, responsive behavior, motion, or polish beyond functional frontend implementation.
origin: community
---

# Frontend Design Direction

Use this skill when the task is about making UI feel purposeful, polished, and appropriate to the product domain, not merely making React code function.

## Scope Boundaries

- Use `frontend-design-direction` for product feel, visual hierarchy, typography, color, layout, motion, affordances, and responsive design intent.
- Use `frontend-patterns` for React/Next/component/state/form/performance implementation patterns.
- Use accessibility-focused skills for WCAG audits or detailed a11y remediation.
- Install the upstream Anthropic `frontend-design` skill separately when the official canonical design skill is required.

## Workflow

1. Name the purpose, audience, tone, memorable design idea, constraints, and existing design system.
2. Match the direction to the domain: dense and quiet for repeated tools; expressive only when the product benefits from it.
3. Preserve usable product workflow in the first screen unless marketing copy is explicitly requested.
4. Implement or review responsive constraints, typography fit, contrast, assets, and motion states.
5. Return concrete design direction and the highest-impact changes, not vague taste commentary.

## Constraints

- Avoid generic generated tropes: purple gradients, blobs, oversized cards, vague hero copy, stock-like filler imagery.
- Do not add dependencies for decorative flourishes without clear payoff.
- Do not hide primary workflows behind marketing sections when building an app/tool UI.

## Supporting Material

- Read `references/design-direction-heuristics.md` for detailed heuristics, anti-patterns, and review checklist.
