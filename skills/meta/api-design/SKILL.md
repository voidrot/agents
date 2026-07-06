---
name: api-design
description: Use when designing or reviewing HTTP API contracts, including REST resources, methods, status codes, pagination, filtering, versioning, rate limits, and OpenAPI-facing behavior.
origin: ECC
---

# API Design Patterns

Use this skill for the external API contract: resource shape, HTTP semantics, request/response envelopes, pagination, filtering, versioning, and documentation-visible errors.

## Scope Boundaries

- Use `api-design` for client-visible API contracts and protocol decisions.
- Use `backend-patterns` for server internals: service layers, repositories, caching, queues, middleware composition, and data access.
- Use `error-handling` for cross-language error taxonomies, retry policy, and where errors are created, logged, or surfaced.
- Use language/framework-specific skills for implementation details once the contract is chosen.

## Workflow

1. Identify the API audience, compatibility needs, and existing endpoint conventions.
2. Model resources as nouns and choose methods/status codes by HTTP semantics.
3. Define validation, authorization outcomes, error envelopes, pagination, filtering, sorting, rate-limit headers, and versioning rules.
4. Check the design against existing OpenAPI/Swagger docs or update those docs as part of the work.
5. Return concrete endpoint contracts plus edge cases and verification steps.

## Constraints

- Do not expose stack traces, database errors, secrets, or internal identifiers in public responses.
- Prefer consistency with an existing API over introducing a new envelope style for one endpoint.
- Treat error responses as part of the API contract; coordinate taxonomy with `error-handling`.

## Supporting Material

- Read `references/http-api-guidance.md` for detailed examples, status-code tables, pagination choices, versioning notes, and implementation snippets.
- Review references and assets with candidate material merged from `api-design-principles` when the request overlaps that source's specialized workflow.
  - `references/api-design-principles-merge-notes.md`
  - `references/details.md`
  - `references/graphql-schema-design.md`
  - `references/rest-best-practices.md`
  - `assets/api-design-checklist.md`
  - `assets/rest-api-template.py`
