# Formal structure and bundled-validator limits

Read this before creating a skill directory, editing frontmatter, or treating a validation result as evidence.

## Required package shape

An Agent Skill is a directory containing `SKILL.md`. Its YAML frontmatter must include:

- `name`: 1–64 characters; lowercase Unicode letters, numbers, and hyphens only; no leading, trailing, or consecutive hyphens; exactly matches the parent directory name.
- `description`: a non-empty string of 1–1024 characters.

The recognized optional frontmatter fields are `license`, `compatibility` (at most 500 characters), string-to-string `metadata`, and experimental `allowed-tools`.

Use conventional directories only when they earn their cost:

```text
my-skill/
├── SKILL.md
├── scripts/       # repeated deterministic operations
├── references/    # detail read only when needed
└── assets/        # templates or other non-instruction artifacts
```

These directories are conventions, not a reason to add empty folders. Keep resource paths relative. Prefer a reference one directory below `SKILL.md`; deep chains make activation and review harder.

## Progressive disclosure budget

Consumers first see metadata for discovery, then load `SKILL.md` when the skill activates, then read or execute linked resources on demand. Keep `SKILL.md` focused on the workflow—recommended under 500 lines and 5,000 tokens—and move supporting detail to references or scripts.

## What the bundled validator checks

`../scripts/validate_skill.py` checks the required field limits and name shape, the stated `compatibility` limit, simple string-to-string metadata, and local Markdown destinations. It rejects a relative Markdown path that resolves outside the skill root and reports a missing local target.

It deliberately uses Python's standard library rather than a YAML dependency. It supports ordinary top-level scalar fields, single-line quoted scalars, and indented `|`/`>` block scalars. It rejects or reports unsupported YAML constructs (including flow mappings/sequences, anchors, aliases, tags, multiline quoted scalars, and complex metadata) instead of guessing. Its Unicode name check is conservative: it accepts alphanumeric Unicode code points whose cased letters are lowercase, but may reject otherwise valid combining-character spellings. It is **not** parity with `skills-ref` or any official YAML parser. Run `uv run skill-eval validate SKILL_DIR --strict` when available for the repository's stricter validation.

Markdown inspection covers ordinary inline and reference-definition links outside fenced code blocks. It ignores remote, anchor-only, and mail links. It is not a complete Markdown parser, so inspect unusual Markdown link syntax manually.

## Source basis

- [Agent Skills specification](https://agentskills.io/specification) (authoritative source supplied for this skill; checked 2026-09-01)
