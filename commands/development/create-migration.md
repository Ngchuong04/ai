---
name: create-migration
model: standard
description: Create a database migration with safety checks, rollback plan, and verification queries
usage: /create-migration <migration-name> [--type schema|data|index]
---

# /create-migration

Create a database migration with automatic safety analysis, expand-contract handling for destructive changes, rollback generation, and verification queries.

## Usage

```
/create-migration <migration-name> [--type schema|data|index]
```

**Arguments:**
- `migration-name` — Descriptive name for the migration (e.g., `add-user-email-verified`, `rename-orders-status`)
- `--type` — Migration category (default: auto-detected from name). Accepts `schema`, `data`, `index`
  - `schema` — DDL changes: add/alter/drop tables, columns, constraints
  - `data` — DML changes: backfill, transform, seed data
  - `index` — Index creation, removal, or rebuild

## Examples

```
/create-migration add-user-email-verified
/create-migration rename-orders-status-column --type schema
/create-migration backfill-user-display-names --type data
/create-migration add-index-orders-created-at --type index
/create-migration drop-legacy-sessions-table --type schema
/create-migration migrate-roles-to-permissions --type data
```

## When to Use

- Adding or modifying database tables, columns, or constraints
- Creating or dropping indexes for query performance
- Running data backfills or transformations
- Renaming or removing columns safely with zero downtime
- Any change to database schema that needs to be versioned and reversible

## What It Does

1. **Detects** the database engine and migration tool in use
2. **Analyzes** the requested change for safety (additive vs. destructive)
3. **Generates** the migration file following the tool's conventions
4. **Creates** expand-contract steps for destructive changes
5. **Generates** a rollback migration
6. **Adds** verification queries to confirm correctness

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Detect Database and Migration Tool

Use `Glob` and `Grep` to identify the database engine and migration tool. Check in order and stop at the first match:

| Tool | Detection Signal | Migration Directory |
|------|-----------------|-------------------|
| **Prisma** | `prisma/schema.prisma` or `prisma` in `package.json` | `prisma/migrations/` |
| **Drizzle** | `drizzle.config.ts` or `drizzle-kit` in `package.json` | `drizzle/` or `migrations/` |
| **Knex** | `knexfile.js` or `knex` in `package.json` | `migrations/` |
| **TypeORM** | `ormconfig.ts` or `typeorm` in `package.json` | `src/migrations/` |
| **Alembic** | `alembic.ini` or `alembic/` directory | `alembic/versions/` |
| **Django** | `manage.py` and `DATABASES` in settings | `<app>/migrations/` |
| **golang-migrate** | `migrate` in `go.mod` or `migrations/` with `.up.sql`/`.down.sql` files | `migrations/` |
| **Diesel** | `diesel.toml` or `diesel` in `Cargo.toml` | `migrations/` |
| **Raw SQL** | `migrations/` directory with numbered `.sql` files | `migrations/` |

Also detect the database engine:

| Engine | Detection Signal |
|--------|-----------------|
| **PostgreSQL** | `postgres` or `postgresql` in connection strings, Prisma `provider = "postgresql"` |
| **MySQL** | `mysql` in connection strings, Prisma `provider = "mysql"` |
| **SQLite** | `sqlite` in connection strings, `.db` or `.sqlite` files |
| **MongoDB** | `mongodb` in connection strings, Mongoose imports |

If no migration tool is detected, ask the user. Suggest Prisma for TypeScript projects, Alembic for Python, golang-migrate for Go.

### Phase 2: Analyze Change Safety

Parse the migration name and type to classify the change:

| Category | Examples | Risk Level | Strategy |
|----------|----------|-----------|----------|
| **Additive** | Add table, add nullable column, add index | Safe | Direct migration, no downtime |
| **Additive with default** | Add column with `NOT NULL` and default | Safe (small tables) / Risky (large tables) | Direct for small tables; batched `ALTER` for large |
| **Rename** | Rename column, rename table | Destructive | Expand-contract pattern required |
| **Drop** | Drop column, drop table, drop constraint | Destructive | Expand-contract pattern required |
| **Type change** | Change column type, alter constraint | Destructive | Expand-contract pattern required |
| **Data migration** | Backfill, transform, merge | Varies | Batched execution with progress tracking |
| **Index** | Create index | Safe (with `CONCURRENTLY`) | Use `CREATE INDEX CONCURRENTLY` on PostgreSQL |

Print the safety analysis before generating files:

```
Migration Analysis
==================

  Name:     rename-orders-status-column
  Type:     schema (destructive)
  Risk:     HIGH — column rename requires expand-contract
  Strategy: 5-step expand-contract migration

  Step 1: Add new column 'order_status' (this migration)
  Step 2: Deploy dual-write code
  Step 3: Backfill existing rows
  Step 4: Switch reads to new column
  Step 5: Drop old column 'status' (separate migration)
```

### Phase 3: Generate Migration File

Create the migration file using the detected tool's conventions.

Use `Glob` to find existing migration files and `Read` one to match the naming pattern, timestamp format, and code style.

For each tool, follow its conventions:

| Tool | File Naming | Format |
|------|-------------|--------|
| **Prisma** | Auto-generated by `prisma migrate dev` | Modify `schema.prisma`, then run CLI |
| **Drizzle** | `NNNN_migration_name.ts` | TypeScript with Drizzle schema changes |
| **Knex** | `YYYYMMDDHHMMSS_migration_name.ts` | `exports.up` and `exports.down` functions |
| **Alembic** | `<revision>_migration_name.py` | `upgrade()` and `downgrade()` functions |
| **golang-migrate** | `NNNNNN_migration_name.up.sql` / `.down.sql` | Raw SQL in paired files |
| **Django** | Auto-generated by `manage.py makemigrations` | Modify models, then run CLI |
| **Raw SQL** | `NNNN_migration_name.up.sql` / `.down.sql` | Raw SQL in paired files |

