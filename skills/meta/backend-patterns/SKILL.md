---
name: backend-patterns
description: Use when designing backend service structure, data access, middleware, caching, background jobs, transactions, or server-side architecture behind an API or application.
origin: ECC
---

# Backend Development Patterns

Use this skill for maintainable server-side implementation structure: boundaries between handlers, services, repositories, transactions, caches, jobs, middleware, and observability.

## Scope Boundaries

- Use `backend-patterns` for backend internals and operational architecture.
- Use `api-design` for HTTP contract choices: resource names, response envelopes, status codes, pagination, and versioning.
- Use `error-handling` for error taxonomy, retry policy, circuit breakers, and user/developer message separation.
- Use `frontend-patterns` for browser/client implementation; use this skill only for server-rendering or backend-for-frontend concerns.

## Workflow

1. Locate the existing server entry points, dependency seams, data access patterns, and deployment/runtime constraints.
2. Choose the smallest useful layering: handler/controller, service/domain logic, repository/gateway, and integration adapters only where they buy locality or testability.
3. Design data access, transactions, caching, background work, auth middleware, logging, and rate limiting around real traffic and failure modes.
4. Keep framework examples subordinate to the project’s existing conventions.
5. Return a concrete structure, ownership of concerns, risks, and verification commands.

## Constraints

- Do not add architectural layers that merely pass arguments through.
- Do not use per-process in-memory state for production rate limits, jobs, or cross-request coordination in multi-instance/serverless deployments.
- Keep API-visible behavior synchronized with `api-design` and production failures synchronized with `error-handling`.

## Supporting Material

- Read `references/backend-architecture-guidance.md` for examples of repositories, services, middleware, caching, transactions, jobs, logging, and auth patterns.
- Review references and assets with candidate material merged from `backend-patterns` when the request overlaps that source's specialized workflow.
  - `references/backend-patterns-merge-notes.md`
