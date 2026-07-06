# Documentation Artifacts

## ADR

Use for decisions that change architecture, interfaces, data flow, ownership, or long-term constraints.

Format:

```md
# ADR: <decision>

## Status
Proposed | Accepted | Superseded

## Context
What forced the decision.

## Decision
The chosen path.

## Consequences
Benefits, costs, risks, and follow-ups.

## Alternatives Considered
Rejected options and why.
```

## Glossary Entry

Use when terms are ambiguous, overloaded, or central to the domain model.

Format:

```md
## <Term>

Definition: <one precise meaning>

Use when: <where this term applies>

Avoid: <nearby terms or meanings that are different>
```

## Decision Log Entry

Use for smaller choices that matter but do not need a full ADR.

Format:

```md
- Decision: <choice>
  Why: <reason>
  Revisit when: <trigger, if any>
```

## Boundaries

- Do not create docs for every answer; capture decisions that future agents or contributors will need.
- Prefer linking to existing plans, issues, or ADRs over duplicating them.
- Keep unresolved questions visible instead of pretending they are decisions.
