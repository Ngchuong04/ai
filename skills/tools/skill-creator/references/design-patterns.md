# Skill Design Patterns

## Workflow Patterns

### Sequential Workflow
For multi-step processes with clear order:

```markdown
## Workflow

### Step 1: Check Prerequisites
Check if required files exist...

### Step 2: Analyze Input
Read and parse the input...

### Step 3: Generate Output
Create the output based on analysis...

### Step 4: Validate
Run validation checks...
```

### Conditional Workflow
For skills with multiple paths:

```markdown
## Mode Selection

**Mode A**: User wants X
→ Follow Workflow A

**Mode B**: User wants Y  
→ Follow Workflow B

---

## Workflow A
[Steps for mode A]

## Workflow B
[Steps for mode B]
```

### Iterative Workflow
For tasks that repeat until success:

```markdown
## Workflow

1. Run check command
2. If errors found:
   - Apply fixes
   - Go to step 1
3. If no errors: Done

**Stop conditions**:
- Success (no errors)
- Max iterations (10)
- Same error 3 times (stuck)
```

---

## Output Patterns

### Template-Based Output
When skill produces structured output:

```markdown
## Output Format

Use this template:

\`\`\`markdown
# [TITLE]

## Section 1
[CONTENT]

## Section 2  
[CONTENT]
\`\`\`

Fill placeholders based on analysis.
```

### Quality-Gated Output
When output must meet standards:

```markdown
## Quality Criteria

Output must have:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

Do not finalize until all criteria met.
```

### Validation-Required Output
When output needs automated checks:

```markdown
## Validation

Run validation script:
\`\`\`bash
python scripts/validate.py <output-file>
\`\`\`

Fix any issues before finalizing.
```

---

## Reference Patterns

### Domain-Organized References
Organize by topic when skill covers multiple domains:

```
skill/
├── SKILL.md
└── references/
    ├── domain-a.md
    ├── domain-b.md
    └── domain-c.md
```

SKILL.md includes:
```markdown
## References

Load based on user's domain:
- Finance queries: [references/finance.md](references/finance.md)
- Sales queries: [references/sales.md](references/sales.md)
```

### Framework-Organized References
Organize by framework when skill supports multiple options:

```
skill/
├── SKILL.md
└── references/
    ├── react.md
    ├── vue.md
    └── svelte.md
```

### Conditional Loading
Only load references when needed:

```markdown
## Advanced Features

For basic usage, the above is sufficient.

For advanced features:
- **Forms**: Load [references/forms.md](references/forms.md)
- **Validation**: Load [references/validation.md](references/validation.md)
```

---

## Description Patterns

### Standard Format
```yaml
description: |
  WHAT: One sentence describing capability.
  WHEN: Contexts and trigger conditions.
  KEYWORDS: "phrase 1", "phrase 2", "phrase 3"
```

### Multi-Context Format
```yaml
description: |
  WHAT: Create X for Y.
  
  WHEN: 
  (1) User asks for X
  (2) User needs Y
  (3) User mentions Z
  
  KEYWORDS: "create X", "make Y", "generate Z"
```

---

## Anti-Patterns to Avoid

### Information Duplication
❌ Same content in SKILL.md AND references
✅ Content in ONE place only

### Nested References
❌ references/category/subcategory/file.md
✅ references/file.md (one level deep)

### Missing Guidance
❌ Link to reference without explaining when to use
✅ "For form handling, load [forms.md](forms.md)"

### Vague Descriptions
❌ "A skill that helps with things"
✅ "Create X when user asks for Y"
