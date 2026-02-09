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

### Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.ai-skills/agents/extraction .cursor/rules/extraction-agent
```

### Claude Code (per-project)

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/extraction .claude/agents/extraction
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/extraction ~/.claude/agents/extraction
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/extract-discovery`, `/extract-categorize`.

---

Part of the [Agents](../) directory.
