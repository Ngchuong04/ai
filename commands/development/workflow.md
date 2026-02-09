---
name: workflow
model: reasoning
description: Full development workflow orchestrating intent through completion with stage gates
usage: /workflow <task> [--type feature|bugfix|refactor] [--skip-plan] [--resume]
---

# /workflow

Orchestrate the complete development lifecycle from intent to completion — nothing gets skipped.

## Usage

```
/workflow <task> [--type feature|bugfix|refactor] [--skip-plan] [--resume]
```

**Arguments:**
- `task` — Short description of the work, ticket ID, or quoted goal (e.g., `"add rate limiting to API"`)
- `--type` — Override automatic workflow type detection (`feature`, `bugfix`, `refactor`)
- `--skip-plan` — Skip the planning stage for trivial tasks (blocked for `large` and `epic` complexity)
- `--resume` — Resume a previously started workflow from the last completed stage

## Examples

```
/workflow "add OAuth2 login with Google provider"
/workflow fix-checkout-race-condition --type bugfix
/workflow "extract shared validation into a library" --type refactor
/workflow PROJ-287 --skip-plan
/workflow --resume
```

## What It Does

1. **Detects** the workflow type (feature, bugfix, refactor) from task keywords or the `--type` flag
2. **Estimates** complexity to determine which stages are required and whether `--skip-plan` is allowed
3. **Initializes** a workflow state file to track progress across all stages
4. **Executes** the Intent stage — delegates to `/start-task` to capture scope and context
5. **Executes** the Plan stage — delegates to `/start-task` plan output or `/new-feature` spec creation
6. **Executes** the Execute stage — delegates to `/new-feature`, `/refactor`, or direct implementation
7. **Executes** the Test stage — delegates to `/test-feature` to generate and run tests
8. **Executes** the Document stage — delegates to `/generate-docs` or inline documentation updates
9. **Executes** the Complete stage — delegates to `/review-code`, commits, and produces a session summary
10. **Enforces** gate checks between stages — tests must pass before documentation, build must succeed before completion
11. **Tracks** duration, decisions, and outputs at every stage in the workflow state file
12. **Outputs** a final workflow summary with all stages, timings, and artifacts produced

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Detect Workflow Type

Analyze the task description and match against the type detection table. The `--type` flag overrides auto-detection.

| Type | Keyword Signals | Primary Command | Branch Prefix |
|------|----------------|-----------------|---------------|
| **feature** | add, create, implement, build, new, introduce, support, enable | `/new-feature` | `feat/` |
| **bugfix** | fix, bug, broken, crash, error, wrong, incorrect, regression, patch | direct implementation | `fix/` |
| **refactor** | refactor, restructure, reorganize, simplify, extract, clean up, decouple | `/refactor` | `refactor/` |

If the type cannot be determined and `--type` is not provided, ask the user:
> "What type of workflow is this? (feature / bugfix / refactor)"

### Phase 2: Estimate Complexity and Resolve Stages

Score complexity using the same signals as `/start-task`:

| Complexity | Files | Dependencies | Required Stages | Skip-Plan Allowed |
|------------|-------|-------------|-----------------|-------------------|
| **trivial** | 1 | None | Intent → Execute → Test → Complete | Yes |
| **small** | 2–3 | Minor | Intent → Plan → Execute → Test → Complete | Yes |
| **medium** | 4–8 | Moderate | All stages | No |
| **large** | 9–20 | Significant | All stages | No |
| **epic** | 20+ | Cross-cutting | All stages (recommend breakdown first) | No |

If `--skip-plan` is used on a `large` or `epic` task, reject it:
> "Planning cannot be skipped for tasks of this complexity. Remove `--skip-plan` to proceed."

### Phase 3: Initialize Workflow State

Create `.workflow-state.json` in the project root to track progress:

```json
{
  "task": "<task description>",
  "type": "feature | bugfix | refactor",
  "complexity": "trivial | small | medium | large | epic",
  "branch": "<branch-name>",
  "started_at": "ISO-8601",
  "stages": {
    "intent":    { "status": "pending", "started_at": null, "completed_at": null, "output": null },
    "plan":      { "status": "pending", "started_at": null, "completed_at": null, "output": null },
    "execute":   { "status": "pending", "started_at": null, "completed_at": null, "output": null },
    "test":      { "status": "pending", "started_at": null, "completed_at": null, "output": null },
    "document":  { "status": "pending", "started_at": null, "completed_at": null, "output": null },
    "complete":  { "status": "pending", "started_at": null, "completed_at": null, "output": null }
  },
  "gate_results": {},
  "artifacts": []
}
```

