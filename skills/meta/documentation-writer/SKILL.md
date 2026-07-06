---
name: documentation-writer
description: Use this skill when writing, restructuring, or reviewing technical documentation with Diátaxis-style separation of tutorials, how-to guides, reference, and explanation.
---

# Documentation Writer

Use this skill for focused documentation writer work. Keep the active conversation centered on the user's concrete task and load detailed supporting material only when needed.

## Workflow

1. Clarify the request, target audience, expected artifact, and any repository or project conventions.
2. Inspect existing project context before proposing new structure or content.
3. Apply the focused workflow from this skill; use supporting references for detailed checklists, examples, and templates.
4. Produce the requested artifact or implementation guidance with explicit assumptions, open questions, and verification steps.

## Constraints

- Prefer existing project conventions over generic templates.
- Keep generated output concise, actionable, and easy for another agent or human to continue.
- Do not invent file paths, commands, APIs, or external requirements; verify them in the target project or documentation.
- Preserve user-provided terminology unless it conflicts with established project language.

## Supporting Material

- Read `references/full-guidance.md` for the preserved source guidance, examples, and detailed checklists.
- Review references and assets with candidate material merged from `convert-plaintext-to-md` when the request overlaps that source's specialized workflow.
  - `references/convert-plaintext-to-md-merge-notes.md`
- Review references and assets with candidate material merged from `create-readme` when the request overlaps that source's specialized workflow.
  - `references/create-readme-merge-notes.md`
