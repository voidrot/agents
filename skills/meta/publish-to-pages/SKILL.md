---
name: publish-to-pages
description: Use this skill when publishing presentations or static web content to GitHub Pages, including converting PPTX/PDF inputs and returning a live Pages URL.
---

# Publish To Pages

Use this skill for focused publish to pages work. Keep the active conversation centered on the user's concrete task and load detailed supporting material only when needed.

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
- Use `scripts/convert-pdf.py` when you need the preserved supporting material or template.
- Use `scripts/convert-pptx.py` when you need the preserved supporting material or template.
- Use `scripts/publish.sh` when you need the preserved supporting material or template.
