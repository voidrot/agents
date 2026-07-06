# PostgreSQL Safe Migration Recipes

Use these recipes as starting points, then verify against the target PostgreSQL version and migration tool transaction behavior.

## Adding Columns

Prefer nullable columns or constant defaults. For existing large tables, avoid patterns that require scanning every row while holding restrictive locks.

```sql
-- Nullable: metadata-only for ordinary cases.
ALTER TABLE users ADD COLUMN avatar_url text;

-- Constant default: safe on modern PostgreSQL, but still verify lock duration.
ALTER TABLE users ADD COLUMN is_active boolean NOT NULL DEFAULT true;
```

For a required value that must be computed per row:

1. Add the column nullable.
2. Deploy code that writes both old and new shape.
3. Backfill in batches.
4. Add `NOT NULL` only after validation.

```sql
ALTER TABLE users ADD COLUMN normalized_email text;

-- Backfill in repeated small batches from application code or a migration runner.
UPDATE users
SET normalized_email = lower(email)
WHERE id IN (
  SELECT id
  FROM users
  WHERE normalized_email IS NULL
  ORDER BY id
  LIMIT 10000
  FOR UPDATE SKIP LOCKED
);

ALTER TABLE users ALTER COLUMN normalized_email SET NOT NULL;
```

## Indexes Without Blocking Writes

Use concurrent index operations on existing large tables.

```sql
CREATE INDEX CONCURRENTLY idx_users_email ON users (email);
DROP INDEX CONCURRENTLY IF EXISTS idx_users_email;
```

Important PostgreSQL constraint: concurrent index operations cannot run inside a transaction block. Configure the migration tool accordingly or run that migration outside the default transaction wrapper.

## Rename/Replace With Expand-Contract

Direct renames are fast at the database level but unsafe for rolling deploys because old and new application versions disagree on the column name.

```text
Phase 1: EXPAND
  - Add new nullable column/table/constraint.
  - Deploy app that writes both old and new shape.
  - Backfill old rows.

Phase 2: MIGRATE READS
  - Deploy app that reads the new shape and still writes both if needed.
  - Verify old/new consistency.

Phase 3: CONTRACT
  - Deploy app that stops referencing old shape.
  - Drop old column/table/index in a later migration.
```

## Removing Columns Safely

1. Remove all application reads/writes.
2. Deploy and observe.
3. Drop indexes/constraints referencing the column.
4. Drop the column in a separate migration.

For frameworks with model state (for example Django), separate application/model state changes from physical database drops when doing rolling deploys.

## Large Data Backfills

- Run in small batches with explicit progress logging.
- Keep transactions short.
- Prefer primary-key windows or `FOR UPDATE SKIP LOCKED` for worker-safe batches.
- Make the operation idempotent so it can be resumed.
- Avoid long table-wide updates inside a single migration transaction.

## Common Anti-Patterns

| Anti-pattern | Risk | Safer alternative |
| --- | --- | --- |
| Edit a deployed migration | Environment drift | Create a new migration |
| Schema + large data update together | Long locks, hard rollback | Split schema and data phases |
| `CREATE INDEX` on a hot large table | Blocks writes | `CREATE INDEX CONCURRENTLY` |
| Rename/drop before code deploy | Runtime errors | Expand-contract |
| Unbounded backfill | Lock and replication pressure | Batches with resume marker |
