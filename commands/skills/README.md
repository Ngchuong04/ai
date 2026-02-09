# Skills commands

Create, update, validate, and maintain the skill library.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [archive-skill](archive-skill.md) | Move a deprecated skill to archive | `/archive-skill <name> [category]` |
| [check-overlaps](check-overlaps.md) | Find redundant or overlapping skills | `/check-overlaps [category]` |
| [create-skill](create-skill.md) | Guided skill creation with quality criteria | `/create-skill <name> [category]` |
| [update-skill](update-skill.md) | Update an existing skill with improvements | `/update-skill <path>` |
| [validate-skill](validate-skill.md) | Check a skill against quality criteria | `/validate-skill <path>` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/skills
cp ~/.ai-skills/commands/skills/*.md .cursor/commands/skills/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/skills
cp ~/.ai-skills/commands/skills/*.md ~/.cursor/commands/skills/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/skills
cp ~/.ai-skills/commands/skills/*.md .claude/commands/skills/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/skills
cp ~/.ai-skills/commands/skills/*.md ~/.claude/commands/skills/
```

---

Part of the [Commands](../) directory.
