# Documentation commands

Auto-generate documentation from code comments and structure.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [generate-docs](generate-docs.md) | Auto-generate documentation from code comments and structure | `/generate-docs <target> [--format markdown\|jsdoc\|docstring] [--output <path>] [--update]` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/documentation
cp ~/.ai-skills/commands/documentation/*.md .cursor/commands/documentation/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/documentation
cp ~/.ai-skills/commands/documentation/*.md ~/.cursor/commands/documentation/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/documentation
cp ~/.ai-skills/commands/documentation/*.md .claude/commands/documentation/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/documentation
cp ~/.ai-skills/commands/documentation/*.md ~/.claude/commands/documentation/
```

---

Part of the [Commands](../) directory.
