# PostgreSQL Operations and Diagnostics

## Slow Query Visibility

Enable and query `pg_stat_statements` when available.

```sql
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 20;
```

Use `EXPLAIN (ANALYZE, BUFFERS)` in non-production or carefully controlled production sessions; it executes the query.

## Unindexed Foreign Keys

Foreign keys do not automatically create indexes on the referencing columns.

```sql
SELECT conrelid::regclass AS table_name, a.attname AS column_name
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1
    FROM pg_index i
    WHERE i.indrelid = c.conrelid
      AND a.attnum = ANY(i.indkey)
  );
```

## Vacuum/Bloat Signals

```sql
SELECT relname, n_live_tup, n_dead_tup, last_vacuum, last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
```

High dead tuples are a signal to investigate workload, autovacuum settings, long-running transactions, and table-specific maintenance. Do not blindly run disruptive maintenance during peak traffic.

## Conservative Runtime Settings

Tune per workload and hosting environment; avoid cargo-cult values.

```sql
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';
SELECT pg_reload_conf();
```

`work_mem`, connection limits, autovacuum, and WAL settings depend on RAM, concurrency, query shape, and managed-service limits. Prefer measured changes with rollback notes.
