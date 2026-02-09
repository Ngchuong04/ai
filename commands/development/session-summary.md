---
name: session-summary
model: fast
description: Generate an end-of-session summary capturing commits, TODOs, decisions, and next steps
usage: /session-summary [--since <timestamp|duration>] [--save]
---

# /session-summary

Generate a structured summary of work completed during the current session.

## Usage

```
/session-summary [--since <timestamp|duration>] [--save]
```

**Arguments:**
- `--since` (optional) — Start of the session window. Accepts ISO timestamp (`2025-06-15T09:00`), relative duration (`3h`, `90m`), or `today`. Defaults to `3h`.
- `--save` (optional) — Save the summary to `docs/sessions/YYYY-MM-DD.md` in addition to terminal output.

## Examples

```
/session-summary                              # Summarize the last 3 hours (default)
/session-summary --since 2h                   # Summarize the last 2 hours
/session-summary --since 2025-06-15T09:00     # Summarize since a specific timestamp
/session-summary --since today                # Summarize everything committed today
/session-summary --since 4h --save            # Summarize last 4 hours and save to file
```

## What It Does

1. **Resolves** the session window from the `--since` argument or defaults to the last 3 hours
2. **Parses** git log for all commits made within the session window using `git log --since`
3. **Collects** diff stats for every file changed during the session via `git diff --stat`
4. **Scans** `TODO.md` and `task_plan.md` to identify TODOs completed and still pending
5. **Reads** commit messages and inline comments for decision signals (keywords: "decided", "chose", "switched to", "trade-off", "instead of")
6. **Extracts** blockers and open questions from TODOs, commit messages, and code comments tagged `FIXME`, `HACK`, `XXX`, or `QUESTION`
7. **Compiles** a list of next steps inferred from pending TODOs, open questions, and incomplete work
8. **Formats** the summary using the session summary template (see Output section)
9. **Outputs** the summary to the terminal for review
10. **Saves** the summary to `docs/sessions/YYYY-MM-DD.md` when `--save` is passed, creating the directory if needed

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Resolve Session Window

Determine the start boundary of the session from the `--since` argument.

| Input Format | Resolution |
|-------------|------------|
| `Nh` (e.g., `3h`) | Current time minus N hours |
| `Nm` (e.g., `90m`) | Current time minus N minutes |
| `today` | Midnight of the current day |
| ISO timestamp (e.g., `2025-06-15T09:00`) | Use as-is |
| No argument | Default to `3h` |

Store the resolved timestamp as `SESSION_START` for use in all subsequent phases.

### Phase 2: Parse Git Log

Run the following git commands to gather commit and file-change data:

```bash
# All commits in the session window
git log --since="$SESSION_START" --format="%h|%s|%an|%ai" --reverse

# Per-file insertion/deletion counts
git diff --numstat $(git log --since="$SESSION_START" --format="%H" | tail -1)^..HEAD
```

If no commits are found in the session window:
> "No commits found since `SESSION_START`. Expand the window with `--since` or check `git log`."

### Phase 3: Collect File Change Stats

From the `git diff --numstat` output, build a table of files changed grouped by type: **added**, **modified**, **deleted**, **renamed**.

### Phase 4: Scan TODO Status

Read the following files to determine TODO state. Skip any that do not exist.

| File | Purpose |
|------|---------|
| `TODO.md` | Project-wide task tracking |
| `task_plan.md` | Current task acceptance criteria |
| `docs/planning/roadmap.md` | Sprint and backlog items |

Classify each TODO into one of three categories:

| Status | Detection |
|--------|-----------|
| **Completed** | Marked `[x]` and the file was modified within the session window |
| **Pending** | Marked `[ ]` and referenced in session commits or task plan |
| **Unrelated** | Marked `[ ]` but not referenced in session work — exclude from summary |

### Phase 5: Extract Decisions

Search commit messages and changed files for decision signals:

```bash
# Decision keywords in commit messages
git log --since="$SESSION_START" --format="%s" | grep -iE "decided|chose|switched|trade-off|instead of|went with|opted for"

# Inline decision comments in diffs
git diff $(git log --since="$SESSION_START" --format="%H" | tail -1)^..HEAD -U0 | grep -iE "DECISION:|TRADE-OFF:|chose .* over|went with"
```

Also check for ADR files created or modified during the session. Format each decision as a single-line entry with context.

### Phase 6: Identify Blockers and Open Questions

