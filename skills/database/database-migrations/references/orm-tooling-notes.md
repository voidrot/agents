# Migration Tooling Notes

Inspect generated SQL and confirm transaction behavior before production. The official docs for each tool are the source of truth for exact command flags.

## Prisma

```bash
npx prisma migrate dev --name add_user_avatar
npx prisma migrate deploy
npx prisma generate
```

- Use `migrate dev --create-only` when you need to hand-edit SQL.
- Review generated SQL for destructive changes before applying.
- PostgreSQL concurrent indexes usually require manual SQL and special handling because they cannot run inside a transaction block.
- Do not use reset-style commands against shared or production databases.

## Drizzle

```bash
npx drizzle-kit generate
npx drizzle-kit migrate
```

- Treat `push` as development-only unless your project explicitly accepts schema sync without reviewed migration files.
- Keep generated migrations in version control.
- Review generated SQL when adding constraints, defaults, or indexes to large tables.

## Kysely

```typescript
import { type Kysely, sql } from 'kysely'

export async function up(db: Kysely<any>): Promise<void> {
  await db.schema
    .createTable('user_profile')
    .addColumn('id', 'serial', (col) => col.primaryKey())
    .addColumn('email', 'varchar(255)', (col) => col.notNull().unique())
    .execute()

  await sql`CREATE INDEX CONCURRENTLY idx_user_profile_email ON user_profile (email)`.execute(db)
}

export async function down(db: Kysely<any>): Promise<void> {
  await db.schema.dropTable('user_profile').execute()
}
```

- Use `Kysely<any>` in migrations so historical migrations do not depend on the current typed schema.
- Handle migration runner errors explicitly and fail the process on migration failure.
- Confirm whether your runner wraps migrations in transactions before using PostgreSQL concurrent operations.

## Django

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
python manage.py makemigrations --empty app_name -n backfill_display_names
```

- Use empty migrations for custom data backfills.
- Use `SeparateDatabaseAndState` when model state and physical database state must change in different deploys.
- Keep data migrations idempotent and batch large updates rather than loading every row at once.

## TypeORM

- Generate migrations only as a starting point; review SQL before committing.
- Keep `up` and `down` explicit.
- Avoid schema sync in production.
- For PostgreSQL concurrent index operations, disable per-migration transaction wrapping where supported or run the operation separately.

## golang-migrate

```bash
migrate create -ext sql -dir migrations -seq add_user_avatar
migrate -path migrations -database "$DATABASE_URL" up
migrate -path migrations -database "$DATABASE_URL" down 1
```

- Keep `.up.sql` and `.down.sql` pairs reviewable.
- Use `force` only after manually verifying database state; it changes recorded version state and can hide partial application.
- Split non-transactional PostgreSQL operations into their own migration files when needed.
