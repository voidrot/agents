---
name: changelog-automation
description: Use when generating or automating changelogs, release notes, Conventional Commit based release summaries, Keep a Changelog files, or version history workflows.
---

# Changelog Automation

Use this skill for changelog automation work in Git or GitHub repositories.

## When to activate

- Setting up automated changelog or release note generation.
- Converting commit or PR history into user-facing change entries.
- Choosing changelog categories, SemVer impact, or release-note workflow.

## Workflow

1. Identify the source of truth: commits, PRs, tags, issues, or an existing changelog.
2. Classify changes into user-facing categories and determine version impact.
3. Generate or update changelog/release notes in the project format.
4. Verify links, dates, versions, and omitted internal-only changes.

## Safety rules

- Do not invent changes that are not present in commits, PRs, issues, or user-provided notes.
- Keep generated release notes factual and user-facing.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
- [references/details.md](references/details.md) — supporting material; open only when needed.
