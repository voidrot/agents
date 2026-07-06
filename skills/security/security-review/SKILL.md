---
name: security-review
description: Use when reviewing application code or product changes for security risks in auth, authorization, user input, data exposure, secrets, dependencies, payments, APIs, uploads, or sensitive workflows.
origin: ECC
---

# Security Review

Use this skill for human-guided security review of code and product behavior. For scanning Claude Code / agent configuration with AgentShield, use `security-scan` instead.

## When to activate

- Adding or changing authentication, authorization, session, token, or permission logic.
- Handling user input, file uploads, HTML/Markdown rendering, redirects, webhooks, or third-party callbacks.
- Creating or changing APIs, database access, payment flows, secrets handling, dependency surfaces, or sensitive data storage/transmission.
- Reviewing a PR, design, or codebase for OWASP-style application security risks.

## Boundary

- **Use this skill** for threat modeling, code review, abuse cases, data-flow review, dependency risk triage, and remediation guidance for application/product security.
- **Use `security-scan`** for automated inspection of Claude Code/agent configuration files, MCP servers, hooks, and AgentShield CI usage.

## Review workflow

1. Identify assets, trust boundaries, entry points, actors, framework conventions, and attacker-controlled data.
2. Map the change to risk areas: authentication, authorization, validation, injection, XSS, CSRF, SSRF, secrets, logging, data exposure, uploads, rate limits, dependencies, and deployment controls.
3. Trace dangerous data flows across files and verify missing server-side enforcement, unsafe defaults, and business-logic abuse cases.
4. Check dependencies and configuration for known risky packages, exposed secrets, weak crypto, and unsafe deployment assumptions.
5. Verify mitigations with tests, configuration checks, negative cases, and residual-risk notes.
6. Report findings by severity with exploit path, evidence, recommended fix, and confidence.

## Priority checks

- No hardcoded secrets, tokens, credentials, or sensitive values in code, config, logs, examples, or generated output.
- All authorization decisions happen server-side and are checked before sensitive operations.
- User input is validated and encoded/sanitized at the correct trust boundary.
- Database and shell calls use parameterization or safe builders; no attacker-controlled strings reach dangerous sinks unsafely.
- Cookies, sessions, CSRF defenses, CORS, CSP, and security headers match the app's threat model.
- Errors and logs do not expose secrets, stack traces, payment data, tokens, or private user data.
- Dependency and deployment risks are identified with evidence, not hidden behind generic audit advice.

## References

Read only the sections relevant to the change:

- [Application security checklist](references/application-security-checklist.md) — OWASP-aligned review prompts.
- [Security code examples](references/security-code-examples.md) — safe/unsafe patterns for validation, SQL, XSS, auth, logging, and tests.
- [Deployment checklist](references/deployment-checklist.md) — release-time controls and verification.
- [Language patterns](references/language-patterns.md) — language-specific vulnerability patterns.
- [Secret patterns](references/secret-patterns.md) — credential and token detection heuristics.
- [Vulnerability categories](references/vuln-categories.md) — deeper category checklist for review coverage.
- [Vulnerable packages](references/vulnerable-packages.md) — dependency watchlist for fast triage.
- [Report format](references/report-format.md) — structured output template for larger audits.
- [Candidate merge notes](references/candidate-merge-notes.md) — preserved source guidance; use only for deeper audit workflow detail.
- External: [OWASP Top 10](https://owasp.org/www-project-top-ten/), [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/), [PortSwigger Web Security Academy](https://owasp.org/www-project-web-security-testing-guide/).

## Output

Return a concise threat summary, findings sorted by severity, exact file/flow evidence when available, fixes, tests to add, confidence, and unresolved assumptions.
