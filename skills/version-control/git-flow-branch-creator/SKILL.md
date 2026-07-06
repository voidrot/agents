---
name: git-flow-branch-creator
description: Use when creating Git Flow style branches from current work, choosing feature/fix/hotfix/release/support branch types, or naming branches from repository changes.
---

# Git Flow Branch Creator

Use this skill for git flow branch creator work in Git or GitHub repositories.

## When to activate

- User asks to create a Git Flow branch or choose a branch name.
- Need to classify changes into feature, bugfix, hotfix, release, or support branch types.

## Workflow

1. Inspect current branch, status, and diff.
2. Classify the work and choose the appropriate Git Flow branch prefix.
3. Generate a short lowercase kebab-case branch slug.
4. Create or report the branch command, preserving uncommitted work.

## Safety rules

- Do not switch branches if it would overwrite or strand uncommitted work.
- Confirm release/hotfix base branch expectations when they are not obvious.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
