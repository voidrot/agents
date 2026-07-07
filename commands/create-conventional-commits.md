---
description: Review uncommitted work and create one or more Conventional Commits with repository-aware scopes.
model: openai/gpt-5.4-mini
---

# Create Conventional Commits

You are helping the user turn the current uncommitted work into clean, logical Conventional Commits.

Arguments supplied by the user:

```text
$ARGUMENTS
```

## Required skills and references

Before acting, load @git-commit.

Use the Conventional Commits specification as the format authority:

- https://www.conventionalcommits.org/en/v1.0.0/#specification

If available from @git-commit, also consult its Conventional Commit supporting reference before generating messages.

## Operating mode

Default behavior is to create commits, not merely suggest messages, unless the user explicitly asks for dry-run/message-only output.

Supported user intent in `$ARGUMENTS`:

- `--dry-run` or wording like "message only": review the work and propose commit plan/messages without staging or committing.
- `--all`: include all tracked and untracked work that is safe to commit.
- Paths or descriptions: limit the commit plan to those files/areas when possible.
- Explicit type/scope/description hints: honor them if they match the actual diff and repository conventions.

## Non-negotiable safety rules

1. Work from evidence: inspect Git state and diffs before choosing files, types, scopes, or messages.
2. Do not commit secrets, credentials, `.env` files, private keys, generated caches, unrelated local changes, or editor artifacts.
3. Do not use interactive staging (`git add -p`) in this environment.
4. Do not amend, reset, stash, force-push, skip hooks, or change Git config unless the user explicitly asks.
5. Prefer one logical commit. Split into multiple commits only when the diff contains clearly unrelated logical changes.
6. Stage explicit file paths for each logical commit; never blindly `git add .` unless the user supplied `--all` and the reviewed file list is safe.
7. If hooks fail, report the failure and the safest next step. Do not bypass hooks unless explicitly requested.

## Discovery workflow

Run non-interactive Git commands as needed:

1. Confirm this is a Git repository.
2. Inspect current branch and status, including untracked files.
3. Inspect staged and unstaged diffs.
4. If files are already staged, treat the staged set as the user's likely intended commit set, but still inspect unstaged work and report anything left out.
5. Identify whether the uncommitted work contains one logical change or several.

## Repository scope discovery

Before selecting any Conventional Commit scope, look for repository-defined scopes or release automation configuration.

Prioritize local evidence in this order:

1. Release Please configuration, if present, such as:
   - `release-please-config.json`
   - `.release-please-manifest.json`
   - `release-please.yml` / `release-please.yaml`
   - `.github/workflows/*release*please*.yml` / `.github/workflows/*release*please*.yaml`
2. Commitlint or conventional-commit tooling, if present, such as:
   - `commitlint.config.*`
   - `.commitlintrc*`
   - `package.json` commitlint or release tooling config
3. Monorepo/workspace/package boundaries, if present, such as:
   - package/workspace names in `package.json`, `pnpm-workspace.yaml`, `yarn.lock`, `turbo.json`, `nx.json`
   - Rust crates, Go modules, Python packages, Terraform modules, Helm charts, or other obvious module roots
4. Existing commit history, only as secondary evidence, to learn scope spelling and style.

If repo-defined scopes are found, use only a matching scope unless the diff clearly requires no scope or a new scope. If no files define scopes, report that no repository scope registry/configuration was found and choose the best scope from the changed paths/modules. If no defensible scope can be determined, omit the scope entirely.

Scope rules:

- Use lowercase kebab-case unless repository evidence shows a different convention.
- Prefer the smallest stable product/package/module boundary over a file name.
- Do not invent broad scopes like `misc`, `general`, `repo`, or `changes`.
- Do not use a scope when the change affects the whole repository or the scope would be misleading.

## Commit message rules

Generate messages in Conventional Commits format:

```text
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

Allowed types:

- `feat` for user-visible functionality
- `fix` for bug fixes
- `docs` for documentation-only changes
- `style` for formatting/style-only changes with no behavior change
- `refactor` for code restructuring with no behavior change
- `perf` for performance improvements
- `test` for tests only
- `build` for build system, dependency, packaging, or generated lockfile changes
- `ci` for CI/CD workflow changes
- `chore` for maintenance that does not fit the above
- `revert` for reverting prior commits

Description requirements:

- imperative mood: `add`, `fix`, `update`, not `added`, `fixes`, `updated`
- lower-case first word unless it is a proper noun or identifier
- no trailing period
- concise enough for a readable subject line

Breaking changes:

- Use `!` after type/scope when the diff contains a breaking change.
- Include a `BREAKING CHANGE:` footer explaining the impact and migration path when known.

## Execution workflow

For each logical commit:

1. Present the planned commit internally from the inspected evidence: files, type, optional scope, subject, body/footer if needed.
2. Stage only the files for that logical commit.
3. Verify the staged diff matches the intended logical change.
4. Run `git commit -m` non-interactively. For body/footer, use multiple `-m` arguments.
5. After each commit, re-check status before continuing to another commit.

If dry-run/message-only was requested, do not stage or commit. Output the proposed commit plan instead.

## Final response

Keep the final response terse and table-formatted.

Include:

| Item | Result |
| --- | --- |
| Commits | commit hash and subject for each commit, or proposed subject in dry-run mode |
| Scope source | config/tool/history evidence used, or `none found; best-effort path/module inference`, or `none determined; scope omitted` |
| Files left uncommitted | only if any remain |
| Warnings | only if needed |
