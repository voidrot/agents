---
name: improve-codebase-architecture
description: Use when scanning a codebase for shallow modules, poor seams, testability friction, or deepening opportunities and presenting candidates for user selection.
disable-model-invocation: true
---

# Improve Codebase Architecture

Surface architectural friction and propose deepening opportunities: refactors that turn shallow modules into deeper, more local, more testable modules.

## Workflow

1. Load domain language from `CONTEXT.md`/`CONTEXT-MAP.md` and relevant ADRs before judging seams.
2. Use the `codebase-design` vocabulary exactly: module, interface, implementation, depth, seam, adapter, leverage, and locality.
3. Explore organically for friction: bouncing across modules, pass-through layers, hidden coupling, test seams that miss real behavior, and shallow wrappers.
4. Produce a self-contained HTML report in the OS temp directory, not the repo, with visual before/after candidates and a top recommendation.
5. Ask which candidate to explore; do not propose final interfaces until the user chooses one.
6. For the chosen candidate, use `grilling`, `domain-modeling`, and `codebase-design` follow-ups as decisions crystallize.

## Constraints

- Do not relitigate ADRs unless real friction justifies reopening one.
- Do not list theoretical refactors without files, problem, solution, benefits, test impact, and recommendation strength.
- Do not write report artifacts into the repository unless the user explicitly asks.

## Supporting Material

- Read `references/architecture-review-workflow.md` for detailed process and candidate criteria.
- Use `assets/html-report-template.md` for the report scaffold, diagram guidance, and visual sections.
