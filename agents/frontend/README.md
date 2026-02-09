# Frontend Agent

Autonomous workflow for designing, building, and polishing production-grade frontend interfaces end-to-end. Handles design system setup, component architecture, responsive layouts, accessibility, and performance.

## Workflow Phases

- **Phase 1: Requirements** — UI scope, users, devices, design input, accessibility, content, interactivity; technical constraints
- **Phase 2: Design system** — Design tokens, typography, color, spacing, motion; extend or create
- **Phase 3: Component architecture** — Component tree, composition, state, responsive breakpoints
- **Phase 4: Implementation** — Build components following framework best practices
- **Phase 5: Polish** — Transitions, loading/error/empty states
- **Phase 6: Verification** — Accessibility, responsiveness, visual quality

## Skills Used

- `ui-design` — UI design fundamentals, layout principles, visual hierarchy
- `react-best-practices` — React performance patterns and idiomatic usage
- `react-composition` — Compound components, render props, slots
- `responsive-design` — Container queries, fluid typography, mobile-first
- `frontend-design` — Creative aesthetics and distinctive visual design
- `tailwind-v4-shadcn` — Tailwind CSS v4 + shadcn/ui setup and configuration
- `ui-ux-pro-max` — Design database for styles, palettes, fonts, charts

## Trigger Phrases

- "build a component for [feature]"
- "create a page for [route]"
- "design the UI for [feature]"
- "build the frontend for [project]"
- "create a landing page for [product]"
- "implement the design for [mockup/spec]"
- "build a dashboard for [domain]"
- "create a form for [workflow]"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add frontend
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/frontend .cursor/rules/frontend-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/frontend .claude/skills/frontend-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/frontend ~/.claude/skills/frontend-agent
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
