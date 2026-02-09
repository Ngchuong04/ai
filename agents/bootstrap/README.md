# Bootstrap Agent

Autonomous workflow for scaffolding new projects with opinionated structure, documentation, and tooling. Use when starting a new project from scratch.

## Workflow Phases

- **Phase 1: Gather requirements** — Project type (monorepo, app, library, service), stack, features (Docker, testing, docs, CI/CD)
- **Phase 2: Scaffold structure** — Directory layout via `/bootstrap-project`, `/bootstrap-docs`, `/bootstrap-design-system`
- **Phase 3: Initialize documentation** — Architecture, planning, decisions, product personas, runbooks
- **Phase 4: Configure tooling** — Linting, formatting, testing, CI
- **Phase 5: Initialize git** — Initial commit, branch strategy

## Skills Used

- `project-documentation` — Documentation patterns and structure
- Optional by project type: `docker`, `tailwind-v4-shadcn`, `turborepo` (monorepo)

## Trigger Phrases

- "bootstrap new project"
- "scaffold [type] project"
- "create new [type] project"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add bootstrap
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/bootstrap .cursor/rules/bootstrap-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/bootstrap .claude/skills/bootstrap-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/bootstrap ~/.claude/skills/bootstrap-agent
```

For best results, also install the skills this agent references (see Skills Used above). Commands used by this agent live in `ai/commands/bootstrap/`.

---

Part of the [Agents](../) directory.
