---
name: intent
model: fast
description: Quick intent capture at the start of any work session
usage: /intent <goal>
---

# /intent

Capture what you want to accomplish in natural language, match it against existing work, and log a session file — all without full planning overhead.

## Usage

```
/intent <goal>
/intent --detailed <goal>
```

**Arguments:**
- `goal` — What you want to accomplish, in plain language (e.g., `"fix the login redirect bug"`, `"add dark mode"`)
- `--detailed` — Optional flag to expand intent capture with scope, constraints, and related file discovery

## Examples

```
/intent "fix the broken logout flow"
/intent refactor the auth middleware
/intent "add pagination to the users endpoint"
/intent --detailed "migrate from REST to GraphQL for the billing service"
/intent PROJ-281
```

## What It Does

1. **Prompts** for a goal if none is provided, accepting free-form natural language
2. **Parses** the goal into structured intent fields: action, target, and scope
3. **Detects** the intent mode — quick (default) or detailed (when `--detailed` is passed or complexity warrants it)
4. **Reads** `TODO.md` and `docs/planning/roadmap.md` to find related or duplicate items
5. **Searches** recent git history (`git log --oneline -15`) for commits touching the same area
6. **Matches** existing TODOs by keyword overlap, file path references, and semantic similarity
7. **Creates** a session file at `.cursor/sessions/YYYY-MM-DD-HHMMSS.md` with the captured intent
8. **Displays** related context — matching TODOs, recent commits, and relevant files — so you can start work immediately
9. **Suggests** next actions: jump straight into coding, or escalate to `/start-task` if the scope is large
10. **Keeps** a lightweight session log so you can resume context after breaks or across days

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Capture the Goal

If a goal argument is provided, use it directly. Otherwise, prompt:

> "What do you want to work on? (one sentence is fine)"

Accept any format — sentence, ticket ID, file path, keyword phrase. Do not require structure.

### Phase 2: Parse Intent

Extract structured fields from the raw goal using the intent parsing table:

| Field | How to Extract | Example |
|-------|---------------|---------|
| **Action** | First verb or verb phrase | `fix`, `add`, `refactor`, `migrate`, `update` |
| **Target** | Primary noun or system being acted on | `login redirect`, `auth middleware`, `users endpoint` |
| **Scope** | Implied boundaries — files, modules, services | `auth/`, `api/users`, `billing service` |
| **Qualifier** | Adjectives or constraints that narrow intent | `broken`, `slow`, `for multi-tenant` |

If the goal is a ticket ID (e.g., `PROJ-281`), search for it in `TODO.md`, commit messages, and branch names to resolve it to a description.

### Phase 3: Choose Mode

| Mode | When | What It Captures |
|------|------|-----------------|
| **Quick** | Default — goal is clear and scoped | Action, target, scope, related TODOs |
| **Detailed** | `--detailed` flag, or goal implies cross-cutting work | Everything in quick + constraints, affected files, risks, suggested breakdown |

Auto-escalate to detailed if any of these signals are present:
- Goal mentions multiple services or modules
- Goal contains words like `migrate`, `rewrite`, `redesign`, `overhaul`
- More than 5 related TODOs are found

### Phase 4: Match Related TODOs

Search for related work across project files:

1. Tokenize the goal into keywords (strip stop words).
2. Search `TODO.md` for lines containing any keyword.
3. Search `docs/planning/roadmap.md` for matching items.
4. Run `git log --oneline -15 --grep="<keyword>"` for each significant keyword.

Score each match:

| Match Quality | Criteria | Display |
|--------------|----------|---------|
| **Strong** | 2+ keyword overlaps or exact target match | Show with highlight |
| **Moderate** | 1 keyword overlap or same scope area | Show normally |
| **Weak** | Tangential keyword match only | Show collapsed or omit |

Present matches ranked by quality:

```
Related work found:
  [strong]   TODO.md:8        — "[ ] Fix redirect loop after logout"
  [strong]   commit 3a1f2c9   — "auth: add session expiry check"
  [moderate] roadmap.md:22    — "[ ] Auth hardening (backlog)"
```

