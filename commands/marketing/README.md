# Marketing commands

Conversion optimization and copywriting workflows.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [cro-audit](cro-audit.md) | Conversion rate optimization audit with scoring and recommendations | `/cro-audit [page-file-or-url] [--type landing\|signup\|pricing\|onboarding]` |
| [write-copy](write-copy.md) | Marketing copy with persona targeting and psychology frameworks | `/write-copy [page-type] [--persona <persona>] [--tone <tone>]` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/marketing
cp ~/.ai-skills/commands/marketing/*.md .cursor/commands/marketing/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/marketing
cp ~/.ai-skills/commands/marketing/*.md ~/.cursor/commands/marketing/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/marketing
cp ~/.ai-skills/commands/marketing/*.md .claude/commands/marketing/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/marketing
cp ~/.ai-skills/commands/marketing/*.md ~/.claude/commands/marketing/
```

---

Part of the [Commands](../) directory.
