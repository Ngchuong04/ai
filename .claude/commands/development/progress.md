---
name: progress
model: fast
description: Show progress across all tracking files — TODOs, roadmap phases, commits, blockers, and velocity
usage: /progress [--days <N>] [--roadmap <path>]
---

# /progress

Display a unified progress dashboard across TODOs, roadmap phases, recent commits, blockers, and velocity metrics.

## Usage

```
/progress [--days <N>] [--roadmap <path>]
```

**Arguments:**
- `--days` (optional) — Lookback window for commit history and staleness detection. Defaults to `7`.
- `--roadmap` (optional) — Path to the roadmap file. Defaults to `docs/planning/roadmap.md`.

## Examples

```
/progress                                    # Full dashboard with 7-day lookback (default)
/progress --days 14                          # Two-week lookback for velocity and staleness
/progress --days 3                           # Short window for daily standups
/progress --roadmap ROADMAP.md              # Use a custom roadmap file location
/progress --days 30 --roadmap docs/PLAN.md  # Monthly view with custom roadmap
```

## What It Does

1. **Reads** `TODO.md` and counts items by status — completed, in-progress, pending, and blocked
2. **Reads** the roadmap file and determines phase status — done, active, upcoming, or blocked
3. **Parses** git log for the lookback window to collect commits, contributors, and files changed
4. **Detects** stale items — TODOs and roadmap entries with no matching commit activity for N days
5. **Identifies** blockers from TODO tags (`[blocked]`, `[question]`) and roadmap annotations
6. **Calculates** velocity metrics — tasks completed per day, rolling average, and trend direction
7. **Computes** completion percentages for the overall project and per roadmap phase
8. **Renders** progress bars and a summary dashboard in markdown format
9. **Highlights** at-risk items — stale work, declining velocity, or phases past their target date
10. **Outputs** the full dashboard to the terminal for review

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Read TODO Status

Read `TODO.md` and classify every item using regex pattern matching:

| Pattern | Status | Symbol |
|---------|--------|--------|
| `- [x]` or `* [x]` | **Completed** | `[x]` |
| `- [-]` or `~.*~` | **Cancelled** | `[-]` |
| `- [/]` or `[in.progress]` tag | **In-Progress** | `[/]` |
| `- [ ]` with `[blocked]` tag | **Blocked** | `[!]` |
| `- [ ]` (default) | **Pending** | `[ ]` |

Use these regex patterns for detection:

```
completed:    /^[\s]*[-*]\s*\[x\]/mi
cancelled:    /^[\s]*[-*]\s*\[-\]/mi
in_progress:  /^[\s]*[-*]\s*\[\/\]|(?:\[in.progress\])/mi
blocked:      /^[\s]*[-*]\s*\[ \].*\[blocked\]/mi
pending:       /^[\s]*[-*]\s*\[ \]/mi
```

Group TODOs by section header (H2/H3) if the file uses headings. Count items per status and compute the overall completion percentage:

```
completion_pct = (completed + cancelled) / total * 100
```

### Phase 2: Read Roadmap Phases

Read the roadmap file and extract phase information. Detect phases from H2/H3 headers and classify:

| Phase Marker | Status |
|-------------|--------|
| Header contains `✅`, `[done]`, or `[complete]` | **Done** |
| Header contains `🔄`, `[active]`, `[current]`, or `[in-progress]` | **Active** |
| Header contains `⏳`, `[upcoming]`, `[planned]`, or `[next]` | **Upcoming** |
| Header contains `🚫`, `[blocked]`, or `[on-hold]` | **Blocked** |
| No marker — infer from child items | **Inferred** |

For phases without explicit markers, infer status from child TODO items:
- All `[x]` → Done
- Mix of `[x]` and `[ ]` → Active
- All `[ ]` → Upcoming

Calculate per-phase completion:

```
phase_pct = phase_completed / phase_total * 100
```

### Phase 3: Parse Git History

Run git commands to collect commit data within the lookback window:

```bash
# Commits in the lookback window
git log --since="$DAYS days ago" --format="%H|%h|%s|%an|%ai" --reverse

# Files changed with stats
git log --since="$DAYS days ago" --format="" --numstat

# Commit count per day
git log --since="$DAYS days ago" --format="%ad" --date=short | sort | uniq -c
```

Build a per-day commit frequency table for velocity calculations.

### Phase 4: Detect Stale Items

Cross-reference TODO items and roadmap entries against git history to find stale work:

1. Extract keywords from each pending or in-progress TODO item
2. Search git log messages for those keywords within the lookback window
3. Flag items with **zero matching commits** as stale

| Staleness | Threshold | Label |
|-----------|-----------|-------|
| **Fresh** | Activity within the last 3 days | — |
| **Aging** | No activity for 4–7 days | `⚠ aging` |
| **Stale** | No activity for 8–14 days | `🔴 stale` |
| **Dormant** | No activity for 15+ days | `💀 dormant` |

Staleness thresholds scale with the `--days` flag — if `--days 30`, the thresholds double.

### Phase 5: Identify Blockers

Collect blockers from multiple sources:

| Source | Detection |
|--------|-----------|
| `TODO.md` | Items tagged `[blocked]`, `[question]`, or `[waiting]` |
| Roadmap | Phases marked `[blocked]` or `[on-hold]` |
| Git messages | Commits containing `blocked`, `blocker`, `waiting on`, `depends on` |
| Code comments | `FIXME`, `HACK`, `XXX` markers in files changed within the lookback window |

Deduplicate blockers by keyword similarity and present as a flat list with source attribution.

### Phase 6: Calculate Velocity

Compute velocity metrics from TODO completions and commit history:

```
tasks_per_day     = completed_in_window / days
commits_per_day   = total_commits / days
trend             = (last_half_avg - first_half_avg) / first_half_avg * 100
```

