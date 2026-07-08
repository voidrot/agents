# Voidrot Agents

Custom skills, commands, agents, hooks, and plugins for OpenCode.

## How to use this repo

Use this repository as a local source of reusable OpenCode assets.

### 1. Link local assets into OpenCode

For day-to-day local use, symlink the repo's skills and commands into the user-level OpenCode locations:

```sh
scripts/link-opencode-assets.sh --dry-run
scripts/link-opencode-assets.sh
```

The link script installs:

| Asset | Source | Destination |
| --- | --- | --- |
| Skills | `skills/*/*` | `~/.agents/skills/<skill-name>` |
| Commands | `commands/*.md` and `.opencode/commands/*.md` | `~/.config/opencode/commands/<command-name>.md` |

Use `--force` only when you intentionally want to replace an existing non-matching path:

```sh
scripts/link-opencode-assets.sh --force
```

Restart OpenCode after linking or replacing skills, commands, agents, hooks, or plugins so discovery reloads the new files.

### 2. Add or update assets

- Add skills under `skills/<category>/<skill-name>/SKILL.md`.
- Add commands under `commands/*.md` unless they are project-local OpenCode examples, which belong under `.opencode/commands/`.
- Run `scripts/link-opencode-assets.sh --dry-run` before replacing existing local links.

## Commands

Commands are Markdown prompt files for OpenCode slash commands.

Command locations:

| Directory | Purpose | Link destination |
| --- | --- | --- |
| `commands/` | Shared commands intended for normal use | `~/.config/opencode/commands/` |
| `.opencode/commands/` | Repo-local command examples or project-specific commands | `~/.config/opencode/commands/` |

Each command file should use YAML frontmatter for OpenCode command metadata, followed by the command prompt body.

Allowed frontmatter keys:

- `description`
- `agent`
- `model`
- `variant`
- `subtask`

Command bodies can reference repo skills with exact `@skill-name` entries. Skill names must match a skill directory that contains `SKILL.md` under `skills/` or `.agents/skills/`.

Current shared commands:

- `accessibility-audit.md`
- `code-explain.md`
- `create-conventional-commits.md`
- `deps-audit.md`
- `doc-generate.md`
- `extract-design-md.md`
- `full-review.md`
- `new-branch.md`
- `pr-enhance.md`
- `python-scaffold.md`
- `refactor-clean.md`
- `tech-debt.md`

Current repo-local command examples:

- `integrate-new-skills.md`

## Agents

Coming Soon

## Hooks

Coming Soon

## Plugins

Coming Soon

## Skills

Skills are stored under the `skills/` directory. Each skill lives in its own directory and must contain a `SKILL.md` file. Supporting files should be placed next to the skill in purpose-specific subdirectories.

Skills should be small, focused, and action-oriented. Each skill should teach an agent how to perform a specific class of work, not act as a general knowledge dump.

### Skill Structure

```text
skills/
└── <category>/
    └── <skill-name>/
        ├── SKILL.md
        ├── references/
        ├── scripts/
        └── assets/
```

Use lowercase kebab-case for category and skill directory names. Skill directory names must also:

- Be 1-64 characters long
- Contain only lowercase letters, numbers, and hyphens
- Not start or end with a hyphen
- Not contain consecutive hyphens
- Match the `name` field in the skill's `SKILL.md` frontmatter

Current top-level categories are ecosystem or domain roots:

- `typescript/`
- `golang/`
- `python/`
- `infrastructure/`
- `database/`
- `security/`
- `platforms/`
- `version-control/`
- `meta/`
- `design/`

Examples:

```text
skills/
└── golang/
    └── golang-code-review/
        ├── SKILL.md
        ├── references/
        └── scripts/
```

### `SKILL.md`

Every skill must include a `SKILL.md` file. This file is the entry point for both humans and agents.

Keep `SKILL.md` concise. It should describe when the skill should be used, what the skill does, how the agent should approach the task, and where to find supporting material if needed.

A `SKILL.md` file should usually include:

- Required frontmatter metadata, including `name` and `description`
- Optional frontmatter metadata when useful: `license`, `compatibility`, `metadata`, and experimental `allowed-tools`
- A clear description of when to use the skill
- A brief workflow or procedure
- Important constraints, assumptions, or safety rules
- Expected output format, when applicable
- References to supporting files that should be opened only when needed

The `description` should be written as an activation signal for agents. It should explain the situations where the skill is useful, not just summarize the topic.

Example:

```markdown
---
name: golang-code-review
description: Use this skill when reviewing, debugging, or refactoring Go code, especially when checking idiomatic error handling, interfaces, concurrency, tests, package layout, or module structure.
license: MIT
compatibility: Go projects using standard Go tooling.
metadata:
  owner: voidrot
allowed-tools: grep read bash
---

# Go Code Review

Use this skill to review Go code for correctness, maintainability, idiomatic style, and production readiness.

## Workflow

1. Identify the package purpose and execution path.
2. Check correctness, error handling, concurrency behavior, and test coverage.
3. Review API boundaries, naming, package layout, and dependency usage.
4. Provide findings in priority order with concrete fixes.

## Supporting Material

- For detailed review criteria, read `references/review-checklist.md`.
- For common refactor examples, read `references/refactor-patterns.md`.
- For helper commands, use scripts from `scripts/`.
```

Avoid putting large code blocks, long documentation excerpts, generated output, large datasets, or full templates directly in `SKILL.md`. Put those in supporting files and reference them from the workflow.

### `references/`

The `references/` directory contains supporting documentation used by the skill.

Use this directory for:

- Detailed procedures
- Long checklists
- External documentation summaries
- Domain-specific rules
- Sample snippets
- Decision tables
- Larger examples
- Data files that are useful but not always needed

Reference files should be named clearly and loaded only when relevant. `SKILL.md` should tell the agent when a reference file is useful.

Example:

```text
references/
├── review-checklist.md
├── module-layout.md
└── concurrency-patterns.md
```

### `scripts/`

The `scripts/` directory contains executable helpers used by the skill.

Use this directory for:

- Validation scripts
- Code generation helpers
- Formatters
- Linters
- Test helpers
- Small utilities that reduce repeated manual work

Scripts should be deterministic where possible, documented well enough to run safely, and named according to their purpose.

Example:

```text
scripts/
├── validate.sh
├── generate-template.py
└── collect-diagnostics.sh
```

If a script has dependencies, expected inputs, or safety concerns, document them in either the script header or a nearby README.

### `assets/`

The `assets/` directory contains static resources needed by the skill.

Use this directory for:

- Document, code, prompt, report, and configuration templates
- Images
- Diagrams
- Screenshots
- Data files, lookup tables, and schemas
- Audio or video files
- Static binary files
- Other media used by the skill

Keep templates out of `SKILL.md` unless they are very small and essential to understanding the skill. Do not use `assets/` for long documentation or executable scripts. Prefer `references/` for documentation and `scripts/` for executable helpers.

Example:

```text
assets/
├── terraform-module/
├── github-action.yml
├── review-report.md
└── architecture-diagram.png
```

### Skill Design Guidelines

A good skill should be:

- **Focused**: It should cover one coherent workflow or task family.
- **Discoverable**: Its name and description should make its purpose obvious.
- **Actionable**: It should tell the agent what to do, not just describe a topic.
- **Small by default**: It should avoid loading large supporting material unless needed.
- **Composable**: It should not duplicate broad instructions that belong in another skill.
- **Maintained**: Supporting files should be organized, named clearly, and removed when obsolete.

Before adding a new skill, check whether an existing skill can be extended without becoming too broad. Prefer multiple narrow skills over one large general-purpose skill.