If `--resume` is passed and `.workflow-state.json` exists, read it and jump to the first stage with status `pending`. If the file does not exist, abort:
> "No workflow state found. Start a new workflow without `--resume`."

### Phase 4: Stage Execution

Execute each stage in order. Update `.workflow-state.json` after each stage completes.

#### Stage 1: Intent

| Property | Value |
|----------|-------|
| **Delegates to** | `/start-task <task>` |
| **Input** | Task description from the user |
| **Output** | `task_plan.md` with scope, criteria, and context files |
| **Gate to next** | `task_plan.md` exists and contains acceptance criteria |

Run `/start-task` with the task argument. Verify the output file was created and contains at least one acceptance criterion. Record the path in `artifacts`.

#### Stage 2: Plan

| Property | Value |
|----------|-------|
| **Delegates to** | `/new-feature` spec phase (feature) or `/refactor` analysis phase (refactor) or skip (bugfix trivial) |
| **Input** | `task_plan.md` from Stage 1 |
| **Output** | Implementation plan approved by user |
| **Gate to next** | User explicitly approves the plan |
| **Skip condition** | `--skip-plan` flag and complexity is `trivial` or `small` |

For **feature** workflows: run the planning and spec phases of `/new-feature`.
For **refactor** workflows: run Phases 1–4 of `/refactor` (identify, safety check, analyze, plan).
For **bugfix** workflows: read the relevant code, identify the root cause, and present a fix plan.

Present the plan and wait for approval:
> "Plan ready for review. Approve to proceed to implementation, or suggest changes."

#### Stage 3: Execute

| Property | Value |
|----------|-------|
| **Delegates to** | `/new-feature` (feature) or `/refactor` (refactor) or direct implementation (bugfix) |
| **Input** | Approved plan from Stage 2 |
| **Output** | Working implementation with all changes applied |
| **Gate to next** | Code compiles/builds without errors; linter passes |

For **feature** workflows: run the implementation phases of `/new-feature`.
For **refactor** workflows: run Phase 5 (incremental execution) of `/refactor`.
For **bugfix** workflows: apply the fix, verify the specific bug is resolved.

After execution, run the build gate:

```
# Detect and run build/compile check
npm run build          # Node.js projects
cargo check            # Rust projects
go build ./...         # Go projects
python -m py_compile   # Python projects
```

If the build fails, fix the errors before proceeding. Do not advance to testing with broken code.

#### Stage 4: Test

| Property | Value |
|----------|-------|
| **Delegates to** | `/test-feature <feature>` |
| **Input** | Implemented code from Stage 3 |
| **Output** | Test files created, all tests passing |
| **Gate to next** | All tests pass (zero failures) |

Run `/test-feature` targeting the changed files. If tests fail:
1. Attempt to fix the test (not the source) up to 3 times.
2. If tests still fail, fix the source code and re-run.
3. If the issue persists, stop and report to the user.

Record test count and pass rate in the workflow state.

#### Stage 5: Document

| Property | Value |
|----------|-------|
| **Delegates to** | `/generate-docs` or inline documentation |
| **Input** | Implemented and tested code from Stages 3–4 |
| **Output** | Updated documentation, JSDoc/docstrings, changelog entry |
| **Gate to next** | At minimum, public API functions are documented |

Documentation tasks by workflow type:

| Type | Documentation Required |
|------|----------------------|
| **feature** | API docs, usage examples, changelog entry, README update if public-facing |
| **bugfix** | Changelog entry, comment explaining the fix and root cause |
| **refactor** | Update any docs referencing changed APIs, architecture notes if structural |

If `/generate-docs` is not available, add documentation inline: JSDoc for TypeScript, docstrings for Python, doc comments for Rust/Go.

#### Stage 6: Complete

| Property | Value |
|----------|-------|
| **Delegates to** | `/review-code`, git commit, session summary |
| **Input** | All artifacts from previous stages |
| **Output** | Committed code, review findings addressed, workflow summary |
| **Gate** | None — this is the final stage |

Steps:
1. Run `/review-code` on all changed files. Address any critical findings.
2. Stage and commit all changes with a descriptive message referencing the task.
3. Update `task_plan.md` to mark acceptance criteria as complete.
4. Remove `.workflow-state.json` (workflow is finished).
5. Output the final workflow summary (see Output section).

### Phase 5: Gate Checks

Gates enforce quality between stages. A stage cannot begin until its predecessor's gate passes.

