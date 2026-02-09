---
name: accessibility-audit
model: standard
description: Audit a file or component against WCAG 2.1 AA accessibility standards
usage: /accessibility-audit <file-or-component> [--level <AA|AAA>] [--fix]
---

# /accessibility-audit

Run a quick accessibility audit against WCAG 2.1 AA standards and generate a categorized report with fix suggestions.

## Usage

```
/accessibility-audit <file-or-component> [--level <AA|AAA>] [--fix]
```

**Arguments:**
- `file-or-component` — Path to the file or component to audit (e.g., `src/components/LoginForm.tsx`, `app/page.tsx`)
- `--level <AA|AAA>` — WCAG conformance level to audit against (default: `AA`)
- `--fix` — Automatically apply fixes for issues that have safe, unambiguous solutions

## Examples

```
/accessibility-audit src/components/LoginForm.tsx
/accessibility-audit app/(marketing)/pricing/page.tsx --level AAA
/accessibility-audit src/components/navbar/ --fix
/accessibility-audit src/components/Modal.tsx --fix --level AA
```

## When to Use

- Before shipping a component or page to production
- After receiving a design handoff and implementing the UI
- When a user reports accessibility issues
- During a code review focused on frontend quality
- As part of a pre-launch checklist

## What It Does

1. **Reads** the target file(s) and parses the rendered structure
2. **Checks** against WCAG 2.1 requirements across eight categories
3. **Categorizes** findings by severity: Critical, High, Medium, Low
4. **Generates** a report with issue descriptions, locations, and fix suggestions
5. **Applies** safe fixes automatically when `--fix` is set

## Implementation Steps

### Phase 1: Read and Parse

- Read the target file(s) using `Read`. If a directory is given, audit all component files within it.
- Identify the framework (React, Vue, Svelte, etc.) to understand the rendering model.
- Map the component structure: elements, attributes, event handlers, styles.

### Phase 2: Run Checks

Audit against the following categories, drawn from the ui-design and web-design skills:

| Category | What to Check |
|----------|---------------|
| **Color Contrast** | Text/background contrast ratios — 4.5:1 for normal text, 3:1 for large text (≥18px or ≥14px bold). Check all color combinations including hover/focus states. |
| **Keyboard Navigation** | All interactive elements reachable via Tab. Logical tab order follows visual layout. Focus is visible on every focusable element. No keyboard traps. |
| **Semantic HTML** | Correct elements used (`<button>` not `<div onClick>`; `<a>` for navigation; `<nav>`, `<main>`, `<header>`, `<footer>` for landmarks). Heading hierarchy is sequential (no skipped levels). |
| **Images and Media** | All `<img>` elements have `alt` text. Decorative images use `alt=""` or `aria-hidden`. Videos have captions or transcripts. |
| **Touch Targets** | Interactive elements are at least 44×44px. Adequate spacing between adjacent targets to prevent mis-taps. |
| **Motion Safety** | Animations and transitions respect `prefers-reduced-motion`. No auto-playing motion that can't be paused. No content that flashes more than 3 times per second. |
| **ARIA Usage** | ARIA attributes used only when native HTML semantics are insufficient. Roles, states, and properties are correct and complete. `aria-label` or `aria-labelledby` present when visual labels are absent. |
| **Forms** | Every input has an associated `<label>`. Required fields are marked with `aria-required`. Error messages are linked with `aria-describedby`. Form validation errors are announced to screen readers. |

### Phase 3: Categorize Findings

Assign each issue a severity:

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Blocks access for users with disabilities | Missing form labels, keyboard traps, no alt text on informational images, `<div>` buttons with no role or keyboard handling |
| **High** | Significant barrier, workaround may exist | Low contrast text, missing focus indicators, skip-nav absent, heading hierarchy broken |
| **Medium** | Degraded experience, still usable | Touch targets slightly undersized, decorative images not hidden, redundant ARIA roles |
| **Low** | Best-practice improvement | Missing `lang` attribute, inconsistent focus styles, verbose alt text, missing landmark regions |

### Phase 4: Generate Report

Output a structured report:

```
Accessibility Audit: [component/file]
======================================
Standard: WCAG 2.1 [AA|AAA]
Files audited: N

Summary:
  Critical: N issues
  High:     N issues
  Medium:   N issues
  Low:      N issues

────────────────────────────────────
CRITICAL ISSUES
────────────────────────────────────

[C1] Missing form label
  File: src/components/LoginForm.tsx:42
  Element: <input type="email" placeholder="Email" />
  Rule: WCAG 1.3.1 (Info and Relationships)
  Fix: Add an associated <label> element or aria-label attribute

  Suggested fix:
    <label htmlFor="email">Email</label>
    <input id="email" type="email" placeholder="Email" />

────────────────────────────────────
HIGH ISSUES
────────────────────────────────────

[H1] Insufficient color contrast
  File: src/components/LoginForm.tsx:18
  Element: <p className="text-gray-400">Help text</p>
  Contrast ratio: 3.2:1 (required: 4.5:1)
  Rule: WCAG 1.4.3 (Contrast Minimum)
  Fix: Use text-gray-600 or darker for sufficient contrast

...

────────────────────────────────────
PASSED CHECKS
────────────────────────────────────
✓ Keyboard navigation — all interactive elements focusable
✓ ARIA usage — no misused roles or properties
✓ Motion safety — prefers-reduced-motion respected
```

### Phase 5: Auto-Fix (when `--fix` is set)

Apply fixes only when the correction is unambiguous and safe:

| Safe to Auto-Fix | Not Safe to Auto-Fix |
|------------------|----------------------|
| Add `alt=""` to decorative images | Choose alt text for informational images |
| Add `type="button"` to non-submit buttons | Restructure heading hierarchy |
| Add `aria-hidden="true"` to icon-only decorative elements | Change color palette for contrast |
| Add missing `htmlFor`/`id` pairs on labels and inputs | Rewrite component structure for semantics |
| Wrap animations in `prefers-reduced-motion` | Choose between `aria-label` vs visible label |

After applying fixes, re-run the audit and report the updated counts.

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER add ARIA attributes to fix what semantic HTML would solve** | Prefer native elements (`<button>`, `<nav>`) over `role` attributes on `<div>` |
| **NEVER auto-fix alt text by guessing image content** | Alt text requires understanding the image's purpose in context |
| **NEVER remove focus indicators to "clean up" the UI** | Focus visibility is required for keyboard users |
| **NEVER suppress audit findings without justification** | Every suppression must include a documented reason |

## Output

- Categorized accessibility report with issue locations and fix suggestions
- Updated file(s) with applied fixes when `--fix` is set
- Summary of pass/fail counts

## Related

- **Skill:** `ai/skills/design-systems/ui-design/SKILL.md` — Accessibility requirements and checklist
- **Skill:** `ai/skills/design-systems/web-design/SKILL.md` — Web Interface Guidelines including accessibility
