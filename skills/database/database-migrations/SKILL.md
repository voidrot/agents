---
name: database-migrations
description: Use for safe schema/data migrations, rollback planning, migration tooling, and zero-downtime database changes.
origin: ECC
---

# Database Migration Patterns

Activation and routing layer for production-safe database changes.

## When to Activate

- Creating, altering, or dropping database tables, columns, constraints, or indexes
- Planning schema changes for live traffic or large tables
- Writing data backfills or data transforms
- Choosing migration workflow for Prisma, Drizzle, Kysely, Django, TypeORM, or golang-migrate
- Reviewing rollback, recovery, or expand/contract deployment plans

## Core Workflow

1. **Classify the change**: schema-only, data-only, mixed, destructive, or operational.
2. **Separate phases**: split schema changes, app compatibility changes, and data backfills.
3. **Design for forward recovery**: in production, prefer a new corrective migration over editing or reverting a deployed migration.
4. **Check locking and table size**: use concurrent/online patterns where the database supports them.
5. **Dry-run realistically**: test on production-like data and record expected duration, locks, and rollback path.

## Non-Negotiables

- Do not edit a migration that has run in production.
- Do not combine long data backfills with DDL in one transaction.
- Do not drop or rename a field until deployed code no longer depends on the old shape.
- PostgreSQL `CREATE INDEX CONCURRENTLY` / `DROP INDEX CONCURRENTLY` must not run inside a transaction block.
- Treat ORM-generated SQL as a draft; inspect it before applying it to production.

## Reference Routing

- PostgreSQL locking, column, index, backfill, and expand/contract recipes: [references/postgresql-safe-changes.md](references/postgresql-safe-changes.md)
- Prisma, Drizzle, Kysely, Django, TypeORM, and golang-migrate workflow notes: [references/orm-tooling-notes.md](references/orm-tooling-notes.md)
- Production rollout and review checklist: [references/zero-downtime-checklist.md](references/zero-downtime-checklist.md)

## Boundaries

- Use this skill for **migration-safe schema/data changes**.
- Use `postgres-patterns` for query design, indexes for query plans, RLS, and PostgreSQL runtime operations.
- Use `redis-patterns` for cache/session/rate-limit state, not relational schema evolution.

## Expected Output

- Migration sequence with deploy order
- Locking and rollback/forward-fix notes
- Tool-specific commands or files to create
- Verification query or operational check
