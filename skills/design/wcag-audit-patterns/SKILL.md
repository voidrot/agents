---
name: wcag-audit-patterns
description: Use when auditing existing web content for WCAG 2.2 conformance, combining automated checks, manual evidence, severity, remediation, and accessibility report output.
---

# WCAG Audit Patterns

Use this skill for structured accessibility audits. For designing or implementing accessible components before an audit, use `accessibility` instead.

## When to use

- Auditing a page, flow, component library, or product against WCAG 2.2.
- Triage and remediation planning for accessibility violations.
- Preparing evidence for ADA, Section 508, EN 301 549, VPAT, or internal conformance work.
- Combining axe/Lighthouse/pa11y results with manual keyboard, screen-reader, zoom, motion, and form checks.

## Boundary

- **Use this skill** for audit scope, evidence collection, severity, reports, and remediation queues.
- **Use `accessibility`** for implementation-time component patterns, semantic choices, and platform-specific accessibility APIs.

## Audit workflow

1. Define scope: URLs, components, user flows, viewport/device targets, WCAG level, assistive technology matrix, and exclusions.
2. Run automated checks, but treat them as partial coverage only.
3. Perform manual checks for keyboard access, focus order/visibility, names/roles/values, forms, content structure, reflow, zoom, contrast, reduced motion, and error recovery.
4. Record each finding with WCAG success criterion, user impact, reproduction steps, evidence, severity, and remediation.
5. Prioritize blockers that prevent task completion, then serious barriers, then moderate/minor issues.
6. Re-test fixed issues and note residual risk or manual follow-up.

## Evidence requirements

Every finding should include: location, affected users, WCAG criterion, observed behavior, expected behavior, reproduction steps, evidence artifact when available, and a concrete fix.

## References

- [Audit playbook](references/audit-playbook.md) — WCAG checklists, automated tests, and remediation examples.
- [WCAG guidelines](references/wcag-guidelines.md) — detailed WCAG compliance notes when criterion-level depth is needed.
- [ARIA patterns](references/aria-patterns.md) — ARIA audit details for names, roles, states, widgets, and interaction patterns.
- [Mobile accessibility](references/mobile-accessibility.md) — iOS VoiceOver and Android TalkBack audit considerations.
- [Additional compliance details](references/details.md) — source compliance guidance preserved for edge cases.
- External: [WCAG 2.2](https://www.w3.org/TR/WCAG22/), [WAI-ARIA APG](https://www.w3.org/WAI/ARIA/apg/), [WebAIM contrast resources](https://webaim.org/resources/contrastchecker/), [axe-core](https://github.com/dequelabs/axe-core).

## Output

Return an audit summary, findings table, prioritized remediation plan, and verification status. Do not claim full conformance from automated checks alone.
