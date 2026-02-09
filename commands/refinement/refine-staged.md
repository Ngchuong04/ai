---
name: refine-staged
model: reasoning
description: Process and consolidate all staged content
usage: /refine-staged
---

# /refine-staged

Consolidate staged skills into production-ready patterns.

## Usage

```
/refine-staged
```

## Examples

```
/refine-staged                 # Process all staged content
```

## When to Use

- After extracting patterns from **multiple projects**
- Staging folder has 5+ skills ready for consolidation
- Want to identify overlaps and merge similar patterns
- Ready to promote multiple skills at once
- For **single skill** promotion, use `/promote-skill` instead

**Prerequisites:**
- Content exists in `ai/staging/skills/` or `ai/staging/docs/`
## What It Does

1. **Inventories** all content in `ai/staging/skills/` and `ai/staging/docs/`
2. **Identifies** overlapping patterns across projects
3. **Analyzes** which skills share common approaches
4. **Applies** consolidation rules (merge, keep, archive)
5. **Verifies** each skill against quality criteria
6. **Promotes** refined skills to `ai/skills/[category]/`
7. **Updates** methodology docs with new patterns
8. **Cleans** staging folder after promotion

## Consolidation Rules

| Scenario | Action |
|----------|--------|
| Same pattern, different values | Create pattern skill with examples |
| Same pattern, same approach | Merge into single skill |
| Unique pattern, high value | Keep as standalone |
| Unique pattern, low value | Archive to `ai/archive/` |

## Quality Criteria

Before promotion, each skill must pass:

- [ ] >70% expert knowledge (not in base model)
- [ ] <300 lines (max 500)
- [ ] Has WHAT, WHEN, KEYWORDS in description
- [ ] Includes specific NEVER Do list
- [ ] Project-agnostic (no hardcoded names)

## Output Locations

- Consolidated skills → `ai/skills/[category]/`
- Methodology updates → `docs/METHODOLOGY.md`
- Archived content → `ai/archive/`
- Cleaned staging → `ai/staging/`

## Related

- **Skill:** [`ai/skills/refinement/SKILL.md`](ai/skills/refinement/SKILL.md)
- **Agent:** [`ai/agents/refinement/`](ai/agents/refinement/)
- **Quality criteria:** [`ai/skills/extraction/references/skill-quality-criteria.md`](ai/skills/extraction/references/skill-quality-criteria.md)