---
name: accessibility
description: Use when designing or implementing accessible UI across web, iOS, or Android; routes WCAG, semantic HTML/ARIA, native accessibility labels, focus, contrast, and inclusive component behavior.
origin: ECC
---

# Accessibility

Use this skill to build accessibility into UI and component implementation. For an audit of existing web content against WCAG evidence and report requirements, use `wcag-audit-patterns` instead.

## When to use

- Designing or implementing accessible web, iOS, Android, or cross-platform components.
- Choosing native semantics, ARIA roles, accessible names, labels, hints, traits, or state announcements.
- Fixing focus management, keyboard operation, contrast, target size, reduced motion, reflow, or form-error behavior during implementation.
- Translating product/design requirements into WCAG 2.2 AA implementation constraints.

## Boundary

- **Use this skill** for implementation guidance and component patterns before or during build.
- **Use `wcag-audit-patterns`** for structured audits, evidence capture, violation severity, remediation reports, VPAT/Section 508/ADA support, and manual + automated testing plans.

## Workflow

1. Identify the user task, platform, and assistive-technology path.
2. Prefer native semantic controls before custom roles or accessibility overrides.
3. Validate POUR coverage: perceivable content, operable controls, understandable interactions, robust name/role/value.
4. Check focus order, keyboard/switch operation, visible focus, target size, text alternatives, error messaging, live updates, and reduced-motion behavior.
5. Provide implementation-ready recommendations with exact attributes, component changes, and verification steps.

## Key constraints

- Do not use ARIA to replace native HTML or platform controls when a native semantic element works.
- Do not remove visible focus indicators; style them to meet contrast and visibility expectations.
- Do not convey state, errors, or required actions by color alone.
- Treat WCAG 2.2 AA as the default baseline unless the project states a stricter target.

## References

Read only the sections needed for the task:

- [Implementation checklist](references/implementation-checklist.md) — POUR checks, anti-patterns, and verification prompts.
- [Platform mapping](references/platform-mapping.md) — web/iOS/Android accessibility attribute mapping and architecture diagram.
- [Component examples](references/component-examples.md) — concise web, iOS, and Android examples.
- External: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/), [Apple accessibility](https://developer.apple.com/accessibility/), [Android accessibility](https://developer.android.com/guide/topics/ui/accessibility).

## Output

Return component-specific changes, code snippets only where helpful, and a short verification checklist.
