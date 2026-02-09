# Conflict Resolution Guide

How to detect and resolve conflicts when refining and promoting skills.

---

## When Conflicts Occur

Conflicts arise when:

1. **Staged skill duplicates existing skill** — Same name or purpose
2. **Overlapping patterns** — Similar "When to Use" triggers
3. **Contradicting approaches** — Different solutions to same problem
4. **Naming conflicts** — Same name, different implementations

---

## Conflict Detection Process

### Step 1: Scan Existing Skills

```bash
# List all existing skills
ls -la ai/skills/*/

# Get skill descriptions for comparison
for f in ai/skills/*/SKILL.md; do head -10 "$f"; done
```

### Step 2: Compare Staged Skills

For each staged skill, check:

| Check | Command |
|-------|---------|
| Same name exists? | `ls ai/skills/*/[name]` |
| Similar description? | Compare descriptions manually |
| Overlapping triggers? | Compare "When to Use" sections |

### Step 3: Run Overlap Check

```
/check-overlaps
```

This will report:
- HIGH OVERLAP (>80% similarity) — Likely conflict
- MODERATE OVERLAP (50-80%) — Possible conflict
- LOW OVERLAP (30-50%) — Usually acceptable

---

## Conflict Types and Resolutions

### Type 1: Exact Duplicate

**Signs:**
- Same skill name
- Identical or near-identical description
- Same code examples

**Resolution:**
```
Action: Skip staged skill, keep existing
Rationale: No value in duplicating
```

If staged version is better:
```
Action: Update existing skill with improvements
Command: /update-skill ai/skills/[category]/[name]
```

### Type 2: Similar Purpose, Different Approach

**Signs:**
- Different names but same problem domain
- Similar "When to Use" triggers
- Different code patterns

**Resolution Options:**

| Option | When to Use |
|--------|-------------|
| Merge into one | Approaches are complementary |
| Keep both, clarify | Approaches serve different use cases |
| Archive one | One is clearly inferior |

**Merge strategy:**
1. Create unified skill with best of both
2. Include both approaches as alternatives
3. Add decision tree for when to use each

**Keep both strategy:**
1. Clarify distinct "When to Use" triggers
2. Cross-reference each other in Related
3. Document why they're separate

### Type 3: Overlapping Triggers

**Signs:**
- Same keywords in description
- Similar activation patterns
- User confusion about which to use

**Resolution:**
1. Sharpen trigger specificity
2. Add negative triggers ("NOT for...")
3. Update descriptions to be more distinct

**Example fix:**
```markdown
# Before (conflicting)
Skill A: "Use for React component patterns"
Skill B: "Use for React UI patterns"

# After (distinct)
Skill A: "Use for React state management and data flow patterns"
Skill B: "Use for React visual/styling patterns and animations"
```

### Type 4: Contradicting Advice

**Signs:**
- One skill says "always do X"
- Another skill says "never do X"

**Resolution:**
1. Determine which is correct (or context-dependent)
2. If context-dependent, document when each applies
3. If one is wrong, update or archive it

---

## Merge Strategies

### Additive Merge

When skills cover different aspects of same domain:

```
Skill A: Token architecture
Skill B: Component patterns
→ Combined: Design system patterns (tokens + components)
```

### Alternative Merge

When skills offer different approaches:

```markdown
## Pattern A: Token-first approach
[Content from Skill A]

## Pattern B: Component-first approach
[Content from Skill B]

## When to Use Each
| Situation | Use |
|-----------|-----|
| New project | Token-first |
| Existing codebase | Component-first |
```

### Best-of-Both Merge

Cherry-pick best sections:

```
Take from Skill A: Code examples
Take from Skill B: NEVER Do list
Take from Skill A: Decision tree
Combine: When to Use from both
```

---

## Conflict Resolution Workflow

```
┌─────────────────────────────────────────┐
│ 1. Detect conflict with /check-overlaps │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 2. Classify conflict type               │
│    - Exact duplicate?                   │
│    - Similar purpose?                   │
│    - Overlapping triggers?              │
│    - Contradicting advice?              │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 3. Choose resolution strategy           │
│    - Skip staged                        │
│    - Update existing                    │
│    - Merge                              │
│    - Keep both (clarify)                │
│    - Archive inferior                   │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 4. Execute resolution                   │
│    - /update-skill or manual merge      │
│    - Update descriptions                │
│    - Add cross-references               │
└───────────────┬─────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────┐
│ 5. Verify with /check-overlaps          │
│    - Overlap should be LOW or NONE      │
└─────────────────────────────────────────┘
```

---

## After Resolution

### Update Cross-References

If keeping both skills:
```markdown
## Related Skills

- **Alternative:** [other-skill](path) — Use when [different context]
```

### Document Decision

In the merged/updated skill:
```markdown
<!-- 
Consolidated from:
- project-a-pattern (staged 2024-01-15)
- project-b-pattern (staged 2024-01-15)
Resolution: Merged - complementary approaches
-->
```

### Verify Triggers

Test that both skills now trigger on distinct inputs:
```
Test 1: "I need to [Skill A trigger]" → Should suggest Skill A only
Test 2: "I need to [Skill B trigger]" → Should suggest Skill B only
```

---

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|--------------|-----|
| Keeping both without clarifying | User confusion | Add distinct triggers |
| Merging incompatible approaches | Contradictions | Keep separate or pick one |
| Deleting without archiving | Lose valuable content | Archive first |
| Ignoring overlap | Skills compete for activation | Resolve before promoting |

---

## Related

- **Overlap check:** [`/check-overlaps`](../../../commands/skills/check-overlaps.md)
- **Skill update:** [`/update-skill`](../../../commands/skills/update-skill.md)
- **Archive:** [`/archive-skill`](../../../commands/skills/archive-skill.md)
- **Refinement skill:** [`../SKILL.md`](../SKILL.md)
