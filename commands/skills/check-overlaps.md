---
name: check-overlaps
model: standard
description: Find redundant or overlapping skills
usage: /check-overlaps [category]
---

# /check-overlaps

Find redundant or overlapping skills in the library.

## Usage

```
/check-overlaps [category]
```

**Arguments:**
- `category` — Specific category to check (optional, checks all if omitted)

## Examples

```
/check-overlaps                # Check all categories
/check-overlaps ai-chat        # Check AI chat skills only
/check-overlaps design-systems # Check design system skills only
```

## When to Use

- **Before promoting** new skills (check for duplicates first)
- **After adding multiple skills** to ensure no redundancy
- **During periodic cleanup** of the skill library
- When skills seem to conflict or cover similar ground
- Before archiving to understand impact

## What It Does

1. **Scans** all skills in specified category (or all categories)
2. **Analyzes** skill descriptions for keyword overlap
3. **Compares** "When to Use" triggers
4. **Identifies** skills with similar patterns
5. **Reports** potential overlaps with similarity score
6. **Suggests** consolidation opportunities

## Sample Output

```
Checking for overlaps in: ai/skills/

Potential Overlaps Found:

1. HIGH OVERLAP (85% similarity):
   - ai-chat/vercel-ai-chat-integration
   - ai-chat/ai-streaming-routes
   Reason: Both cover streaming chat patterns
   Suggestion: Verify distinct use cases or consolidate

2. MODERATE OVERLAP (60% similarity):
   - design-systems/distinctive-design-systems
   - design-systems/design-system-components
   Reason: Overlapping component patterns
   Suggestion: Clear - one is tokens, one is components

3. LOW OVERLAP (40% similarity):
   - realtime/websocket-hub-patterns
   - realtime/resilient-connections
   Reason: Both mention connection handling
   Suggestion: Acceptable - different focus areas

Summary:
  Skills checked: 25
  High overlaps:  1
  Moderate:       2
  Low:            3
```

## Overlap Thresholds

| Level | Similarity | Action |
|-------|------------|--------|
| High | >80% | Review for consolidation |
| Moderate | 50-80% | Verify distinct purposes |
| Low | 30-50% | Usually acceptable |
| None | <30% | No action needed |

## What Gets Compared

- Description keywords
- "When to Use" triggers
- Code pattern similarity
- Referenced technologies

## Output Locations

- No files created — displays to terminal only

## Related

- **Validate skill:** `/validate-skill` (check individual skill)
- **Refine staged:** `/refine-staged` (consolidates during promotion)