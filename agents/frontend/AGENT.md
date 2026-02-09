---
name: frontend-agent
models:
  requirements: reasoning
  design_system: standard
  component_architecture: reasoning
  implementation: standard
  polish: standard
  verification: fast
description: "Autonomous agent for building production-grade frontend interfaces from component design through implementation, styling, accessibility, and performance. Handles design system setup, component architecture, responsive layouts, and polish. Use when building UI components, pages, or full frontend features. Triggers on 'build a component', 'create a page', 'design the UI for', 'build the frontend', 'create a landing page', 'implement the design'."
---

# Frontend Agent

Autonomous workflow for designing, building, and polishing production-grade frontend interfaces end-to-end.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/skills/design-systems/ui-design/SKILL.md`](ai/skills/design-systems/ui-design/SKILL.md) — UI design fundamentals, layout principles, visual hierarchy
2. [`ai/skills/frontend/react-best-practices/SKILL.md`](ai/skills/frontend/react-best-practices/SKILL.md) — React performance patterns and idiomatic usage
3. [`ai/skills/frontend/react-composition/SKILL.md`](ai/skills/frontend/react-composition/SKILL.md) — Component composition patterns (compound components, render props, slots)
4. [`ai/skills/frontend/responsive-design/SKILL.md`](ai/skills/frontend/responsive-design/SKILL.md) — Responsive layout patterns, container queries, fluid typography
5. [`ai/skills/frontend/frontend-design/SKILL.md`](ai/skills/frontend/frontend-design/SKILL.md) — Creative aesthetics and distinctive visual design
6. [`ai/skills/frontend/tailwind-v4-shadcn/SKILL.md`](ai/skills/frontend/tailwind-v4-shadcn/SKILL.md) — Tailwind CSS v4 + shadcn/ui setup and configuration
7. [`ai/skills/design-systems/ui-ux-pro-max/SKILL.md`](ai/skills/design-systems/ui-ux-pro-max/SKILL.md) — Design database CLI for styles, palettes, fonts, and charts

**Verify:**
- [ ] User has described the UI to build (component, page, feature, or full application)
- [ ] Target framework detected or specified (React, Next.js, Vue, Svelte, etc.)
- [ ] Design direction is known or can be inferred (existing design system, mockups, brand guidelines, or creative freedom)

---

## Purpose

Design and deliver production-quality frontend interfaces with intentional craft:
1. Translate UI requirements into component architecture and design tokens
2. Establish or extend a design system with consistent typography, color, spacing, and motion
3. Build accessible, responsive, performant components following framework best practices
4. Polish with transitions, loading states, error states, and empty states
5. Verify accessibility, responsiveness, and visual quality before delivery

**When NOT to use this agent:**
- Building backend APIs or server-side logic (use the API agent or backend agent)
- Writing tests for existing frontend code (use the testing agent)
- Deploying or configuring CI/CD (use the deployment agent)
- Refactoring existing code without UI changes (use the refactoring agent)
- Single CSS fix or style tweak (make the change directly)

---

## Activation

```
"build a component for [feature]"
"create a page for [route]"
"design the UI for [feature]"
"build the frontend for [project]"
"create a landing page for [product]"
"implement the design for [mockup/spec]"
"build a dashboard for [domain]"
"create a form for [workflow]"
```

---

## Workflow

### Phase 1: Requirements

Understand what needs to be built, for whom, and under what constraints.

**Step 1 — Gather UI requirements:**

Ask the user to describe what they need. Extract:

| Element | Question | Example |
|---------|----------|---------|
| Scope | What is being built? | Product card component, settings page, full dashboard |
| Users | Who will use this? | End users on mobile, admin on desktop, both |
| Devices | What viewports must work? | Mobile-first, tablet + desktop, desktop-only |
| Design input | Is there a mockup, brand guide, or existing design system? | Figma link, existing Tailwind config, creative freedom |
| Accessibility | What level of accessibility is required? | WCAG 2.1 AA (default), AAA for government, basic |
| Content | What data drives the UI? | API responses, static content, user-generated content |
| Interactivity | What user actions are supported? | Forms, drag-and-drop, real-time updates, filters |

**Step 2 — Identify technical constraints:**

| Constraint | How to Detect |
|------------|---------------|
| Framework | `package.json` dependencies, `next.config.*`, `vite.config.*`, `nuxt.config.*` |
| Styling approach | Tailwind config, CSS modules, styled-components, CSS-in-JS imports |
| Component library | shadcn/ui, Radix, MUI, Chakra, Headless UI imports |
| State management | React Context, Zustand, Redux, Jotai, Pinia imports |
| Routing | Next.js App Router, React Router, file-based routing convention |
| Existing design tokens | CSS custom properties, Tailwind theme config, design token files |

**Step 3 — Confirm scope with user:**
Present a summary of what will be built, target viewports, design direction, and accessibility level. Do NOT proceed without approval.

**Output:** Approved scope document with UI requirements, constraints, and design direction.

**Validation:** User has confirmed scope. Target devices are defined. Accessibility level is set. Technical constraints are identified.

---

### Phase 2: Design System

Establish or reference the visual foundation for the interface.

**Step 1 — Audit existing design tokens:**

Check for existing design system artifacts:

| Artifact | Where to Look |
|----------|---------------|
| Color palette | `tailwind.config.*`, CSS custom properties in `globals.css`, theme files |
| Typography scale | Font imports, font-size utilities, `@font-face` declarations |
| Spacing scale | Tailwind spacing config, CSS custom properties, component padding patterns |
| Border radius | Consistent `rounded-*` usage, CSS `--radius` variables |
| Shadow system | `box-shadow` values, Tailwind shadow config |
| Motion tokens | `transition-*` utilities, CSS animation keyframes |

**Step 2 — Define or extend tokens:**

If no design system exists, establish one using the `ui-design` and `ui-ux-pro-max` skills:

```css
/* Design Tokens */
:root {
  /* Colors — semantic, not literal */
  --color-primary: ...;
  --color-primary-foreground: ...;
  --color-secondary: ...;
  --color-muted: ...;
  --color-destructive: ...;
  --color-border: ...;
  --color-background: ...;
  --color-foreground: ...;

  /* Typography */
  --font-sans: ...;
  --font-mono: ...;
  --font-size-sm: ...;
  --font-size-base: ...;
  --font-size-lg: ...;
  --font-size-xl: ...;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  /* ... */

  /* Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* Shadows */
  --shadow-sm: ...;
  --shadow-md: ...;

  /* Motion */
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --transition-ease: cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Step 3 — Verify contrast ratios:**

For every foreground/background color pairing:

| WCAG Level | Normal Text | Large Text |
|------------|-------------|------------|
| AA (minimum) | 4.5:1 | 3:1 |
| AAA (enhanced) | 7:1 | 4.5:1 |

Use computed contrast ratios. Do not guess.

**Step 4 — Configure tooling:**

If using Tailwind + shadcn/ui, follow the `tailwind-v4-shadcn` skill for setup: CSS variables → Tailwind mapping → base styles → dark mode.

**Output:** Design token file or Tailwind theme configuration integrated into the project.

**Validation:** Color palette has sufficient contrast ratios. Typography scale is defined. Spacing scale is consistent. Dark mode tokens exist if applicable.

---

### Phase 3: Component Architecture

Plan the component tree, API surface, and composition patterns before writing code.

**Step 1 — Decompose the UI into components:**

Break the interface into a component tree:

```
PageLayout
├── Header
│   ├── Logo
│   ├── Navigation
│   └── UserMenu
├── Main
│   ├── Sidebar (if applicable)
│   │   ├── FilterGroup
│   │   └── FilterItem
│   └── Content
│       ├── ContentHeader
│       ├── CardGrid / DataTable
│       │   └── Card / Row
│       └── Pagination
└── Footer
```

**Step 2 — Define component APIs:**

For each component, define:

| Property | Description | Example |
|----------|-------------|---------|
| Props | External interface | `variant`, `size`, `disabled`, `children` |
| State | Internal state needs | Open/closed, loading, selected items |
| Events | Callbacks and handlers | `onClick`, `onSubmit`, `onChange` |
| Slots | Composition points | `header`, `footer`, `action` via children or render props |
| Variants | Visual variations | `default`, `destructive`, `outline`, `ghost` |

**Step 3 — Choose composition patterns:**

Reference the `react-composition` skill to select patterns:

| Pattern | When to Use |
|---------|-------------|
| Compound components | Multi-part components with shared state (Tabs, Accordion, Select) |
| Render props / slots | Components that need flexible rendering of children |
| Polymorphic `as` prop | Components that can render as different HTML elements |
| Context providers | State shared across a subtree without prop drilling |
| Controlled / uncontrolled | Form elements and toggles with optional external state |

**Step 4 — Plan data flow:**

Map how data moves through the component tree:

| Source | Flow | Consumer |
|--------|------|----------|
| Server data (API, RSC) | Props drilled or context | Display components |
| User input | Controlled state / form library | Validation, submission |
| URL state | Router params / search params | Filters, pagination |
| Client state | Zustand / Context / useState | Interactive UI elements |

**Output:** Component tree diagram, props API definitions, and composition pattern selections.

**Validation:** Every visible UI element maps to a component. Props APIs are minimal and consistent. No prop drilling deeper than 2 levels without context or composition.

---

### Phase 4: Implementation

Build the components with proper patterns, accessibility, and responsiveness.

**Step 1 — Build bottom-up:**

Start with leaf components and work up to page-level compositions:

1. **Primitives** — Buttons, inputs, badges, avatars, icons
2. **Composites** — Cards, form groups, navigation items, list items
3. **Sections** — Headers, sidebars, content areas, footers
4. **Pages** — Full page compositions with layout and data fetching

**Step 2 — For each component, implement:**

| Concern | Implementation |
|---------|----------------|
| Semantics | Correct HTML elements (`button`, `nav`, `main`, `article`, `section`, not `div` soup) |
| Accessibility | ARIA attributes, roles, labels, focus management, keyboard navigation |
| Responsive design | Mobile-first styles, breakpoint-appropriate layouts, fluid typography |
| State handling | Proper React patterns (controlled vs uncontrolled, derived state, reducers for complex state) |
| Performance | Memoization where needed (`memo`, `useMemo`, `useCallback` for referential stability), lazy loading for heavy components |
| Error boundaries | Graceful error UI at section level, not per-component |

**Step 3 — Implement accessibility correctly:**

For every interactive element:

| Element | Requirements |
|---------|-------------|
| Buttons | `type` attribute, visible focus ring, disabled state, loading state with `aria-busy` |
| Links | Meaningful text (not "click here"), `aria-current` for active navigation |
| Forms | Labels associated via `htmlFor`/`id`, error messages linked with `aria-describedby`, required fields marked |
| Modals/Dialogs | Focus trap, `Escape` to close, `aria-modal`, return focus on close |
| Lists/Grids | `role="list"` if styled, `aria-label` for unnamed lists |
| Images | Meaningful `alt` text or `alt=""` for decorative, `loading="lazy"` for below-fold |
| Dynamic content | `aria-live` regions for updates, `aria-expanded` for collapsibles |

**Step 4 — Implement responsive design:**

Reference the `responsive-design` skill for patterns:

| Viewport | Strategy |
|----------|----------|
| Mobile (< 640px) | Single column, stacked layouts, bottom navigation, touch targets ≥ 44px |
| Tablet (640px–1024px) | Two-column layouts, collapsible sidebars, adapted navigation |
| Desktop (> 1024px) | Full multi-column layouts, hover interactions, keyboard shortcuts |

Use container queries for component-level responsiveness when appropriate.

**Step 5 — Verify build:**

```bash
# Verify no TypeScript errors
npx tsc --noEmit

# Verify no linting errors
npx eslint [new-files]

# Verify the build succeeds
npm run build
```

**Output:** Complete set of component files, styled and accessible, building without errors.

**Validation:** All components render correctly. No TypeScript or linting errors. Build succeeds. Every interactive element is keyboard-accessible.

---

### Phase 5: Polish

Add the refinements that separate prototype quality from production quality.

**Step 1 — Implement state variations:**

Every component that displays data must handle all states:

| State | Implementation |
|-------|----------------|
| Loading | Skeleton screens (not spinners) that match the content layout |
| Error | Contextual error message with retry action, not generic "Something went wrong" |
| Empty | Helpful empty state with illustration or icon, description, and primary action |
| Partial | Graceful degradation when some data is available but not all |
| Success | Confirmation feedback for user actions (toast, inline message, visual change) |

**Step 2 — Add motion and transitions:**

| Interaction | Animation |
|-------------|-----------|
| Page transitions | Fade or slide with `duration-normal` |
| Hover / focus | Subtle scale, color shift, or shadow with `duration-fast` |
| Enter / exit | Fade + translate for modals, popovers, dropdowns |
| Layout shifts | `transition-all` on dimension changes to prevent jarring jumps |
| Loading feedback | Skeleton pulse, progress indicators |

Always respect `prefers-reduced-motion`:

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Step 3 — Polish typography and spacing:**

- Verify consistent use of the type scale (no arbitrary `text-[17px]` values)
- Check vertical rhythm — consistent spacing between sections
- Ensure readable line lengths (45–75 characters for body text)
- Verify proper text truncation for overflow content (`truncate`, `line-clamp`)

**Step 4 — Add micro-interactions:**

- Button press feedback (subtle scale or color)
- Form field validation feedback (inline, as-you-type for complex fields)
- Toggle and switch animations
- Scroll-triggered reveals for landing pages (if appropriate)

**Output:** Polished interface with complete state handling, smooth transitions, and production-quality typography.

**Validation:** All five data states implemented. Animations respect `prefers-reduced-motion`. No arbitrary spacing or typography values. Micro-interactions provide clear feedback.

---

### Phase 6: Verification

Final quality checks across accessibility, responsiveness, and performance.

**Step 1 — Accessibility audit:**

| Check | Method | Pass Criteria |
|-------|--------|---------------|
| Keyboard navigation | Tab through every interactive element | Logical focus order, visible focus indicators, no focus traps |
| Screen reader | Verify landmark structure and ARIA | All content reachable, meaningful announcements |
| Color contrast | Check every text/background pair | Meets WCAG AA (4.5:1 normal, 3:1 large) |
| Reduced motion | Enable `prefers-reduced-motion` | No animations, no loss of information |
| Zoom | Test at 200% browser zoom | No content overlap, no horizontal scroll |
| Touch targets | Measure interactive element sizes | Minimum 44×44px on touch devices |

**Step 2 — Responsive testing:**

Test at these breakpoints as a minimum:

| Viewport | Width | Check |
|----------|-------|-------|
| Small mobile | 320px | Content readable, no horizontal overflow |
| Standard mobile | 375px | Layout correct, touch targets adequate |
| Large mobile | 428px | No awkward gaps or stretched elements |
| Tablet portrait | 768px | Layout adapts, navigation adjusts |
| Tablet landscape | 1024px | Sidebar visible if applicable |
| Desktop | 1280px | Full layout, all features accessible |
| Wide desktop | 1536px | Content doesn't stretch uncomfortably |

**Step 3 — Performance check:**

| Metric | Target | How to Check |
|--------|--------|--------------|
| Bundle size | No single component > 50KB gzipped | Analyze build output |
| Images | All images optimized, using `next/image` or `loading="lazy"` | Review image elements |
| Layout shift | CLS < 0.1 | Reserve space for dynamic content, set image dimensions |
| Render performance | No unnecessary re-renders | React DevTools profiler or `React.memo` audit |
| Font loading | No FOIT/FOUT | `font-display: swap`, preload critical fonts |

**Step 4 — Visual review:**

- Screenshots at each breakpoint
- Dark mode rendering (if applicable)
- Consistency with design tokens (no rogue colors, spacing, or fonts)
- Print stylesheet (if applicable)

**Output:** Verified, production-ready frontend interface.

**Validation:** Accessibility audit passes. All breakpoints tested. Performance metrics within targets. Visual consistency confirmed.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| User's requirements are vague or incomplete | Ask specific questions about scope, devices, and design direction before proceeding |
| No design system or tokens exist in the project | Create a minimal token set using the `ui-design` and `ui-ux-pro-max` skills; confirm with user |
| Framework not detected | Ask the user which framework to target; do not guess |
| Component library conflicts (multiple UI libraries) | Identify the primary library from usage frequency; use it consistently; warn the user about conflicts |
| Design mockup uses components not in the library | Build custom components matching the mockup; do not substitute with mismatched library components |
| Accessibility issues found during audit | Fix immediately; accessibility is not optional and must not be deferred |
| Responsive layout breaks at an intermediate viewport | Add targeted styles at the breaking width; avoid fixed-width containers |
| Build fails after component changes | Read error output; fix TypeScript or import errors; rebuild before proceeding |
| Performance issue: excessive re-renders | Profile with React DevTools; apply `memo`, `useMemo`, or restructure state to reduce render scope |
| Dark mode colors have insufficient contrast | Recalculate contrast ratios for dark theme tokens independently; do not assume light mode ratios transfer |
| Existing code uses inconsistent patterns | Match the dominant pattern in the codebase; note inconsistencies to the user but do not refactor unrelated code |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Design tokens | `globals.css`, `tailwind.config.*`, or dedicated token file | Visual foundation for consistency |
| Component files | Per project convention (e.g., `src/components/`, `app/components/`) | Reusable UI building blocks |
| Page/route files | Per routing convention (e.g., `app/[route]/page.tsx`, `src/pages/`) | Composed page layouts |
| Utility styles | Global CSS or Tailwind utilities | Shared patterns (animations, typography, layout) |
| Component tree | Presented in chat | Architecture approval before implementation |

---

## Quality Checklist

Before marking the frontend agent workflow complete:

- [ ] Component tree approved by the user before implementation began
- [ ] Design tokens are defined and used consistently (no arbitrary values)
- [ ] All components use semantic HTML elements (not `div`/`span` soup)
- [ ] Keyboard navigation works for every interactive element
- [ ] Color contrast meets WCAG AA for all text/background pairs
- [ ] Responsive layout tested at mobile, tablet, and desktop breakpoints
- [ ] Loading, error, and empty states implemented for all data-driven components
- [ ] Animations respect `prefers-reduced-motion`
- [ ] No TypeScript errors, no linting errors, build succeeds
- [ ] Touch targets are ≥ 44px on mobile viewports
- [ ] Images use lazy loading and have appropriate `alt` text
- [ ] Component props APIs are minimal, consistent, and documented via TypeScript types
- [ ] No hardcoded strings (content is extractable for i18n if needed)

---

## Related

- **Skill:** [`ai/skills/design-systems/ui-design/SKILL.md`](ai/skills/design-systems/ui-design/SKILL.md)
- **Skill:** [`ai/skills/frontend/react-best-practices/SKILL.md`](ai/skills/frontend/react-best-practices/SKILL.md)
- **Skill:** [`ai/skills/frontend/react-composition/SKILL.md`](ai/skills/frontend/react-composition/SKILL.md)
- **Skill:** [`ai/skills/frontend/responsive-design/SKILL.md`](ai/skills/frontend/responsive-design/SKILL.md)
- **Skill:** [`ai/skills/frontend/frontend-design/SKILL.md`](ai/skills/frontend/frontend-design/SKILL.md)
- **Skill:** [`ai/skills/frontend/tailwind-v4-shadcn/SKILL.md`](ai/skills/frontend/tailwind-v4-shadcn/SKILL.md)
- **Skill:** [`ai/skills/design-systems/ui-ux-pro-max/SKILL.md`](ai/skills/design-systems/ui-ux-pro-max/SKILL.md)
- **Testing agent:** [`ai/agents/testing/`](ai/agents/testing/)
- **Design system agent:** [`ai/agents/design-system/`](ai/agents/design-system/)
- **API agent:** [`ai/agents/api/`](ai/agents/api/)

---

## NEVER Do

- **Never skip accessibility** — Accessibility is a requirement, not a feature. Every component must be keyboard-navigable, screen-reader-compatible, and contrast-compliant before delivery. Retrofitting accessibility is 10x harder than building it in.
- **Never use arbitrary spacing values** — `p-[13px]`, `mt-[7px]`, and `gap-[22px]` break visual rhythm and make maintenance impossible. Use the spacing scale from design tokens. If the scale doesn't have the right value, extend the scale intentionally.
- **Never ignore the mobile viewport** — Mobile is the primary viewport for most users. Every component must be designed mobile-first and verified at 320px minimum width. A desktop-only component is an unfinished component.
- **Never skip loading, error, and empty states** — Components that only handle the happy path will break in production. Every data-driven component needs skeleton loading, error with retry, and helpful empty states. These are not optional follow-ups.
- **Never use inline styles over design tokens** — `style={{ color: '#3b82f6' }}` and arbitrary Tailwind values bypass the design system. All visual values must come from tokens so they can be themed, maintained, and kept consistent.
- **Never build without checking contrast ratios** — "It looks fine to me" is not an accessibility check. Compute the actual contrast ratio for every text/background pair. WCAG AA requires 4.5:1 for normal text and 3:1 for large text. Measure, don't guess.
- **Never skip keyboard navigation testing** — Tab through every interactive element before delivery. Verify logical focus order, visible focus indicators, no focus traps, and that all actions are reachable without a mouse. Modal focus management is especially critical.
- **Never use generic fonts without intention** — `font-family: sans-serif` or unspecified system fonts produce inconsistent rendering across platforms. Choose fonts deliberately, configure `font-display: swap`, and preload critical font files.
- **Never commit without responsive testing** — A component that works at 1280px may overflow at 375px, stack incorrectly at 768px, or stretch awkwardly at 1536px. Test at a minimum of 5 breakpoints before delivery.
- **Never ignore `prefers-reduced-motion`** — Users who enable reduced motion have a reason (vestibular disorders, motion sickness, personal preference). All animations and transitions must be disabled or minimized when this media query is active. Decorative motion is never worth causing discomfort.
