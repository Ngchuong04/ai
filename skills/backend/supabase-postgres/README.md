# Supabase Postgres Best Practices

Comprehensive Postgres performance guide — covering indexing, connection management, RLS security, schema design, locking, data access patterns, and monitoring. Organized by impact priority with incorrect vs. correct SQL examples.

## What's Inside

- Query Performance — index WHERE and JOIN columns, index types (B-tree, GIN, BRIN, Hash), partial indexes
- Connection Management — connection pooling (PgBouncer), transaction vs session mode, connection limits
- Security & RLS — Row-Level Security fundamentals, RLS policy optimization with `(select ...)` wrapper
- Schema Design — data types (bigint, text, timestamptz, numeric), primary key strategies, FK indexes
- Concurrency & Locking — deadlock prevention, consistent lock ordering, SKIP LOCKED
- Data Access Patterns — N+1 elimination, cursor-based pagination, batch inserts, upserts
- Monitoring & Diagnostics — EXPLAIN ANALYZE, pg_stat_statements, vacuum/analyze
- Quick Reference table mapping problems to solutions
- Detailed reference files for 25+ specific rules

## When to Use

- Writing SQL queries or designing schemas
- Implementing or reviewing indexes
- Debugging slow queries or connection issues
- Configuring connection pooling
- Implementing Row-Level Security (RLS)
- Reviewing database performance

## Installation

```bash
npx skills add supabase-postgres
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/backend/supabase-postgres .cursor/skills/supabase-postgres
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/backend/supabase-postgres ~/.cursor/skills/supabase-postgres
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/backend/supabase-postgres .claude/skills/supabase-postgres
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/backend/supabase-postgres ~/.claude/skills/supabase-postgres
```

## Related Skills

- `postgres-job-queue` — PostgreSQL-based job queue using SKIP LOCKED
- `service-layer-architecture` — API layer patterns for database access

---

Part of the [Backend](..) skill category.
