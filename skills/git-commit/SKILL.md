---
name: git-commit
description: "Review repository conventions and uncommitted changes, then safely plan or create focused Git commits. Use when asked to commit work, draft commit messages, or organize changes into commits; prefer Conventional Commits unless the repository clearly follows another convention."
---

# Git Commit

Create an accurate, reviewable commit plan from the actual changes. A request to commit authorizes creating commits, but not pushing or rewriting history.

## Defaults and boundaries

- Prefer the repository's established commit-message convention when it is clear from local instructions, commit templates, commit tooling, or recent history. Otherwise use Conventional Commits.
- Do not push, amend, reset, rebase, stash, force-push, skip hooks, change Git configuration, or add co-authors unless the user explicitly requests it.
- Do not commit secrets, credentials, `.env` files, private keys, generated caches, editor artifacts, or unrelated local work. Pause and ask if a potentially sensitive or ambiguous file appears intended for the commit.
- Treat already staged changes as likely user intent, but inspect them and report relevant unstaged or untracked work left out.
- For a dry-run, message-only, or planning request, do not stage or commit.

## Inspect the repository

1. Confirm the current directory is a Git worktree. Inspect the branch and concise status, including untracked files.
2. Review staged and unstaged diffs (and relevant untracked-file contents) before choosing files or a message. Never infer a commit's purpose from filenames alone.
3. Determine repository convention in this order:
   1. Local contributor instructions and commit templates.
   2. Commit-message tooling and release configuration, such as `commitlint`, `semantic-release`, or Release Please.
   3. Package/workspace/module boundaries that define valid scopes.
   4. Recent commit history, looking for a clear dominant format.
4. If the evidence is mixed or no convention is clear, state that and use the Conventional Commit default. Do not mechanically imitate isolated historical exceptions.

## Plan focused commits

1. Prefer one logical commit. Split only when changes are clearly independent and can be committed, tested, and understood separately. Keep related tests, documentation, and implementation together.
2. For each commit, identify the exact files and the message before staging. Stage explicit reviewed paths; do not use `git add .` or `git add -A` unless the user explicitly requests all safe changes and the complete file list was reviewed.
3. When staged changes do not match the plan, do not silently mix them with other work. Either preserve the staged set as its own coherent commit or ask the user how to proceed.

## Write the message

When Conventional Commits applies, use the official structure:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- Select the type from the diff: commonly `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `perf`, `style`, or `chore`.
- Use a scope only when repository evidence or a stable changed module supports it. Omit it rather than inventing vague scopes such as `misc`, `general`, or `repo`.
- Write a concise, imperative subject without a trailing period. Follow repository casing and length rules when they exist; otherwise keep the subject readable (normally no more than 72 characters).
- Use a body only when it explains important context or consequences. For a breaking change, use `!` and a `BREAKING CHANGE:` footer that explains impact and migration when known.
- If the repository uses another established convention, follow its format and vocabulary rather than forcing Conventional Commits.

## Stage, verify, and commit

For each planned commit:

1. Stage only its reviewed paths.
2. Reinspect the staged diff and confirm it contains exactly the intended logical change, with no sensitive or unrelated content.
3. Run the normal non-interactive `git commit` command. Supply body and footer separately when needed; allow configured hooks to run.
4. If hooks fail, stop and report their output and the safest next step. Never bypass them automatically. Make a follow-up commit for an authorized fix; do not amend unless explicitly requested.
5. Recheck status after every commit before starting another.

## Report

State the resulting commit hash and subject for each created commit, the convention evidence used, and any files deliberately left uncommitted. For a non-mutating request, report the proposed file groups and messages instead. Mention warnings only when they require attention.
