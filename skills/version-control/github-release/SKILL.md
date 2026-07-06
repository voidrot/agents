---
name: github-release
description: Use when cutting GitHub releases, bumping versions, generating changelogs, creating release PRs or tags, and publishing release notes with `gh` and Git.
---

# GitHub Release

Use this skill for github release work in Git or GitHub repositories.

## When to activate

- User wants to release, ship, tag, bump a version, or generate release notes.
- Need SemVer classification and Keep a Changelog style release notes.
- Need a release branch, release PR, or GitHub Release draft/publish workflow.

## Workflow

1. Inspect repository state, tags, current version, changelog, and unreleased changes.
2. Classify SemVer impact and draft release notes.
3. Confirm write actions before version bumps, tags, branches, PRs, or publishing.
4. Run verification and report release artifacts, URLs, and unresolved risks.

## Safety rules

- Keep reconnaissance read-only until the release version and write actions are clear.
- Do not publish, tag, or push without explicit user approval.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
- [references/commit-classification.md](references/commit-classification.md) — supporting material; open only when needed.
- [references/semver-rules.md](references/semver-rules.md) — supporting material; open only when needed.
