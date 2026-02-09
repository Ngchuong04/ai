---
name: sprint-review
model: standard
description: Generate a sprint review summary from completed work, metrics, and retrospective signals
usage: /sprint-review [--days <N>] [--save] [--team]
---

# /sprint-review

Generate a comprehensive sprint review report from git history, completed TODOs, roadmap progress, and retrospective signals — covering a full sprint period.

## Usage

```
/sprint-review [--days <N>] [--save] [--team]
```

**Arguments:**
- `--days` (optional) — Sprint duration in days. Defaults to `14` (two-week sprint).
- `--save` (optional) — Save the review to `docs/sprints/sprint-YYYY-MM-DD.md` in addition to terminal output.
- `--team` (optional) — Include per-author breakdowns in commits and metrics sections.

## Examples

```
/sprint-review                                # Two-week sprint review (default)
/sprint-review --days 7                       # One-week sprint review
/sprint-review --days 21                      # Three-week sprint
/sprint-review --days 14 --save               # Default sprint, save to file
/sprint-review --days 14 --team               # Include per-author breakdown
/sprint-review --days 14 --save --team        # Full report saved with team stats
```

## What It Does

1. **Resolves** the sprint window from `--days` argument (defaults to 14 days back from today)
2. **Parses** git log for all commits within the sprint window, grouped by day and author
3. **Scans** `TODO.md` for items completed during the sprint
4. **Reads** `docs/planning/roadmap.md` to determine roadmap phase progress
5. **Collects** demo-worthy items — features, UI changes, and user-facing improvements
6. **Computes** sprint metrics — velocity, throughput, completion rate, and trends
7. **Extracts** retrospective signals — what went well, what was painful, recurring patterns
8. **Identifies** carryover items — work planned but not completed during the sprint
9. **Formats** the sprint review using the output template
10. **Outputs** the review to the terminal and optionally saves to file

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Resolve Sprint Window

Determine the sprint boundaries from the `--days` argument.

| Parameter | Resolution |
|-----------|------------|
| `--days 14` (default) | 14 calendar days before today at midnight → today at current time |
| `--days 7` | 7 calendar days before today at midnight → today |
| `--days N` | N calendar days before today at midnight → today |

Store as `SPRINT_START` and `SPRINT_END`. All subsequent phases use this window.

### Phase 2: Parse Git History

Run git commands to collect the full commit history for the sprint:

```bash
# All commits in the sprint, chronological order
git log --since="$SPRINT_START" --until="$SPRINT_END" --format="%H|%h|%s|%an|%ai" --reverse

# Commits per day
git log --since="$SPRINT_START" --until="$SPRINT_END" --format="%ad" --date=short | sort | uniq -c

# File change stats
git log --since="$SPRINT_START" --until="$SPRINT_END" --format="" --numstat

# Per-author commit counts (if --team)
git log --since="$SPRINT_START" --until="$SPRINT_END" --format="%an" | sort | uniq -c | sort -rn
```

Group commits into logical categories by scanning commit message prefixes and keywords:

| Category | Keyword Signals |
|----------|----------------|
| **Features** | `feat:`, `add`, `implement`, `introduce`, `new`, `create` |
| **Bug Fixes** | `fix:`, `bug`, `patch`, `resolve`, `correct` |
| **Refactoring** | `refactor:`, `clean`, `restructure`, `simplify`, `extract` |
| **Infrastructure** | `ci:`, `build:`, `deploy`, `docker`, `config`, `deps` |
| **Documentation** | `docs:`, `readme`, `comment`, `guide` |
| **Tests** | `test:`, `spec`, `coverage`, `assert` |

### Phase 3: Scan Completed Work

Read planning files to identify work completed during the sprint:

| File | What to Extract |
|------|----------------|
| `TODO.md` | Items marked `[x]` with matching commit activity in the sprint window |
| `docs/planning/roadmap.md` | Phase items completed, phases that transitioned to "Done" |
| `task_plan.md` | Acceptance criteria checked off during the sprint |
| `docs/sessions/*.md` | Session summaries from within the sprint window (if they exist) |
| `CHANGELOG.md` | Entries added during the sprint window |

Cross-reference completed TODOs against git history to validate they were truly completed within the sprint, not before.

### Phase 4: Identify Demo-Worthy Items

