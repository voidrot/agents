---
name: gh-cli
description: Use when operating GitHub from the command line with `gh`: repositories, issues, pull requests, Actions, releases, gists, codespaces, organizations, or GitHub API calls.
---

# GitHub CLI

Use this skill for github cli work in Git or GitHub repositories.

## When to activate

- User asks to inspect or change GitHub state via CLI.
- Need `gh` commands for issues, PRs, Actions, releases, repos, or API endpoints.
- Need non-interactive command examples for automation.

## Workflow

1. Confirm repository context and authentication requirements.
2. Prefer specific `gh` subcommands; use `gh api` for gaps.
3. Use non-interactive flags and JSON output where automation or parsing is needed.
4. Report commands run, results, and any required permissions.

## Safety rules

- Avoid commands that mutate GitHub state until the user intent is clear.
- Never expose tokens or secrets from auth/config output.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
