---
name: github-ops
description: Use for GitHub repository operations with `gh`: issue triage, PR management, CI status, releases, security alerts, stale items, contributor workflows, and repository maintenance.
---

# GitHub Operations

Use this skill for github operations work in Git or GitHub repositories.

## When to activate

- Triaging issues or pull requests.
- Checking CI, workflow runs, release readiness, or repository health.
- Managing GitHub operational tasks beyond local Git commands.

## Workflow

1. Confirm repository, permissions, and desired mutation level.
2. Gather current GitHub state with `gh` read commands or JSON output.
3. Perform the smallest requested operational change.
4. Report URLs, commands, state changes, and follow-up risks.

## Safety rules

- Do not merge, close, delete, publish, or change settings unless specifically requested.
- Avoid exposing tokens or private repository data.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
