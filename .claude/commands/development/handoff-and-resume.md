---
name: handoff-and-resume
model: standard
description: Create a handoff document capturing session state and generate resume instructions for the next session
usage: /handoff-and-resume [--resume <path>] [--save]
---

# /handoff-and-resume

Capture current work state and produce resume instructions so the next session starts with full context.

## Usage

```
/handoff-and-resume [--resume <path>] [--save]
```

**Arguments:**
- `--resume <path>` (optional) — Path to an existing handoff document to resume from instead of creating a new one. Loads the context and walks through the resume steps.
- `--save` (optional) — Save the handoff document to `.cursor/handoffs/YYYY-MM-DD-HHMMSS.md`. Without this flag, output goes to the terminal only.

## Examples

```
/handoff-and-resume                                  # Generate handoff to terminal
/handoff-and-resume --save                           # Generate and save to .cursor/handoffs/
/handoff-and-resume --resume .cursor/handoffs/2026-02-06-143022.md  # Resume from a saved handoff
/handoff-and-resume --save --resume latest           # Resume the most recent handoff, then save a new one
```

## What It Does

1. **Snapshots** the current git state — branch name, last commit, uncommitted changes, stash entries, and remote tracking status
2. **Reads** `TODO.md`, `task_plan.md`, and `docs/planning/roadmap.md` to identify completed, in-progress, and pending items
3. **Parses** recent git history to build a summary of what was accomplished since the branch diverged or within the last session
4. **Detects** uncommitted work and staged-but-not-committed changes that would be lost between sessions
5. **Extracts** open decisions and blockers from commit messages, code comments (`DECISION:`, `FIXME`, `HACK`, `QUESTION`, `TBD`), and TODO markers
6. **Inventories** context files — the files most relevant to resuming work, ranked by recency of modification
7. **Generates** ordered resume steps the next session should follow to regain full context before writing code
8. **Compiles** environment metadata — Node/Python/Go version, active `.env` files, running services, and dependency lock state
9. **Writes** the handoff document to `.cursor/handoffs/YYYY-MM-DD-HHMMSS.md` when `--save` is passed
10. **Loads** an existing handoff document and walks through resume steps when `--resume` is passed

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Snapshot Git State

Run the following commands to capture the full repository state:

```bash
# Current branch and tracking info
git branch --show-current
git status --porcelain

# Last commit on this branch
git log -1 --format="%H|%s|%an|%ai"

# Uncommitted changes summary
git diff --stat
git diff --cached --stat

# Stash entries
git stash list

# Remote tracking status
git status --branch --porcelain=v2
```

Build a structured git state object from the results:

| Field | Source |
|-------|--------|
| `branch` | `git branch --show-current` |
| `last_commit` | Hash, message, author, and timestamp from `git log -1` |
| `uncommitted_files` | Files from `git status --porcelain` with modification type |
| `staged_files` | Files from `git diff --cached --stat` |
| `stash_count` | Number of entries from `git stash list` |
| `ahead_behind` | Commits ahead/behind remote from `git status --branch` |

### Phase 2: Summarize Completed Work

Gather what was accomplished during the current working session:

```bash
# Commits on this branch not yet on main
git log main..HEAD --format="%h|%s|%ai" --reverse

# If no divergence from main, fall back to recent commits
git log --since="8h" --format="%h|%s|%ai" --reverse
```

Group commits by theme (feature work, bug fixes, refactoring, tests, docs) using the same keyword signals as `/start-task`.

### Phase 3: Identify In-Progress Work

Read the following files to determine what is still in progress. Skip any that do not exist.

| File | Purpose |
|------|---------|
| `TODO.md` | Active tasks with `[ ]` and `[x]` markers |
| `task_plan.md` | Current task scope and acceptance criteria |
| `docs/planning/roadmap.md` | Sprint items and their status |

Cross-reference pending `[ ]` items against session commits to separate "touched but incomplete" from "not yet started."

### Phase 4: Extract Blockers and Decisions

Search for unresolved items and recorded decisions:

```bash
# Decision markers in recent commits
git log main..HEAD --format="%s" | grep -iE "decided|chose|switched|trade-off|instead of|went with|opted for"

# Open questions and blockers in changed files
git diff main..HEAD -U0 | grep -iE "FIXME|HACK|XXX|QUESTION|TBD|BLOCKER|TODO"
```

Also scan `TODO.md` for items tagged `[blocked]`, `[question]`, or `[waiting]`.

### Phase 5: Inventory Context Files

Identify the files the next session must read to regain context. Rank by relevance:

| Priority | Criteria |
|----------|----------|
| **Critical** | Files with uncommitted changes or staged modifications |
| **High** | Files modified in the last 3 commits on this branch |
| **Medium** | Files referenced in `task_plan.md` or `TODO.md` as in-progress |
| **Low** | Config files, env files, or dependency files changed during the session |

List each file with a one-line reason for its relevance.

### Phase 6: Capture Environment Metadata

Detect and record the development environment state:

| Check | Command |
|-------|---------|
| Node.js version | `node --version` (if `package.json` exists) |
| Python version | `python3 --version` (if `requirements.txt` or `pyproject.toml` exists) |
| Go version | `go version` (if `go.mod` exists) |
| Active env files | `ls .env .env.local .env.development 2>/dev/null` |
| Lock file hash | First 8 chars of `md5 package-lock.json` or equivalent |
| Docker status | `docker compose ps --format json 2>/dev/null` (if `docker-compose.yml` exists) |

Only run checks relevant to the detected project type. Skip silently if a runtime is not installed.

