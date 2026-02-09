# Debugging Agent

Autonomous workflow for systematic error diagnosis, root cause analysis, fix application with verification, and recurrence prevention. Handles stack trace parsing, context gathering, hypothesis formation, incremental fix verification, and prevention (tests, types, linting).

## Workflow Phases

- **Phase 1: Error capture** — Parse error input, extract structured fields, classify error type
- **Phase 2: Context gathering** — Source code, git history, dependencies, related patterns
- **Phase 3: Root cause analysis** — Error pattern matching, hypothesis ranking
- **Phase 4: Fix application** — Incremental fixes with verification at each step
- **Phase 5: Prevention** — Tests, types, linting, monitoring recommendations

## Skills Used

- `clean-code` — Clean code principles for quality fixes
- `debugging` — Debugging techniques and strategies
- `logging-observability` — Structured logging and observability patterns
- Command: `debug-error` — Single-error debugging with structured output

## Trigger Phrases

- "debug this error"
- "why is this failing"
- "fix this error in [file/module]"
- "investigate this bug"
- "diagnose this issue"
- "this keeps crashing, help"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add debugging
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/debugging .cursor/rules/debugging-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/debugging .claude/skills/debugging-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/debugging ~/.claude/skills/debugging-agent
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
