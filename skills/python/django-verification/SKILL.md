---
name: django-verification
description: Run Django verification loops for migrations, checks, tests, coverage, security, and release readiness.
origin: ECC
---

# Django Verification

## When to use

- verifying Django changes before PR, deploy, or release
- designing a Django test/check command sequence
- debugging failures in migrations, checks, tests, coverage, static files, or deployment checks

## Workflow

1. Identify the app, settings module, database requirements, and test runner.
2. Run the smallest relevant verification loop first, then widen to full project checks.
3. Include migrations and system checks for model/settings changes.
4. Add security/deploy checks for production-impacting changes.
5. Report exact commands run, results, and any skipped checks with reasons.

## Constraints

- Use non-interactive commands suitable for CI.
- Do not mark release-ready if migrations, security checks, or critical tests were skipped without owner approval.
- Move command matrices and checklists to references.

## References

- [moved verification commands and checklists](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
