---
name: production-audit
description: Use for local-evidence production readiness audits before launch, deploy, demo, or rollout when the user asks what could break in production.
origin: community
---

# Production Audit

Assess application production readiness from local and user-authorized evidence. This is engineering triage, not legal/compliance certification.

## When to Use

- The user asks whether an app is production-ready, ready to ship, or what would break in prod.
- A release branch, deployed URL, PR, or current checkout needs pre-launch or post-merge risk review.
- CI is green but the user wants operational, data, auth, payment, UX, or rollback risk assessed.

## Workflow

1. Establish the release surface and available evidence.
2. Inspect current branch state, recent changes, runtime boundaries, CI, tests, migrations, env docs, deployment config, rollback path, and critical user flows.
3. Score readiness with blockers and confidence tied to evidence, not vibes.
4. Produce a short ship/block recommendation, missing evidence, and one next action.

## Constraints

- Do not run unpinned remote code, upload repo data, or call external scanners without explicit user approval for that tool and data flow.
- Do not treat green CI as production readiness.
- Do not produce a score without listing evidence checked and evidence missing.

## Supporting Material

- Read `references/audit-checklists.md` for detailed evidence checklist, risk lenses, scoring caps, output example, and anti-patterns.
