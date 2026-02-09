# Bootstrap commands

Project and infrastructure scaffolding from scratch. Use when starting a new project or adding documentation/design-system structure to an existing one.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [bootstrap-design-system](bootstrap-design-system.md) | Initialize design system structure | `/bootstrap-design-system` |
| [bootstrap-docs](bootstrap-docs.md) | Add documentation structure to existing project | `/bootstrap-docs` |
| [bootstrap-project](bootstrap-project.md) | Scaffold a new project with opinionated setup | `/bootstrap-project` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wustep/ai-agent-toolkit ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/bootstrap
cp ~/.ai-skills/commands/bootstrap/*.md .cursor/commands/bootstrap/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/bootstrap
cp ~/.ai-skills/commands/bootstrap/*.md ~/.cursor/commands/bootstrap/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/bootstrap
cp ~/.ai-skills/commands/bootstrap/*.md .claude/commands/bootstrap/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/bootstrap
cp ~/.ai-skills/commands/bootstrap/*.md ~/.claude/commands/bootstrap/
```

---

Part of the [Commands](../) directory.
