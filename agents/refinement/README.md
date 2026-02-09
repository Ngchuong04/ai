# Refinement Agent

Autonomous workflow for consolidating and refining extracted skills from staging into production-ready, project-agnostic patterns. Use when staging has content ready for consolidation.

## Workflow Phases

- **Phase 1: Inventory** — Scan `ai/staging/skills/` and `ai/staging/docs/`, catalog contents
- **Phase 2: Pattern analysis** — Identify overlapping patterns across projects (design systems, architecture, workflows)
- **Phase 3: Consolidation** — Merge into project-agnostic skills, apply quality criteria
- **Phase 4: Quality check** — Validate against skill quality criteria
- **Phase 5: Promotion** — Move consolidated content to `ai/skills/`, update methodology
- **Phase 6: Cleanup** — Archive or remove processed staging content

## Skills Used

- `staged-content-refinement` (refinement) — Refinement methodology
- Extraction references: `skill-quality-criteria` — Quality requirements for promoted skills

## Trigger Phrases

- "refine staged content"
- "consolidate staged skills"
- "process staging folder"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add refinement
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/refinement .cursor/rules/refinement-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/refinement .claude/skills/refinement-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/refinement ~/.claude/skills/refinement-agent
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/list-staging`, `/analyze-patterns`. Requires `ai/staging/` structure in this repo.

---

Part of the [Agents](../) directory.
