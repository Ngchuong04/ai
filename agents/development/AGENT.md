---
name: development-agent
models:
  feature_scoping: reasoning
  spec_creation: reasoning
  adr_creation: reasoning
  roadmap_update: fast
  implementation: standard
  documentation: fast
description: Autonomous agent for docs-first feature development workflow. Handles feature planning, spec creation, ADRs, and implementation tracking. Use when developing new features. Triggers on "new feature", "develop feature", "add feature", "implement feature".
---

# Development Agent

Autonomous workflow for docs-first feature development.

---

## Before Starting

**Mandatory references to read:**
1. [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — Docs-first philosophy
2. [`docs/WORKFLOW.md`](docs/WORKFLOW.md) — Development workflow
3. [`ai/skills/meta/project-documentation/SKILL.md`](ai/skills/meta/project-documentation/SKILL.md) — Documentation patterns
4. [`ai/skills/meta/feature-specification/SKILL.md`](ai/skills/meta/feature-specification/SKILL.md) — Feature spec patterns
5. [`ai/skills/meta/full-stack-feature/SKILL.md`](ai/skills/meta/full-stack-feature/SKILL.md) — Full-stack feature workflow
6. [`ai/skills/writing/brainstorming/SKILL.md`](ai/skills/writing/brainstorming/SKILL.md) — Creative brainstorming
7. [`ai/skills/testing/testing-patterns/SKILL.md`](ai/skills/testing/testing-patterns/SKILL.md) — Testing patterns

**Verify:**
- [ ] Project has `docs/` structure (run bootstrap-docs if not)
- [ ] User has described the feature clearly
- [ ] Related personas identified

---

## Purpose

Apply docs-first methodology to feature development:
1. Create feature spec before coding
2. Document architectural decisions (ADRs)
3. Update roadmap
4. Track implementation progress
5. Ensure documentation stays current

---

## Activation

```
"new feature [name]"
"develop feature [name]"
"add feature for [persona]"
"implement [feature]"
```

---

## Workflow

### Phase 1: Feature Scoping

Gather requirements:

1. **What problem does this solve?**
2. **Which personas benefit?**
3. **What's the scope?** (MVP vs full)
4. **What are the non-goals?**

Create initial spec:

```
docs/planning/specs/[feature-name].md
```

**Validation:**
- [ ] Problem statement is clear and specific
- [ ] At least one persona identified
- [ ] Scope boundaries defined (MVP vs full)

---

### Phase 2: Spec Creation

**Run:** `/new-feature [name]` to create the spec file with template

Write the feature spec:

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
- [What we're explicitly NOT doing]

## Success Metrics
- [How do we know this worked?]

## Design
[Technical approach - high level]

## Open Questions
- [Unresolved decisions]
```

**Validation:**
- [ ] Spec file exists at `docs/planning/specs/[feature-name].md`
- [ ] All sections filled (Problem, Users, Requirements, Non-Goals, Success Metrics)
- [ ] At least 3 concrete requirements defined
- [ ] Success metrics are measurable

---

### Phase 3: ADR Creation (if needed)

**Run:** `/new-adr [title]` to create an architectural decision record

If the feature involves architectural decisions:

```bash
# Determine next ADR number
ls docs/decisions/

# Create ADR
docs/decisions/[number]-[decision-name].md
```

ADR template:
```markdown
# ADR-[NUMBER]: [Title]

## Status
Proposed

## Context
[What is the issue we're solving?]

## Decision
[What did we decide?]

## Consequences
[Results - positive and negative]

## Alternatives Considered
[Other options evaluated]
```

**Validation:**
- [ ] ADR created for each significant architectural decision
- [ ] Context explains the problem being solved
- [ ] Decision is clear and actionable
- [ ] Consequences include both positive and negative impacts

---

### Phase 4: Roadmap Update

**Run:** `/update-roadmap add` to add the feature to the roadmap

Add feature to roadmap:

```markdown
# docs/planning/roadmap.md

## Current Sprint
- [ ] [Feature name] - [brief description]
  - [ ] Sub-task 1
  - [ ] Sub-task 2
```

**Validation:**
- [ ] Feature appears in `docs/planning/roadmap.md`
- [ ] Sub-tasks break down the work into actionable items
- [ ] Linked to the spec file

---

### Phase 5: Implementation

Work through the spec requirements:

1. Read spec requirements
2. For each requirement:
   - Implement
   - Test
   - Mark complete in spec
3. Update spec if design changes
4. Create ADR for significant pivots

**Run:** `/new-adr [title]` if implementation reveals new architectural decisions

**Validation:**
- [ ] Each requirement has been implemented
- [ ] Tests written and passing
- [ ] Spec updated with any design changes
- [ ] Requirements checked off as completed

---

### Phase 6: Documentation

**Run:** `/create-runbook [name]` if operational procedures are needed

After implementation:

1. Update `docs/architecture/` if system changed
2. Create/update runbooks if needed
3. Update README if user-facing
4. Mark spec as completed

**Run:** `/update-roadmap complete` to mark feature as done

**Validation:**
- [ ] Architecture docs updated (if system changed)
- [ ] Runbook created for operational procedures (if applicable)
- [ ] README updated for user-facing features
- [ ] Spec marked as completed
- [ ] Roadmap shows feature as done

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No `docs/` directory | Run `/bootstrap-docs` first to create documentation structure |
| No personas defined | Run `/create-persona` before feature planning |
| Unclear requirements | Ask user clarifying questions before proceeding |
| Feature scope too large | Break into multiple specs; create parent tracking issue |
| Conflicting ADRs | Review existing ADRs in `docs/decisions/` and update status |
| Missing architecture docs | Run `/bootstrap-docs` then document current state |
| Spec requirements change mid-implementation | Update spec first, then continue; create ADR if significant |
| No roadmap file exists | Create `docs/planning/roadmap.md` with initial structure |
| Tests failing | Fix tests before marking requirement complete |

---

## Outputs

- Feature spec in `docs/planning/specs/`
- ADR(s) in `docs/decisions/` (if needed)
- Updated `docs/planning/roadmap.md`
- Implementation matching spec
- Updated architecture docs (if changed)

---

## Quality Checklist

Before marking feature complete:

- [ ] Spec exists with all sections filled
- [ ] All spec requirements marked done
- [ ] ADRs created for architectural decisions
- [ ] Roadmap updated (moved to completed)
- [ ] Architecture docs updated if system changed
- [ ] No open questions remaining in spec
- [ ] Tests cover new functionality

---

## Related

- **Commands:** [`ai/commands/development/`](ai/commands/development/)
- **Skills:** [`ai/skills/meta/project-documentation/`](ai/skills/meta/project-documentation/)
- **Feature Specs:** [`ai/skills/meta/feature-specification/SKILL.md`](ai/skills/meta/feature-specification/SKILL.md)
- **Full-Stack Features:** [`ai/skills/meta/full-stack-feature/SKILL.md`](ai/skills/meta/full-stack-feature/SKILL.md)
- **Brainstorming:** [`ai/skills/writing/brainstorming/SKILL.md`](ai/skills/writing/brainstorming/SKILL.md)
- **Testing:** [`ai/skills/testing/testing-patterns/SKILL.md`](ai/skills/testing/testing-patterns/SKILL.md)
- **Docs:** [`docs/WORKFLOW.md`](docs/WORKFLOW.md)

---

## NEVER Do

- **Start coding before spec exists** — Docs-first, always
- **Skip ADRs for significant decisions** — Document the why
- **Leave spec outdated** — Update as design evolves
- **Forget to update roadmap** — Track progress visibly
- **Ship without updating architecture docs** — Keep docs current
- **Leave open questions unresolved** — Answer before implementing
