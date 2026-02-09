---
name: create-component
model: standard
description: Scaffold a UI component with variants, props, accessibility, and documentation
usage: /create-component <name> [--variant] [--interactive] [--with-tests] [--with-story]
---

# /create-component

Scaffold a production-ready UI component with variants, typed props, accessibility, and optional tests and stories.

## Usage

```
/create-component <name> [--variant] [--interactive] [--with-tests] [--with-story]
```

**Arguments:**
- `name` — Component name in PascalCase (e.g., `Button`, `UserCard`, `SearchInput`)
- `--variant` — Include visual variants (primary, secondary, outline, ghost, etc.)
- `--interactive` — Add event handlers, state management, and controlled/uncontrolled modes
- `--with-tests` — Generate a co-located test file with unit tests for props, variants, and accessibility
- `--with-story` — Generate a Storybook story file with variant showcases and controls

## Examples

```
/create-component Button --variant --interactive --with-tests --with-story
/create-component UserCard --variant --with-story
/create-component SearchInput --interactive --with-tests
/create-component Modal --variant --interactive --with-tests --with-story
/create-component Avatar --variant
```

## When to Use

- Starting a new UI component from scratch
- Adding a component to an existing design system or component library
- Replacing an ad-hoc element with a properly typed, accessible component
- Prototyping a component that needs variant support from day one
- When you need consistent file structure across a component library

## What It Does

1. **Parses** the component name and flags from the input
2. **Detects** the project's framework and styling approach automatically
3. **Generates** the component file with typed props and sensible defaults
4. **Adds** visual variants and prop-driven styling when `--variant` is set
5. **Adds** accessibility attributes, keyboard navigation, and ARIA roles
6. **Generates** test and story files when `--with-tests` or `--with-story` are set
7. **Creates** a barrel export and reports all generated files

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Input

- Extract the component `name` from the first argument.
- Validate that the name is PascalCase. If not, convert it and warn:
  > "Converted `user-card` to `UserCard`."
- Parse boolean flags: `--variant`, `--interactive`, `--with-tests`, `--with-story`.
- Derive the kebab-case directory name from the PascalCase name (e.g., `UserCard` -> `user-card`).

### Phase 2: Detect Framework and Styling

Use `Glob` and `Grep` to scan the project root and `src/` for configuration files and import patterns.

**Framework detection:**

| Indicator | Framework | File Extension |
|-----------|-----------|----------------|
| `tsconfig.json` + `.tsx` files | React (TypeScript) | `.tsx` |
| `.jsx` files, `react` in `package.json` | React (JavaScript) | `.jsx` |
| `*.vue` files, `vue` in `package.json` | Vue (SFC) | `.vue` |
| `*.svelte` files, `svelte` in `package.json` | Svelte | `.svelte` |
| `@angular/core` in `package.json` | Angular | `.component.ts` |
| `react-native` in `package.json` | React Native | `.tsx` |
| `solid-js` in `package.json` | Solid | `.tsx` |

If multiple indicators match, prefer the one with the most file hits. If none match, default to React with TypeScript and inform the user.

**Styling detection:**

| Indicator | Approach | Usage |
|-----------|----------|-------|
| `tailwind.config.*` or `@tailwind` in CSS | Tailwind CSS | Utility classes in `className` |
| `*.module.css` or `*.module.scss` files | CSS Modules | Import as `styles`, use `styles.className` |
| `styled-components` in `package.json` | Styled Components | Tagged template literals |
| `@emotion/react` or `@emotion/styled` in `package.json` | Emotion | `css` prop or styled API |
| `*.css` files co-located with components | Vanilla CSS | Plain class names |
| None of the above | Inline styles | `style` prop as fallback |

**Component directory detection:**

Use `Glob` to find the existing component directory. Check in order:
1. `src/components/`
2. `components/`
3. `app/components/`
4. `lib/components/`
5. `src/ui/`

If no component directory exists, create `src/components/` and inform the user.

### Phase 3: Generate Component

Create the component file based on detected framework. Place it at `[component-dir]/[kebab-name]/[Name].[ext]`.

