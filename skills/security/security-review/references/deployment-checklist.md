# Security deployment checklist

Before production deployment, verify the applicable items and document accepted risk.

- [ ] Secrets are stored in the deployment secret manager and absent from source/history.
- [ ] Authentication and authorization tests pass, including negative tests.
- [ ] Input validation and output encoding/sanitization are covered for changed flows.
- [ ] SQL/NoSQL queries are parameterized or use safe query builder APIs.
- [ ] CSRF, CORS, cookies, and session settings match the deployed domain model.
- [ ] CSP and other security headers are configured and tested.
- [ ] Rate limits or abuse controls protect high-cost and sensitive endpoints.
- [ ] User-facing errors do not leak internals; operational logs redact sensitive data.
- [ ] File uploads enforce size/type/path restrictions and are scanned or isolated when needed.
- [ ] Dependency vulnerabilities are scanned and triaged.
- [ ] HTTPS is enforced and local/debug bypasses are disabled in production.
- [ ] Rollback and incident-response owners are known for high-risk releases.
