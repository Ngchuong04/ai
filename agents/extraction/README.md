# Extraction Agent

Autonomous workflow for extracting reusable patterns from codebases into skills and documentation. Covers design systems, architecture patterns, workflow patterns, and domain-specific patterns.

## Workflow Phases

- **Phase 1: Discovery** — Analyze project structure, config files, CSS, docs, identify patterns present
- **Phase 2: Categorization** — Map discoveries to extraction priorities (design systems, UI, architecture, workflows, domain)
- **Phase 3: Extraction** — Extract and normalize patterns per category
- **Phase 4: Validation** — Consistency, completeness, no conflicts
- **Phase 5: Output** — Write skills and documentation to staging/output directories

## Skills Used

- `pattern-extraction` (extraction) — Full extraction methodology, priority order, extraction categories

## Trigger Phrases

- "extract patterns from [path]"
- "analyze this project for patterns"
- "extract design system from [path]"
- "capture patterns from this repo"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add extraction
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/extraction .cursor/rules/extraction-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/extraction .claude/skills/extraction-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/extraction ~/.claude/skills/extraction-agent
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/extract-discovery`, `/extract-categorize`.

---

Part of the [Agents](../) directory.
