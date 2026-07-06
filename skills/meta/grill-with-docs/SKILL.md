---
name: grill-with-docs
description: Stress-test a plan through an interview while producing durable ADR, glossary, or decision-log artifacts.
---

# Grill With Docs

## When to Use

- The user wants a rigorous plan/design interview and durable documentation.
- Decisions will affect architecture, domain language, or future contributors.
- A normal `grill-me` session would lose important context unless captured as artifacts.

## Workflow

1. Run the same one-question-at-a-time interview style as `grill-me`.
2. Track decisions, terms, rejected options, and unresolved risks as they emerge.
3. Create or update only the documentation artifacts that the conversation justifies.
4. Keep asking until the decision tree is clear enough to hand off or implement.
5. End by listing changed docs and remaining open decisions.

## Output

- ADRs for significant architectural decisions.
- Glossary entries for domain terms that need consistent language.
- Decision log entries for smaller choices, trade-offs, and rejected options.
- A short next-step summary linking to the artifacts.

## Supporting Material

- [references/doc-artifacts.md](references/doc-artifacts.md) — concise artifact formats and boundaries.
