---
name: cro-audit
model: reasoning
description: Run a conversion rate optimization audit on a page, scoring each area and generating prioritized recommendations
usage: /cro-audit [page-file-or-url] [--type <landing|signup|pricing|onboarding>]
---

# /cro-audit

Run a structured CRO audit on any page, scoring key conversion factors and generating prioritized, actionable recommendations.

## Usage

```
/cro-audit [page-file-or-url] [--type <landing|signup|pricing|onboarding>]
```

**Arguments:**
- `page-file-or-url` — Path to a page file in the project (e.g., `app/page.tsx`) or a URL to audit
- `--type <type>` — Page type to apply the right audit framework: `landing`, `signup`, `pricing`, `onboarding` (auto-detected if omitted)

## Examples

```
/cro-audit app/pricing/page.tsx --type pricing
/cro-audit src/pages/landing.tsx --type landing
/cro-audit app/signup/page.tsx --type signup
/cro-audit app/onboarding/page.tsx --type onboarding
/cro-audit https://example.com/pricing
```

## When to Use

- A page has low conversion rates and you need to diagnose why
- Before launching a new landing page, signup flow, or pricing page
- After a redesign to verify no conversion regressions
- When prioritizing CRO improvements across multiple pages
- During a quarterly optimization review

## What It Does

1. **Analyzes** the page structure, copy, and user flow
2. **Selects** the right CRO framework based on page type
3. **Scores** each conversion factor: Strong / Needs Improvement / Critical Issue
4. **Generates** prioritized recommendations sorted by impact and effort
5. **Identifies** quick wins — low-effort changes with high conversion potential

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Page Analysis

- If the input is a file path, read the file and analyze the component structure, copy, and layout.
- If the input is a URL, use `browser_navigate` to load the page, then `browser_snapshot` to capture the structure.
- Auto-detect page type if `--type` is not specified:

| Signals | Detected Type |
|---------|---------------|
| Pricing tables, plan comparisons, payment references | `pricing` |
| Form with email/password, "Sign up" / "Create account" | `signup` |
| Step indicators, progress bars, welcome messages | `onboarding` |
| Hero section, single CTA, social proof, feature list | `landing` |

### Phase 2: Select Audit Framework

Load the appropriate CRO skill for the detected page type:

| Page Type | Skill | Focus Areas |
|-----------|-------|-------------|
| `landing` | `page-cro` | Above-fold impact, CTA clarity, social proof, value proposition |
| `signup` | `signup-flow-cro` | Form friction, field count, social login, error handling, trust signals |
| `pricing` | `page-cro` | Plan clarity, feature comparison, anchoring, FAQ coverage, CTA per tier |
| `onboarding` | `onboarding-cro` | Time-to-value, progressive disclosure, empty states, activation metrics |

### Phase 3: Score Conversion Factors

Evaluate each factor and assign a score:

| Score | Meaning | Indicator |
|-------|---------|-----------|
| **Strong** | Working well, no changes needed | ✅ |
| **Needs Improvement** | Opportunity for optimization | ⚠️ |
| **Critical Issue** | Likely hurting conversions now | 🔴 |

**Universal factors (all page types):**

| Factor | What to Check |
|--------|--------------|
| **Above-fold content** | Is the value prop clear within 5 seconds? Is there a visible CTA? |
| **CTA clarity** | Is the primary CTA specific, action-oriented, and visually prominent? |
| **Social proof** | Are there testimonials, logos, user counts, or case studies? Are they credible? |
| **Trust signals** | Security badges, guarantees, privacy policies, recognizable logos? |
| **Mobile optimization** | Does the layout, font size, and tap targets work on mobile? |
| **Page speed signals** | Large images, excessive JS, render-blocking resources? |
| **Copy quality** | Benefits over features? Specific over vague? Scannable? |
| **Visual hierarchy** | Clear heading structure? Eye flow guides to CTA? |
| **Friction points** | Unnecessary steps, confusing navigation, information overload? |
| **Objection handling** | Are common objections addressed on the page (FAQ, guarantees, comparisons)? |

**Type-specific factors:**

| Page Type | Additional Factors |
|-----------|-------------------|
| `landing` | Single clear goal, message match with ad/source, urgency elements |
| `signup` | Field count, inline validation, social login, password requirements UX |
| `pricing` | Recommended plan highlight, annual/monthly toggle, feature gating clarity |
| `onboarding` | Progress indication, skip options, personalization, first-value delivery |

### Phase 4: Generate Recommendations

For each "Needs Improvement" or "Critical Issue" factor:

1. **Describe the issue** — what's wrong and why it matters
2. **Recommend a fix** — specific, actionable change
3. **Estimate impact** — High / Medium / Low
4. **Estimate effort** — High / Medium / Low
5. **Prioritize** — sort by impact-to-effort ratio (high impact + low effort first)

### Phase 5: Identify Quick Wins

Extract the top 3–5 changes that are:
- Low effort (copy changes, layout tweaks, adding elements)
- High potential impact (directly affect conversion decision points)
- Implementable immediately (no dependencies on design, data, or engineering)

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER score without evidence** | Every score must reference a specific element or absence on the page |
| **NEVER recommend changes without rationale** | Each recommendation must explain the conversion principle behind it |
| **NEVER ignore mobile** | Over 50% of traffic is mobile — always check responsive behavior |
| **NEVER suggest dark patterns** | No fake urgency, misleading copy, or manipulative tactics |
| **NEVER give only high-level advice** | Recommendations must be specific enough to implement without further research |

## Output

```
CRO Audit: [page name or URL]
==============================
Page Type: [detected or specified type]
Overall Score: X/100

✅ Strong:
- [what's working well — with specific references]

⚠️ Needs Improvement:
- [P1] [recommendation] — Impact: High, Effort: Low
- [P2] [recommendation] — Impact: High, Effort: Medium
- [P3] [recommendation] — Impact: Medium, Effort: Low

🔴 Critical Issues:
- [must-fix item with specific guidance]

⚡ Quick Wins:
1. [low-effort, high-impact change with implementation detail]
2. [low-effort, high-impact change with implementation detail]
3. [low-effort, high-impact change with implementation detail]

📊 Factor Scores:
| Factor              | Score              |
|---------------------|--------------------|
| Above-fold content  | ✅ / ⚠️ / 🔴       |
| CTA clarity         | ✅ / ⚠️ / 🔴       |
| Social proof        | ✅ / ⚠️ / 🔴       |
| Trust signals       | ✅ / ⚠️ / 🔴       |
| Mobile optimization | ✅ / ⚠️ / 🔴       |
| Copy quality        | ✅ / ⚠️ / 🔴       |
| Visual hierarchy    | ✅ / ⚠️ / 🔴       |
| Friction points     | ✅ / ⚠️ / 🔴       |
| Objection handling  | ✅ / ⚠️ / 🔴       |
```

## Related

- **Skill:** [`page-cro`](ai/skills/marketing/page-cro/SKILL.md) — landing and marketing page CRO checklist
- **Skill:** [`signup-flow-cro`](ai/skills/marketing/signup-flow-cro/SKILL.md) — signup and registration flow optimization
- **Skill:** [`onboarding-cro`](ai/skills/marketing/onboarding-cro/SKILL.md) — post-signup activation optimization
- **Agent:** [`marketing`](ai/agents/marketing/AGENT.md) — full marketing agent
- **Command:** `/write-copy` — generate optimized copy for a page
