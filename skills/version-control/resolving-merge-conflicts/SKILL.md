---
name: resolving-merge-conflicts
description: Use when a git merge, rebase, cherry-pick, or stash apply is already conflicted and needs safe semantic conflict resolution plus verification.
---

# Resolving Merge Conflicts

Use this skill for active conflict states. For general branch strategy, commit policy, merge/rebase decisions, and team workflow design, use `git-workflow`.

## When to activate

- Git reports unresolved conflicts during merge, rebase, cherry-pick, revert, or stash apply.
- Files contain conflict markers such as `<<<<<<<`, `=======`, or `>>>>>>>`.
- A rebase/merge is paused and needs resolution, staging, validation, and continuation.

## Conflict workflow

1. **Protect context**: check `git status`, identify the operation in progress, and note the target/source branches or commits.
2. **Inventory conflicts**: list conflicted files and classify each as content, rename/delete, binary, generated, lockfile, or config conflict.
3. **Understand intent**: inspect both sides, nearby code, commit messages, tests, issues/PRs when available, and current architecture.
4. **Resolve semantically**: preserve both intents when compatible; when incompatible, choose the result that matches the merge goal and document the trade-off.
5. **Remove markers and stage**: ensure no conflict markers remain, format only what is necessary, and stage resolved files.
6. **Validate**: run the relevant typecheck/tests/format or the smallest credible subset first, then broader checks if risk warrants.
7. **Finish operation**: continue rebase/cherry-pick or commit the merge using non-interactive Git commands where possible.

## Safety rules

- Do not blindly choose `--ours` or `--theirs` without explaining why that side is correct.
- Do not invent new behavior unrelated to either side of the conflict.
- Do not abort unless the user explicitly asks or continuing would destroy work.
- Treat lockfiles, generated files, migrations, snapshots, and binary files as special cases that may need regeneration or tool-specific handling.
- Verify that all conflict markers are gone before finishing.

## References

- [Conflict resolution playbook](references/conflict-resolution-playbook.md) — conflict types, examples, commands, and verification checklist.
- External: [Git merge documentation](https://git-scm.com/docs/git-merge), [Git rebase documentation](https://git-scm.com/docs/git-rebase), [Git rerere](https://git-scm.com/docs/git-rerere).

## Output

Return conflicted files, resolution decisions, commands/checks run, unresolved risks, and the final Git operation state.
