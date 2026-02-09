---
name: create-runbook
model: standard
description: Create an operations runbook
usage: /create-runbook <name>
---

# /create-runbook

Create an operations runbook for common procedures.

## Usage

```
/create-runbook <name>
```

**Arguments:**
- `name` — Runbook name (kebab-case, descriptive)

## Examples

```
/create-runbook database-migration
/create-runbook incident-response
/create-runbook release-process
/create-runbook onboarding-new-developer
```

## When to Use

- Documenting **operational procedures** that get repeated
- After doing something manually that should be automated
- Creating on-call documentation
- Onboarding new team members
- Any multi-step procedure with verification needs

## What It Does

1. **Creates** runbook at `docs/runbooks/[name].md`
2. **Prompts** for procedure purpose
3. **Asks** for prerequisites
4. **Guides** through step documentation
5. **Prompts** for verification steps
6. **Adds** troubleshooting section

## Runbook Template

```markdown
# Runbook: [Name]

## Purpose
[What this runbook helps you accomplish]

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]

## Prerequisites
- [ ] [Prerequisite 1]
- [ ] [Prerequisite 2]

## Procedure

### Step 1: [First Step]
\`\`\`bash
# Commands to run
\`\`\`
**Expected output:** [What you should see]

### Step 2: [Second Step]
[Instructions]

### Step 3: [Third Step]
[Instructions]

## Verification
- [ ] [How to verify success]
- [ ] [What to check]

## Rollback
[How to undo if something goes wrong]

## Troubleshooting

### Problem: [Common issue]
**Cause:** [Why it happens]
**Solution:** [How to fix]

## Related
- [Links to related runbooks or docs]
```

## Good Runbook Qualities

| Quality | Description |
|---------|-------------|
| Atomic steps | Each step does one thing |
| Verifiable | Each step has expected outcome |
| Reversible | Rollback procedure included |
| Complete | Prerequisites listed upfront |

## Output Locations

- Runbook → `docs/runbooks/[name].md`

## Related

- **Docs structure:** `/bootstrap-docs` (creates runbooks/)
- **Local dev:** Default runbook in `docs/runbooks/local-dev.md`
- **Deploy:** Default runbook in `docs/runbooks/deploy.md`
