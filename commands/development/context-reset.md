---
name: context-reset
model: fast
description: Archive stale context files and reset to fresh templates for a clean working state
usage: /context-reset [--dry-run] [--no-confirm]
---

# /context-reset

Archive all context files to a dated directory and reset them with fresh templates so the next task starts from a clean slate.

## Usage

```
/context-reset [--dry-run] [--no-confirm]
```

**Arguments:**
- `--dry-run` (optional) — Show what would be archived and reset without making any changes. Use this to preview the operation.
- `--no-confirm` (optional) — Skip the confirmation prompt and proceed immediately. Use with caution.

## Examples

```
/context-reset                    # Archive context, reset templates (with confirmation)
/context-reset --dry-run          # Preview what will be archived and reset
/context-reset --no-confirm       # Skip confirmation and reset immediately
```

## What It Does

1. **Inventories** all context files in the project — task plans, findings, handoffs, session summaries, and scratch notes
2. **Creates** a dated archive directory at `docs/archive/YYYY-MM-DD/`
3. **Copies** every context file into the archive (originals remain until reset)
4. **Resets** context files with fresh, empty templates ready for the next task
5. **Preserves** `TODO.md` and `docs/planning/roadmap.md` in place but creates archived copies
6. **Adds** a reset marker to `TODO.md` so the history of resets is visible
7. **Generates** a reset log entry at `docs/archive/YYYY-MM-DD/reset-log.md` capturing what was archived and why

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Inventory Context Files

Scan the project for all context files. Classify each file as **archive-and-reset** or **preserve-in-place**:

| Action | Files | Reason |
|--------|-------|--------|
| **Archive & Reset** | `task_plan.md` | Scoped to a single task — stale across tasks |
| **Archive & Reset** | `findings.md` | Investigation notes from a prior task |
| **Archive & Reset** | `decisions.md` | Decisions tied to a specific task context |
| **Archive & Reset** | `progress.md` | Progress tracking for a completed or abandoned task |
| **Archive & Reset** | `scratch.md` | Temporary working notes |
| **Archive & Reset** | `.cursor/handoffs/*.md` | Session handoffs from prior work |
| **Archive & Reset** | `docs/sessions/*.md` | Session summaries from prior work |
| **Preserve (copy only)** | `TODO.md` | Long-lived task tracker — add reset marker, do not clear |
| **Preserve (copy only)** | `docs/planning/roadmap.md` | Long-lived project roadmap — never reset |
| **Skip** | `CHANGELOG.md` | Permanent project history — never archive |
| **Skip** | `docs/planning/specs/*.md` | Feature specs — independent of context state |
| **Skip** | `docs/architecture/*.md` | Architecture docs — permanent reference |

Build a manifest of files found and their classification. If a file does not exist, skip it silently.

### Phase 2: Confirmation Prompt

Unless `--no-confirm` is passed, display the manifest and ask the user to confirm:

```
Context Reset Preview
=====================
Archive directory:  docs/archive/2026-02-06/

Files to archive & reset:
  task_plan.md                          → archived + reset to template
  findings.md                           → archived + reset to template
  .cursor/handoffs/2026-02-04-091500.md → archived
  .cursor/handoffs/2026-02-05-163000.md → archived
  docs/sessions/2026-02-04.md           → archived
  docs/sessions/2026-02-05.md           → archived

Files to preserve (archived copy only):
  TODO.md                               → copy archived, original preserved
  docs/planning/roadmap.md              → copy archived, original preserved

Proceed with context reset? (yes/no)
```

If the user declines, abort with: "Context reset cancelled. No files were changed."

If `--dry-run` is passed, display the preview and exit without making changes.

### Phase 3: Create Archive Directory

Create the archive directory with the current date:

```bash
mkdir -p docs/archive/YYYY-MM-DD
```

If the directory already exists (multiple resets in one day), append a sequence number:
- `docs/archive/2026-02-06/` (first reset)
- `docs/archive/2026-02-06-2/` (second reset)
- `docs/archive/2026-02-06-3/` (third reset)

### Phase 4: Copy Files to Archive

Copy every file from the manifest into the archive directory, preserving relative paths:

```bash
# Archive-and-reset files
cp task_plan.md docs/archive/YYYY-MM-DD/task_plan.md
cp findings.md docs/archive/YYYY-MM-DD/findings.md

# Handoffs — flatten into archive
cp .cursor/handoffs/*.md docs/archive/YYYY-MM-DD/handoffs/

# Session summaries — flatten into archive
cp docs/sessions/*.md docs/archive/YYYY-MM-DD/sessions/

# Preserve files — copy only
cp TODO.md docs/archive/YYYY-MM-DD/TODO.md
cp docs/planning/roadmap.md docs/archive/YYYY-MM-DD/roadmap.md
```

### Phase 5: Reset Context Files with Fresh Templates

Replace each archive-and-reset file with a clean template:

**`task_plan.md` template:**

```markdown
# Task Plan

## Summary
**Task:** [describe the task]
**Type:** [feature | bugfix | refactor | docs | infra]
**Complexity:** [trivial | small | medium | large | epic]
**Branch:** [branch name]
**Date:** YYYY-MM-DD

## Intent
[Why does this task exist? What does success look like?]

## Scope
### In Scope
- [Deliverable 1]

### Out of Scope
- [Non-goal 1]

## Acceptance Criteria
- [ ] [Criterion 1]

## Context Files
- `path/to/file` — [why it matters]

## Implementation Steps
1. [Step 1]

## Risks and Open Questions
- [Risk or question]
```

