---
name: git-commit
description: Use when creating commits, staging logical changes, generating Conventional Commit messages from diffs, or checking commit message type, scope, body, footer, and breaking-change notation.
---

# Git Commit

Use this skill for git commit work in Git or GitHub repositories.

## When to activate

- User asks to commit current changes or generate a commit message.
- Need to split staged/unstaged work into logical commits.
- Need to validate or write a Conventional Commit.

## Workflow

1. Inspect `git status` and staged/unstaged diffs.
2. Group files into one logical change; ask before mixing unrelated work.
3. Choose Conventional Commit type, optional scope, imperative description, and body/footer when useful.
4. Run `git commit -m` non-interactively, unless the user only asked for the message.

## Safety rules

- Never commit secrets or unrelated local changes.
- Do not use interactive staging in this environment; stage explicit paths.
- Do not skip hooks, amend, reset, or force-push unless explicitly requested.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
- [references/conventional-commit-prompt.md](references/conventional-commit-prompt.md) — supporting material; open only when needed.
