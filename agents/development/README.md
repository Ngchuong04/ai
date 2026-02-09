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

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add development
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/development .cursor/rules/development-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/development .claude/skills/development-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/development ~/.claude/skills/development-agent
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/new-feature`. Requires `docs/` structure (run bootstrap-docs if missing).

---

Part of the [Agents](../) directory.
