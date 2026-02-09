# Commands

48 slash commands — structured workflows invoked in AI chat to automate common development tasks. Each command is a markdown file with usage, examples, implementation steps, and output format.

> **Note:** Commands are not published to [skills.sh](https://skills.sh). Install them by cloning this repo and copying the commands directory into your project.

---

## Command Catalog

| Group | Commands | Description |
|-------|----------|-------------|
| [bootstrap](bootstrap/) | 3 | Project and infrastructure scaffolding from scratch |
| [development](development/) | 31 | Day-to-day coding, debugging, deployment, and workflow |
| [docs](docs/) | 3 | Structured documentation artifacts (personas, PRDs, runbooks) |
| [documentation](documentation/) | 1 | Auto-generate docs from code |
| [extraction](extraction/) | 1 | Mine reusable patterns from projects |
| [marketing](marketing/) | 2 | Conversion optimization and copywriting |
| [refinement](refinement/) | 2 | Promote and consolidate staged skills |
| [skills](skills/) | 5 | Create, update, validate, and maintain the skill library |

---

## Installation

Clone the repo and copy commands into your project:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands
cp -r ~/.ai-skills/commands/* .cursor/commands/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands
cp -r ~/.ai-skills/commands/* ~/.cursor/commands/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands
cp -r ~/.ai-skills/commands/* .claude/commands/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands
cp -r ~/.ai-skills/commands/* ~/.claude/commands/
```

> **Tip:** Copy a single group instead of all commands:
> ```bash
> mkdir -p .cursor/commands/development
> cp ~/.ai-skills/commands/development/*.md .cursor/commands/development/
> ```

---

## How Commands Work

- Each command is a single markdown file with optional YAML frontmatter (`name`, `model`, `description`, `usage`).
- Sections typically include: **Usage**, **Examples**, **When to Use**, **What It Does**, **Implementation Steps**, **Output**, **Related**.
- Agents in `agents/` reference commands in their workflows. When an agent is installed alongside the commands, it can follow those command definitions.

---

## Common Workflows

```
# New project
/bootstrap-project → /bootstrap-design-system → /bootstrap-docs

# Feature end-to-end
/new-feature → /create-component → /create-api-route → /test-feature → /review-code

# UI
/design-ui → /create-component → /accessibility-audit → /check-performance

# Backend
/create-service → /create-migration → /create-api-route → /test-feature

# Ship
/check-performance → /security-review → /deploy staging → /deploy production

# Session
/intent → /start-task → /workflow → /complete-task → /session-summary
```

---

## See Also

| Resource | Path | Description |
|----------|------|-------------|
| Agents | [../agents/](../agents/) | 16 agents that invoke these commands |
| Skills | [../skills/](../skills/) | 118 skills |
