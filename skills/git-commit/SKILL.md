---
name: git-commit
description: "Review repository conventions and uncommitted changes, then safely plan or create focused Git commits. Use when asked to commit work, draft commit messages, or organize changes into commits; produce release-please-compatible Conventional Commits when that release automation is present."
---

# Git Commit

Create an accurate, reviewable commit plan from the actual changes. A request to commit authorizes creating commits, but not pushing or rewriting history.

## Defaults and boundaries

- Prefer the repository convention established by local instructions, commit templates, commit tooling, or recent history. When Release Please is configured, its Conventional Commit contract takes precedence over stylistic patterns in history. Otherwise use Conventional Commits.
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

## Write a Release Please-compatible message

When Release Please is configured, or when no other convention is established, use this exact structure:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

- Write the type in lowercase, put an optional scope in parentheses, put an optional `!` immediately before the colon, and put exactly one space after the colon. The first line must stand alone as a parseable header; do not prefix it with an emoji, ticket number, Markdown bullet, or other text.
- Choose the release-significant type from the user-visible effect:
  - `fix:` for a backward-compatible bug fix; Release Please treats it as a patch change.
  - `feat:` for backward-compatible functionality; Release Please treats it as a minor change.
  - `<type>!:` for a breaking change; Release Please treats the `!` as a major change. Use the truthful type, commonly `feat!:` or `fix!:`.
- Use `docs`, `refactor`, `test`, `build`, `ci`, `perf`, `style`, `chore`, or `revert` only when they accurately describe the diff. Do not label a feature or fix as `chore` to avoid a release. Whether other types appear in a changelog or trigger a release can depend on repository Release Please configuration.
- Use a scope only when repository evidence or a stable changed component supports it. Omit it rather than inventing vague scopes such as `misc`, `general`, or `repo`. In a manifest or monorepo setup, prefer the configured component/package name when the change belongs to one component.
- Write a concise, imperative description without a trailing period. Follow repository casing and length rules when they exist; otherwise keep the complete header readable, normally no more than 72 characters.
- Separate a body from the header with one blank line. Use it only for important context or consequences; do not put another Conventional Commit header in the body during ordinary commit creation.
- For a breaking change, use both the `!` marker and a final `BREAKING CHANGE: <impact and migration>` footer, separated from the body or header by a blank line. The marker ensures Release Please detects the major change; the footer makes the break explicit to readers.
- Add `Release-As: x.y.z` only when the user explicitly requests that exact next version. It overrides the version inferred from commit types.
- If the repository explicitly uses another release system or a customized Release Please type/section policy, follow that checked-in configuration and report the evidence used.

Examples:

```text
fix(parser): preserve escaped delimiters

feat(cli): add JSON output

feat(api)!: require explicit tenant IDs

BREAKING CHANGE: callers must pass tenant_id when creating a client.
```

## Stage, verify, and commit

For each planned commit:

1. Stage only its reviewed paths.
2. Reinspect the staged diff and confirm it contains exactly the intended logical change, with no sensitive or unrelated content.
3. Run the normal non-interactive `git commit` command. Supply body and footer separately when needed; allow configured hooks to run.
4. If hooks fail, stop and report their output and the safest next step. Never bypass them automatically. Make a follow-up commit for an authorized fix; do not amend unless explicitly requested.
5. Recheck status after every commit before starting another.

## Report

State the resulting commit hash and subject for each created commit, the convention evidence used, and any files deliberately left uncommitted. For a non-mutating request, report the proposed file groups and messages instead. Mention warnings only when they require attention.
