---
name: start-task
model: fast
description: Document task intent and establish context before implementation begins
usage: /start-task <task>
---

# /start-task

Document intent, scope, and context for a task before writing any code.

## Usage

```
/start-task <task>
```

**Arguments:**
- `task` — Short description of the task, ticket ID, or quoted goal (e.g., `"add rate limiting to API"`)

## Examples

```
/start-task "add rate limiting to the /api/auth endpoints"
/start-task fix-memory-leak-in-worker
/start-task PROJ-142
/start-task "refactor database connection pooling for multi-tenant support"
/start-task "add OpenTelemetry tracing to payment service"
```

## What It Does

1. **Reads** `TODO.md`, `docs/planning/roadmap.md`, and any existing task plans to understand current project state
2. **Parses** the task argument to extract intent, affected area, and implied scope
3. **Classifies** the task type (feature, bugfix, refactor, docs, infra) from keywords and context
4. **Estimates** complexity based on scope signals (files touched, dependencies, risk)
5. **Searches** existing TODOs and roadmap for related or duplicate work
6. **Prompts** the user for missing context: acceptance criteria, constraints, dependencies
7. **Creates** `task_plan.md` in the project root with structured sections
8. **Adds** the task to `docs/planning/roadmap.md` under the appropriate section if not already tracked
9. **Lists** context files the AI should read before implementation begins
10. **Outputs** a summary of the task plan so the user can confirm or adjust before work starts

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Read Project Context

Read the following files to understand current project state. Skip any that do not exist.

| File | Purpose |
|------|---------|
| `TODO.md` | Active tasks, priorities, and pending items |
| `docs/planning/roadmap.md` | Sprint status, backlog, and completed work |
| `task_plan.md` | Previous task plan (archive or warn if still present) |
| `CHANGELOG.md` | Recent changes for context on what has shipped |
| `docs/planning/specs/*.md` | Existing feature specs that may overlap |

If `task_plan.md` already exists, warn the user:
> "An existing task plan was found. Archive it before starting a new task, or confirm to overwrite."

### Phase 2: Classify the Task

Analyze the task description and match against the type detection table:

| Type | Keyword Signals | Default Branch Prefix |
|------|----------------|-----------------------|
| **feature** | add, create, implement, build, new, introduce, support | `feat/` |
| **bugfix** | fix, bug, broken, crash, error, wrong, incorrect, regression | `fix/` |
| **refactor** | refactor, restructure, reorganize, simplify, extract, clean up | `refactor/` |
| **docs** | document, docs, readme, explain, guide, comment, annotate | `docs/` |
| **infra** | deploy, ci, pipeline, docker, k8s, config, migrate, upgrade, dependency | `infra/` |

If the type cannot be determined from keywords, ask the user:
> "What type of task is this? (feature / bugfix / refactor / docs / infra)"

### Phase 3: Estimate Complexity

Score the task against these signals to produce a complexity estimate:

| Complexity | Files Touched | Dependencies | Risk | Typical Duration |
|------------|--------------|--------------|------|-----------------|
| **trivial** | 1 | None | None | < 30 min |
| **small** | 2–3 | Minor | Low | 30 min – 2 hrs |
| **medium** | 4–8 | Moderate | Medium | 2 hrs – 1 day |
| **large** | 9–20 | Significant | High | 1–3 days |
| **epic** | 20+ | Cross-cutting | Very high | 3+ days, needs breakdown |

If estimated as **epic**, recommend breaking the task into smaller subtasks before proceeding:
> "This task is estimated as epic. Break it into 3–5 smaller tasks with `/start-task` for each."

### Phase 4: Check for Related Work

Use `Grep` to search for related items across project planning files:

1. Search `TODO.md` for keywords from the task description.
2. Search `docs/planning/roadmap.md` for matching items.
3. Search `docs/planning/specs/*.md` for overlapping feature specs.
4. Search recent git history: `git log --oneline -30 --grep="<keyword>"`.

If related items are found, present them:

```
Related items found:
  TODO.md:14        — "[ ] Add rate limiting middleware"
  roadmap.md:38     — "[ ] API security hardening (backlog)"
  specs/api-v2.md:9 — "Rate limiting mentioned in API v2 spec"
```

Ask the user whether this task supersedes, extends, or is independent of each related item.

### Phase 5: Prompt for Missing Context

Ask the user to fill in any gaps. Present only the questions that cannot be inferred:

