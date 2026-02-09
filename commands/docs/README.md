# Docs commands

Create structured documentation artifacts: user personas, Product Requirements Documents, and operations runbooks.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [create-persona](create-persona.md) | Create a user persona document | `/create-persona <name>` |
| [create-prd](create-prd.md) | Create a Product Requirements Document | `/create-prd <name>` |
| [create-runbook](create-runbook.md) | Create an operations runbook | `/create-runbook <name>` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/docs
cp ~/.ai-skills/commands/docs/*.md .cursor/commands/docs/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/docs
cp ~/.ai-skills/commands/docs/*.md ~/.cursor/commands/docs/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/docs
cp ~/.ai-skills/commands/docs/*.md .claude/commands/docs/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/docs
cp ~/.ai-skills/commands/docs/*.md ~/.claude/commands/docs/
```

---

Part of the [Commands](../) directory.
