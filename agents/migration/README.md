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

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add migration
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/migration .cursor/rules/migration-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/migration .claude/skills/migration-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/migration ~/.claude/skills/migration-agent
```

For best results, also install the skills this agent references (see Skills Used above). Ensure git is clean and tests pass before starting a migration.

---

Part of the [Agents](../) directory.