**`findings.md` template:**

```markdown
# Findings

> Investigation notes for the current task. Reset on YYYY-MM-DD.

## Observations
- [What did you find?]

## Evidence
- [Links, logs, screenshots]

## Conclusions
- [What do the findings mean for the task?]
```

**`decisions.md` template:**

```markdown
# Decisions

> Decisions made during the current task. Reset on YYYY-MM-DD.

| Decision | Rationale | Date |
|----------|-----------|------|
| [What was decided] | [Why] | YYYY-MM-DD |
```

**`progress.md` template:**

```markdown
# Progress

> Task progress tracker. Reset on YYYY-MM-DD.

## Current Status
- **Phase:** Not started
- **Blockers:** None

## Log
| Date | Update |
|------|--------|
| YYYY-MM-DD | Context reset — fresh start |
```

**`scratch.md` template:**

```markdown
# Scratch

> Temporary working notes. Reset on YYYY-MM-DD.
```

Delete all files in `.cursor/handoffs/` and `docs/sessions/` after archiving — these are session-specific and should not carry forward.

### Phase 6: Update TODO.md with Reset Marker

Prepend a reset marker to `TODO.md` so the history of resets is visible:

```markdown
---

> **Context Reset — YYYY-MM-DD HH:MM**
> Archived to `docs/archive/YYYY-MM-DD/`. All context files reset to fresh templates.

---
```

Insert this marker after the file's title heading but before the first task section.

### Phase 7: Generate Reset Log

Write a reset log to `docs/archive/YYYY-MM-DD/reset-log.md`:

```markdown
# Context Reset Log — YYYY-MM-DD HH:MM

**Triggered by:** /context-reset
**Archive directory:** docs/archive/YYYY-MM-DD/

## Archived Files

| File | Size | Last Modified | Status |
|------|------|---------------|--------|
| task_plan.md | 2.1 KB | 2026-02-04 | Archived & reset |
| findings.md | 1.4 KB | 2026-02-05 | Archived & reset |
| TODO.md | 3.8 KB | 2026-02-06 | Copy archived |
| docs/planning/roadmap.md | 5.2 KB | 2026-02-03 | Copy archived |

## Reset Templates Created

- task_plan.md
- findings.md
- decisions.md
- progress.md
- scratch.md

## Reason
[Context became stale after completing or abandoning prior task(s). Fresh templates created for the next task.]
```

## Output

The terminal output follows this structure:

```
Context Reset Complete
======================
Archive:     docs/archive/2026-02-06/
Archived:    8 files (4 reset, 2 preserved, 2 handoffs)
Reset:       5 templates created
Log:         docs/archive/2026-02-06/reset-log.md

Files reset:
  ✓ task_plan.md          → fresh template
  ✓ findings.md           → fresh template
  ✓ decisions.md          → fresh template
  ✓ progress.md           → fresh template
  ✓ scratch.md            → fresh template

Files preserved (copies archived):
  ✓ TODO.md               → reset marker added
  ✓ docs/planning/roadmap.md → unchanged

Cleared:
  ✓ .cursor/handoffs/     → 2 files archived and removed
  ✓ docs/sessions/        → 2 files archived and removed

Next steps:
  1. Run /start-task to begin a new task with clean context
  2. Review TODO.md — carried-over items may need re-prioritization
  3. Check docs/archive/2026-02-06/ if you need prior context
```

## NEVER Do

- **Never delete files without archiving first.** Every file must be copied to the archive directory before it is reset or removed.
- **Never reset `TODO.md` or `roadmap.md` to empty templates.** These are long-lived files — only add a reset marker and create an archived copy.
- **Never skip the confirmation prompt unless `--no-confirm` is explicitly passed.** A context reset is destructive and should require explicit consent.
- **Never overwrite an existing archive directory.** Use sequence numbers to prevent collisions when multiple resets happen on the same day.
- **Never archive `CHANGELOG.md`, feature specs, or architecture docs.** These are permanent project artifacts, not session context.
- **Never fabricate file sizes or modification dates in the reset log.** Only report actual file metadata from the filesystem.
- **Never proceed if the inventory finds zero context files.** Report: "No context files found to archive. Nothing to reset."

## Error Handling

- If no context files exist (no `task_plan.md`, `findings.md`, handoffs, or sessions), abort with: "No context files found. Nothing to archive or reset."
- If `docs/archive/` cannot be created (permissions or disk space), abort with: "Cannot create archive directory. Check filesystem permissions."
- If `TODO.md` does not exist, skip the reset marker step and note: "No TODO.md found — reset marker skipped."
- If `docs/planning/roadmap.md` does not exist, skip the roadmap archive and note: "No roadmap found — roadmap archiving skipped."
- If `.cursor/handoffs/` does not exist or is empty, skip handoff archiving silently.
- If `docs/sessions/` does not exist or is empty, skip session archiving silently.
- If a file copy fails mid-operation, halt the reset, report which files were archived successfully, and do not reset any files that failed to copy.
- If not in a git repository, warn but proceed: "Not a git repository — git-based metadata will be unavailable in the reset log."

## Automation

- **Optional automation:** Run `python3 scripts/archive_stale.py` to auto-archive context files older than a configurable threshold.

## Related

- **Command:** `/start-task` (begin a new task after resetting context)
- **Command:** `/handoff-and-resume` (for preserving context across sessions instead of resetting)
- **Command:** `/session-summary` (for summarizing a session before resetting)
- **Command:** `/complete-task` (for formally closing a task before resetting)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
