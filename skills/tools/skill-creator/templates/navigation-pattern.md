---
name: your-skill-name
description: <!-- CUSTOMIZE: Write a clear description covering what this skill knows and when to use it. Include specific trigger keywords and phrases. For navigation skills, list the domains/topics covered so Claude can match user queries accurately. -->
---

# <!-- CUSTOMIZE: Skill Title -->

<!-- CUSTOMIZE: One sentence positioning this skill as a knowledge resource. Example: "Comprehensive guide for [domain] covering [scope]." -->

## When Invoked

<!-- CUSTOMIZE: Define the entry point. Navigation skills typically start with classification - what is the user asking about? -->

1. Classify the request into a category from the catalog below
2. Load the relevant section or reference file
3. Apply the guidance to the user's specific context

<!-- CUSTOMIZE: If some requests fall outside this skill's scope, add routing here. -->

**Out of scope:** For <!-- CUSTOMIZE: adjacent topic -->, use <!-- CUSTOMIZE: other skill --> instead.

## Quick Reference

<!-- CUSTOMIZE: A scannable lookup table covering the most common items. This is the core of a navigation skill - users need to find the right thing fast. -->

| <!-- CUSTOMIZE: Item --> | Use For | Key Details |
|--------------------------|---------|-------------|
| <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> |
| <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> |
| <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> |
| <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> |
| <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> | <!-- CUSTOMIZE --> |

<!-- CUSTOMIZE: For large catalogs (10+ items), move the full catalog to references/ and keep only the top 5-8 here with a link: "For complete catalog: See [full-catalog.md](references/full-catalog.md)" -->

## Categories

<!-- CUSTOMIZE: Organize knowledge into 3-6 categories. Each category groups related items and provides enough context to select the right one. -->

### Category 1: <!-- CUSTOMIZE: Category Name -->

<!-- CUSTOMIZE: Brief description of when this category applies. -->

**<!-- CUSTOMIZE: Item A -->**
- When to use: <!-- CUSTOMIZE: Specific trigger or context -->
- Key considerations: <!-- CUSTOMIZE -->
- Example: <!-- CUSTOMIZE: Brief concrete example -->

**<!-- CUSTOMIZE: Item B -->**
- When to use: <!-- CUSTOMIZE -->
- Key considerations: <!-- CUSTOMIZE -->
- Example: <!-- CUSTOMIZE -->

### Category 2: <!-- CUSTOMIZE: Category Name -->

<!-- CUSTOMIZE: Repeat the pattern. Keep each item to 3-4 lines. Detailed guidance belongs in reference files. -->

**<!-- CUSTOMIZE: Item C -->**
- When to use: <!-- CUSTOMIZE -->
- Key considerations: <!-- CUSTOMIZE -->
- Example: <!-- CUSTOMIZE -->

**<!-- CUSTOMIZE: Item D -->**
- When to use: <!-- CUSTOMIZE -->
- Key considerations: <!-- CUSTOMIZE -->
- Example: <!-- CUSTOMIZE -->

### Category 3: <!-- CUSTOMIZE: Category Name -->

**<!-- CUSTOMIZE: Item E -->**
- When to use: <!-- CUSTOMIZE -->
- Key considerations: <!-- CUSTOMIZE -->
- Example: <!-- CUSTOMIZE -->

## Selection Guide

<!-- CUSTOMIZE: Help Claude pick the right item when the user's intent is ambiguous. Use a decision tree, matrix, or conditional logic. -->

To select the right approach:

1. **What is the primary goal?**
   - <!-- CUSTOMIZE: Goal A --> -> Use <!-- CUSTOMIZE: Item -->
   - <!-- CUSTOMIZE: Goal B --> -> Use <!-- CUSTOMIZE: Item -->
   - <!-- CUSTOMIZE: Goal C --> -> Use <!-- CUSTOMIZE: Item -->

2. **What constraints apply?**
   - <!-- CUSTOMIZE: Constraint --> -> Prefer <!-- CUSTOMIZE: Item -->
   - <!-- CUSTOMIZE: Constraint --> -> Prefer <!-- CUSTOMIZE: Item -->

## Implementation Notes

<!-- CUSTOMIZE: Common patterns that apply across categories. Keep brief - detailed examples go in references. -->

### Common Pattern: <!-- CUSTOMIZE -->

<!-- CUSTOMIZE: A reusable pattern that applies to multiple items in the catalog. -->

```
<!-- CUSTOMIZE: Code or markup example -->
```

### Common Pattern: <!-- CUSTOMIZE -->

<!-- CUSTOMIZE: Another reusable pattern. -->

```
<!-- CUSTOMIZE: Code or markup example -->
```

## Combination Patterns

<!-- CUSTOMIZE: Show how items can be combined. Navigation skills often involve using multiple items together. Remove if not applicable. -->

| Scenario | Combine |
|----------|---------|
| <!-- CUSTOMIZE: Use case --> | <!-- CUSTOMIZE: Item --> + <!-- CUSTOMIZE: Item --> |
| <!-- CUSTOMIZE: Use case --> | <!-- CUSTOMIZE: Item --> + <!-- CUSTOMIZE: Item --> |

## Resources

<!-- CUSTOMIZE: Reference files allow progressive loading - keep SKILL.md as the index, move detailed content to references. -->

### references/

| Reference | Description | When to Read |
|-----------|-------------|--------------|
| [full-catalog.md](references/full-catalog.md) | <!-- CUSTOMIZE: Complete item catalog with detailed examples --> | <!-- CUSTOMIZE: When the quick reference above is insufficient --> |
| [examples.md](references/examples.md) | <!-- CUSTOMIZE: Detailed implementation examples --> | <!-- CUSTOMIZE: When implementing specific items --> |

<!-- CUSTOMIZE: For very large knowledge bases, organize references by category:
- [category-1.md](references/category-1.md) - Detailed guide for Category 1
- [category-2.md](references/category-2.md) - Detailed guide for Category 2
This way Claude only loads the relevant category. -->
