# /refine-staged

Process staged skills and docs from multiple projects into consolidated patterns.

## Usage

```
/refine-staged
```

## Prerequisites

Staging folders should have content from multiple projects:

```
ai/staging/
├── skills/
│   ├── project-a-design-system/
│   ├── project-b-ui-patterns/
│   └── ...
└── docs/
    ├── project-a-summary.md
    ├── project-b-design-system.md
    └── ...
```

## What It Does

1. **Inventories** all staged skills and docs
2. **Analyzes** for patterns across projects
3. **Consolidates** similar patterns into unified skills
4. **Updates** methodology docs with insights
5. **Promotes** refined skills to active locations
6. **Cleans** staging folder

## Output

**Refined skills:**
```
ai/skills/[consolidated-pattern]/
```

**Updated docs:**
```
docs/METHODOLOGY.md   # New insights
docs/TECH-STACK.md    # New patterns
```

## Example

After extracting from 3 projects with design systems:

```
# Before refinement
ai/staging/skills/
├── project-a-design-system/
├── project-b-design-system/
└── project-c-design-system/

# After refinement
ai/skills/
└── distinctive-design-systems/  # Consolidated, project-agnostic
```

## Related

- Full skill: [`SKILL.md`](SKILL.md)
- Extraction skill: [`../extraction/SKILL.md`](../extraction/SKILL.md)
- Staging README: [`../../staging/README.md`](../../staging/README.md)
