---
name: daily-standup
model: fast
description: Generate a daily standup summary from git history, TODOs, and roadmap — no manual input required
usage: /daily-standup [--since <timestamp|duration>] [--save]
---

# /daily-standup

Generate a structured daily standup report from existing context files — commits, TODOs, and roadmap — without requiring manual input.

## Usage

```
/daily-standup [--since <timestamp|duration>] [--save]
```

**Arguments:**
- `--since` (optional) — Start of the "yesterday" window. Accepts ISO timestamp (`2025-06-14T09:00`), relative duration (`24h`, `1d`), or `yesterday`. Defaults to `yesterday` (midnight of the previous calendar day).
- `--save` (optional) — Save the standup report to `docs/standups/YYYY-MM-DD.md` in addition to terminal output.

## Examples

```
/daily-standup                                # Standup from yesterday midnight to now (default)
/daily-standup --since 24h                    # Standup covering the last 24 hours
/daily-standup --since 2025-06-14T09:00       # Standup since a specific timestamp
/daily-standup --since yesterday --save       # Default window, save to file
/daily-standup --since 2d                     # Cover a long weekend (Friday to Monday)
```

## What It Does

1. **Resolves** the time window from the `--since` argument or defaults to yesterday midnight
2. **Parses** git log for all commits within the time window
3. **Scans** `TODO.md` for items completed (`[x]`) within the window
4. **Identifies** next pending items from `TODO.md` and `docs/planning/roadmap.md`, ranked by priority
5. **Detects** blockers — stale items, items tagged `[blocked]`, and dependency issues
6. **Computes** summary metrics — tasks completed, commits made, files changed
7. **Formats** the standup report using the output template
8. **Outputs** the standup to the terminal for review
9. **Saves** to `docs/standups/YYYY-MM-DD.md` when `--save` is passed

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Time Window

Determine the start boundary of the standup window from the `--since` argument.

| Input Format | Resolution |
|-------------|------------|
| `yesterday` (default) | Midnight of the previous calendar day |
| `Nd` (e.g., `2d`) | Current time minus N days |
| `Nh` (e.g., `24h`) | Current time minus N hours |
| ISO timestamp (e.g., `2025-06-14T09:00`) | Use as-is |
| No argument | Default to `yesterday` |

Store the resolved timestamp as `WINDOW_START`. The end boundary is always the current time.

### Phase 2: Scan Git Log for Commits

Run git commands to collect all commits within the window:

```bash
# All commits in the window, ordered chronologically
git log --since="$WINDOW_START" --format="%h|%s|%an|%ai" --reverse

# Diff stats for the window
git diff --stat $(git log --since="$WINDOW_START" --format="%H" | tail -1)^..HEAD

# File count and line changes
git log --since="$WINDOW_START" --format="" --numstat
```

If no commits exist in the window, note it and proceed — the standup may still have planned items and blockers.

Group commits by theme where possible (e.g., multiple commits touching the same module). Present each commit as a single-line entry with hash and message.

### Phase 3: Scan TODO.md for Completed Items

Read `TODO.md` and identify items completed within the window:

1. Find all items marked `[x]` (completed)
2. Cross-reference against git log — a completed item must have a matching commit or file modification within the window
3. Items marked `[x]` with no matching commit activity are assumed to have been completed before the window — exclude them

If `TODO.md` does not exist, skip this phase and note it in the output.

Also read `task_plan.md` if it exists and check acceptance criteria completion status.

### Phase 4: Identify Planned Items for Today

Collect pending items from planning files to populate the "Planned" section:

| Source | What to Extract |
|--------|----------------|
| `TODO.md` | Items marked `[ ]` or `[/]` (in-progress), ordered by position in file (top = higher priority) |
| `docs/planning/roadmap.md` | Active phase items that are still pending |
| `task_plan.md` | Unchecked acceptance criteria and remaining implementation steps |

Rank planned items by priority:
1. In-progress items (`[/]`) — these are already started
2. Blocked items that have become unblocked
3. Items at the top of `TODO.md` (positional priority)
4. Active roadmap phase items

Limit the planned list to **5–7 items** — a standup should reflect realistic daily capacity.

### Phase 5: Detect Blockers

Search for blockers across multiple sources:

