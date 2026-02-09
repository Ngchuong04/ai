# Refinement commands

Promote and consolidate staged skills into production-ready patterns.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [promote-skill](promote-skill.md) | Move a skill from staging to active | `/promote-skill <name> [category]` |
| [refine-staged](refine-staged.md) | Process and consolidate all staged content | `/refine-staged` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/refinement
cp ~/.ai-skills/commands/refinement/*.md .cursor/commands/refinement/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/refinement
cp ~/.ai-skills/commands/refinement/*.md ~/.cursor/commands/refinement/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/refinement
cp ~/.ai-skills/commands/refinement/*.md .claude/commands/refinement/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/refinement
cp ~/.ai-skills/commands/refinement/*.md ~/.claude/commands/refinement/
```

---

Part of the [Commands](../) directory.
