---
name: design-system-agent
models:
  discovery: fast
  token_extraction: standard
  analysis: reasoning
  generation: standard
  documentation: fast
description: Autonomous agent for extracting design tokens from codebases or reference sites and generating Tailwind + CSS variable configurations. Use when analyzing existing designs or creating new design systems. Triggers on "extract design system", "analyze design tokens", "create design system from".
---

# Design System Agent

Autonomous workflow for extracting and generating design system configurations.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/skills/extraction/SKILL.md`](ai/skills/extraction/SKILL.md) — Extraction methodology
2. [`ai/skills/design-systems/distinctive-design-systems/SKILL.md`](ai/skills/design-systems/distinctive-design-systems/SKILL.md) — Design system patterns
3. [`ai/skills/meta/design-system-creation/SKILL.md`](ai/skills/meta/design-system-creation/SKILL.md) — Complete workflow
4. [`ai/skills/design-systems/ui-design/SKILL.md`](ai/skills/design-systems/ui-design/SKILL.md) — Comprehensive UI design
5. [`ai/skills/design-systems/ui-ux-pro-max/SKILL.md`](ai/skills/design-systems/ui-ux-pro-max/SKILL.md) — Searchable design database
6. [`ai/skills/design-systems/theme-factory/SKILL.md`](ai/skills/design-systems/theme-factory/SKILL.md) — Theme application
7. [`ai/skills/design-systems/web-design/SKILL.md`](ai/skills/design-systems/web-design/SKILL.md) — CSS patterns
8. [`ai/skills/design-systems/animated-financial-display/SKILL.md`](ai/skills/design-systems/animated-financial-display/SKILL.md) — Animated financial displays

**Verify:**
- [ ] Source path exists and contains design files
- [ ] Backup exists for any files that will be overwritten
- [ ] Target project uses Tailwind (or specify alternative)

---

## Purpose

1. Extract design tokens from existing codebases
2. Analyze reference sites for color/typography patterns
3. Generate Tailwind config + CSS variables
4. Create component library scaffolding

---

## Activation

```
"extract design system from [path]"
"analyze design tokens in [project]"
"create design system from [reference]"
```

---

## Workflow

### Phase 1: Discovery

**Run:** `/bootstrap-design-system` to create initial structure

Scan for design-related files:

```
*.css, *.scss           # CSS variables, color definitions
tailwind.config.*       # Existing Tailwind configuration
**/tokens.*             # Design token files
**/theme.*              # Theme configurations
**/colors.*             # Color palettes
```

**Validation:**
- [ ] At least one CSS or config file found
- [ ] Source directory structure documented
- [ ] Existing design patterns identified

### Phase 2: Token Extraction

**Run:** `/extract-design-tokens [source-path]` to parse design files

Extract from CSS:
- CSS custom properties (--color-*, --font-*, --spacing-*)
- Color values (hex, hsl, rgb)
- Font stacks
- Spacing values
- Border radius
- Shadow definitions

Extract from Tailwind:
- Custom colors
- Font families
- Extended spacing
- Custom animations

**Validation:**
- [ ] Token count > 0 for at least colors or typography
- [ ] All color values normalized to consistent format (hsl preferred)
- [ ] No duplicate token names with conflicting values

### Phase 3: Analysis

**Run:** `/analyze-design-patterns` to categorize and identify scales

Categorize tokens:

| Category | Tokens Found |
|----------|-------------|
| Colors | --primary, --secondary, --background |
| Typography | --font-sans, --font-mono |
| Spacing | --space-1 through --space-12 |
| Motion | --duration-fast, --ease-out |

Identify patterns:
- Color scale (50-950)
- Typography scale
- Spacing scale

**Validation:**
- [ ] Tokens organized into logical categories
- [ ] Color scales identified (semantic + numeric)
- [ ] Aesthetic foundation articulated

### Phase 4: Generation

**Run:** `/generate-design-system-config` to create output files

Generate outputs:

**globals.css**
```css
:root {
  /* Extracted color tokens */
  --primary: [value];
  --secondary: [value];
  /* ... */
}
```

**tailwind.config.ts**
```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: 'hsl(var(--primary))',
        // ...
      },
    },
  },
};
```

**design-tokens.ts**
```typescript
export const colors = {
  primary: 'hsl(var(--primary))',
  // ...
};
```

**Validation:**
- [ ] CSS variables defined in globals.css
- [ ] Tailwind config references CSS variables (not hardcoded values)
- [ ] TypeScript exports compile without errors
- [ ] No duplicate variable declarations

### Phase 5: Documentation

**Run:** `/generate-design-docs [project-name]` to create documentation

Generate design system doc:

```markdown
# Design System: [Project Name]