### Phase 7: Generate Resume Steps

Produce an ordered list of steps for the next session to follow. Always include these categories in order:

1. **Verify environment** — check runtime versions, install dependencies if lock file changed
2. **Review git state** — confirm branch, check for uncommitted changes, pull latest from remote
3. **Read context files** — list the critical and high-priority files from Phase 5
4. **Review blockers** — re-read open decisions and blockers before proceeding
5. **Continue work** — specific next actions derived from in-progress items

### Phase 8: Write or Load Handoff

**Creating a handoff (`--save`):**

1. Create `.cursor/handoffs/` directory if it does not exist
2. Write the handoff document to `.cursor/handoffs/YYYY-MM-DD-HHMMSS.md`
3. Output the file path and a summary to the terminal

**Resuming from a handoff (`--resume <path>`):**

1. Read the specified handoff document (or the most recent one if `--resume latest`)
2. Validate that the branch and last commit still match — warn if they diverge
3. Walk through each resume step, checking off items as they are verified
4. Output any drift detected since the handoff was created

## Output

The handoff document and terminal output follow this structure:

```markdown
# Handoff — YYYY-MM-DD HH:MM

**Branch:** feat/add-rate-limiting
**Last Commit:** a1b2c3d — "Add token bucket middleware"
**Created:** 2026-02-06 14:30:22

## Summary

Brief 2-3 sentence description of the current state of work and what the session accomplished.

## Completed

- [x] Implemented rate limiting middleware with token bucket algorithm
- [x] Added configuration for per-route rate limits
- [x] Fixed token refresh race condition in auth flow

## In Progress

- [ ] Integration tests for rate limiting endpoints (3 of 7 written)
- [ ] API documentation update for rate limit headers

## Blockers

- QUESTION: Should rate limits be tenant-configurable? Needs product decision.
- BLOCKED: Staging deploy requires DevOps to update Nginx config.

## Decisions Made

- Chose token bucket over sliding window — simpler, sufficient for current scale
- Rate limit headers will follow IETF draft `RateLimit-*` format

## Git State

| Property | Value |
|----------|-------|
| Branch | `feat/add-rate-limiting` |
| Last Commit | `a1b2c3d` — Add token bucket middleware |
| Uncommitted Files | 2 modified, 1 untracked |
| Staged Files | 0 |
| Stash Entries | 1 |
| Ahead/Behind | 3 ahead, 0 behind `origin/feat/add-rate-limiting` |

### Uncommitted Changes

- `src/middleware/rate-limit.ts` — partially refactored burst handling
- `tests/middleware/rate-limit.test.ts` — new test file, 3 tests passing

## Context Files

| File | Priority | Reason |
|------|----------|--------|
| `src/middleware/rate-limit.ts` | Critical | Uncommitted changes to burst handling |
| `tests/middleware/rate-limit.test.ts` | Critical | New test file, incomplete |
| `src/auth/token.ts` | High | Modified in last commit |
| `task_plan.md` | Medium | Active task scope and acceptance criteria |
| `.env.development` | Low | Contains rate limit config values |

## Resume Steps

1. Verify Node.js version matches `v20.11.0` and run `npm ci` if `package-lock.json` changed
2. Checkout branch `feat/add-rate-limiting` and confirm last commit is `a1b2c3d`
3. Review uncommitted changes in `src/middleware/rate-limit.ts` — burst handling refactor in progress
4. Read `task_plan.md` for full task scope and remaining acceptance criteria
5. Resolve blocker: get product decision on tenant-configurable rate limits
6. Continue writing integration tests — 4 of 7 remaining
7. Update API docs with `RateLimit-*` response headers
```

## NEVER Do

- **Never fabricate git state.** Only report branch, commit, and file data from actual git commands.
- **Never mark work as completed without evidence.** Completed items must have corresponding commits or `[x]` markers in source files.
- **Never omit uncommitted changes.** Uncommitted work is the most critical information in a handoff — losing it means losing progress.
- **Never generate resume steps without reading the actual project state.** Every resume step must correspond to real files, real branches, and real TODOs.
- **Never overwrite an existing handoff file.** Each handoff gets a unique timestamp-based filename.
- **Never include secrets or credentials in the handoff.** Reference `.env` files by name but never inline their values.
- **Never skip the git state section.** Even if the session was purely exploratory with no commits, document the branch and working tree status.

## Error Handling

- If not in a git repository, abort with: "Not a git repository. Run this command from within a git project."
- If `TODO.md` and `task_plan.md` do not exist, generate the handoff from git state alone and note: "No TODO.md or task_plan.md found — handoff based on git history only."
- If `--resume` points to a nonexistent file, list available handoffs in `.cursor/handoffs/` and prompt the user to select one.
- If `--resume latest` is used but `.cursor/handoffs/` is empty, report: "No saved handoffs found. Create one first with `/handoff-and-resume --save`."
- If the branch referenced in a resumed handoff no longer exists, warn: "Branch `<name>` not found. It may have been merged or deleted. Check `git branch -a`."
- If the last commit in a resumed handoff does not match HEAD, warn: "HEAD has moved since this handoff was created. Review `git log` for new commits before proceeding."
- If `.cursor/handoffs/` cannot be created, fall back to saving in the project root and warn the user.

## Related

- **Command:** `/session-summary` (for end-of-session summaries without resume instructions)
- **Command:** `/start-task` (for beginning a new task with full context — use after resuming)
- **Command:** `/complete-task` (for closing out a task before creating a handoff)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
