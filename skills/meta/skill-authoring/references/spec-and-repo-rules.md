# Agent Skills Spec And Repo Rules

Use this checklist when creating or reviewing a skill in this repository.

## Required Entry Point

- Every skill directory must contain `SKILL.md`.
- `SKILL.md` must begin with YAML frontmatter followed by a Markdown body.
- Required frontmatter fields are `name` and `description`.
- Optional fields may include `license`, `compatibility`, `metadata`, and the
  allowed tools field when useful.

## Name Rules

- 1-64 characters.
- Lowercase letters, numbers, and hyphens only.
- No leading or trailing hyphen.
- No consecutive hyphens.
- Must match the parent directory name.

## Description Rules

- Non-empty and within the Agent Skills specification limit.
- Written as an activation signal: what the skill does and when to use it.
- Include concrete trigger keywords only when they help routing.
- Avoid long negative trigger catalogs in frontmatter; put nuance in the body or references.

## Progressive Disclosure

The load order should be:

1. Metadata at startup.
2. `SKILL.md` when activated.
3. Supporting reference material, helper scripts, or static assets only when
   needed.

Keep `SKILL.md` concise. Move long examples, detailed checklists, command matrices, copied docs, and templates out of `SKILL.md`.

## Support Directories

- The references support directory is for detailed procedures, long checklists,
  external documentation summaries, domain rules, examples, and decision tables.
- The scripts support directory is for deterministic executable helpers with
  documented inputs, dependencies, and safe failure modes.
- The assets support directory is for templates, images, diagrams, schemas,
  static examples, and other media.

Do not reference a support directory unless the referenced file exists.

## Repository README Alignment

- Skills live under a category directory and then a skill-name directory; for
  example, replace the category and skill-name placeholders with real lowercase
  kebab-case names.
- Category and skill directories use lowercase kebab-case.
- Skills should be small, focused, discoverable, actionable, and small by default.
- `SKILL.md` should explain when to use the skill, what to do, constraints, expected output, and when to open supporting material.
