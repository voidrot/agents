---
name: mysql-patterns
description: Use for MySQL/InnoDB schema design, indexing, transactions, locking, online DDL, replication, and MySQL-specific performance diagnostics.
---

# MySQL Patterns

Activation and routing layer for safe, measurable MySQL/InnoDB changes.

## When to Activate

- Designing MySQL tables, primary keys, data types, character sets, or JSON columns
- Choosing MySQL/InnoDB indexes, partitioning, or full-text search patterns
- Diagnosing slow MySQL queries with `EXPLAIN` / `EXPLAIN ANALYZE`
- Reviewing transaction isolation, gap locks, deadlocks, or `SELECT ... FOR UPDATE`
- Planning MySQL online DDL, connection handling, or replication-lag safeguards

## Workflow

1. Define workload and constraints (read/write mix, latency target, data volume, MySQL version, hosting platform).
2. Read only the relevant reference files linked in each section below.
3. Propose the smallest change that can solve the problem, including trade-offs.
4. Validate with evidence (`EXPLAIN`, `EXPLAIN ANALYZE`, lock/connection metrics, and production-safe rollout steps).
5. For production changes, include rollback and post-deploy verification.

## Reference Routing

- Primary-key and clustered-index design: [references/primary-keys.md](references/primary-keys.md)
- Data types, character sets, collations, and JSON column patterns: [references/data-types.md](references/data-types.md), [references/character-sets.md](references/character-sets.md), [references/json-column-patterns.md](references/json-column-patterns.md)
- Composite, covering, full-text, and maintenance-oriented indexes: [references/composite-indexes.md](references/composite-indexes.md), [references/covering-indexes.md](references/covering-indexes.md), [references/fulltext-indexes.md](references/fulltext-indexes.md), [references/index-maintenance.md](references/index-maintenance.md)
- Partitioning and large-table maintenance: [references/partitioning.md](references/partitioning.md)
- MySQL query-plan analysis and query pitfalls: [references/explain-analysis.md](references/explain-analysis.md), [references/query-optimization-pitfalls.md](references/query-optimization-pitfalls.md), [references/n-plus-one.md](references/n-plus-one.md)
- Isolation levels, deadlocks, and row-locking behavior: [references/isolation-levels.md](references/isolation-levels.md), [references/deadlocks.md](references/deadlocks.md), [references/row-locking-gotchas.md](references/row-locking-gotchas.md)
- Online DDL, connections, and replication lag: [references/online-ddl.md](references/online-ddl.md), [references/connection-management.md](references/connection-management.md), [references/replication-lag.md](references/replication-lag.md)

## Boundaries

- Use this skill for MySQL/InnoDB-specific schema, query, locking, and runtime behavior.
- Use `sql-code-review` for database-agnostic SQL security and maintainability review.
- Use `sql-optimization` for database-agnostic SQL performance work.
- Use `database-migrations` for production migration sequencing, rollback planning, and migration tooling.

## Guardrails

- Prefer measured evidence over blanket rules of thumb.
- Note MySQL-version-specific behavior when giving advice.
- Ask for explicit human approval before destructive data operations (drops/deletes/truncates).
