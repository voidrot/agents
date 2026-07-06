---
name: auth-implementation-patterns
description: Use when implementing, reviewing, or debugging authentication and authorization flows including sessions, JWTs, OAuth2/OIDC, SSO, MFA, RBAC/ABAC, token storage, and API access control.
---

# Auth Implementation Patterns

Use this skill as the activation and routing layer for auth implementation patterns work. Keep the main response grounded in the user's system, repository, and constraints; load supporting references only when the task needs detail.

## Workflow

1. Separate authentication, authorization, session/token lifecycle, and audit requirements before choosing mechanisms.
2. Identify trust boundaries, identity providers, token issuers, clients, resources, and privileged operations.
3. Select patterns that fit the app: server sessions, OAuth2/OIDC, signed tokens, policy checks, MFA, and service-to-service auth.
4. Check secure defaults for password storage, cookies, CSRF, CORS, redirects, token expiry/rotation, rate limits, and server-side enforcement.
5. Add negative tests and operational controls for lockout, revocation, logging, recovery, and incident response.

## Constraints

- Verify tool-specific commands, platform settings, legal/compliance claims, and framework APIs against current official documentation before treating them as authoritative.
- Prefer concrete evidence, traceability, and testable mitigations over generic security advice.
- Call out assumptions and residual risk instead of overstating certainty.
- Keep generated outputs concise unless the user asks for a full report.

## References

- references/details.md for detailed patterns, examples, and implementation notes.
- references/quick-reference.md for the original summary and common pitfalls.

## Output

Return the relevant model, table, checklist, or findings list with priorities, evidence, recommended actions, verification steps, and unresolved assumptions.