From the completed work, extract items suitable for a sprint demo — user-visible changes that stakeholders would care about:

| Signal | Demo Candidate |
|--------|---------------|
| New API endpoint or route | Yes — demonstrate with example request/response |
| UI component added or changed | Yes — screenshot or describe the visual change |
| Performance improvement | Yes — include before/after metrics if available |
| New CLI command or tool | Yes — show example usage |
| Internal refactor only | No — mention in metrics, not demo |
| CI/CD pipeline change | No — unless it enables a new workflow |
| Dependency update | No — unless it fixes a user-facing issue |

Present demo items as a numbered list with a one-line description and the evidence (commit hash, file, or TODO reference).

### Phase 5: Compute Sprint Metrics

Calculate quantitative metrics for the sprint:

| Metric | Calculation |
|--------|-------------|
| **Tasks completed** | Count of `[x]` items in `TODO.md` with sprint-window commits |
| **Tasks planned** | Count of items that were `[ ]` at sprint start (infer from git history of `TODO.md`) |
| **Completion rate** | `tasks_completed / tasks_planned * 100` |
| **Total commits** | Count of commits in the sprint window |
| **Files changed** | Unique files modified across all commits |
| **Lines added** | Sum of insertions from `--numstat` |
| **Lines removed** | Sum of deletions from `--numstat` |
| **Commits/day** | `total_commits / days` |
| **Tasks/day** | `tasks_completed / days` |
| **Velocity trend** | Compare first-half vs second-half commit rates |
| **Focus ratio** | `feature_commits / total_commits * 100` — higher means more feature work vs maintenance |

If `--team` is passed, compute per-author breakdowns for commits, lines changed, and top files modified.

### Phase 6: Extract Retrospective Signals

Automatically detect retrospective-worthy patterns from the sprint data:

**What went well (detect from):**
- High completion rate (>80%)
- Velocity trend upward (▲)
- Zero blockers or blockers quickly resolved
- Clean commit history (few reverts, few "fix fix" commits)
- Tests added alongside features

**What needs improvement (detect from):**
- Low completion rate (<60%)
- Velocity trend downward (▼)
- Persistent blockers (tagged `[blocked]` for >3 days)
- High churn files (same file modified in 5+ commits)
- "Fix" commits that reference the same area repeatedly
- Missing tests for new features
- Revert commits

**Patterns to flag:**
- Commits concentrated in the last 2 days of the sprint ("sprint cramming")
- Large commits (>200 lines changed) vs many small commits
- Ratio of bug fixes to features (>50% bug fixes suggests tech debt)

### Phase 7: Identify Carryover Items

Find work that was planned for this sprint but not completed:

1. Read `TODO.md` for items still marked `[ ]` that have partial commit activity in the sprint
2. Check `task_plan.md` for unchecked acceptance criteria
3. Check roadmap active phase for incomplete items
4. Flag items that were in-progress (`[/]`) but not completed

Classify carryover by reason:

| Reason | Detection |
|--------|-----------|
| **Not started** | `[ ]` with zero commit activity |
| **Partially done** | `[ ]` or `[/]` with some commit activity |
| **Blocked** | Tagged `[blocked]` or `[waiting]` |
| **Descoped** | Tagged `[-]` or `[cancelled]` during the sprint |

### Phase 8: Format and Output

Assemble the full sprint review using the output template. If `--save` is passed:

1. Create `docs/sprints/` directory if it does not exist
2. Write the review to `docs/sprints/sprint-YYYY-MM-DD.md` (date = sprint end date)
3. If the file already exists, overwrite with the latest data

## Output

The terminal output and saved file follow this structure:

