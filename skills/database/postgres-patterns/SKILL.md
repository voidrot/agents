---
name: postgres-patterns
description: Use for PostgreSQL query design, schema/table design, indexing, RLS, EXPLAIN-based optimization, feature-specific SQL review, and operational diagnostics.
origin: ECC
---

# PostgreSQL Patterns

Activation and routing layer for PostgreSQL application and operations patterns.

## When to Activate

- Designing queries, indexes, schemas, or tables for PostgreSQL
- Reviewing PostgreSQL-specific SQL, migrations, functions, triggers, JSONB, arrays, custom types, or extensions
- Troubleshooting slow queries with `EXPLAIN` / `EXPLAIN ANALYZE`
- Implementing Row Level Security policies
- Choosing data types, pagination, UPSERT, queue, partitioning, or transaction patterns
- Checking bloat, vacuum pressure, connection usage, or `pg_stat_statements` diagnostics

## Quick Workflow

1. Start from the actual schema, query, and access pattern.
2. Confirm PostgreSQL version and enabled extensions before relying on feature-specific advice.
3. Prefer PostgreSQL-native types and constraints over application-only validation.
4. Inspect query plans before adding indexes or rewriting SQL.
5. Keep RLS policies simple and benchmark them with representative rows.
6. Separate query/index tuning from migration rollout safety.

## Reference Routing

- Query, index, RLS, UPSERT, cursor pagination, and queue recipes: [references/query-index-rls-recipes.md](references/query-index-rls-recipes.md)
- Schema/table design, data types, constraints, partitioning, JSONB, and extensions: [references/schema-design.md](references/schema-design.md)
- PostgreSQL-specific code review checklist for JSONB, arrays, functions, triggers, RLS, and privileges: [references/code-review-checklist.md](references/code-review-checklist.md)
- Advanced PostgreSQL features, full-text search, range/geometric types, extensions, and optimization examples: [references/advanced-features-and-optimization.md](references/advanced-features-and-optimization.md)
- `pg_stat_statements`, bloat/vacuum checks, connection checks, and conservative config notes: [references/operations-diagnostics.md](references/operations-diagnostics.md)

## Boundaries

- Use this skill for PostgreSQL-specific schema, query, runtime, and review patterns.
- Use `sql-code-review` for database-agnostic SQL security/maintainability review.
- Use `sql-optimization` for database-agnostic SQL performance work.
- Use `database-migrations` for production migration sequencing, lock-aware rollout, and ORM migration tooling.
- Use `redis-patterns` when the state is cache/session/rate-limit/event-stream oriented.

## Expected Output

- Proposed SQL or schema pattern
- Index rationale tied to a query shape
- PostgreSQL-specific risks, feature requirements, or version assumptions
- Verification query or `EXPLAIN` check
- Operational caveats for production use
