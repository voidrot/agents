---
name: git-advanced-workflows
description: Use for advanced Git operations such as rebase, cherry-pick, bisect, reflog recovery, worktrees, history cleanup, branch synchronization, or complex repository troubleshooting.
---

# Git Advanced Workflows

Use this skill for git advanced workflows work in Git or GitHub repositories.

## When to activate

- Cleaning or reorganizing local history before review.
- Finding regressions with bisect or recovering work with reflog.
- Applying commits across branches or using worktrees for parallel work.

## Workflow

1. Inspect current Git state before proposing history-changing commands.
2. Identify whether the operation touches private or shared history.
3. Choose the least destructive command sequence and explain rollback points.
4. Validate status, branch, and expected commits after the operation.

## Safety rules

- Do not rewrite shared/protected branch history without explicit approval.
- Prefer `--force-with-lease` over force pushes when force-push is explicitly allowed.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
- [references/details.md](references/details.md) — supporting material; open only when needed.
