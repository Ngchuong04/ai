---
name: design-ui
model: reasoning
description: Design and implement a UI component or page with proper design system, accessibility, and responsive behavior
usage: /design-ui <component-or-page-name> [--style <style>] [--device <device>]
---

# /design-ui

Design and implement a UI component or page using design system fundamentals, creative direction, and accessibility best practices.

## Usage

```
/design-ui <component-or-page-name> [--style <style>] [--device <device>]
```

**Arguments:**
- `component-or-page-name` — What to design (e.g., `PricingPage`, `DashboardSidebar`, `OnboardingWizard`)
- `--style <style>` — Visual style hint (e.g., `minimal`, `glassmorphism`, `brutalist`, `playful`). Defaults to project conventions or `minimal`.
- `--device <device>` — Primary target device: `desktop`, `mobile`, `tablet`, or `all` (default: `all`)

## Examples

```
/design-ui PricingPage --style minimal
/design-ui DashboardSidebar --device desktop
/design-ui OnboardingWizard --style playful --device mobile
/design-ui SettingsPanel
/design-ui HeroSection --style glassmorphism
```

## When to Use

- Designing a new component or page from scratch with intentional visual direction
- Replacing a generic or placeholder UI with a polished, production-quality design
- Building a page that needs proper typography, color, spacing, and visual hierarchy
- When the default output feels like "generic AI aesthetics" and you want something distinctive

## What It Does

1. **Analyzes** the design target — what is being built, who it's for, and which devices it must support
2. **Generates** a design system if the project lacks one, using the ui-ux-pro-max design system generator
3. **Applies** ui-design fundamentals: typography scale, color palette, spacing system, visual hierarchy
4. **References** frontend-design for creative direction to avoid generic AI aesthetics
5. **Implements** with full accessibility (WCAG 2.1 AA), responsive breakpoints, and component states
6. **Runs** a pre-delivery checklist to verify quality

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Analyze Requirements

- Identify **what** is being designed (component, page, layout, form, etc.)
- Determine the **target audience** — who will use this UI and what are their expectations?
- Confirm **device targets** — desktop, mobile, tablet, or all.
- Check the project for an existing design system, theme, or style tokens.

### Phase 2: Establish Design System

If the project has no design system or tokens:

- Run the ui-ux-pro-max design system generator:
  ```
  python3 ai/skills/design-systems/ui-ux-pro-max/scripts/search.py "<context>" --design-system
  ```
- This produces a color palette, typography scale, spacing system, and component tokens.
- If a design system already exists, read and follow it.

### Phase 3: Apply Design Fundamentals

Use the ui-design skill to ensure:

| Principle | Requirement |
|-----------|-------------|
| **Typography** | Clear hierarchy with max 2 font families, consistent scale (e.g., 1.25 ratio) |
| **Color** | Purposeful palette — primary, secondary, neutral, semantic (success/warning/error) |
| **Spacing** | Consistent spacing scale (4px or 8px base), adequate whitespace |
| **Hierarchy** | Visual weight guides the eye — size, color, contrast, position |
| **Layout** | Grid-based alignment, balanced composition, intentional grouping |

### Phase 4: Creative Direction

Reference the frontend-design skill to push beyond generic output:

- Choose a distinctive visual approach that fits the product personality
- Avoid default shadows, rounded corners, and blue gradients unless intentional
- Add texture through typography, whitespace, and subtle motion — not decoration
- Ensure the design feels cohesive and intentional, not templated

### Phase 5: Implement

- Build the component/page with the detected framework and styling approach
- Include all interactive states: default, hover, focus, active, disabled, loading
- Implement responsive behavior:
  - Mobile-first breakpoints
  - Fluid typography and spacing where appropriate
  - Layout shifts at breakpoints (stack, reflow, hide/show)
- Add micro-interactions and transitions with `prefers-reduced-motion` safety

### Phase 6: Accessibility and Quality Check

Run through the pre-delivery checklist:

| Check | Standard |
|-------|----------|
| Color contrast | 4.5:1 normal text, 3:1 large text (WCAG AA) |
| Keyboard navigation | Full tab order, focus visible, no traps |
| Semantic HTML | Correct elements (`<nav>`, `<main>`, `<button>`, etc.) |
| Touch targets | Minimum 44×44px on mobile |
| Screen readers | Labels, roles, and live regions where needed |
| Reduced motion | Animations respect `prefers-reduced-motion` |
| Responsive | No horizontal scroll, readable text at all breakpoints |

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER use default blue + white + gray without justification** | This produces generic AI aesthetics that lack personality |
| **NEVER skip the accessibility check** | Inaccessible UI excludes users and fails compliance |
| **NEVER hardcode pixel values for typography or spacing** | Use tokens or a consistent scale for maintainability |
| **NEVER add decorative elements without purpose** | Every visual element should serve hierarchy, grouping, or interaction |
| **NEVER ignore existing project conventions** | Match the established design language, tokens, and component patterns |

## Output

- Implemented component/page file(s) with proper styling
- Design tokens or theme file if none existed
- Summary of design decisions made (palette, typography, layout rationale)

## Related

- **Skill:** `ai/skills/design-systems/ui-design/SKILL.md` — Typography, color, spacing, hierarchy fundamentals
- **Skill:** `ai/skills/design-systems/ui-ux-pro-max/SKILL.md` — Design system generator with 50 styles and 21 palettes
- **Skill:** `ai/skills/frontend/frontend-design/SKILL.md` — Creative direction, avoiding generic AI output
- **Skill:** `ai/skills/frontend/responsive-design/SKILL.md` — Container queries, fluid typography, mobile-first breakpoints
- **Agent:** `ai/agents/frontend/AGENT.md`
