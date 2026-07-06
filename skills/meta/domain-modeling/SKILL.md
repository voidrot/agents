---
name: domain-modeling
description: Use when sharpening domain terminology, maintaining a glossary, resolving overloaded concepts, or recording consequential architecture decisions as ADRs.
---

# Domain Modeling

Actively build the project’s domain language while design decisions are being made. This skill is for changing or clarifying the model, not merely reading existing vocabulary.

## Workflow

1. Locate the relevant `CONTEXT.md` or `CONTEXT-MAP.md`; create files lazily only when a term or decision is ready to record.
2. Challenge vague or conflicting terms immediately and ask for the canonical meaning.
3. Stress-test relationships with concrete scenarios and edge cases.
4. Cross-check claims against code when implementation behavior may contradict the stated model.
5. Update `CONTEXT.md` inline as terms crystallize.
6. Offer an ADR only for decisions that are hard to reverse, surprising without context, and the result of a real trade-off.

## Constraints

- `CONTEXT.md` is a glossary, not a spec, scratch pad, or implementation decision log.
- Do not batch resolved glossary changes; capture them when they happen.
- Do not create ADRs for ephemeral preferences or obvious implementation details.

## Supporting Material

- Use `references/context-format.md` for glossary structure.
- Use `references/adr-format.md` for ADR structure.
- Review references and assets with candidate material merged from `architecture-decision-records` when the request overlaps that source's specialized workflow.
  - `references/architecture-decision-records-merge-notes.md`
