# Configure mode — force-trigger Go skills in a project

This workflow adds a `## Required Go skills` block to the project's agent config file so that specific skills always load, regardless of trigger heuristics.

## When to use

- The project has a hard requirement on a local skill (for example, `go-safety` or `go-error-handling` must always apply, not just when the user mentions the topic).
- The team has agreed on a fixed set of Go standards to enforce on every AI interaction.
- A company skill overrides a community default (⚙️ skills) and must always win.

## Step 1 — Detect the project config file

Check in this precedence order:

```
1. CLAUDE.md          (Claude Code)
2. AGENTS.md          (OpenAI Codex, OpenCode, multi-agent)
3. .cursor/rules      (Cursor)
4. .github/copilot-instructions.md  (GitHub Copilot)
```

Use `Glob` to detect which files exist at the project root. If multiple exist, use all of them (different tools read different files). If none exist, ask the user which one to create with `AskUserQuestion`.

## Step 2 — Idempotency check

Before writing, grep each file for an existing `## Required Go skills` block:

```bash
grep -n "## Required Go skills" CLAUDE.md
```

If the block already exists, read it and confirm with the user whether to update it in place (replace the existing list) or skip.

## Step 3 — Confirm the skill set with the user

Use `AskUserQuestion` to confirm which skills to always load. Present the ⭐️ recommended skills as the default selection. Remind the user of the token budget (each always-loaded skill adds its description tokens to every session — the 11 recommended skills add ~1,100 tokens at startup).

Recommended ⭐️ set for most projects:

```
go-code-style
go-data-structures
go-error-handling
go-naming
go-safety
go-testing
go-troubleshooting
```

Additional skills to suggest based on codebase context:

- Database, CI, Cobra, Viper, samber/lo, or other library-specific imports detected → note that these topics need manual/external guidance unless the repo later adds matching local skills.

## Step 4 — Write the block

### Template

```markdown
## Required Go skills

The following local Go skills MUST always be applied when working on this project. Load them at the start of every Go-related task, regardless of whether the user explicitly mentions them.

- `go-error-handling`
- `go-safety`
- `go-testing`
```

Replace the skill list with the confirmed set from Step 3. Use the local skill name, such as `go-error-handling`, for each skill.

### Insertion point

- If the file is empty: write the block at the top.
- If the file has existing content: append after the last section, separated by a blank line.
- If a `## Required Go skills` block already exists: replace only the bullet list inside it, preserving surrounding content.

### Edit the file

Use the `Edit` tool (preferred over a bash script) to apply the change. For append operations:

```python
# Conceptually: read the file, find the insertion point, apply Edit
```

Perform an idempotency check after writing: re-read the file and verify the block appears exactly once.

## Step 5 — Confirm to the user

After writing, summarize:

- Which file(s) were updated
- Which skills were added to the always-load list
- Approximate startup token cost (number of skills × ~100 tokens per description)
- Note: skills marked ⚙️ (overridable) will be superseded if a company skill explicitly declares the override in its body

## Notes on company overrides (⚙️ skills)

Skills marked ⚙️ in the README support company overrides. If the project has a company skill that supersedes a community default, use the company skill FQN in the block instead — do NOT list both.

To declare an override in a company skill body, add near the top:

```
> This skill supersedes `go-error-handling` for [Company] projects.
```

Current local Go skills: `go-how-to`, `go-code-style`, `go-error-handling`, `go-naming`, `go-project-layout`, `go-safety`, `go-testing`, and `go-troubleshooting`.
