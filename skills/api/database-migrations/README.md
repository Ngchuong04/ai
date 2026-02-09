# Database Migration Patterns

Safe, zero-downtime database migration strategies — schema evolution, rollback planning, data migration, tooling, and anti-pattern avoidance for production systems. Use when planning schema changes, writing migrations, or reviewing migration safety.

## What's Inside

- Schema Evolution Strategies — additive-only, expand-contract, parallel change, lazy migration
- Zero-Downtime Patterns — add column, rename column, drop column, change type, add index, split table, change constraint, add enum value
- Migration Tools — Prisma, Knex, Drizzle, Alembic, Django, Flyway, golang-migrate, Atlas
- Rollback Strategies — reversible, forward-only, hybrid approaches
- Data Preservation — soft-delete, snapshot tables, point-in-time recovery, logical backups
- Blue-Green Database pattern
- Data Migration Patterns — backfill strategies, batch processing, dual-write period
- Testing Migrations — production-like data, migration CI pipeline
- Migration Checklist — pre-migration, during, and post-migration steps

## When to Use

- Planning schema changes for production databases
- Writing safe, zero-downtime migrations
- Choosing a migration tool for your stack
- Reviewing migration safety before deployment
- Handling data migrations and backfills on large tables
- Setting up migration CI pipelines

## Installation

```bash
skills add database-migrations
```

### Manual Installation

Copy this directory to your project:

```bash
# Cursor
cp -r ~/.skills/ai/skills/api/database-migrations .cursor/rules/database-migrations

# Claude Code  
cp -r ~/.skills/ai/skills/api/database-migrations .agents/skills/database-migrations
```

## Related Skills

- `api-versioning` — API versioning often accompanies schema migrations
- `api-development` — Database migrations as part of the API development lifecycle

---

Part of the [API](..) skill category.