| Metric | Calculation |
|--------|-------------|
| **Tasks/day** | TODOs marked `[x]` with matching commits in window ÷ days |
| **Commits/day** | Total commits in window ÷ days |
| **Trend** | Compare first-half vs second-half of window, report as ▲/▼/► percentage |
| **Est. completion** | Pending items ÷ tasks/day = estimated days remaining |

If velocity is zero (no completions in the window), report "No tasks completed in the last N days" and skip estimated completion.

### Phase 7: Render Progress Bars

Generate markdown-compatible progress bars using block characters:

```
# Full block: █  Empty block: ░  Width: 20 characters

def progress_bar(pct):
    filled = round(pct / 100 * 20)
    empty  = 20 - filled
    return f"{'█' * filled}{'░' * empty} {pct:.0f}%"

# Examples:
# ████████████████░░░░ 80%
# ██████████░░░░░░░░░░ 50%
# ████░░░░░░░░░░░░░░░░ 20%
```

Render a bar for:
- Overall project completion
- Each roadmap phase
- TODO categories (completed vs total)

### Phase 8: Assemble Dashboard

Combine all data into the output template (see Output section). Ensure every section has data or an explicit "N/A" note. Output to the terminal.

## Output

The terminal output follows this structure:

```markdown
# Progress Dashboard — YYYY-MM-DD

**Window:** Last N days
**Generated:** YYYY-MM-DD HH:MM

---

## TODO Status

| Status      | Count | Bar                          |
|-------------|-------|------------------------------|
| ✅ Completed | 12    | ████████████████░░░░ 80%     |
| 🔄 In-Progress | 2  | ██░░░░░░░░░░░░░░░░░░ 13%     |
| ⏳ Pending   | 1     | █░░░░░░░░░░░░░░░░░░░ 7%      |
| 🚫 Blocked   | 0     | ░░░░░░░░░░░░░░░░░░░░ 0%      |
| **Total**   | **15** | ████████████████░░░░ **80%** |

## Roadmap Phases

| Phase                    | Status   | Progress                     |
|--------------------------|----------|------------------------------|
| Phase 1: Foundation      | ✅ Done   | ████████████████████ 100%    |
| Phase 2: Core Features   | 🔄 Active | ████████████░░░░░░░░ 60%     |
| Phase 3: Polish          | ⏳ Upcoming | ░░░░░░░░░░░░░░░░░░░░ 0%    |

## Recent Commits (last N days)

| Date       | Count | Highlights                                |
|------------|-------|-------------------------------------------|
| 2026-02-06 | 4     | Add auth middleware, fix token refresh     |
| 2026-02-05 | 6     | Implement user dashboard, add tests        |
| 2026-02-04 | 2     | Update dependencies, fix CI pipeline       |

**Total:** 12 commits across 8 files (+340, -87 lines)

## Blockers

| # | Source     | Description                                   |
|---|-----------|-----------------------------------------------|
| 1 | TODO.md:8  | Waiting on API key from payment provider       |
| 2 | roadmap    | Phase 3 blocked on design review completion    |

## Stale Items

| Item                              | Last Activity | Status       |
|-----------------------------------|---------------|--------------|
| Add CSV export to reports         | 12 days ago   | 🔴 stale      |
| Refactor notification service     | 18 days ago   | 💀 dormant    |

## Velocity

| Metric            | Value          |
|-------------------|----------------|
| Tasks/day         | 1.7            |
| Commits/day       | 4.2            |
| Trend (7d)        | ▲ +15%         |
| Est. completion   | ~3 days        |

---

Overall: ████████████████░░░░ 80% complete
```

## NEVER Do

- **Never modify `TODO.md` or the roadmap.** This command is read-only. Report status without changing source files.
- **Never fabricate commit data.** Only include commits that appear in `git log` for the lookback window.
- **Never count the same item twice.** Deduplicate TODOs that appear in both `TODO.md` and the roadmap.
- **Never report velocity without sufficient data.** If the window contains fewer than 2 completed tasks, note that velocity is unreliable.
- **Never assume item status from keywords alone.** Use the checkbox pattern (`[x]`, `[ ]`) as the source of truth, not the text content.
- **Never skip staleness detection.** Stale items are the most actionable insight — always surface them.
- **Never render progress bars wider than 20 characters.** Wider bars break alignment in terminal output and narrow editors.
- **Never report estimated completion as a commitment.** Always prefix with `~` or `est.` and note that it assumes constant velocity.

## Error Handling

- If `TODO.md` does not exist, skip the TODO section and note: "No TODO.md found — create one to enable task tracking."
- If the roadmap file does not exist, skip the roadmap section and note: "No roadmap found at `[path]`. Use `--roadmap` to specify a custom location."
- If the git repository has no commits in the lookback window, report: "No commits in the last N days. Expand the window with `--days`."
- If the project is not a git repository, skip commit history, velocity, and staleness detection. Report TODO and roadmap status only.
- If `TODO.md` uses a non-standard format (no checkboxes), attempt to parse by line and warn: "Non-standard TODO format detected — counts may be approximate."
- If velocity is zero, skip estimated completion and note: "No tasks completed in the window — estimated completion unavailable."

## Automation

- **Optional automation:** Run `python3 scripts/context_health.py` to score context health (0–100) across freshness, completeness, consistency, and coverage.
- **Optional automation:** Run `python3 scripts/aggregate_context.py` to aggregate all context files into a unified summary.

## Related

- **Command:** `/session-summary` (detailed single-session view vs cross-session progress)
- **Command:** `/start-task` (creates the task plans that feed into progress tracking)
- **Command:** `/review-code` (quality check before marking tasks complete)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
