---
name: prompt-engineering-patterns
description: Use this skill when designing, debugging, or optimizing production prompts, prompt templates, few-shot examples, structured outputs, or advanced prompting workflows.
---

# Prompt Engineering Patterns

Use this skill for focused prompt engineering patterns work. Keep the active conversation centered on the user's concrete task and load detailed supporting material only when needed.

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
- Open `references/chain-of-thought.md` when its focused details are needed.
- Open `references/details.md` when its focused details are needed.
- Open `references/few-shot-learning.md` when its focused details are needed.
- Open `references/prompt-optimization.md` when its focused details are needed.
- Open `references/prompt-templates.md` when its focused details are needed.
- Open `references/system-prompts.md` when its focused details are needed.
- Use `scripts/optimize-prompt.py` when you need the preserved supporting material or template.
- Use `assets/few-shot-examples.json` when you need the preserved supporting material or template.
- Use `assets/prompt-template-library.md` when you need the preserved supporting material or template.
