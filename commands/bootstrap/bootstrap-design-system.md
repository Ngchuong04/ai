---
name: bootstrap-design-system
model: standard
description: Initialize design system structure
usage: /bootstrap-design-system
---

# /bootstrap-design-system

Set up design system infrastructure for a project.

## Usage

```
/bootstrap-design-system
```

## Examples

```
/bootstrap-design-system       # Initialize design system files
```

## What It Does

1. **Creates** `styles/` directory with token files
2. **Generates** `globals.css` with CSS variable structure
3. **Creates** `design-tokens.ts` for TypeScript exports
4. **Updates** or creates `tailwind.config.ts` with token references
5. **Creates** `components/ui/` with base primitives
6. **Generates** `docs/design-system.md` documentation

## Output Locations

```
styles/
├── globals.css                # CSS variables (source of truth)
├── design-tokens.ts           # TypeScript exports
└── theme.css                  # Component patterns

tailwind.config.ts             # Token integration

components/ui/
├── surface.tsx                # Surface primitive with CVA
├── skeleton.tsx               # Loading states
└── button.tsx                 # Button variants

docs/
└── design-system.md           # Aesthetic documentation
```

## Template Content

### globals.css
```css
:root {
  /* Colors */
  --primary: 200 90% 65%;
  --background: 222 47% 11%;
  --foreground: 210 40% 98%;
  
  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

### tailwind.config.ts
```typescript
colors: {
  primary: 'hsl(var(--primary))',
  background: 'hsl(var(--background))',
  foreground: 'hsl(var(--foreground))',
}
```

## Next Steps

1. **Document aesthetic** — Fill in `docs/design-system.md`
2. **Define palette** — Update CSS variables
3. **Choose typography** — Set font families
4. **Build Surface** — Customize surface primitive
5. **Add motion** — Define animation tokens

## Related

- **Meta-skill:** [`ai/skills/meta/design-system-creation/`](ai/skills/meta/design-system-creation/)
- **Agent:** [`ai/agents/design-system/`](ai/agents/design-system/)
- **Skills:** [`ai/skills/design-systems/`](ai/skills/design-systems/)
- **Skill:** [`ui-design`](ai/skills/design-systems/ui-design/SKILL.md) (UI design fundamentals and principles)
- **Skill:** [`ui-ux-pro-max`](ai/skills/design-systems/ui-ux-pro-max/SKILL.md) (comprehensive UI/UX design intelligence)