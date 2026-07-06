# Git operations cookbook

## Merge vs rebase

Use merge when preserving branch topology matters or the branch is shared.

```bash
git checkout main
git merge feature/user-auth
```

Use rebase to update a local/private feature branch onto the latest target.

```bash
git checkout feature/user-auth
git fetch origin
git rebase origin/main
git push --force-with-lease origin feature/user-auth
```

Do not rebase protected branches, already-merged branches, or branches that others are using unless the team has explicitly agreed.

## Branch names

```text
feature/user-authentication
fix/login-redirect-loop
hotfix/critical-security-patch
release/1.2.0
experiment/new-caching-strategy
```

## Branch cleanup

```bash
git fetch -p
git branch --merged main
git branch -d feature/user-auth
git push origin --delete feature/user-auth
```

## Stash workflow

```bash
git stash push -m "WIP: user authentication"
git stash list
git stash pop
git stash apply stash@{2}
git stash drop stash@{0}
```

## Releases and tags

```bash
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
git tag -l
git tag -d v1.2.0
git push origin --delete v1.2.0
```

## Useful safe defaults

```bash
git config --global init.defaultBranch main
git config --global push.default current
git config --global diff.algorithm histogram
```

Set pull behavior per project/team rather than globally if merge vs rebase policy varies.

## Hooks

Hooks should be fast, deterministic, and non-interactive. Keep expensive checks in CI or pre-push.

```bash
#!/bin/sh
npm run lint || exit 1
npm test || exit 1
```

Avoid hooks that silently ignore failures (`|| true`) or inspect secrets with brittle patterns as the only protection.

## Quick commands

| Task | Command |
| --- | --- |
| Create branch | `git checkout -b feature/name` |
| Switch branch | `git checkout branch-name` |
| Delete merged branch | `git branch -d branch-name` |
| Merge branch | `git merge branch-name` |
| Rebase branch | `git rebase main` |
| View history | `git log --oneline --graph` |
| View changes | `git diff` |
| Stage changes | `git add <path>` |
| Commit | `git commit -m "type(scope): subject"` |
| Stash | `git stash push -m "message"` |
| Revert public commit | `git revert <sha>` |
