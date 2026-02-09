# Extraction commands

Mine reusable patterns from existing projects into staging for later refinement.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [extract-patterns](extract-patterns.md) | Extract reusable patterns from the current project into staging | `/extract-patterns [focus]` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/extraction
cp ~/.ai-skills/commands/extraction/*.md .cursor/commands/extraction/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/extraction
cp ~/.ai-skills/commands/extraction/*.md ~/.cursor/commands/extraction/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/extraction
cp ~/.ai-skills/commands/extraction/*.md .claude/commands/extraction/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/extraction
cp ~/.ai-skills/commands/extraction/*.md ~/.claude/commands/extraction/
```

---

Part of the [Commands](../) directory.