Include comments in the migration file explaining:
- What the migration does
- Why it's safe or what precautions are needed
- Any manual steps required (for expand-contract)

### Phase 4: Handle Destructive Changes

For destructive changes, generate the full expand-contract sequence as separate migration files:

**Step 1 — Expand (safe to deploy immediately):**
```sql
-- Add new column alongside old one
ALTER TABLE orders ADD COLUMN order_status varchar(50);
```

**Step 2 — Dual-write (application code change, not a migration):**
Generate a code comment or TODO explaining:
```
-- TODO: Update application code to write to BOTH 'status' AND 'order_status'
-- Deploy this code change before proceeding to Step 3
```

**Step 3 — Backfill (data migration):**
```sql
-- Backfill new column from old column
-- Run in batches for large tables
UPDATE orders SET order_status = status WHERE order_status IS NULL LIMIT 10000;
```

**Step 4 — Switch reads (application code change):**
```
-- TODO: Update application code to read from 'order_status' instead of 'status'
-- Update all queries, indexes, and constraints to reference the new column
-- Deploy this code change before proceeding to Step 5
```

**Step 5 — Contract (point of no return, separate migration):**
```sql
-- Drop old column (only after confirming no code references it)
ALTER TABLE orders DROP COLUMN status;
```

Warn clearly which step is the point of no return.

### Phase 5: Generate Rollback Migration

Create a rollback migration that reverses the change:

- For additive changes: `DROP TABLE`, `DROP COLUMN`, `DROP INDEX`
- For destructive changes: reverse the expand step only (cannot rollback after contract)
- For data migrations: generate a reverse transform or note if irreversible

If the migration is irreversible (e.g., data transformation that loses information), clearly document this:

```sql
-- IRREVERSIBLE MIGRATION
-- This data transformation cannot be automatically rolled back.
-- To reverse: restore from backup taken before migration.
```

### Phase 6: Add Verification Queries

Generate SQL queries that verify the migration ran correctly:

```sql
-- Verification Queries
-- ====================

-- 1. Confirm column exists
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'orders' AND column_name = 'order_status';

-- 2. Confirm no NULL values (after backfill)
SELECT COUNT(*) AS null_count
FROM orders
WHERE order_status IS NULL;

-- 3. Confirm row count unchanged
SELECT COUNT(*) AS total_rows FROM orders;

-- 4. Confirm constraint is valid
SELECT conname, convalidated
FROM pg_constraint
WHERE conrelid = 'orders'::regclass;

-- 5. Spot-check data integrity
SELECT id, status, order_status
FROM orders
LIMIT 10;
```

Save verification queries in a separate file or as comments at the end of the migration.

### Phase 7: Report

Print a summary:

```
Created Files
=============

  migrations/20250206120000_add_order_status.up.sql     (expand: add new column)
  migrations/20250206120000_add_order_status.down.sql   (rollback: drop new column)
  migrations/20250206120001_backfill_order_status.up.sql (backfill data)
  migrations/20250206120001_backfill_order_status.down.sql (rollback: clear backfill)
  migrations/verification/verify_order_status.sql        (verification queries)

Safety Summary
==============

  Risk level:  HIGH (destructive change)
  Strategy:    Expand-contract (5 steps)
  Current:     Steps 1 + 3 generated (expand + backfill)
  Remaining:   Steps 2, 4 require application code changes
  Point of no return: Step 5 (drop old column) — generate separately when ready

Next Steps
==========

  1. Review the generated migration files
  2. Run: make migrate (or tool-specific command)
  3. Run verification queries to confirm correctness
  4. Update application code for dual-write (Step 2)
  5. Deploy, then generate Step 5 when confident
```

## NEVER Do

| Rule | Reason |
|------|--------|
| Never run destructive migrations without expand-contract | Column renames and drops cause downtime if application code still references the old name |
| Never skip rollback generation | Every migration must be reversible or explicitly documented as irreversible |
| Never use `ALTER TABLE` on large tables without batching | Locks the table for the duration; use batched updates or online DDL tools |
| Never create indexes without `CONCURRENTLY` on PostgreSQL | Blocks writes on the table; `CREATE INDEX CONCURRENTLY` avoids this |
| Never assume migration tools handle rollback automatically | Always verify the down migration works by reviewing the generated SQL |
| Never run data migrations without a row count check | Verify row counts before and after to catch silent data loss |
| Never combine schema and data changes in one migration | Separate DDL and DML for safer rollback and clearer history |

## Error Handling

| Situation | Action |
|-----------|--------|
| Migration tool not detected | Ask the user; suggest tool based on stack |
| Database engine unclear | Check connection strings in `.env`, config files, or `docker-compose.yml` |
| Migration name conflicts with existing | Append a timestamp or increment the sequence number |
| Large table detected for schema change | Warn about potential lock time and suggest online DDL or batched approach |
| Irreversible data transformation | Clearly document irreversibility and recommend a backup before running |
| Multiple databases in project | Ask which database the migration targets |

## Output

- **Migration file(s)** in the project's migration directory following existing conventions
- **Rollback file(s)** reversing the migration changes
- **Verification queries** to confirm migration correctness
- **Safety analysis** with risk level and deployment strategy

## Related

- **Database best practices:** `supabase-postgres-best-practices` skill (for PostgreSQL optimization)
- **API routes:** `/create-api-route` (when the migration supports a new endpoint)
- **Service scaffolding:** `/create-service` (when building the service that needs the migration)
- **Feature workflow:** `/new-feature` (when the migration is part of a larger feature)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
