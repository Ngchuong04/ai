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

### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/bootstrap .cursor/agents/bootstrap
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/bootstrap ~/.cursor/agents/bootstrap
```

### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/bootstrap .claude/agents/bootstrap
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/bootstrap ~/.claude/agents/bootstrap
```

For best results, also install the skills this agent references (see Skills Used above). Commands used by this agent live in `ai/commands/bootstrap/`.

---

Part of the [Agents](../) directory.