**Component structure by framework:**

| Framework | Props Definition | Component Pattern | Export Style |
|-----------|-----------------|-------------------|-------------|
| React (TS) | `interface [Name]Props` | `forwardRef` function component | Named export |
| React (JS) | JSDoc + `propTypes` | `forwardRef` function component | Named export |
| Vue | `defineProps<{}>()` | `<script setup lang="ts">` SFC | Default export |
| Svelte | `export let prop` declarations | Svelte component | Default export |
| Angular | `@Input()` decorators | `@Component` class | Class export |
| React Native | `interface [Name]Props` | `forwardRef` function component | Named export |
| Solid | `interface [Name]Props` | Function component with `splitProps` | Named export |

Every generated component must include:
- A `Props` type or interface with JSDoc comments on each prop
- A `displayName` (React) or equivalent identifier
- A `ref` forwarding mechanism when the framework supports it
- Default prop values where sensible
- A `className` or `class` prop for style overriding

### Phase 4: Add Variants and Props

Skip this phase if `--variant` was not set.

- Define a `variant` prop with a union type: `'default' | 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive'`.
- Define a `size` prop with a union type: `'sm' | 'md' | 'lg'`.
- Map each variant and size to styling using the detected styling approach.
- For Tailwind: use a variant mapping object with `cva` or a plain record.
- For CSS Modules: generate a `.module.css` file with classes for each variant.
- For Styled Components / Emotion: use a `variants` prop pattern.
- For vanilla CSS: generate a `.css` file with BEM-style variant classes.
- Export the variant and size types so consumers can reference them.

### Phase 5: Add Accessibility

Apply the following checklist to the generated component. Every item must be addressed:

| Requirement | Implementation |
|-------------|----------------|
| **ARIA role** | Set the semantic role (`button`, `dialog`, `alert`, etc.) or use the correct HTML element |
| **Keyboard navigation** | Handle `Enter`, `Space`, `Escape`, `Tab`, and arrow keys as appropriate for the role |
| **Focus management** | Ensure focusable elements have visible focus indicators; manage focus traps for modals/dialogs |
| **Screen reader labels** | Add `aria-label`, `aria-labelledby`, or `aria-describedby` when visual label is absent |
| **Color contrast** | Add a code comment noting WCAG AA contrast requirement (4.5:1 for text, 3:1 for large text) |
| **Disabled state** | Support `disabled` prop with `aria-disabled` and prevent interaction when disabled |
| **Loading state** | Support `loading` prop with `aria-busy="true"` and a visually-hidden status message |
| **Reduced motion** | Wrap animations in `prefers-reduced-motion` media query or equivalent |

For interactive components (`--interactive`), also add:
- `role` and `aria-expanded` for collapsible elements
- `aria-haspopup` for menu triggers
- `aria-pressed` for toggle buttons
- Keyboard event handlers that mirror click behavior

### Phase 6: Generate Tests and Stories

**Tests** (when `--with-tests` is set):

Detect the test runner:

| Indicator | Runner | Import |
|-----------|--------|--------|
| `vitest` in `package.json` | Vitest | `import { describe, it, expect } from 'vitest'` |
| `jest` in `package.json` | Jest | `import { describe, it, expect } from '@jest/globals'` |
| `@testing-library/react` | React Testing Library | `import { render, screen } from '@testing-library/react'` |
| `@testing-library/vue` | Vue Testing Library | `import { render } from '@testing-library/vue'` |
| `@testing-library/svelte` | Svelte Testing Library | `import { render } from '@testing-library/svelte'` |

Generate a test file at `[component-dir]/[kebab-name]/[Name].test.[ext]` with:
- Renders without crashing
- Renders with default props
- Renders each variant (if `--variant`)
- Renders each size (if `--variant`)
- Handles click events (if `--interactive`)
- Supports disabled state
- Meets accessibility baseline (`toHaveNoViolations` if `jest-axe` or `vitest-axe` is available)
- Forwards ref correctly

**Stories** (when `--with-story` is set):

