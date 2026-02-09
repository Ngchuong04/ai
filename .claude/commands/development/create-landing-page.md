---
name: create-landing-page
model: reasoning
description: Scaffold a complete landing page with copy, design system, and implementation
usage: /create-landing-page <product-name> [--style <style>] [--stack <stack>]
---

# /create-landing-page

Scaffold a complete landing page with marketing copy, design system, and a responsive, accessible implementation.

## Usage

```
/create-landing-page <product-name> [--style <style>] [--stack <stack>]
```

**Arguments:**
- `product-name` — Name of the product or project (e.g., `Acme`, `FlowBoard`, `NightOwl`)
- `--style <style>` — Visual style (e.g., `minimal`, `bold`, `elegant`, `playful`, `brutalist`). Defaults to `minimal`.
- `--stack <stack>` — Implementation stack: `html-tailwind`, `nextjs`, `react`, `vue`, `svelte`, `astro`. Defaults to `html-tailwind`.

## Examples

```
/create-landing-page Acme --style minimal --stack html-tailwind
/create-landing-page FlowBoard --style bold --stack nextjs
/create-landing-page NightOwl --style elegant
/create-landing-page DevSync --stack react
/create-landing-page Harvest --style playful --stack astro
```

## When to Use

- Launching a new product or side project and need a landing page fast
- Building a marketing page for an existing product
- Replacing a placeholder or template page with something polished and conversion-optimized
- Prototyping a product concept with a realistic landing page

## What It Does

1. **Gathers** context about the product: name, audience, value proposition, desired style
2. **Generates** a design system with palette, typography, and spacing tokens
3. **Writes** marketing copy for each page section using proven copywriting frameworks
4. **Designs** the layout with proper visual hierarchy and section flow
5. **Implements** the page with the chosen stack — responsive, accessible, and performant
6. **Runs** a CRO checklist to optimize for conversions before delivery

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Gather Context

Ask for or infer the following (skip what's already provided):

| Input | Question | Default |
|-------|----------|---------|
| Product name | What is the product called? | (required) |
| One-liner | What does it do in one sentence? | Inferred from name/context |
| Target audience | Who is this for? | "developers and teams" |
| Value proposition | Why should someone care? | Inferred from description |
| Style | What visual feel? | `minimal` |
| Stack | What tech stack? | `html-tailwind` |

### Phase 2: Generate Design System

Run the ui-ux-pro-max design system generator:

```
python3 ai/skills/design-systems/ui-ux-pro-max/scripts/search.py "<product-name> <style>" --design-system
```

This produces:
- **Color palette** — primary, secondary, accent, neutral, semantic colors
- **Typography** — font pairing, size scale, weight usage
- **Spacing** — consistent spacing scale
- **Component tokens** — border radius, shadow, transition values

Apply the design system as CSS custom properties or Tailwind theme extensions.

### Phase 3: Write Copy

Write copy for each section using copywriting skill principles:

| Section | Content | Framework |
|---------|---------|-----------|
| **Hero** | Headline (benefit-driven, max 10 words), subheadline (clarify the what), primary CTA | PAS or AIDA |
| **Social proof** | Logos, testimonials, or metrics (pick what fits the product maturity) | Authority + Social proof |
| **Features** | 3–6 features with icon, title, and one-sentence description | Feature → Benefit framing |
| **How it works** | 3 steps explaining the user journey | Simplicity bias |
| **CTA section** | Reinforce the value, secondary headline, CTA button | Urgency or loss aversion |
| **Footer** | Links, copyright, optional newsletter signup | Standard layout |

Copy rules:
- Lead with benefits, not features
- Use concrete language — numbers, specifics, outcomes
- Keep headlines under 10 words
- One CTA per section, consistent wording
- Write at an 8th-grade reading level

### Phase 4: Design Layout

Using the ui-design skill, structure the page with:

- **Visual hierarchy** — Hero gets the most visual weight. Each section has a clear focal point.
- **Section rhythm** — Alternate between content-heavy and breathing-room sections.
- **Contrast** — Key sections (hero, CTA) use the primary palette. Supporting sections use neutrals.
- **Whitespace** — Generous padding between sections (80–120px vertical on desktop).
- **Flow** — The page tells a story: problem → solution → proof → action.

### Phase 5: Implement

Build the page with the chosen stack:

| Stack | Output |
|-------|--------|
| `html-tailwind` | Single `index.html` with Tailwind via CDN, inline styles for tokens |
| `nextjs` | `page.tsx` in App Router with component breakdown |
| `react` | `LandingPage.tsx` with sub-components |
| `vue` | `LandingPage.vue` SFC |
| `svelte` | `+page.svelte` with components |
| `astro` | `index.astro` with component islands |

Implementation requirements:
- **Mobile-first** responsive design with breakpoints at 640px, 768px, 1024px, 1280px
- **Accessible** — WCAG 2.1 AA compliance (contrast, keyboard, semantics, alt text)
- **Performant** — No unnecessary JS, optimized images, minimal dependencies
- **Semantic HTML** — Proper landmarks (`<header>`, `<main>`, `<section>`, `<footer>`)
- **Component states** — Hover, focus, and active states on all interactive elements

### Phase 6: CRO Checklist

Before delivery, verify against the page-cro skill checklist:

| Check | Requirement |
|-------|-------------|
| Above the fold | Headline, value prop, and CTA visible without scrolling |
| CTA clarity | Button text is specific ("Start free trial" not "Submit") |
| CTA contrast | Primary CTA visually dominates the page |
| Load time | Page loads in under 3 seconds on 3G |
| Mobile experience | Thumb-friendly CTAs, readable text without zooming |
| Trust signals | Social proof appears before the primary conversion ask |
| Single focus | One primary action per page — don't split attention |
| Objection handling | FAQ or "how it works" section addresses common hesitations |

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER use placeholder copy ("Lorem ipsum")** | Every word on the page should be real, benefit-driven copy |
| **NEVER include more than one primary CTA style** | Multiple competing CTAs reduce conversion |
| **NEVER skip mobile layout** | Over 50% of landing page traffic is mobile |
| **NEVER use stock photo placeholders without noting it** | Mark any placeholder images clearly so they get replaced |
| **NEVER add animations without `prefers-reduced-motion`** | Motion must be safe for users with vestibular disorders |
| **NEVER ignore the existing brand if one exists** | Match established colors, fonts, and voice |

## Output

- Complete landing page file(s) ready to preview
- Design system tokens (CSS custom properties or Tailwind config)
- Copy document with all section text (for review before implementation, if requested)

Summary:

```
Landing Page Created
====================
Product:    [name]
Style:      [style]
Stack:      [stack]
Sections:   Hero, Social Proof, Features, How It Works, CTA, Footer

Files created:
  [list of files]

Design system:
  Primary:    [color]
  Typography: [font pairing]
  
Preview: Open [main file] in browser
```

## Related

- **Skill:** `ai/skills/design-systems/ui-design/SKILL.md` — Typography, color, spacing, visual hierarchy
- **Skill:** `ai/skills/design-systems/ui-ux-pro-max/SKILL.md` — Design system generator with styles and palettes
- **Skill:** `ai/skills/marketing/copywriting/SKILL.md` — Headline frameworks, CTA copy, benefit-driven writing
- **Skill:** `ai/skills/marketing/page-cro/SKILL.md` — Conversion rate optimization checklist
- **Skill:** `ai/skills/frontend/frontend-design/SKILL.md` — Creative direction, distinctive visual output
- **Agent:** `ai/agents/frontend/AGENT.md`
- **Agent:** `ai/agents/marketing/AGENT.md`
