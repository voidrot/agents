---
name: django-security
description: Review Django authentication, authorization, CSRF, cookies, headers, secrets, and deployment hardening.
origin: ECC
---

# Django Security

## When to use

- reviewing Django apps for security vulnerabilities or deployment readiness
- configuring auth, permissions, CSRF, sessions, cookies, CORS, HTTPS, or security middleware
- responding to security-sensitive Django bug reports or audit findings

## Workflow

1. Map trust boundaries: users, staff/admin, APIs, third-party callbacks, and background jobs.
2. Check Django’s built-in protections before adding custom security code.
3. Harden settings for the target environment and run manage.py check --deploy where applicable.
4. Verify authorization at object and action level, not just view access.
5. Test the exploit path or regression case without exposing secrets.

## Constraints

- Never disable CSRF, escaping, cookie security, or host validation without an explicit, documented compensating control.
- Do not log secrets, session IDs, raw tokens, or sensitive request bodies.
- Move hardening matrices and deployment checklists to references.

## References

- [moved Django security guidance](references/full-guidance.md)
- [verification sources](references/official-docs.md)

## Expected output

- A brief summary of the change or recommendation.
- Commands/checks run, or the reason verification was not run.
- Any version assumptions or official-doc checks that matter for the result.
