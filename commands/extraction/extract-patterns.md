---
name: extract-patterns
model: reasoning
description: Extract reusable patterns from the current project into staging
usage: /extract-patterns [focus]
---

# /extract-patterns

Extract reusable patterns from the current project.

## Usage

```
/extract-patterns [focus]
```

**Focus options:**
- `all` (default) — Full extraction across all categories
- `design` — Design system and visual patterns only
- `arch` — Code organization and patterns only
- `workflow` — Build, dev, deploy patterns only

## Examples

```
/extract-patterns              # Full extraction
/extract-patterns design       # Design system only
/extract-patterns arch         # Architecture only
/extract-patterns workflow     # Build/dev/deploy only
```

## What It Does

1. **Loads** the extraction skill from `ai/skills/extraction/`
2. **Scans** project structure to identify tech stack
3. **Discovers** design system signals (Tailwind config, CSS variables, themes)
4. **Finds** architecture patterns (folder structure, components, data flow)
5. **Captures** workflow patterns (Makefile, scripts, CI/CD)
6. **Generates** methodology documentation
7. **Creates** skills for reusable patterns in staging

## Categories

| Category | What It Extracts |
|----------|-----------------|
| design | Design tokens, colors, typography, motion, components |
| arch | Folder structure, data flow, API patterns |
| workflow | Build scripts, dev setup, deploy processes |
| docs | Documentation patterns, templates |
| infra | Docker, K8s, monitoring configurations |

## Output Locations

```
ai/staging/
├── skills/[project]-[category]/
│   └── SKILL.md
└── docs/[project]-summary.md
```

## Related

- **Skill:** [`ai/skills/extraction/SKILL.md`](ai/skills/extraction/SKILL.md)
- **Agent:** [`ai/agents/refinement/`](ai/agents/refinement/) (for consolidation)
- **Next step:** `/refine-staged` (to consolidate extracted patterns)
