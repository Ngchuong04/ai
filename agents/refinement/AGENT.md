---
name: refinement-agent
models:
  inventory: fast
  pattern_analysis: reasoning
  consolidation: reasoning
  quality_check: standard
  promotion: fast
  cleanup: fast
description: Autonomous agent for consolidating and refining extracted skills from staging into production-ready, project-agnostic patterns. Use when staging has content ready for consolidation. Triggers on "refine staged content", "consolidate skills", "process staging".
---

# Refinement Agent

Autonomous workflow for consolidating staged skills into production-ready patterns.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/skills/refinement/SKILL.md`](ai/skills/refinement/SKILL.md) — Refinement methodology
2. [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md) — Quality requirements

**Verify:**
- [ ] `ai/staging/skills/` contains content to process
- [ ] `ai/staging/docs/` checked for methodology updates
- [ ] Target categories exist in `ai/skills/`

---

## Purpose

Take extracted skills and docs from multiple projects and:
1. Identify overlapping patterns
2. Consolidate into project-agnostic skills
3. Apply quality criteria
4. Update methodology docs
5. Promote to active locations

---

## Activation

```
"refine staged content"
"consolidate staged skills"
"process staging folder"
```

---

## Workflow

### Phase 1: Inventory

Scan staging and catalog contents:

```
ai/staging/
├── skills/           # Extracted skills
│   ├── [project-a]-[category]/
│   ├── [project-b]-[category]/
└── docs/             # Methodology docs
    ├── [project-a]-summary.md
    └── [project-a]-design-system.md
```

Create inventory table:
| Source | Type | Content | Common Patterns? |
|--------|------|---------|------------------|
| project-a | skill | design-system | Yes |
| project-b | skill | design-system | Yes |

**Run:** `/list-staging` to enumerate all staged content

**Validation:** Inventory table completed with all staged content cataloged

### Phase 2: Pattern Analysis

Identify patterns across projects:

1. **Design system patterns** (highest priority)
   - Common token structures
   - Similar aesthetic approaches

2. **Architecture patterns**
   - Similar folder structures
   - Common data flow patterns

3. **Workflow patterns**
   - Common Makefile targets
   - Similar CI/CD approaches

**Run:** `/analyze-patterns [category]` to identify cross-project patterns

**Validation:** Pattern analysis documented with similarity scores for each category

### Phase 3: Consolidation

Apply consolidation rules:

| Scenario | Action |
|----------|--------|
| Same pattern, different values | Create pattern skill with examples |
| Same pattern, same approach | Merge into single skill |
| Unique pattern, high value | Keep as standalone |
| Unique pattern, low value | Archive or discard |

**Run:** `/merge-skills [skill-a] [skill-b] --output [name]` for similar skills

**Run:** `/archive-skill [path]` for low-value unique patterns

**Validation:** All overlapping patterns consolidated; no duplicate skills remain in staging

### Phase 4: Quality Check

Verify against quality criteria:

- [ ] >70% expert knowledge (not in base model)
- [ ] <300 lines (max 500)
- [ ] Has WHAT, WHEN, KEYWORDS in description
- [ ] Includes specific NEVER list
- [ ] Project-agnostic (no hardcoded names)

**Run:** `/check-overlaps` before promotion to detect conflicts with existing skills

**Run:** `/validate-skill [path]` to verify each skill meets quality criteria

**Validation:** All skills pass quality check with no overlap warnings

### Phase 5: Promotion

Move refined skills to active:

```bash
mv ai/staging/skills/[refined-skill]/ ai/skills/[category]/
```

Update methodology docs with insights.

**Run:** `/promote-skill [name] [category]` for each refined skill

**Run:** `/update-methodology` to sync docs with new patterns

**Validation:** Skills appear in `ai/skills/[category]/`; methodology docs updated

### Phase 6: Cleanup

```bash
rm -rf ai/staging/skills/*
rm -rf ai/staging/docs/*
```

**Run:** `/clean-staging` to remove processed content

**Validation:** Staging folders empty; all content either promoted or archived

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| Staging empty | Run extraction first; see extraction agent |
| Quality check fails | Return skill to staging for improvement |
| Similar skill exists | Merge into existing or archive duplicate |
| Pattern analysis unclear | Break into smaller categories; re-analyze |
| Promotion conflicts | Use `/check-overlaps` to identify; resolve manually |
| Methodology out of sync | Run `/update-methodology` to reconcile |

---

## Outputs

- Consolidated skills in `ai/skills/[category]/`
- Updated `docs/METHODOLOGY.md`
- Clean staging folder

---

## Quality Checklist

Before completing, verify each promoted skill:

- [ ] >70% expert knowledge (not in base Claude model)
- [ ] <300 lines (max 500)
- [ ] Description has WHAT, WHEN, KEYWORDS
- [ ] Includes specific NEVER Do list
- [ ] Project-agnostic (no hardcoded project names)
- [ ] Has "When to Use" section
- [ ] Has code examples (if applicable)
- [ ] Placed in correct category folder

After promotion:
- [ ] Methodology docs updated with new patterns
- [ ] Staging folder cleaned
- [ ] No duplicate skills created

---

## Related

- **Commands:** [`ai/commands/refinement/`](ai/commands/refinement/)
- **Skills:** [`ai/skills/refinement/SKILL.md`](ai/skills/refinement/SKILL.md)
- **Quality criteria:** [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md)
- **Skill Judge:** [`ai/skills/tools/skill-judge/SKILL.md`](ai/skills/tools/skill-judge/SKILL.md) — Quality validation during refinement
- **Production Readiness:** [`ai/skills/meta/production-readiness/SKILL.md`](ai/skills/meta/production-readiness/SKILL.md)

---

## NEVER Do

- **Keep project-specific details** — Strip all project names and paths
- **Create redundant skills** — Check for overlaps before promoting
- **Skip methodology updates** — New patterns should update docs
- **Promote low-quality skills** — Apply quality criteria strictly
- **Leave staging cluttered** — Clean up after promotion
- **Merge without analyzing patterns** — Identify common patterns first