| Question | When to Ask |
|----------|-------------|
| What is the acceptance criteria? | Always — unless the task is trivial |
| Are there constraints or non-goals? | When the scope is ambiguous |
| What dependencies does this have? | When other tasks or services are involved |
| Is there a deadline or priority? | When roadmap placement matters |
| Which files or modules are affected? | When the task description is vague |

### Phase 6: Create `task_plan.md`

Write the task plan to the project root using the template below. Fill in every section from the information gathered in previous phases.

```markdown
# Task Plan

## Summary
**Task:** [task description]
**Type:** [feature | bugfix | refactor | docs | infra]
**Complexity:** [trivial | small | medium | large | epic]
**Branch:** [suggested branch name]
**Date:** [YYYY-MM-DD]

## Intent
[1–3 sentences describing WHY this task exists and what success looks like]

## Scope
### In Scope
- [Specific deliverable 1]
- [Specific deliverable 2]

### Out of Scope
- [Explicit non-goal 1]
- [Explicit non-goal 2]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Context Files
[Files the AI should read before starting implementation]
- `path/to/relevant/file.ts` — [why this file matters]
- `path/to/another/file.ts` — [why this file matters]

## Related Work
- [Link or reference to related TODO, spec, or ADR]

## Implementation Steps
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Risks and Open Questions
- [Risk or question 1]
- [Risk or question 2]
```

### Phase 7: Update Roadmap

If `docs/planning/roadmap.md` exists and the task is not already listed:

1. Add the task to the **Current Sprint** or **Backlog** section based on priority.
2. Include the task type prefix: `[feature]`, `[bugfix]`, `[refactor]`, `[docs]`, or `[infra]`.
3. Reference the task plan: `(see task_plan.md)`.
4. Maintain dependency ordering — place the new item after its prerequisites.

If the roadmap file does not exist, skip this step and note it in the output.

### Phase 8: Report Summary

Output the task plan summary to the terminal so the user can confirm or adjust.

## Output

The command creates one file and optionally updates another:

- **Created:** `task_plan.md` in the project root
- **Updated:** `docs/planning/roadmap.md` (if it exists and the task is new)

The terminal output follows this structure:

```
Task Plan Created
=================
Task:        [description]
Type:        [feature | bugfix | refactor | docs | infra]
Complexity:  [trivial | small | medium | large | epic]
Branch:      [suggested branch name]

Scope:       [N] deliverables, [M] acceptance criteria
Context:     [K] files to read before starting
Related:     [J] existing items found

Files:
  created   task_plan.md
  updated   docs/planning/roadmap.md

Next steps:
  1. Review task_plan.md and adjust if needed
  2. Create branch: git checkout -b [branch-name]
  3. Begin implementation with full context established
```

## NEVER Do

- **Never start coding before the task plan is written.** The entire purpose of this command is to establish intent and context first.
- **Never skip reading existing TODOs and roadmap.** Duplicate or conflicting work wastes effort and causes merge pain.
- **Never create a task plan without acceptance criteria.** A task without criteria has no definition of done.
- **Never overwrite an existing `task_plan.md` without warning.** The previous plan may still be in progress.
- **Never auto-assign epic complexity without recommending a breakdown.** Large tasks need decomposition to be actionable.
- **Never add to the roadmap without checking for duplicates.** Search before inserting to prevent redundant entries.
- **Never fabricate context files.** Only list files that actually exist in the project and are relevant to the task.

## Error Handling

- If `TODO.md` does not exist, skip it and note: "No TODO.md found. Consider creating one to track tasks."
- If `docs/planning/roadmap.md` does not exist, skip the roadmap update and note: "No roadmap found. Task plan created without roadmap entry."
- If the task description is empty or too vague to classify, ask the user for a clearer description before proceeding.
- If a previous `task_plan.md` exists and the user does not confirm overwrite, append a timestamp to the filename: `task_plan-YYYY-MM-DD.md`.
- If no related work is found, state it explicitly: "No related TODOs, specs, or roadmap items found."
- If the project has no `docs/` directory, create the task plan in the project root only — do not create directory structures unprompted.

## Automation

- **Optional automation:** Run `python3 scripts/context_preflight.py` to run pre-work validation ensuring context files are fresh and consistent before starting.
- **Optional automation:** Run `python3 scripts/load_context.py` to load and summarize relevant context files for the task.

## Related

- **Command:** `/new-feature` (for full docs-first feature development after the task plan is set)
- **Command:** `/update-roadmap` (for managing roadmap entries independently)
- **Command:** `/new-adr` (if the task requires an architectural decision)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
