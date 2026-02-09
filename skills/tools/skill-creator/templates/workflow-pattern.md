---
name: your-skill-name
description: <!-- CUSTOMIZE: Write a clear description of what this skill does AND when to trigger it. Include specific trigger phrases users might say. This is the primary mechanism for skill activation - be comprehensive. -->
---

# <!-- CUSTOMIZE: Skill Title -->

<!-- CUSTOMIZE: One sentence summarizing what this skill does and the value it provides. -->

## Overview

<!-- CUSTOMIZE: 2-3 sentences explaining the workflow at a high level. Describe the input (what the user brings) and the output (what they leave with). -->

## Mode Selection

<!-- CUSTOMIZE: If the skill has distinct modes (e.g., create vs resume, analyze vs generate), add branching logic here. Remove this section if the skill is single-mode. -->

Determine which mode applies:

**Mode A?** <!-- CUSTOMIZE: Condition description -->
- Follow: Mode A Workflow below

**Mode B?** <!-- CUSTOMIZE: Condition description -->
- Follow: Mode B Workflow below

## Workflow

<!-- CUSTOMIZE: Replace these phases with your actual workflow steps. Each phase should have a clear entry condition, actions, and exit/quality gate. -->

The process involves these steps:

1. Understand the request
2. Gather context
3. Execute the core task
4. Validate the output
5. Deliver the result

### Phase 1: Understand the Request

<!-- CUSTOMIZE: What information must be gathered before starting? What questions should be asked? -->

Before starting, clarify:
- <!-- CUSTOMIZE: Key question 1 -->
- <!-- CUSTOMIZE: Key question 2 -->
- <!-- CUSTOMIZE: Key question 3 -->

Ask questions one at a time. Prefer multiple choice when possible.

**Quality gate:** Proceed only when <!-- CUSTOMIZE: condition for moving forward -->.

### Phase 2: Gather Context

<!-- CUSTOMIZE: What existing state, files, or environment details need to be checked? Include specific commands or tool usage. -->

Analyze the current state:
- <!-- CUSTOMIZE: What to check -->
- <!-- CUSTOMIZE: What to read or inspect -->

```bash
# <!-- CUSTOMIZE: Replace with actual detection/analysis commands -->
```

**Quality gate:** Proceed only when <!-- CUSTOMIZE: what must be confirmed -->.

### Phase 3: Execute

<!-- CUSTOMIZE: The core work of the skill. Break into sub-steps if complex. Include decision points where the approach may branch. -->

**Decision point:**
- If <!-- CUSTOMIZE: condition A --> -> <!-- CUSTOMIZE: approach A -->
- If <!-- CUSTOMIZE: condition B --> -> <!-- CUSTOMIZE: approach B -->

#### Sub-step 3a: <!-- CUSTOMIZE -->

<!-- CUSTOMIZE: Detailed instructions for the first part of execution. -->

#### Sub-step 3b: <!-- CUSTOMIZE -->

<!-- CUSTOMIZE: Detailed instructions for the second part of execution. -->

**Quality gate:** Verify <!-- CUSTOMIZE: what to check before moving on -->.

### Phase 4: Validate

<!-- CUSTOMIZE: How to verify the output is correct. Include specific validation commands, checklists, or scripts. -->

Before finalizing, verify:
- [ ] <!-- CUSTOMIZE: Validation check 1 -->
- [ ] <!-- CUSTOMIZE: Validation check 2 -->
- [ ] <!-- CUSTOMIZE: Validation check 3 -->

```bash
# <!-- CUSTOMIZE: Replace with actual validation commands -->
```

**Do not finalize if <!-- CUSTOMIZE: failure condition -->.**

### Phase 5: Deliver

<!-- CUSTOMIZE: How to present the result to the user. What to report, what format to use. -->

Report to user:
- <!-- CUSTOMIZE: Key output 1 -->
- <!-- CUSTOMIZE: Key output 2 -->
- <!-- CUSTOMIZE: Summary or next steps -->

## Output Format

<!-- CUSTOMIZE: If the skill produces a specific artifact (document, file, report), define its structure here. Remove if the skill is purely interactive. -->

```markdown
# <!-- CUSTOMIZE: Output title -->

## <!-- CUSTOMIZE: Section 1 -->
[Content]

## <!-- CUSTOMIZE: Section 2 -->
[Content]
```

## Key Principles

<!-- CUSTOMIZE: 3-6 guiding principles that shape how this workflow operates. Use imperative form. -->

- **<!-- CUSTOMIZE: Principle name -->** - <!-- CUSTOMIZE: Brief explanation -->
- **<!-- CUSTOMIZE: Principle name -->** - <!-- CUSTOMIZE: Brief explanation -->
- **<!-- CUSTOMIZE: Principle name -->** - <!-- CUSTOMIZE: Brief explanation -->

## Resources

<!-- CUSTOMIZE: List any scripts, references, or assets bundled with this skill. Remove sections that don't apply. -->

### scripts/

| Script | Purpose |
|--------|---------|
| `script_name.py [args]` | <!-- CUSTOMIZE: What it does --> |

### references/

- [reference-name.md](references/reference-name.md) - <!-- CUSTOMIZE: What it contains and when to read it -->
