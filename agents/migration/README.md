# Migration Agent

Autonomous workflow for planning and executing multi-step migrations with rollback safety, zero-downtime strategies, and verification at every stage. Handles database schema, framework/library/language upgrades, architecture migrations, data format changes, and API version migrations.

## Workflow Phases

- **Phase 1: Assessment** — Classify migration type, map dependencies and blast radius, assess risk
- **Phase 2: Planning** — Step-by-step migration plan with rollback points and risk mitigation
- **Phase 3: Preparation** — Backups, feature flags, compatibility layers, shadow systems
- **Phase 4: Execution** — Execute incrementally with verification checkpoints
- **Phase 5: Verification** — Testing, data integrity checks, performance comparison

## Skills Used

- `clean-code` — Clean code principles for migration code
- `architecture-patterns` — Architecture patterns for structural migrations
- `database-migrations` — Database migration patterns and strategies
- Command: `migrate-deps` — Single-dependency upgrade with breaking change analysis

## Trigger Phrases

- "migrate the database schema"
- "upgrade to [framework] v[version]"
- "create a migration plan for [system]"
- "migrate from monolith to microservices"
- "zero-downtime migration for [component]"
- "plan rollback strategy for [migration]"

## Installation

### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/migration .cursor/agents/migration
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/migration ~/.cursor/agents/migration
```

### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/migration .claude/agents/migration
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/migration ~/.claude/agents/migration
```

For best results, also install the skills this agent references (see Skills Used above). Ensure git is clean and tests pass before starting a migration.

---

Part of the [Agents](../) directory.
