---
name: complete-task
model: fast
description: Mark a task as done and generate completion artifacts (changelog, handoff, roadmap update)
usage: /complete-task <task>
---

# /complete-task

Mark a task as complete and generate structured completion artifacts.

## Usage

```
/complete-task <task>
```

**Arguments:**
- `task` — Task description, TODO item text, or ticket ID that was completed (e.g., `"add rate limiting to API"`, `PROJ-142`)

## Examples

```
/complete-task "add rate limiting to the /api/auth endpoints"
/complete-task PROJ-142
/complete-task fix-memory-leak-in-worker
/complete-task "refactor database connection pooling"
/complete-task "migrate auth service to OAuth 2.1"
```

## What It Does

1. **Reads** `TODO.md`, `CHANGELOG.md`, `docs/planning/roadmap.md`, and `task_plan.md` to understand current project state
2. **Locates** the matching TODO item in `TODO.md` by searching for the task description or ticket ID
3. **Marks** the TODO item as complete by replacing `- [ ]` with `- [x]` and appending the completion date
4. **Classifies** the work into a changelog category (Added, Changed, Fixed, Removed, Security, Deprecated)
5. **Generates** a changelog entry and prepends it to `CHANGELOG.md` under the current version heading
6. **Collects** files changed, decisions made, and relevant git commits for the completion summary
7. **Updates** `docs/planning/roadmap.md` to reflect the completed status of the task
8. **Evaluates** whether the completion triggers a handoff condition (milestone reached, end of day, context switch)
9. **Creates** `handoff.md` if a handoff trigger condition is met, capturing full context for the next contributor
10. **Removes** `task_plan.md` if present, since the task is now complete
11. **Outputs** a completion summary to the terminal so the user can verify the artifacts

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Read Project Context

Read the following files to understand current project state. Skip any that do not exist.

| File | Purpose |
|------|---------|
| `TODO.md` | Find and mark the completed task |
| `CHANGELOG.md` | Prepend the new changelog entry |
| `docs/planning/roadmap.md` | Update task status to complete |
| `task_plan.md` | Retrieve intent, scope, and acceptance criteria |
| `.git` (via `git log`) | Collect relevant commits for the completion record |

If `TODO.md` does not exist, warn the user and skip the status update step.

### Phase 2: Mark TODO as Complete

Search `TODO.md` for the matching task using these patterns in order:

| Search Strategy | Pattern | Example Match |
|----------------|---------|---------------|
| Exact text match | Task description substring | `- [ ] Add rate limiting to API` |
| Ticket ID match | `PROJ-\d+` or similar ID | `- [ ] PROJ-142: Add rate limiting` |
| Fuzzy keyword match | Overlapping keywords | `- [ ] Implement rate limiter for auth` |

Apply the status update using regex replacement:

```
Before: - [ ] Add rate limiting to API
After:  - [x] Add rate limiting to API ✓ (2026-02-06)
```

Pattern: Replace `- \[ \]` with `- \[x\]` on the matched line and append ` ✓ (YYYY-MM-DD)`.

If multiple matches are found, present them and ask the user to confirm which item to mark complete.

### Phase 3: Classify and Generate Changelog Entry

Determine the changelog category by analyzing the work performed:

| Category | Signals | Examples |
|----------|---------|----------|
| **Added** | New feature, new endpoint, new component, new file | "Added rate limiting middleware" |
| **Changed** | Refactor, update, improve, enhance, modify behavior | "Changed connection pooling to support multi-tenant" |
| **Fixed** | Bug fix, error correction, patch, resolve issue | "Fixed memory leak in background worker" |
| **Removed** | Delete, remove, drop, deprecate and remove | "Removed legacy v1 API endpoints" |
| **Security** | Auth fix, vulnerability patch, dependency CVE, hardening | "Security: Patched XSS vulnerability in user input" |
| **Deprecated** | Mark for future removal, sunset notice, migration warning | "Deprecated syncUserData in favor of async pipeline" |

If the category cannot be determined from the task description or `task_plan.md`, ask the user:
> "What type of change was this? (Added / Changed / Fixed / Removed / Security / Deprecated)"

Generate the entry and prepend it to `CHANGELOG.md` under the current `## [Unreleased]` heading. If no `[Unreleased]` section exists, create one.

```markdown
## [Unreleased]

### Added
- Rate limiting middleware for `/api/auth` endpoints with configurable thresholds ([commit](link))
```

### Phase 4: Collect Completion Context

Gather the following information for the completion summary:

1. **Files changed** — Run `git diff --name-only` against the branch or recent commits related to this task.
2. **Decisions made** — Extract from `task_plan.md` sections: "Risks and Open Questions", "Scope", and any ADRs created.
3. **Relevant commits** — Run `git log --oneline -20 --grep="<task keyword>"` to find associated commits.
4. **Acceptance criteria status** — If `task_plan.md` has criteria, check each one and note whether it was met.

### Phase 5: Update Roadmap

If `docs/planning/roadmap.md` exists:

