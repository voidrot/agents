# Git branching strategies

## GitHub Flow

Best for continuous deployment and small-to-medium teams.

```text
main (protected, always deployable)
  ├── feature/user-auth      → PR → merge to main
  ├── feature/payment-flow   → PR → merge to main
  └── fix/login-bug          → PR → merge to main
```

Rules:

- `main` is always deployable.
- Create short-lived feature/fix branches from `main`.
- Open a PR for review and CI.
- Merge after approval and passing checks.
- Deploy soon after merge.

## Trunk-based development

Best for experienced teams with strong CI/CD and feature flags.

```text
main (trunk)
  ├── short-lived feature branch
  ├── short-lived feature branch
  └── direct commits only if protected by strict CI/review
```

Rules:

- Keep branches very short-lived.
- Hide incomplete work behind feature flags.
- Require fast, reliable checks.
- Prefer small changes and frequent integration.

## GitFlow

Best for scheduled releases, long stabilization windows, or regulated release trains.

```text
main (production releases)
  └── develop (integration)
        ├── feature/user-auth
        ├── release/1.0.0 → merge to main and develop
        └── hotfix/critical → merge to main and develop
```

Rules:

- `main` contains production-ready releases.
- `develop` integrates upcoming release work.
- Release branches stabilize before tagging.
- Hotfixes start from production and merge back into integration.

## Selection guide

| Strategy | Release cadence | Best for | Cost |
| --- | --- | --- | --- |
| GitHub Flow | Continuous | SaaS, web apps, most repos | Low |
| Trunk-based | Many deploys/day | high-velocity teams with feature flags | Medium |
| GitFlow | Scheduled releases | enterprise/regulatory release trains | High |
