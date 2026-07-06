---
name: skill-authoring
description: Use when writing, reviewing, or maintaining Agent Skills in this repo, including frontmatter, descriptions, directory layout, progressive disclosure, and support files.
license: MIT
compatibility: Agent Skills specification at agentskills.io/specification.
metadata:
  owner: voidrot
---

# Skill Authoring

Use this skill to create or review skills that comply with this repository’s README and the Agent Skills specification.

## Workflow

1. Confirm the skill covers one focused task family or workflow.
2. Put it under the closest ecosystem or domain category in `skills/`.
3. Ensure the directory name matches the `name` field in `SKILL.md`.
4. Write an activation-oriented `description` that says when to use the skill.
5. Keep `SKILL.md` concise: when to use, workflow, constraints, expected output, and links to support files.
6. Move detailed procedures, examples, checklists, and templates into purpose-specific support files.
7. Verify every local reference resolves from the skill directory.

## Key Rules

- `SKILL.md` must start with YAML frontmatter containing `name` and `description`.
- `name` must be 1-64 characters, lowercase kebab-case, with no leading/trailing/consecutive hyphens.
- `description` must be non-empty, under the spec limit, and useful as an activation signal.
- Use `references/` for on-demand documentation, `scripts/` for executable helpers, and `assets/` for templates/media/static resources.
- Do not create empty support directories just to satisfy a shape; reference support directories only when files exist.

## Supporting Material

- Read `references/spec-and-repo-rules.md` for the detailed checklist aligned with README and agentskills.io/specification.
