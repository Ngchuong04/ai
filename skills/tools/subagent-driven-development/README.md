# Subagent-Driven Development

Execute implementation plans by dispatching a fresh subagent per task with two-stage review — spec compliance first, then code quality. Fresh subagent per task means no context pollution, high quality, and fast iteration.

## What's Inside

- Full process flow from plan reading through task completion
- Three subagent roles: Implementer, Spec Reviewer, Code Quality Reviewer
- Prompt templates for each role
- Controller responsibilities (extract tasks, provide context, answer questions, enforce review order)
- Quality gates: self-review, spec review, code review
- Handling failures (questions, reviewer issues, blocked tasks)
- Comparison with manual execution and parallel-session plans

## When to Use

- You have an implementation plan with discrete, mostly independent tasks
- You want to execute the plan within a single session (no human-in-the-loop between tasks)
- Tasks can be implemented and reviewed sequentially without tight coupling

## Installation

```bash
skills add subagent-driven-development
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/tools/subagent-driven-development .cursor/skills/subagent-driven-development
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/tools/subagent-driven-development ~/.cursor/skills/subagent-driven-development
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/tools/subagent-driven-development .claude/skills/subagent-driven-development
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/tools/subagent-driven-development ~/.claude/skills/subagent-driven-development
```

## Related Skills

- **finishing-branch** — Called after all tasks complete to integrate work
- **session-handoff** — For preserving context across sessions

---

Part of the [Tools](..) skill category.
