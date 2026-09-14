---
name: efficient-database-design
description: Design or review a portable relational database schema and compatible migration path; use when modeling entities, relationships, constraints, normalization, logical access paths, or schema evolution, before engine-specific query tuning or operations work.
---

# Efficient Database Design

Use this skill to make a relational model preserve its business rules and support its known reads and writes. Produce a reviewable logical schema and migration plan, not vendor-specific SQL, index syntax, query-plan analysis, replication, backup configuration, or database-server tuning. For PostgreSQL-specific implementation or measurement, use `efficient-postgres`.

## Workflow

1. **Establish the change boundary.** Read the request, existing schema and migrations, application writes, representative reads, tests, and data-retention or privacy rules. List the decision to make, consumers affected, deployment order, existing data to preserve, and unknowns. Do not infer a workload, ownership boundary, or engine capability that the evidence does not establish; mark it as an assumption and request a decision when it changes correctness or compatibility.

2. **Write the data contract before tables.** Name each business entity, its stable identity, required and optional facts, lifecycle states, and authoritative owner. List each invariant in testable language, including uniqueness, valid state combinations, cardinality, ownership, retention, and whether historical facts may change. Distinguish:
   - row-local rules, such as a permitted status or nonnegative quantity;
   - relationship rules, such as every line item belonging to an order; and
   - cross-row or temporal rules, such as no overlapping assignment or a quota across active rows.

   Do not claim a row-local `CHECK` can enforce a cross-row or cross-table rule. Choose a database constraint, a serialized transaction/application rule, or a changed model that can actually enforce it, and state the concurrency assumption for any rule outside a constraint.

3. **Model relationships explicitly.** Give each entity a table when it has independent identity, lifecycle, or attributes. Select cardinality deliberately:
   - Put a foreign key on the many side for one-to-many.
   - Use a separate association table for many-to-many, especially when the relationship has attributes, history, ordering, or lifecycle.
   - Use a foreign key plus a uniqueness constraint for one-to-one only when both sides are independently meaningful; otherwise combine the facts.
   - Represent optionality with nullable relationship columns only when absence has a defined meaning.

   Do not store a repeating collection, delimited identifiers, or a polymorphic reference in one column merely to avoid a table. If several target types are intentional, model the alternatives so invalid target combinations cannot be silently created.

4. **Choose keys and constraints from the contract.** Give every table a primary key whose identity is stable for its expected lifetime. Preserve meaningful alternate identities with `UNIQUE`, including composite uniqueness where identity is scoped by a parent. Add `NOT NULL` for required attributes, foreign keys for required relationships, and `CHECK` constraints for row-local domains and combinations. Define delete and update behavior for every foreign key:
   - use `CASCADE` only for components that cannot exist independently;
   - default to preventing deletion of independently meaningful or auditable records;
   - use `SET NULL` or `SET DEFAULT` only when the resulting row remains valid and its meaning is explicit.

   Keep identifiers and timestamps separate from mutable display names and business facts. Do not make a natural key primary solely because it is currently convenient if it can be corrected, reused, or renamed.

5. **Normalize by default, then justify every duplicate.** Start with one fact stored in one authoritative place and tables whose non-key attributes describe that table's key. Split facts that have independent owners, lifecycles, permissions, retention, or update rates. Denormalize only for a named measured read or operational requirement after recording the source of truth, refresh/write path, consistency expectation, repair method, and verification. Do not add summary tables, copied fields, generic entity-attribute-value structures, or speculative extension points for imagined future needs.

6. **Derive logical access paths from observed operations.** For each important read, write its filters, joins, ordering, expected result size, frequency, and write cost. Ensure relationship lookups and parent delete/update paths have an intentional access path; index a foreign-key column when that workload needs it, not by blanket rule. Prefer a small number of access paths that serve named queries. Record the query pattern each one supports and its added write/storage/maintenance cost. Do not add indexes based on column names, assumptions about selectivity, or unmeasured future scale. Engine-specific index types and plan inspection belong in `efficient-postgres` or the relevant engine guidance.

7. **Design an expand-contract migration.** Inspect existing migration conventions and all readers and writers, including jobs, integrations, reports, and old application versions that can overlap deployment. Version migrations in dependency order. Prefer these stages when compatibility matters:
   1. add new tables, nullable columns, or compatible constraints;
   2. deploy code that writes both representations or tolerates either;
   3. backfill in bounded, observable batches with a restart/rollback decision;
   4. verify completeness and equivalence against explicit invariants;
   5. make new fields required or switch reads only after all writers are compatible;
   6. remove the old representation in a later migration after the compatibility window.

   Avoid combining an irreversible data rewrite, application behavior change, and destructive drop without a tested recovery plan. Make migrations reversible where feasible; when reversal would lose data, state that clearly, retain a restorable backup or export as required by the environment, and require approval before execution. Do not assume DDL locking, transactional DDL, online index creation, or backfill behavior is portable.

8. **Specify maintenance ownership.** State who owns schema changes, migration execution, data correction, retention/deletion, integrity monitoring, and recovery testing. Define how orphaned, duplicated, stale, or denormalized data will be detected and repaired without bypassing constraints. Retain an audit trail when the domain requires reconstructing who changed a material fact and when. Keep maintenance proportional: do not introduce a scheduler, ledger, or reconciliation service without a demonstrated invariant or operational need.

9. **Review the design and verify the highest-risk claims.** Present the proposed tables, columns, keys, constraints, relationship actions, access paths, assumptions, migration stages, and unresolved decisions. Trace every invariant to one enforcement point and every important operation to an access path. Test representative valid and invalid writes against a disposable database using the target migration mechanism where available. Test upgrade from a realistic pre-change schema and data sample, then verify row counts, required fields, relationship integrity, uniqueness, and preserved historical meaning. Use focused application tests for behavior at the data boundary; use `adr-writing` when a consequential, long-lived choice or its trade-offs need a durable decision record.

## Safe defaults and failure handling

- Prefer the smallest normalized schema that enforces the known contract. A table, foreign key, uniqueness constraint, and explicit lifecycle are usually safer than a generic abstraction.
- Reject a design when a required invariant has no enforceable owner, a deletion action destroys independently meaningful data, or the proposed migration cannot preserve required existing data. Resolve the contract before coding around the gap.
- Stop a migration or backfill on constraint violations, unexpected row counts, failed equivalence checks, unacceptable lock/availability impact, or an unrecoverable partial state. Preserve the evidence, restore or roll forward only through the documented recovery path, and diagnose the data rule or compatibility assumption before retrying.
- If a performance concern lacks a representative operation and measured baseline, retain the simple design and record what measurement would justify an access-path or denormalization change. Do not present a hypothetical optimization as a requirement.
- If the target engine cannot enforce a chosen portable constraint or migration step, name the limitation and select an explicit alternative with equivalent enforcement or revise the requirement; never silently weaken integrity.

## Completion evidence

Finish with a concise design record containing:

- the workload, data contract, assumptions, and excluded engine-specific work;
- a schema inventory with primary keys, alternate keys, nullability, foreign keys, delete/update actions, and each invariant's enforcement point;
- named logical access paths tied to representative operations and their write cost;
- each intentional denormalization and its source of truth, synchronization, repair, and verification;
- an ordered compatible migration, backfill validation, rollback or recovery limit, and removal criteria;
- focused validation results, skipped checks, unresolved decisions, and maintenance owner.

Do not call the design complete until every required invariant and existing-data transition has an explicit, reviewable answer.
