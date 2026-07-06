---
name: frontend-patterns
description: Use when implementing React or Next.js UI behavior, component composition, state, data fetching, forms, routing, performance, accessibility, or client-side error boundaries.
origin: ECC
---

# Frontend Development Patterns

Use this skill for frontend implementation structure and behavior in React/Next.js applications.

## Scope Boundaries

- Use `frontend-patterns` for components, hooks, state, forms, data fetching, routing, rendering, performance, and client-side error boundaries.
- Use `frontend-design-direction` for visual hierarchy, design tone, typography, color, layout polish, animation feel, and product-specific design judgment.
- Use `api-design` for server contract decisions; this skill consumes those contracts from the client side.
- Use `backend-patterns` for server-side implementation behind API routes or services.

## Workflow

1. Inspect existing component, routing, styling, state, and data-fetching conventions before adding new patterns.
2. Choose the simplest state model that matches ownership and lifecycle: local state, reducer, context, external store, URL state, or server cache.
3. Compose components around explicit props and accessible semantics; avoid hidden global coupling.
4. Treat loading, empty, error, permission, and optimistic states as part of the implementation.
5. Optimize only measured or obvious bottlenecks; verify bundle, render, or interaction impact when performance is the goal.

## Constraints

- Do not introduce a state library, animation library, or form framework for one isolated need without checking existing conventions.
- Do not use memoization as a blanket fix; use it for expensive computation or stable child props.
- Keep accessibility and responsive behavior wired into components rather than deferred as a separate polish pass.

## Supporting Material

- Read `references/react-frontend-patterns.md` for component, hook, state, performance, form, error boundary, animation, and accessibility examples.
- Review references and assets with candidate material merged from `frontend-patterns` when the request overlaps that source's specialized workflow.
  - `references/frontend-patterns-merge-notes.md`
