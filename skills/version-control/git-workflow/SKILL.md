---
name: git-workflow
description: Use when choosing or documenting Git branch strategy, commit and PR conventions, merge/rebase policy, release tags, hooks, or team collaboration workflow.
origin: ECC
---

# Git Workflow

Use this skill for normal Git collaboration and team policy. For an active merge/rebase/cherry-pick conflict with conflict markers or interrupted Git state, use `resolving-merge-conflicts`.

## When to activate

- Selecting GitHub Flow, trunk-based development, GitFlow, release branches, or hotfix flow.
- Defining branch names, commit message style, PR templates, review expectations, or release tags.
- Deciding merge vs rebase policy for a team.
- Cleaning up branches, syncing forks, stashing work, or setting safe Git defaults.
- Writing docs for repository contribution workflow.

## Boundary

- **Use this skill** for planned workflow design and everyday Git collaboration.
- **Use `resolving-merge-conflicts`** when a repository is already in a conflicted merge/rebase/cherry-pick state and files need semantic conflict resolution.

## Workflow

1. Identify team size, release cadence, deployment model, compliance needs, and repository hosting constraints.
2. Pick the simplest branch model that supports the release process.
3. Define commit, PR, review, and CI gates.
4. Clarify merge/rebase rules, especially whether public history may be rewritten.
5. Document branch cleanup, release tagging, changelog expectations, and exception handling.

## Safety rules

- Do not recommend rebasing protected branches or shared public history.
- Prefer `--force-with-lease` over `--force` when force-pushing a personal branch is explicitly allowed.
- Do not put secrets in commits, examples, hooks, or templates.
- Keep hooks and scripts non-interactive and deterministic for CI.

## References

- [Branching strategies](references/branching-strategies.md) — GitHub Flow, trunk-based development, GitFlow, and selection criteria.
- [Commit and PR templates](references/commit-pr-templates.md) — Conventional Commit examples and PR template.
- [Git operations cookbook](references/git-operations-cookbook.md) — merge/rebase, branch cleanup, stash, releases, hooks, quick commands.
- External: [Git documentation](https://git-scm.com/doc), [Conventional Commits](https://www.conventionalcommits.org/), [Semantic Versioning](https://semver.org/).

## Output

Return the recommended workflow, rules, example commands or templates only where needed, and risks/trade-offs for alternatives rejected.