Search for unresolved items in changed files (`FIXME`, `HACK`, `XXX`, `QUESTION` markers) and commit messages containing `?`, `blocker`, `blocked`, `unclear`, or `TBD`. Also read `TODO.md` for items tagged with `[blocked]` or `[question]`.

### Phase 7: Generate Next Steps

Compile next steps from three sources:

1. **Pending TODOs** — items from Phase 4 that are still `[ ]` and relevant to the session
2. **Blockers** — items from Phase 6 that need resolution before work can continue
3. **Incomplete work** — commits with messages containing "WIP", "partial", "part 1", or "started"
4. **Test gaps** — files changed without corresponding test changes

Present next steps as an ordered list, prioritized: blockers first, then pending TODOs, then follow-up work.

### Phase 8: Format and Output

Assemble the full summary using the template in the Output section. If `--save` is passed:

1. Create `docs/sessions/` directory if it does not exist
2. Write the summary to `docs/sessions/YYYY-MM-DD.md`
3. If the file already exists (multiple sessions in one day), append with an `## Afternoon Session` or `## Session 2` header

## Output

The terminal output and saved file follow this structure:

```markdown
# Session Summary — YYYY-MM-DD

**Window:** HH:MM – HH:MM (Xh Ym)
**Commits:** N
**Files changed:** M (+A, -D lines)

## Commits

| Time  | Hash    | Message                        |
|-------|---------|--------------------------------|
| 09:15 | a1b2c3d | Add rate limiting middleware    |
| 09:42 | d4e5f6a | Fix token refresh race condition|
| 10:30 | b7c8d9e | Add tests for auth flow         |

## Files Changed

| File                          | Changes   | Type     |
|-------------------------------|-----------|----------|
| src/middleware/rate-limit.ts  | +95 -0    | added    |
| src/auth/token.ts             | +18 -7    | modified |
| tests/auth/token.test.ts      | +42 -0    | added    |

## TODOs

### Completed
- [x] Add rate limiting to /api/auth endpoints
- [x] Fix token refresh race condition

### Still Pending
- [ ] Add integration tests for rate limiting
- [ ] Update API documentation for new limits

## Decisions Made

- Chose token bucket algorithm over sliding window for rate limiting (simpler, sufficient for current scale)
- Decided to refresh tokens 5 minutes before expiry instead of on-demand

## Blockers & Open Questions

- QUESTION: Should rate limits be configurable per-tenant? (src/middleware/rate-limit.ts:23)
- FIXME: Token refresh retry logic needs exponential backoff (src/auth/token.ts:87)

## Next Steps

1. Resolve: per-tenant rate limit configuration decision
2. Add exponential backoff to token refresh retries
3. Write integration tests for rate limiting endpoints
4. Update API docs with rate limit headers and status codes
5. Deploy to staging and run load tests
```

## NEVER Do

- **Never fabricate commits.** Only include commits that appear in `git log` for the session window.
- **Never mark a TODO as completed without evidence.** The item must be `[x]` in the source file or addressed by a commit in the session.
- **Never invent decisions.** Only report decisions explicitly stated in commit messages, code comments, or ADRs.
- **Never skip the diff stats.** File change counts are essential for understanding session scope.
- **Never include commits from outside the session window.** Respect the `--since` boundary strictly.
- **Never save to `docs/sessions/` without the `--save` flag.** Terminal-only output is the default.
- **Never overwrite an existing session file without appending.** Multiple sessions in one day should be preserved as separate sections.

## Error Handling

- If no commits exist in the session window, report "No commits found" and suggest expanding the window with `--since`.
- If `TODO.md` does not exist, skip the TODO section and note: "No TODO.md found — TODO tracking skipped."
- If `task_plan.md` does not exist, skip task plan scanning and proceed with git-only analysis.
- If the session window is unreasonably large (>24h), warn: "Session window exceeds 24 hours. Consider narrowing with `--since` for a focused summary."
- If `git log` fails (not a git repository), abort with: "Not a git repository. Run this command from within a git project."
- If `docs/sessions/` cannot be created when `--save` is used, fall back to saving in the project root and warn the user.
- If `gh` CLI is unavailable and PR-linked commits are detected, skip PR metadata and note the limitation.

## Automation

- **Optional automation:** Run `python3 scripts/session_changelog.py` to generate a per-session changelog from git activity.
- **Optional automation:** Run `python3 scripts/context_diff.py` to show what changed in context files during this session.

## Related

- **Command:** `/start-task` (establishes the task context that this command summarizes)
- **Command:** `/review-code` (run a review before closing out the session)
- **Command:** `/debug-error` (for unresolved errors surfaced in the summary)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