Generate a story file at `[component-dir]/[kebab-name]/[Name].stories.[ext]` with:
- Default story
- One story per variant (if `--variant`)
- One story per size (if `--variant`)
- Interactive story with actions (if `--interactive`)
- A "Playground" story with all controls exposed via `argTypes`

### Phase 7: Create Barrel Export and Report

- Create or update `[component-dir]/[kebab-name]/index.[ext]` to re-export the component and its types.
- If a top-level barrel file exists at `[component-dir]/index.[ext]`, append the new export.
- Use `Bash` to verify no syntax errors: run `npx tsc --noEmit` (TypeScript) or the framework's equivalent.
- Report all generated files and their paths.

Output a summary:

```
Component Scaffolded
====================
Name:       [Name]
Framework:  [detected framework]
Styling:    [detected approach]
Directory:  [full path]

Files created:
  [component-dir]/[kebab-name]/[Name].tsx
  [component-dir]/[kebab-name]/[Name].types.ts
  [component-dir]/[kebab-name]/[Name].test.tsx      (--with-tests)
  [component-dir]/[kebab-name]/[Name].stories.tsx    (--with-story)
  [component-dir]/[kebab-name]/index.ts

Props:      [list of props with types]
Variants:   [list of variants, if applicable]
Sizes:      [list of sizes, if applicable]
A11y:       [checklist items addressed]
```

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER generate a component without typed props** | Untyped props erode maintainability and break IDE autocompletion |
| **NEVER skip accessibility attributes** | Components without ARIA roles, keyboard support, and focus management exclude users |
| **NEVER hardcode colors or spacing values** | Always use design tokens, theme variables, or Tailwind classes for consistency |
| **NEVER use `any` or untyped event handlers** | Every handler and prop must have an explicit type signature |
| **NEVER create a default export for React components** | Named exports enable better tree-shaking, refactoring, and import autocompletion |
| **NEVER put business logic inside the component** | Components handle presentation only; logic belongs in hooks, stores, or services |
| **NEVER ignore the existing project conventions** | Match the naming, file structure, and patterns already used in the codebase |
| **NEVER generate files outside the detected component directory** | Respect the project layout; never scatter files across unrelated directories |

## Error Handling

| Situation | Action |
|-----------|--------|
| Component name is not PascalCase | Auto-convert and warn the user (e.g., `user-card` becomes `UserCard`) |
| No framework detected | Default to React with TypeScript. Inform the user and ask to confirm. |
| No component directory found | Create `src/components/` and inform the user of the new directory. |
| Component with the same name already exists | Stop and warn. Ask the user whether to overwrite or choose a different name. |
| Styling approach cannot be determined | Default to vanilla CSS with a plain `.css` file. Inform the user. |
| Test runner not found | Skip test generation even if `--with-tests` was set. Warn the user to install a test runner. |
| Storybook not installed | Skip story generation even if `--with-story` was set. Warn the user to install Storybook. |
| TypeScript check fails after generation | Display the errors and offer to fix them before finishing. |

## Output

- Component file — `[Name].tsx` (or framework-appropriate extension)
- Types/props file — `[Name].types.ts` (or co-located in the component for Vue/Svelte)
- Test file (optional) — `[Name].test.tsx` when `--with-tests` is set
- Story file (optional) — `[Name].stories.tsx` when `--with-story` is set
- Barrel export — `index.ts` re-exporting the component and its types

## Related

- **Skill:** `shadcn-ui` (for installing pre-built accessible components)
- **Skill:** `ui-ux-pro-max` (for design guidance, palettes, and layout patterns)
- **Skill:** [`ui-design`](ai/skills/design-systems/ui-design/SKILL.md) (UI design fundamentals)
- **Skill:** [`react-composition`](ai/skills/frontend/react-composition/SKILL.md) (composition patterns for scalable components)
- **Skill:** [`responsive-design`](ai/skills/frontend/responsive-design/SKILL.md) (responsive layout strategies)
- **Command:** `/new-feature` (for full feature workflows that include component creation)
