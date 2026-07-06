---
name: skill-authoring
description: Use when writing, reviewing, or maintaining Agent Skills in this repository, especially when checking structure, naming, frontmatter, progressive disclosure, or supporting files.
license: MIT
compatibility: Agent Skills specification at agentskills.io/specification.
metadata:
  owner: voidrot
---

# Skill Authoring

Use this skill to create or review Agent Skills for this repository.

## Workflow

1. Confirm the skill has one focused task family or workflow.
2. Put the skill under the closest ecosystem or domain category in `skills/`.
3. Ensure the skill directory name matches the `name` field in `SKILL.md`.
4. Keep `SKILL.md` concise and move detailed material into `references/`, executable helpers into `scripts/`, and static resources or templates into `assets/`.
5. Check that the description explains both what the skill does and when to use it.

## Naming

- Use lowercase letters, numbers, and hyphens only.
- Use task-oriented names like `nextjs-app-router` or `git-conflict-resolution`.
- Avoid bare technology names unless the skill is intentionally broad.
