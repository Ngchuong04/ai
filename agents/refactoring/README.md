# Refactoring Agent

Autonomous workflow for systematic code refactoring with test coverage verification and rollback safety. Handles code smell detection, refactoring planning, incremental execution with test verification, and rollback on failure.

## Workflow Phases

- **Phase 1: Assessment** — Detect code smells (long functions, deep nesting, duplication, god classes, etc.), measure baseline metrics
- **Phase 2: Safety setup** — Ensure tests pass, create branch, define rollback criteria
- **Phase 3: Planning** — Prioritize refactoring targets, plan incremental steps
- **Phase 4: Incremental execution** — Apply one refactor at a time, run tests after each step
- **Phase 5: Verification** — Before/after metrics, confirm behavior unchanged

## Skills Used

- `clean-code` — Clean code principles, anti-patterns, refactoring catalog
- `code-review` — Code review patterns and checklists

## Trigger Phrases

- "refactor this module"
- "clean up this code"
- "improve code quality in [path]"
- "restructure [module/component]"
- "reduce complexity in [path]"
- "this code has too many smells, fix it"

## Installation

### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/refactoring .cursor/agents/refactoring
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/refactoring ~/.cursor/agents/refactoring
```

### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/refactoring .claude/agents/refactoring
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/refactoring ~/.claude/agents/refactoring
```

For best results, also install the skills this agent references (see Skills Used above). Requires a clean git tree and passing tests before starting.

---

Part of the [Agents](../) directory.