If no matches are found, state: "No related TODOs or recent commits found. Starting fresh."

### Phase 5: Create Session File

Write a session file to `.cursor/sessions/YYYY-MM-DD-HHMMSS.md`. Create the `.cursor/sessions/` directory if it does not exist.

**Quick mode template:**

```markdown
# Session: [YYYY-MM-DD HH:MM]

## Intent
**Goal:** [raw goal as entered]
**Action:** [parsed action]
**Target:** [parsed target]
**Scope:** [parsed scope]

## Related Work
- [matched TODO or commit, with source and line]
- [matched TODO or commit, with source and line]

## Status
- [x] Intent captured
- [ ] Work in progress
- [ ] Done
```

**Detailed mode template** (extends quick):

```markdown
# Session: [YYYY-MM-DD HH:MM]

## Intent
**Goal:** [raw goal as entered]
**Action:** [parsed action]
**Target:** [parsed target]
**Scope:** [parsed scope]
**Qualifier:** [parsed qualifier, if any]

## Related Work
- [matched TODO or commit, with source and line]
- [matched TODO or commit, with source and line]

## Context
**Affected files:**
- `path/to/file.ts` — [why relevant]
- `path/to/other.ts` — [why relevant]

**Constraints:**
- [constraint or non-goal, if identified]

**Risks:**
- [risk, if scope is large or ambiguous]

## Status
- [x] Intent captured
- [ ] Scope confirmed
- [ ] Work in progress
- [ ] Done
```

### Phase 6: Display Summary and Next Actions

Output the captured intent and suggest what to do next.

## Output

The command creates one file:

- **Created:** `.cursor/sessions/YYYY-MM-DD-HHMMSS.md`

The terminal output follows this structure:

```
Intent Captured
===============
Goal:      [raw goal]
Action:    [parsed action]
Target:    [parsed target]
Scope:     [parsed scope]
Mode:      [quick | detailed]

Related:   [N] matching items found
Session:   .cursor/sessions/YYYY-MM-DD-HHMMSS.md

Next steps:
  → Start working — context is set, dive in
  → /start-task "[goal]" — escalate to full task plan if scope is large
  → /debug-error — if the goal involves fixing a specific error
```

## NEVER Do

- **Never require structured input.** The whole point is accepting natural language with zero friction.
- **Never create a full task plan.** This command is intentionally lightweight. Use `/start-task` for full planning.
- **Never block on missing context.** Capture what you have, note what is missing, and move on.
- **Never overwrite an existing session file.** Timestamps in the filename ensure uniqueness.
- **Never skip the TODO search.** Even a quick intent benefits from knowing what related work exists.
- **Never auto-escalate to `/start-task` without telling the user.** Suggest it; do not force it.
- **Never fabricate related work.** Only show matches that actually exist in the project files or git history.
- **Never create directories beyond `.cursor/sessions/`.** Do not scaffold project structure unprompted.

## Error Handling

- If `TODO.md` does not exist, skip the TODO search and note: "No TODO.md found — skipping related work check."
- If `.cursor/sessions/` cannot be created due to permissions, fall back to writing the session file in the project root.
- If the goal is a ticket ID that cannot be resolved, use the raw ID as the goal and note: "Could not resolve ticket ID. Using as-is."
- If the goal is empty after prompting, do not create a session file. Ask once more, then abort with: "No intent captured."
- If more than 10 related items are found, show the top 5 strong matches and summarize the rest: "+[N] more moderate/weak matches."
- If the parsed action or target is ambiguous, include both possibilities in the session file and flag for the user to clarify.

## Automation

- **Optional automation:** Run `python3 scripts/intent_to_todo.py` to convert natural language intent into structured TODO items.

## Related

- **Command:** `/start-task` (escalate to full task planning when scope demands it)
- **Command:** `/debug-error` (if the intent is to fix a specific error)
- **Command:** `/review-code` (if the intent is to review before shipping)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
