---
name: git-worktree
description: "Create, use, inspect, and clean up Git worktrees safely. Use when asked to add a parallel checkout, manage a linked worktree, recover worktree metadata, or remove stale worktrees while preserving branches and local work."
---

# Git Worktree

Use Git worktrees for parallel checkouts of one repository. Keep each worktree's branch and files isolated while treating the underlying repository, refs, and most configuration as shared state.

## Safety defaults

- Inspect before changing anything. Do not change the main worktree's branch, alter its files, or assume it is clean.
- Never use `--force`, `-B`, dirty-worktree removal, branch deletion, bulk cleanup, or recursive deletion without the user's explicit approval and a clear explanation of what will be lost or overridden.
- Do not create a second checkout of a branch that is already checked out. Choose a different branch or ask the user; do not override Git's protection with `--force`.
- Do not copy `.env`, credentials, private keys, or other ignored files into a worktree without explicit authorization. Never print their contents.
- A worktree removal does not delete its branch. Preserve branches by default; delete one only when explicitly requested and after checking its state.

## Discover the repository and existing worktrees

1. Confirm the current directory belongs to a Git repository. Check `git rev-parse --is-bare-repository`; for a non-bare checkout, resolve its top-level directory and common Git directory with `git rev-parse --show-toplevel` and `git rev-parse --git-common-dir`. For a bare repository, use its common Git directory and `git worktree list` without requiring a working-tree top level.
2. Identify whether the directory is a linked worktree or a submodule before operating on it. Treat submodules as separate repositories; do not manage them as worktrees of the superproject.
3. Inspect all worktrees before choosing a path or branch. Use `git worktree list --porcelain -z` for scripts and `git worktree list` for a human-readable summary. Record the main worktree, each path, branch or detached commit, and locked/prunable state.
4. Inspect relevant repository instructions and status. A dirty worktree is not a reason to discard, stash, reset, or clean it automatically.

## Create a worktree

1. Honor an explicit user path when it is safe and unused. Otherwise, prefer an existing project convention such as an ignored `.worktrees/` or `worktrees/` directory. If none exists, use a clearly named sibling directory rather than silently adding an unignored directory inside the repository.
2. Verify the target path does not exist or is empty as Git requires, is not another worktree, and will not collide with a current checkout. Ensure any in-repository worktree directory is ignored before creating it; add an ignore rule only with user approval.
3. Use a descriptive, valid branch name. State the branch and explicit start point before creation.
   - For a new branch, use `git worktree add -b <branch> <path> <start-point>`.
   - For an existing local branch not checked out elsewhere, use `git worktree add <path> <branch>`.
   - For a detached, disposable inspection tree, use `git worktree add --detach <path> <commit>` and clearly say it cannot receive ordinary branch commits without first creating a branch.
   - For a remote branch, identify the intended remote unambiguously; create an explicit local tracking branch with `git worktree add --track -b <local-branch> <path> <remote>/<branch>`. Do not guess among similarly named remote branches.
4. Verify the new worktree with `git worktree list`, then report its absolute path, branch or commit, and start point.

## Use worktrees safely

- Run Git commands from the intended worktree and confirm its branch before editing or committing. Do not confuse changes in one checkout with another.
- Each worktree has its own working files and index, but refs and much repository configuration are shared. Do not change shared config merely to customize one worktree.
- When per-worktree configuration is genuinely needed, explain the shared-config impact first. Use Git's worktree-specific configuration support (`extensions.worktreeConfig` and `git config --worktree`) deliberately, not as a default.
- Dependencies, build outputs, ports, editor state, and ignored local configuration may need per-worktree setup. Follow repository setup instructions; ask before installing dependencies, copying ignored configuration, or starting services.
- Git's support for checking out multiple worktrees with submodules is incomplete. Inspect submodule status and use the repository's documented procedure rather than assuming recursive initialization is safe.

## Inspect, repair, and retain

- Use `git worktree lock <path> --reason <reason>` for a worktree on removable storage or one that must not be pruned; use `unlock` only when that protection is no longer needed.
- If a worktree was moved manually, use `git worktree repair` only after confirming the intended paths. Do not hand-edit Git's worktree metadata.
- To find stale metadata, first run `git worktree prune --dry-run`. Run `git worktree prune` only after reviewing what it will remove. Pruning removes stale administrative records, not a substitute for reviewing real worktrees.

## Clean up a worktree

1. Identify the exact linked worktree; never target the main worktree.
2. Inspect its status, untracked files, current branch, and whether the branch has been merged or otherwise intentionally retained. Stop and ask if it is dirty, ambiguous, locked, or contains work that may be needed.
3. Remove a clean linked worktree with `git worktree remove <path>`. Do not substitute `rm -rf` for Git-managed removal.
4. Verify `git worktree list` no longer shows the path. Optionally run a reviewed `git worktree prune` to remove stale metadata.
5. Leave the branch intact unless its deletion was explicitly requested. Before deleting a branch, verify the target and merge/reachability state, then use the least destructive command appropriate to that evidence.

## Report

Report paths, branches, start points, and the commands or setup steps performed. Explicitly list any worktrees, branches, uncommitted files, locks, or destructive operations that were intentionally left untouched.
