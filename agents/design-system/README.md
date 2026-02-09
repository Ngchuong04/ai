# Design System Agent

Autonomous workflow for extracting design tokens from codebases or reference sites and generating Tailwind + CSS variable configurations. Use when analyzing existing designs or creating new design systems.

## Workflow Phases

- **Phase 1: Discovery** — Scan for design-related files (CSS, Tailwind config, tokens, theme files)
- **Phase 2: Token extraction** — Parse CSS custom properties, colors, typography, spacing from source
- **Phase 3: Analysis** — Normalize tokens, resolve conflicts, structure for output
- **Phase 4: Generation** — Tailwind config + CSS variables, component scaffolding
- **Phase 5: Documentation** — Token reference and usage docs

## Skills Used

- `pattern-extraction` (extraction) — Extraction methodology
- `distinctive-design-systems` — Design system patterns
- `design-system-creation` — Complete design system workflow
- `ui-design` — Comprehensive UI design
- `ui-ux-pro-max` — Searchable design database
- `theme-factory` — Theme application
- `web-design` — CSS patterns
- `animated-financial-display` — Animated financial displays (optional)

## Trigger Phrases

- "extract design system from [path]"
- "analyze design tokens in [project]"
- "create design system from [reference]"

## Installation

### Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.ai-skills/agents/design-system .cursor/rules/design-system-agent
```

### Claude Code (per-project)

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/design-system .claude/agents/design-system
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/design-system ~/.claude/agents/design-system
```

For best results, also install the skills this agent references (see Skills Used above). Commands: `/bootstrap-design-system`, `/extract-design-tokens`.

---

Part of the [Agents](../) directory.
