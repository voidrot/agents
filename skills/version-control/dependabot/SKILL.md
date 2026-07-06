---
name: dependabot
description: Use when configuring GitHub Dependabot, dependabot.yml, grouped dependency updates, security update PRs, package ecosystem schedules, or Dependabot PR handling.
---

# Dependabot

Use this skill for dependabot work in Git or GitHub repositories.

## When to activate

- Creating or optimizing `.github/dependabot.yml`.
- Grouping dependency updates or tuning update cadence.
- Triaging Dependabot PRs and security alerts.

## Workflow

1. Identify ecosystems, manifests, package directories, and update goals.
2. Choose schedules, grouping, open PR limits, reviewers, labels, and security behavior.
3. Validate YAML structure and package ecosystem names against GitHub Dependabot docs.
4. Explain PR handling, ignore rules, and operational follow-up.

## Safety rules

- Do not assume one Dependabot config can live outside `.github/dependabot.yml` on the default branch.
- Treat dependency update automation as supply-chain-sensitive; preserve review and CI gates.

## References

- [references/full-guidance.md](references/full-guidance.md) — supporting material; open only when needed.
- [references/dependabot-yml-reference.md](references/dependabot-yml-reference.md) — supporting material; open only when needed.
- [references/example-configs.md](references/example-configs.md) — supporting material; open only when needed.
- [references/pr-commands.md](references/pr-commands.md) — supporting material; open only when needed.
