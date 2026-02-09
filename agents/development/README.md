# Development Agent

Autonomous workflow for docs-first feature development. Handles feature planning, spec creation, ADRs, roadmap updates, implementation tracking, and documentation.

## Workflow Phases

- **Phase 1: Feature scoping** — Problem, personas, scope (MVP vs full), non-goals
- **Phase 2: Spec creation** — Feature spec in `docs/planning/specs/` with template
- **Phase 3: ADR creation** — Document architectural decisions
- **Phase 4: Roadmap update** — Update planning/roadmap
- **Phase 5: Implementation** — Track progress, implement with tests
- **Phase 6: Documentation** — Keep docs current with implementation

## Skills Used

- `project-documentation` — Documentation patterns
- `feature-specification` — Feature spec patterns
- `full-stack-feature` — Full-stack feature workflow
- `brainstorming` — Creative brainstorming
- `testing-patterns` — Testing patterns

## Trigger Phrases

- "new feature [name]"
- "develop feature [name]"
- "add feature for [persona]"
- "implement [feature]"

## Installation

### Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.ai-skills/agents/development .cursor/rules/development-agent
```

### Claude Code (per-project)

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/development .claude/agents/development
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/development ~/.claude/agents/development
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/new-feature`. Requires `docs/` structure (run bootstrap-docs if missing).

---

Part of the [Agents](../) directory.