```
Sprint Review — YYYY-MM-DD to YYYY-MM-DD
=========================================

Sprint Duration: N days
Generated: YYYY-MM-DD HH:MM

## Completed Work

### Features
- [x] User dashboard with real-time charts (a1b2c3d, d4e5f6a)
- [x] Rate limiting on /api/auth endpoints (b7c8d9e)
- [x] CSV export for reports (f0a1b2c)

### Bug Fixes
- [x] Token refresh race condition (c3d4e5f)
- [x] Pagination offset error on search results (e6f7a8b)

### Infrastructure
- [x] Upgrade Node.js to v20 LTS (d9e0f1a)
- [x] Add GitHub Actions caching for CI (a2b3c4d)

### Documentation
- [x] API rate limiting guide (f5a6b7c)

## Demo Items
1. User dashboard — real-time charts with WebSocket updates (src/components/Dashboard.tsx)
2. CSV export — one-click download from any report page (src/features/reports/export.ts)
3. Rate limiting — returns 429 with Retry-After header (src/middleware/rate-limit.ts)

## Sprint Metrics

| Metric           | Value         |
|------------------|---------------|
| Tasks completed  | 8             |
| Tasks planned    | 10            |
| Completion rate  | 80%           |
| Total commits    | 34            |
| Files changed    | 28            |
| Lines added      | +1,240        |
| Lines removed    | -380          |
| Commits/day      | 2.4           |
| Tasks/day        | 0.6           |
| Velocity trend   | ▲ +12%        |
| Focus ratio      | 65% features  |

## Carryover Items
| Item                            | Status          | Reason          |
|---------------------------------|-----------------|-----------------|
| WebSocket reconnection logic    | [/] In-progress | Partially done  |
| Admin role permissions          | [ ] Pending     | Not started     |

## Retrospective Signals

### What Went Well
- 80% completion rate — strong sprint execution
- Tests added for all new features (12 test files)
- Velocity trending upward (+12%) vs previous period
- Zero revert commits

### Needs Improvement
- 60% of commits landed in the last 3 days (sprint cramming detected)
- src/auth/token.ts modified in 7 commits — high churn suggests unclear requirements
- 2 carryover items — consider smaller scope for next sprint

### Patterns
- Bug fix ratio: 25% — healthy balance of feature vs maintenance work
- Average commit size: 47 lines — good granularity

## Next Sprint Candidates
1. [/] WebSocket reconnection logic (carryover — partially done)
2. [ ] Admin role permissions (carryover — not started)
3. [ ] E2E test suite for auth flows
4. [ ] Performance audit for dashboard queries
5. [ ] API versioning strategy decision
```

## NEVER Do

- **Never fabricate completed work.** Only report items verified through `git log` and `TODO.md` state within the sprint window.
- **Never modify source files.** This command is strictly read-only. Do not update `TODO.md`, roadmap, or any planning files.
- **Never invent retrospective signals.** Only flag patterns detectable from commit history, TODO state, and file change data.
- **Never include commits from outside the sprint window.** Respect the `--days` boundary strictly.
- **Never present carryover as failure.** Frame it neutrally — carryover is normal and helps inform next sprint planning.
- **Never skip the metrics section.** Quantitative data is essential for sprint reviews — always compute and display it.
- **Never report velocity trend without sufficient data.** If the sprint has fewer than 4 commits, note that trend data is unreliable.
- **Never save without the `--save` flag.** Terminal-only output is the default behavior.
- **Never list more than 7 next sprint candidates.** Keep the next sprint focused and realistic.
- **Never attribute individual performance judgments.** The `--team` flag shows contribution distribution, not performance ratings.

## Error Handling

- If no commits exist in the sprint window, report "No commits in the last N days" and suggest adjusting `--days`. Proceed with TODO-only analysis.
- If `TODO.md` does not exist, skip task completion scanning and note: "No TODO.md found — task completion metrics unavailable."
- If `docs/planning/roadmap.md` does not exist, skip roadmap phase analysis and note: "No roadmap found — phase progress unavailable."
- If `task_plan.md` does not exist, skip acceptance criteria analysis and proceed.
- If the project is not a git repository, abort with: "Not a git repository. Run this command from within a git project."
- If `--days` is less than 1 or greater than 90, abort with: "Invalid --days value. Use a value between 1 and 90. For daily summaries, use `/daily-standup`."
- If `docs/sprints/` cannot be created when `--save` is used, fall back to saving in the project root and warn the user.
- If `--team` is used but all commits have the same author, skip the per-author breakdown and note: "Single contributor detected — team breakdown skipped."
- If session summary files exist in `docs/sessions/` for the sprint window, incorporate them. If not, proceed without them.

## Related

- **Command:** `/daily-standup` (daily granularity vs sprint-level review)
- **Command:** `/progress` (real-time progress dashboard with velocity metrics)
- **Command:** `/session-summary` (single-session detail for use during a sprint)
- **Command:** `/start-task` (creates task plans referenced in the sprint review)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