## Aesthetic Foundation
[Inferred from colors and patterns]

## Color Tokens
[Table of extracted colors]

## Typography
[Font stack and scale]

## Implementation
[File locations and usage]
```

**Validation:**
- [ ] Design system doc created in docs/extracted/
- [ ] All token categories documented with examples
- [ ] Usage instructions included
- [ ] Aesthetic foundation clearly articulated

---

## Outputs

- `styles/globals.css` with CSS variables
- `tailwind.config.ts` with token integration
- `styles/design-tokens.ts` with TypeScript exports
- `docs/extracted/[project]-design-system.md`

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No CSS files found | Check for alternative locations (src/styles, app/, public/) |
| Tailwind not configured | Note: may need to extract raw CSS instead of Tailwind tokens |
| Conflicting token names | Rename with project prefix (e.g., --myapp-primary) |
| No color tokens found | Look for inline styles, component-level CSS, or CSS-in-JS |
| Mixed color formats | Normalize all to hsl() for consistency |
| Incomplete font stacks | Add fallback system fonts to extracted font-family |
| Missing spacing scale | Generate from existing values or use 4px base unit |
| Duplicate variable names | Consolidate and document in design system doc |
| TypeScript compile errors | Check for missing type definitions or syntax issues |
| Tailwind config syntax errors | Validate against Tailwind v3/v4 schema |

---

## Quality Checklist

Before completing, verify:

- [ ] All extracted tokens are organized into scales (50-950 for colors)
- [ ] CSS variables follow consistent naming (--color-*, --font-*, --space-*)
- [ ] Tailwind config correctly references CSS variables
- [ ] TypeScript tokens are type-safe
- [ ] Design system doc includes aesthetic foundation
- [ ] No hardcoded color values in generated files
- [ ] Original files backed up if modified

---

## Related

- **Commands:** [`ai/commands/bootstrap/bootstrap-design-system.md`](ai/commands/bootstrap/bootstrap-design-system.md)
- **Skills:** [`ai/skills/design-systems/`](ai/skills/design-systems/)
- **Meta-skill:** [`ai/skills/meta/design-system-creation/`](ai/skills/meta/design-system-creation/)
- **UI Design:** [`ai/skills/design-systems/ui-design/SKILL.md`](ai/skills/design-systems/ui-design/SKILL.md)
- **UI/UX Database:** [`ai/skills/design-systems/ui-ux-pro-max/SKILL.md`](ai/skills/design-systems/ui-ux-pro-max/SKILL.md)
- **Themes:** [`ai/skills/design-systems/theme-factory/SKILL.md`](ai/skills/design-systems/theme-factory/SKILL.md)
- **CSS Patterns:** [`ai/skills/design-systems/web-design/SKILL.md`](ai/skills/design-systems/web-design/SKILL.md)
- **Financial Displays:** [`ai/skills/design-systems/animated-financial-display/SKILL.md`](ai/skills/design-systems/animated-financial-display/SKILL.md)

---

## NEVER Do

- **Overwrite existing config without backup** — Always backup first
- **Generate tokens without organizing into scales** — Scales enable consistency
- **Skip documentation generation** — Design systems need docs
- **Ignore existing token naming conventions** — Match project style
- **Use hardcoded values** — Always reference CSS variables
- **Skip aesthetic documentation** — Vibes before code
