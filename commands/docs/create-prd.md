---
name: create-prd
model: reasoning
description: Create a Product Requirements Document
usage: /create-prd <name>
---

# /create-prd

Create a Product Requirements Document for a feature or product.

## Usage

```
/create-prd <name>
```

**Arguments:**
- `name` — PRD name (kebab-case, descriptive)

## Examples

```
/create-prd user-authentication
/create-prd payment-integration
/create-prd mobile-app-v2
/create-prd api-redesign
```

## When to Use

- Starting a new product or major feature
- Before `/new-feature` for comprehensive planning
- When stakeholder alignment is needed
- For features requiring detailed specifications
- When building something with multiple user personas

## What It Does

1. **Creates** PRD file at `docs/product/prd-[name].md`
2. **Prompts** for problem statement
3. **Asks** about target personas (references existing personas)
4. **Gathers** requirements and success metrics
5. **Documents** scope (in-scope and out-of-scope)
6. **Captures** technical considerations
7. **Generates** structured PRD document

## PRD Template

```markdown
# PRD: [Name]

## Overview
**Author:** [name]
**Created:** [date]
**Status:** Draft | In Review | Approved | In Progress | Complete

## Problem Statement
[What problem are we solving? Why now?]

## Target Users
| Persona | Primary Need | How This Helps |
|---------|--------------|----------------|
| [Persona 1] | [Need] | [Solution] |
| [Persona 2] | [Need] | [Solution] |

## Goals
- [Goal 1]
- [Goal 2]

## Non-Goals
- [Explicitly not doing 1]
- [Explicitly not doing 2]

## Requirements

### Must Have (P0)
- [ ] [Requirement]
- [ ] [Requirement]

### Should Have (P1)
- [ ] [Requirement]

### Nice to Have (P2)
- [ ] [Requirement]

## Success Metrics
| Metric | Current | Target |
|--------|---------|--------|
| [Metric 1] | [value] | [value] |

## Technical Considerations
[Architecture impacts, dependencies, risks]

## Timeline
| Phase | Scope | Duration |
|-------|-------|----------|
| Phase 1 | MVP | [estimate] |
| Phase 2 | Full | [estimate] |

## Open Questions
- [ ] [Question 1]
- [ ] [Question 2]
```

## Output Locations

- PRD → `docs/product/prd-[name].md`

## After Creating PRD

1. Review with stakeholders
2. Update status to "Approved" when aligned
3. Create feature specs with `/new-feature`
4. Create ADRs for technical decisions with `/new-adr`

## Related

- **Feature specs:** `/new-feature` (detailed implementation specs)
- **Personas:** `/create-persona` (define target users first)
- **Decisions:** `/new-adr` (document technical choices)
- **Roadmap:** `/update-roadmap` (add to planning)