1. Find the task entry in the roadmap (Current Sprint, In Progress, or Backlog section).
2. Move it to the **Completed** section with the completion date.
3. Update the status marker: replace `[ ]` or `[~]` with `[x]`.
4. Add the completion date: `(completed YYYY-MM-DD)`.

If the roadmap file does not exist, skip this step and note it in the output.

### Phase 6: Evaluate Handoff Triggers

Check whether the completion triggers a handoff. A handoff is warranted when any of the following conditions are met:

| Trigger | Condition | Detection |
|---------|-----------|-----------|
| **Milestone reached** | All tasks in a milestone group are now complete | All items under a `## Milestone` heading in roadmap are `[x]` |
| **End of day** | User indicates EOD or session is wrapping up | User says "EOD", "wrapping up", "done for today" |
| **Context switch** | User is moving to a different project or area | User says "switching to", "moving on", "handing off" |
| **Complex completion** | Task was `large` or `epic` complexity | `task_plan.md` complexity field is `large` or `epic` |

If a handoff trigger is detected, proceed to Phase 7. Otherwise, skip to Phase 8.

### Phase 7: Create Handoff Notes

Write `handoff.md` to the project root with the following template:

```markdown
# Handoff Notes

**Date:** YYYY-MM-DD
**Completed Task:** [task description]
**Author:** [from git config user.name]

## What Was Done
[2-4 sentence summary of the work completed]

## Key Decisions
- [Decision 1 and rationale]
- [Decision 2 and rationale]

## Files Changed
- `path/to/file.ts` — [what changed and why]
- `path/to/another.ts` — [what changed and why]

## Relevant Commits
- `abc1234` — [commit message]
- `def5678` — [commit message]

## Open Items
- [Anything left unfinished or deferred]
- [Follow-up tasks that were identified]

## Context for Next Contributor
[Anything the next person needs to know to pick up where you left off]
```

### Phase 8: Clean Up and Report

1. If `task_plan.md` exists, delete it or prompt the user: "Task is complete. Remove `task_plan.md`?"
2. Output the completion summary to the terminal.

## Output

The command updates existing files and optionally creates new ones:

- **Updated:** `TODO.md` (task marked complete)
- **Updated:** `CHANGELOG.md` (new entry prepended)
- **Updated:** `docs/planning/roadmap.md` (status changed to complete)
- **Created:** `handoff.md` (only if a handoff trigger was met)
- **Deleted:** `task_plan.md` (if it existed and user confirms)

The terminal output follows this structure:

```
Task Completed
==============
Task:       [description]
Category:   [Added | Changed | Fixed | Removed | Security | Deprecated]
Date:       YYYY-MM-DD

Changes:
  TODO.md            marked complete (line 14)
  CHANGELOG.md       entry added under [Unreleased] → Added
  roadmap.md         moved to Completed section
  handoff.md         created (milestone reached)
  task_plan.md       removed

Commits:    3 related commits found
Files:      7 files changed across 4 directories

Next steps:
  1. Review CHANGELOG.md entry for accuracy
  2. Review handoff.md if created
  3. Run /start-task for the next item or /update-roadmap to plan ahead
```

## NEVER Do

- **Never mark a TODO complete without confirming the match.** If multiple items match, ask the user to disambiguate.
- **Never skip the changelog entry.** Every completed task gets a changelog record, even trivial ones.
- **Never fabricate commits or file changes.** Only reference real git history and actual files in the project.
- **Never delete `task_plan.md` without user confirmation.** The user may want to keep it for reference.
- **Never auto-detect the changelog category when the work is ambiguous.** Ask the user rather than guessing wrong.
- **Never create a handoff without a trigger condition.** Handoffs add overhead; only generate them when warranted.
- **Never modify `CHANGELOG.md` structure.** Prepend entries under the existing format; do not reorganize existing entries.

## Error Handling

- If `TODO.md` does not exist, skip the status update and note: "No TODO.md found. Changelog entry created without TODO update."
- If `CHANGELOG.md` does not exist, create it with an `[Unreleased]` section and the new entry.
- If no matching TODO item is found, list the 5 most recent incomplete items and ask the user to select one or provide a more specific description.
- If `docs/planning/roadmap.md` does not exist, skip the roadmap update and note: "No roadmap found. Task completion recorded in TODO.md and CHANGELOG.md only."
- If `git log` returns no matching commits, note: "No related commits found. Add commit references manually if needed."
- If `task_plan.md` does not exist, proceed without it and note: "No task plan found. Completion artifacts generated from task description only."

## Automation

- **Optional automation:** Run `python3 scripts/sync_status.py` to sync TODO/roadmap/task_plan status markers automatically.
- **Optional automation:** Run `python3 scripts/sync_todos_from_git.py` to update TODO status from git commit messages.
- **Optional automation:** Run `python3 scripts/todo_to_changelog.py` to auto-generate changelog entries from completed TODOs.

## Related

- **Command:** `/start-task` (for establishing task context before implementation)
- **Command:** `/update-roadmap` (for managing roadmap entries independently)
- **Command:** `/review-code` (for reviewing the implementation before marking complete)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
