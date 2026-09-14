---
name: efficient-postgres
description: Diagnose and safely change PostgreSQL query performance, indexes and statistics, locking, MVCC and isolation, partitioning, maintenance, observability, backups, or advanced features; use when work targets a PostgreSQL instance or PostgreSQL-specific SQL and operations rather than portable relational schema design.
---

# Efficient PostgreSQL

Use this skill for a measured PostgreSQL change or investigation. Establish the workload and failure mode before changing SQL, configuration, indexes, data layout, or maintenance. Prefer the smallest reversible change that improves an observed outcome.

Do not use this as the primary workflow for portable tables, keys, constraints, relationship modelling, or general migration design; use `efficient-database-design` for that work. Do not infer that PostgreSQL is deployed, what version it runs, or that an extension, replica, superuser privilege, or production access exists. Verify each of those facts from the target environment.

## Workflow

1. **Set the operational boundary.** Identify the database version, deployment topology, owner, maintenance window, allowed privileges, data sensitivity, rollback path, and whether the target is production. State the user-visible symptom and a measurable completion condition: for example, a query's latency and row count, a lock wait, failed transaction rate, or recovery objective. Do not run writes, DDL, cancellation, or load-generating probes against production without authorization and a recovery plan.

2. **Capture a minimal baseline.** Preserve the query or transaction shape, parameter ranges, call frequency/concurrency, relevant schema and indexes, table sizes, and a time-bounded sample of latency, rows, and errors. Redact literals, identifiers, and plans that expose secrets or sensitive data. Use existing PostgreSQL statistics and monitoring views first; record collection time and transaction context because statistics may be cached or lagging. If the symptom cannot be reproduced or sampled, stop and report the missing access, workload, or artifact rather than guessing.

3. **Choose the investigation path.**
   - For a slow query, begin with `EXPLAIN`; compare estimated rows, access paths, joins, sorts, and aggregates to the known query and parameters. Use `EXPLAIN ANALYZE` only when execution is safe and representative. It executes the statement: for a write, use an approved disposable environment or an explicit transaction that is rolled back after collecting evidence.
   - For a lock or stall, inspect active sessions, wait events, transaction age, blockers, and the lock modes involved before acting. Identify the owning application path; a blocked session is not proof that it is the root cause.
   - For excess write cost, table growth, vacuum pressure, stale estimates, or I/O, inspect table and index activity, dead tuples, vacuum/analyze history, and the workload that produces dead versions. Do not label ordinary MVCC churn as bloat without evidence.
   - For a failed transaction, preserve the SQLSTATE, error text, isolation level, retry behavior, and concurrent operation. Reproduce with the smallest concurrent case that distinguishes the candidate cause.

4. **Interpret evidence before proposing a fix.** Rank a small set of falsifiable causes. For plans, distinguish a poor estimate or stale statistics from a query-shape, data-distribution, memory, I/O, or concurrency problem. A sequential scan, nested loop, or sort is not inherently wrong; compare its actual work and elapsed time to the completion condition. Change one material variable per probe and retain before/after plans or measurements. If a representative workload is unavailable, limit the result to a diagnosis hypothesis and request the smallest safe sample needed.

5. **Select the narrowest PostgreSQL-specific remedy.**
   - **Query, index, or statistics:** simplify the observed query only if semantics remain unchanged. Add or alter an index only for a demonstrated filter, join, ordering, uniqueness, or access pattern and account for write and storage cost. Start with the conventional B-tree unless the observed operator and data type justify Hash, GiST, SP-GiST, GIN, BRIN, an expression index, or a partial index. Verify that expression and partial-index predicates match the real query. Refresh statistics or adjust statistics targets only when evidence indicates estimates need it; remeasure after `ANALYZE` rather than assuming it fixes the plan.
   - **Locking, MVCC, or isolation:** shorten transactions, avoid holding transactions open across user or network work, and make lock order consistent where the application controls it. Set bounded, scoped timeouts only when the caller can handle the resulting error. PostgreSQL defaults to Read Committed; do not raise isolation merely to hide a race. When Repeatable Read or Serializable is required, make the application retry the *whole* transaction on serialization failure, with an explicit bounded retry policy and an idempotency review.
   - **Maintenance:** let autovacuum handle routine cleanup unless observed workload, lag, or wraparound risk shows that tuning or a manual operation is needed. Avoid routine `VACUUM FULL`: it requires an ACCESS EXCLUSIVE lock and is a rewrite decision, not normal maintenance. Treat a backup as incomplete until a restore test meets the recovery requirement.
   - **Partitioning:** partition only when measured pruning, retention, maintenance, or data-lifecycle needs outweigh routing, constraint, index, and operational complexity. Define the key, bounds, default/out-of-range behavior, query pruning evidence, retention procedure, and rollback before creating partitions. Do not partition merely because a table is large.
   - **Advanced features:** use extensions, materialized views, logical replication, row-level security, generated columns, full-text search, or other PostgreSQL features only after verifying server version, provider support, privileges, failure modes, ownership, monitoring, backup/restore impact, and an operational exit path. Prefer an existing supported capability over introducing a new extension or background process.

6. **Plan the operational change.** Make the change additive and reversible where feasible. Test it against representative data and concurrent load in an approved non-production environment first. For a production index build that must not block ordinary writes, prefer `CREATE INDEX CONCURRENTLY` when its restrictions fit the deployment: it cannot run inside a transaction block, takes longer, and a failure can leave an INVALID index. Verify validity afterward; investigate and explicitly drop or rebuild an invalid index rather than treating the command's return as success. Schedule or reject changes that require disruptive locks, data rewrites, restarts, or replication changes until the owner accepts the impact.

7. **Verify the intended outcome and guardrails.** Re-run the same representative query, transaction, or workload after the single change. Compare plan shape, estimated versus actual rows, elapsed time, reads/writes, lock waits, error rate, and write overhead as applicable. Confirm semantic results with focused application or database tests; use `efficient-testing` when a changed application contract needs regression coverage. For operational work, also verify connection health, replication or backup signals that the change can affect, and the absence of unexpected invalid indexes, lock waits, or error spikes during an agreed observation window.

8. **Handle failure without improvising.** Stop or roll back when a guardrail breaches, an unexpected lock appears, a plan regresses, the result changes, or a prerequisite is unverified. Do not disable safety checks, force a plan, kill sessions, drop an index, or run a table rewrite as a shortcut without owner approval and impact evidence. Preserve the command, timestamps, error, plan, and rollback result; classify whether the cause is query semantics, application concurrency, database state, infrastructure, or unavailable access before choosing one new probe.

## Completion record

Report only evidence obtained:

- PostgreSQL version/topology assumptions, environment, authorization, and protected data boundaries;
- symptom, representative workload or query parameters, baseline, and completion condition;
- inspected plans, statistics, locks, or maintenance signals and the conclusion each supports;
- exact change, expected write/storage/locking impact, rollback procedure, and whether production execution occurred;
- before/after measurements and semantic verification, including observation-window limits;
- skipped or blocked checks, unknown extension/version/support facts, and remaining operational risks.

Stop when the measured completion condition and relevant safety guardrails are met, or when the missing evidence prevents a safe conclusion. Do not add indexes, partitions, configuration tuning, extensions, or maintenance work for hypothetical future scale.
