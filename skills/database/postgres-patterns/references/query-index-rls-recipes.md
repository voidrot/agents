# PostgreSQL Query, Index, and RLS Recipes

## Index Selection

| Query pattern | Typical index | Notes |
| --- | --- | --- |
| `WHERE col = $1` | B-tree on `col` | Default index type fits equality/range for scalar types. |
| `WHERE a = $1 AND b > $2` | Composite B-tree `(a, b)` | Equality columns first, then range/order columns. |
| `WHERE jsonb_col @> ...` | GIN | Match JSON containment/operator workload. |
| Full text search | GIN on `tsvector` | Store generated tsvector when appropriate. |
| Large append-only time ranges | BRIN | Useful when physical order correlates with the column. |

```sql
CREATE INDEX idx_orders_status_created_at ON orders (status, created_at);
CREATE INDEX idx_users_email_active ON users (email) WHERE deleted_at IS NULL;
CREATE INDEX idx_users_email_covering ON users (email) INCLUDE (name, created_at);
```

Validate with the real query plan; unused indexes slow writes and consume storage.

## Data Type Defaults

| Use case | Prefer | Avoid by default |
| --- | --- | --- |
| Time | `timestamptz` | `timestamp` without time zone for user-facing instants |
| Money/exact decimal | `numeric` | `float` |
| Flexible strings | `text` | Artificial `varchar(255)` limits |
| Flags | `boolean` | String/integer flags |
| Internal monotonically generated IDs | `bigint` / identity | Small `int` if growth is unknown |

## RLS Policy Shape

Keep policies simple and test them under representative cardinality. If using helper functions from an auth extension, follow that extension's current optimization guidance.

```sql
CREATE POLICY orders_owner_select ON orders
  FOR SELECT
  USING (user_id = current_setting('app.user_id')::uuid);
```

Add indexes that match policy predicates, because RLS predicates become part of query execution.

## UPSERT

```sql
INSERT INTO settings (user_id, key, value)
VALUES ($1, $2, $3)
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

Make sure the conflict target has a matching unique constraint or unique index.

## Cursor Pagination

```sql
SELECT *
FROM products
WHERE id > $1
ORDER BY id
LIMIT 20;
```

For composite ordering, include every ordering column in the cursor predicate and index.

## Queue Processing With `SKIP LOCKED`

```sql
UPDATE jobs
SET status = 'processing', started_at = now()
WHERE id = (
  SELECT id
  FROM jobs
  WHERE status = 'pending'
  ORDER BY created_at
  LIMIT 1
  FOR UPDATE SKIP LOCKED
)
RETURNING *;
```

Use a recovery process for stuck jobs and an index on `(status, created_at)`.
