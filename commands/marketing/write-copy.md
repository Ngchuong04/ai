---
name: write-copy
model: reasoning
description: Create marketing copy for a page or component with persona targeting, psychology frameworks, and A/B test variants
usage: /write-copy [page-type] [--persona <persona>] [--tone <tone>]
---

# /write-copy

Create structured marketing copy for any page type, grounded in persona research and behavioral psychology.

## Usage

```
/write-copy [page-type] [--persona <persona>] [--tone <tone>]
```

**Arguments:**
- `page-type` — The type of page to write copy for: `homepage`, `landing`, `pricing`, `feature`, `about`, `product`
- `--persona <persona>` — Target persona name (reads from persona docs if they exist)
- `--tone <tone>` — Writing tone: `professional`, `casual`, `playful`, `authoritative`, `empathetic` (default: `professional`)

## Examples

```
/write-copy homepage --persona "startup-founder" --tone authoritative
/write-copy landing --tone playful
/write-copy pricing --persona "enterprise-buyer" --tone professional
/write-copy feature --tone casual
/write-copy about --tone empathetic
```

## When to Use

- Writing copy for a new marketing page from scratch
- Rewriting an existing page to improve conversions
- Creating copy variations for A/B testing
- Aligning page messaging with a defined persona
- Launching a new product or feature and need positioning copy

## What It Does

1. **Identifies the target persona** — reads persona docs if they exist in the project, otherwise asks clarifying questions about the audience
2. **Defines value proposition** — distills the core value prop, key benefits, and differentiators
3. **Applies psychology frameworks** — uses loss aversion, social proof, anchoring, and urgency where appropriate
4. **Writes copy sections** — generates headline, subheadline, body copy, CTAs, and social proof blocks
5. **Follows copywriting best practices** — specificity over vagueness, benefits over features, active voice, concrete numbers
6. **Generates headline variants** — produces 2–3 headline variations for A/B testing

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Persona Research

- Use `Glob` to check for persona docs (e.g., `**/persona*.md`, `**/personas/**`).
- If found, read and extract: pain points, goals, language patterns, objections.
- If `--persona` is specified but no docs exist, ask the user for key persona details:
  - Who are they? (role, industry, experience level)
  - What problem are they solving?
  - What objections might they have?
  - What language do they use to describe their problem?

### Phase 2: Value Proposition Framework

Define the following before writing any copy:

| Element | Description |
|---------|-------------|
| **Core promise** | The single most important benefit |
| **Key benefits** | 3–5 specific, measurable benefits |
| **Differentiators** | What sets this apart from alternatives |
| **Objection handlers** | Responses to top 3 buyer objections |
| **Social proof points** | Numbers, testimonials, logos, or case studies to reference |

### Phase 3: Apply Psychology Frameworks

Apply these frameworks where they naturally fit — never force them:

| Framework | Application |
|-----------|-------------|
| **Loss aversion** | Frame what they lose by not acting, not just what they gain |
| **Social proof** | Reference user counts, testimonials, logos, case studies |
| **Anchoring** | Present the most valuable option first to anchor expectations |
| **Urgency/scarcity** | Only if genuine — never fabricate urgency |
| **Cognitive ease** | Short sentences, familiar words, clear structure |
| **Specificity** | "4,000+ teams" beats "thousands of teams" |

### Phase 4: Write Copy Sections

Generate copy for each section appropriate to the page type:

**All page types:**
- **Headline** — Clear, benefit-driven, under 10 words
- **Subheadline** — Expand the headline with specificity, 1–2 sentences
- **CTA (primary)** — Action-oriented, specific ("Start free trial" not "Submit")
- **CTA (secondary)** — Lower-commitment alternative ("See how it works")

**Page-type-specific sections:**

| Page Type | Additional Sections |
|-----------|-------------------|
| `homepage` | Hero, features grid, social proof bar, how-it-works, final CTA |
| `landing` | Hero, problem statement, solution, benefits, testimonials, CTA |
| `pricing` | Plan names, plan descriptions, feature comparison, FAQ, CTA per tier |
| `feature` | Feature hero, use cases, before/after, integration callouts |
| `about` | Origin story, mission, team values, milestones |
| `product` | Product hero, key capabilities, specs, comparison, CTA |

### Phase 5: Apply Copywriting Best Practices

Run a quality check against every section:

| Rule | Check |
|------|-------|
| **Benefits over features** | Every feature is paired with a "so that..." benefit |
| **Active voice** | No passive constructions unless intentional for emphasis |
| **Specificity** | Replace vague claims with concrete numbers or examples |
| **Conversational** | Reads like a human wrote it, not a committee |
| **Scannable** | Short paragraphs, clear headings, bullet points for lists |
| **One idea per section** | Each section has a single, clear message |

### Phase 6: Generate Headline Variants

Produce 2–3 headline alternatives using different angles:

| Variant | Angle |
|---------|-------|
| **Benefit-led** | Leads with the primary outcome |
| **Problem-led** | Leads with the pain point being solved |
| **Social-proof-led** | Leads with credibility or adoption numbers |

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER use jargon without explanation** | Copy must be instantly clear to the target persona |
| **NEVER fabricate social proof or statistics** | Use real numbers or leave placeholders for the user to fill |
| **NEVER write walls of text** | Every section should be scannable with clear hierarchy |
| **NEVER use generic CTAs like "Submit" or "Click Here"** | CTAs must be specific and action-oriented |
| **NEVER ignore the persona** | Every word should resonate with the defined audience |
| **NEVER lead with features** | Always lead with outcomes and benefits |

## Output

Structured copy document in markdown with:

```
Copy Brief: [page-type]
=======================
Persona:    [target persona]
Tone:       [selected tone]
Value Prop: [core promise]

Headline Variants:
  A: [benefit-led headline]
  B: [problem-led headline]
  C: [social-proof-led headline]

Sections:
  [section-by-section copy organized by page type]

CTAs:
  Primary:   [main CTA text]
  Secondary: [alternative CTA text]

Social Proof:
  [suggested social proof elements with placeholders]
```

## Related

- **Skill:** [`copywriting`](ai/skills/marketing/copywriting/SKILL.md) — copy frameworks and natural transitions
- **Skill:** [`marketing-psychology`](ai/skills/marketing/marketing-psychology/SKILL.md) — 70+ mental models for persuasion
- **Skill:** [`persona-docs`](ai/skills/writing/persona-docs/SKILL.md) — persona documentation creation
- **Agent:** [`marketing`](ai/agents/marketing/AGENT.md) — full marketing agent
- **Command:** `/cro-audit` — audit existing copy for conversion optimization