| Gate | Between | Check | On Failure |
|------|---------|-------|------------|
| **Intent gate** | Intent → Plan | `task_plan.md` exists with acceptance criteria | Re-run `/start-task` |
| **Plan gate** | Plan → Execute | User approved the plan | Re-present plan for approval |
| **Build gate** | Execute → Test | Code compiles, no syntax errors, linter clean | Fix errors before advancing |
| **Test gate** | Test → Document | All tests pass (0 failures) | Fix failures before advancing |
| **Docs gate** | Document → Complete | Public functions documented | Add missing documentation |

If a gate fails three consecutive times, stop the workflow and report:
> "Gate [name] failed 3 times. Manual intervention required. Workflow paused at stage [stage]."

## Output

The command produces a final workflow summary after all stages complete:

```
Workflow Complete
=================
Task:         [description]
Type:         [feature | bugfix | refactor]
Complexity:   [trivial | small | medium | large | epic]
Branch:       [branch-name]
Duration:     [total elapsed time]

Stages
------
  ✓ Intent      [duration]   task_plan.md created
  ✓ Plan        [duration]   implementation plan approved
  ✓ Execute     [duration]   [N] files changed, [M] additions, [K] deletions
  ✓ Test        [duration]   [X] tests passed, 0 failed
  ✓ Document    [duration]   [D] files documented, changelog updated
  ✓ Complete    [duration]   code reviewed, committed

Artifacts
---------
  task_plan.md                    — task scope and acceptance criteria
  src/auth/oauth.ts               — [new | modified]
  src/auth/__tests__/oauth.test.ts — [new]
  CHANGELOG.md                    — [updated]

Gate Results
------------
  Intent  → Plan:     ✓ acceptance criteria present
  Plan    → Execute:  ✓ plan approved
  Execute → Test:     ✓ build clean, linter clean
  Test    → Document: ✓ 14/14 tests passing
  Document→ Complete: ✓ public API documented

Next Steps
----------
  1. Push branch: git push -u origin [branch-name]
  2. Open PR: gh pr create --title "[task]"
  3. Request review from team
```

## NEVER Do

- **NEVER skip the test stage.** Every workflow produces tested code. There are no exceptions.
- **NEVER advance past a failed gate.** Gates exist to prevent compounding errors. Fix the failure, then proceed.
- **NEVER start execution without a plan** on medium, large, or epic tasks. Planning prevents wasted implementation effort.
- **NEVER modify `.workflow-state.json` manually.** The workflow command owns this file. Manual edits corrupt state tracking.
- **NEVER run the complete stage with failing tests.** The test gate must pass before documentation or completion.
- **NEVER skip documentation for public-facing features.** Undocumented features are unfinished features.
- **NEVER delete `.workflow-state.json` before the workflow finishes.** It is required for `--resume` and progress tracking.
- **NEVER auto-commit without the user seeing a review summary.** The user must confirm before code is committed.

## Error Handling

- If `/start-task` fails or is unavailable, gather intent manually: ask for task description, scope, and acceptance criteria, then write `task_plan.md` directly.
- If `/new-feature` or `/refactor` is unavailable, execute implementation directly using `Read`, `Edit`, and `Shell` tools with the plan as a guide.
- If `/test-feature` is unavailable, detect the test framework and generate tests manually following project conventions.
- If `/generate-docs` is unavailable, add inline documentation (JSDoc, docstrings, doc comments) to all public APIs.
- If `/review-code` is unavailable, perform a manual review: check correctness, security, and performance of all changed files.
- If `.workflow-state.json` is corrupted or unparseable, rebuild it from git history and existing artifacts, then confirm with the user before resuming.
- If the user abandons the workflow mid-stage, preserve `.workflow-state.json` so `--resume` can pick up later.
- If an epic task is detected, recommend breaking it into sub-workflows before proceeding: "This task is epic-scale. Break it into 3–5 smaller `/workflow` invocations."

## Automation

- **Optional automation:** Run `python3 scripts/auto_update_plan.py` to auto-update task_plan.md from git activity.
- **Optional automation:** Run `python3 scripts/sync_from_git.py` to sync git state to context files.
- **Optional automation:** Run `python3 scripts/changelog_preview.py` to preview unreleased changelog entries.

## Related

- **Command:** `/start-task` (intent and planning — Stage 1)
- **Command:** `/new-feature` (feature implementation — Stages 2–3)
- **Command:** `/refactor` (refactoring implementation — Stages 2–3)
- **Command:** `/test-feature` (test generation — Stage 4)
- **Command:** `/generate-docs` (documentation — Stage 5)
- **Command:** `/review-code` (code review — Stage 6)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
