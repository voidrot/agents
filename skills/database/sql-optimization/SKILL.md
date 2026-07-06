---
name: sql-optimization
description: Use when diagnosing slow SQL, analyzing execution plans, designing indexes, optimizing pagination, batching, joins, aggregations, or cross-database query performance.
---

# SQL Optimization

Use this skill as a concise routing layer. Load supporting references only when the task needs detailed patterns, examples, or implementation templates.

## When to Activate

- Debugging slow queries or database-heavy application paths
- Reading EXPLAIN/execution plans and connecting them to query/index changes
- Designing selective, covering, composite, partial, or expression indexes
- Optimizing pagination, joins, aggregations, subqueries, and batch operations across SQL databases

## Quick Workflow

1. Start with the exact query, bind values, cardinality, and workload shape.
2. Capture an execution plan using the database-appropriate EXPLAIN tooling.
3. Identify the bottleneck before adding indexes or rewriting SQL.
4. Prefer sargable predicates, explicit columns, cursor pagination, set-based operations, and measured indexes.
5. Re-run the plan and note write-path, storage, and operational trade-offs.

## Reference Routing

- Full optimization guidance and examples: [references/full-guidance.md](references/full-guidance.md)
- Additional EXPLAIN and indexing patterns: [references/patterns-and-explain.md](references/patterns-and-explain.md)

## Boundaries

- Use `sql-code-review` for security/maintainability review.
- Use `postgres-patterns` for PostgreSQL-specific operations and features.

## Expected Output

- Performance hypothesis tied to plan evidence
- Query rewrite or index recommendation
- Expected trade-offs for writes/storage/locking
- Verification plan and follow-up metrics
