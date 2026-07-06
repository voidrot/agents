---
name: dependency-upgrade
description: Use when planning or executing dependency upgrades, especially major version changes, breaking changes, compatibility checks, staged rollouts, or dependency conflict resolution.
---

# Dependency Upgrade

Use this skill for dependency upgrade work in Git or GitHub repositories.

## When to activate

- Upgrading major framework, runtime, SDK, or library versions.
- Handling breaking changes, migrations, or dependency conflicts.
- Designing a safe incremental upgrade and test plan.

## Workflow

1. Inventory current versions, constraints, lockfiles, and transitive risks.
2. Read release notes and migration guides for breaking changes.
3. Plan small upgrade slices with rollback and verification points.
4. Run targeted tests first, then broader validation before recommending merge/release.

## Safety rules

- Do not upgrade unrelated dependencies in the same change unless explicitly requested.
- Preserve lockfile consistency and document migration risks.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
