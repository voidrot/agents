# Application security checklist

Use this checklist as prompts for code/product security review. Adapt severity to the project's threat model.

## Secrets management

- No API keys, tokens, private keys, passwords, or credentials in source, config examples, logs, screenshots, or git history.
- Runtime secrets are loaded from the deployment secret store or environment.
- Missing secrets fail closed with clear operational errors, not insecure fallbacks.
- `.env`, `.env.local`, and production secret dumps are ignored and never committed.

## Input validation and injection

- Validate external input at the boundary with allowlists or schemas.
- Parameterize SQL and avoid string concatenation for queries.
- Treat headers, cookies, query strings, webhook payloads, uploaded files, filenames, URLs, and metadata as attacker-controlled.
- Avoid command execution; if unavoidable, pass arguments without shell interpolation and validate allowed commands.

## Authentication and authorization

- Authentication verifies issuer, audience, expiry, signature, nonce/state where relevant.
- Authorization checks run server-side before every sensitive read/write.
- Object-level authorization prevents IDOR/BOLA issues.
- Admin, tenant, organization, and ownership boundaries are explicit in code and tests.
- Session fixation, logout, token rotation, and revocation are considered for sensitive systems.

## XSS, CSRF, CORS, and browser controls

- User-controlled HTML is sanitized with a maintained allowlist sanitizer or avoided entirely.
- Output is encoded for the destination context.
- CSP starts strict and exceptions are documented.
- State-changing cookie-authenticated requests have CSRF defenses unless SameSite and API design make risk explicitly negligible.
- CORS allows only required origins, methods, and headers; credentials are not paired with wildcard origins.

## Sensitive data exposure

- Logs redact credentials, tokens, payment data, secrets, and unnecessary PII.
- User-facing errors are generic; server logs keep actionable detail safely.
- Data at rest and in transit match project requirements.
- Cache headers prevent private data from being stored in shared caches.

## Uploads, files, and URLs

- Enforce size, extension, MIME, and content validation where appropriate.
- Store untrusted uploads outside executable/static roots unless intentionally public.
- Generate server-side filenames and avoid path traversal.
- SSRF defenses validate destinations, block private networks where required, and do not trust redirects blindly.

## Rate limiting and abuse

- Login, signup, password reset, expensive search, webhooks, and write APIs have rate limits or abuse controls.
- Limits account for authenticated users, IPs, tenants, and distributed abuse where needed.
- Lockout and throttling do not create trivial denial-of-service against victims.

## Dependencies and supply chain

- Lock files are committed and used in CI.
- Known vulnerabilities are triaged with exploitability and reachable code in mind.
- Postinstall scripts, untrusted packages, and generated artifacts are reviewed for high-risk changes.
