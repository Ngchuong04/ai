---
name: new-feature
model: reasoning
description: Docs-first feature development workflow
usage: /new-feature <name>
---

# /new-feature

Start a new feature with docs-first workflow.

## Usage

```
/new-feature <name>
```

**Arguments:**
- `name` — Feature name (kebab-case recommended)

## Examples

```
/new-feature user-authentication
/new-feature payment-integration
/new-feature dark-mode-toggle
```

## What It Does

1. **Creates** spec file in `docs/planning/specs/[name].md`
2. **Opens** spec template for requirements capture
3. **Asks** clarifying questions (problem, users, scope)
4. **Adds** feature to roadmap in `docs/planning/roadmap.md`
5. **Checks** if architectural decisions needed (prompts for ADR)
6. **Breaks down** into implementation todos
7. **Starts** implementation after spec is complete

## Spec Template

```markdown
# Feature: [Name]

## Problem
[What problem are we solving?]

## Users
[Which personas does this serve?]

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Non-Goals
[What we're explicitly NOT doing]

## Success Metrics
[How do we know this worked?]

## Design
[Technical approach - high level]

## Open Questions
- [Unresolved decisions]
```

## Output Locations

- Spec → `docs/planning/specs/[name].md`
- Roadmap update → `docs/planning/roadmap.md`
- ADR (if needed) → `docs/decisions/[number]-[topic].md`

## Related

- **Agent:** [`ai/agents/development/`](ai/agents/development/)
- **ADR creation:** `/new-adr` (for architectural decisions)
- **Methodology:** [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
