# Zero-Downtime Migration Checklist

## Before Writing the Migration

- [ ] Identify all application versions that may run during rollout.
- [ ] Decide whether the change is backward-compatible, forward-compatible, or destructive.
- [ ] Estimate table size and write traffic.
- [ ] Identify locks, rewrite risks, and transaction boundaries.
- [ ] Decide whether online/concurrent database features are required.

## Migration Design

- [ ] Schema and data changes are separate.
- [ ] Destructive operations are delayed until code no longer depends on old shape.
- [ ] Backfill is idempotent and resumable.
- [ ] Long-running work has bounded batches and progress logging.
- [ ] Rollback is either a true down migration or a documented forward-fix migration.

## Production Rollout

1. Apply expand migration.
2. Deploy compatibility code.
3. Run backfill with observability.
4. Verify consistency.
5. Deploy code that uses the new shape.
6. After a safety window, apply contract migration.

## Verification Ideas

```sql
-- Remaining rows needing backfill.
SELECT count(*) FROM users WHERE normalized_email IS NULL;

-- Index validity after concurrent creation.
SELECT indexrelid::regclass, indisvalid, indisready
FROM pg_index
WHERE indexrelid = 'idx_users_email'::regclass;
```

Record expected runtime, who is watching, and the abort criteria before running production migrations.