| Source | Detection |
|--------|-----------|
| `TODO.md` | Items tagged `[blocked]`, `[waiting]`, or `[question]` |
| `docs/planning/roadmap.md` | Phases marked `[blocked]` or `[on-hold]` |
| Stale items | Pending TODOs with no matching commit activity for 5+ days |
| Git messages | Recent commits containing `blocked`, `waiting on`, `depends on` |
| Code markers | `FIXME`, `HACK`, `XXX` in files changed within the window |

Classify blockers by severity:

| Severity | Criteria |
|----------|----------|
| **Critical** | Explicitly tagged `[blocked]` with no workaround noted |
| **Warning** | Stale for 5–10 days or marked `[question]` |
| **Info** | `FIXME`/`HACK` markers or minor dependency notes |

### Phase 6: Format Standup Report

Assemble the report using the output template. Every section must have content or an explicit "None" entry — do not omit sections.

If `--save` is passed:
1. Create `docs/standups/` directory if it does not exist
2. Write the report to `docs/standups/YYYY-MM-DD.md`
3. If the file already exists (re-running the standup), overwrite it with the latest data

## Output

The terminal output and saved file follow this structure:

```
Daily Standup — YYYY-MM-DD
==========================

## Done (since yesterday)

### Completed Tasks
- [x] Add rate limiting to /api/auth endpoints
- [x] Fix token refresh race condition

### Commits
| Hash    | Message                         | Time  |
|---------|---------------------------------|-------|
| a1b2c3d | Add rate limiting middleware     | 09:15 |
| d4e5f6a | Fix token refresh race condition | 09:42 |
| b7c8d9e | Add tests for auth flow          | 10:30 |

## Planned (today)
1. [ ] Add integration tests for rate limiting
2. [ ] Update API documentation for new limits
3. [/] Implement user dashboard charts
4. [ ] Review PR #42 — database migration

## Blockers
| # | Severity | Description                                    | Source      |
|---|----------|------------------------------------------------|-------------|
| 1 | Critical | Waiting on API key from payment provider        | TODO.md:14  |
| 2 | Warning  | CSV export feature stale for 8 days             | TODO.md:22  |

## Metrics
| Metric          | Value |
|-----------------|-------|
| Tasks completed | 2     |
| Commits         | 3     |
| Files changed   | 5     |
| Lines           | +155 -12 |
```

## NEVER Do

- **Never require manual input.** The entire standup is generated from existing context files and git history. The user should not need to type what they did or plan to do.
- **Never fabricate commits or completed items.** Only report what appears in `git log` and `TODO.md` within the time window.
- **Never list more than 7 planned items.** A standup should reflect realistic daily capacity, not the entire backlog.
- **Never modify source files.** This command is strictly read-only. Do not update `TODO.md`, roadmap, or any other file (except the optional `--save` output).
- **Never include commits from outside the time window.** Respect the `--since` boundary strictly.
- **Never skip the blockers section.** Even if there are no blockers, output "No blockers identified" — explicit absence is valuable.
- **Never invent blocker severity.** Only mark items as "Critical" if they are explicitly tagged `[blocked]` in source files.
- **Never save without the `--save` flag.** Terminal-only output is the default behavior.

## Error Handling

- If no commits exist in the time window, report "No commits since `WINDOW_START`" in the Done section and proceed with planned items and blockers.
- If `TODO.md` does not exist, skip task completion scanning and note: "No TODO.md found — task tracking unavailable."
- If `docs/planning/roadmap.md` does not exist, skip roadmap-based planning and note: "No roadmap found — planned items sourced from TODO.md only."
- If `task_plan.md` does not exist, skip acceptance criteria scanning and proceed.
- If the project is not a git repository, abort with: "Not a git repository. Run this command from within a git project."
- If `--since` value cannot be parsed, abort with: "Invalid --since value. Use a duration (24h, 2d), 'yesterday', or an ISO timestamp."
- If `docs/standups/` cannot be created when `--save` is used, fall back to saving in the project root and warn the user.
- If the time window exceeds 7 days, warn: "Time window exceeds 7 days. For longer periods, consider `/sprint-review` instead."

## Automation

- **Optional automation:** Run `python3 scripts/detect_blockers.py` to detect stalled tasks, dependency chains, and stale branches.

## Related

- **Command:** `/sprint-review` (longer-period review covering full sprints)
- **Command:** `/session-summary` (single-session detail vs daily standup overview)
- **Command:** `/progress` (project-wide progress dashboard with velocity metrics)
- **Command:** `/start-task` (establishes task plans referenced in the standup)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
