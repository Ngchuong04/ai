# Testing Agent

Autonomous workflow for generating comprehensive test suites, identifying untested code, and establishing test strategies. Handles test strategy, test generation, coverage analysis, and testing infrastructure setup.

## Workflow Phases

- **Phase 1: Discovery** — Detect test framework, scan for existing tests, identify coverage gaps
- **Phase 2: Strategy** — Test strategy tailored to codebase and risk profile
- **Phase 3: Generation** — Generate tests for happy paths, edge cases, error scenarios
- **Phase 4: Coverage analysis** — Identify untested code, suggest additional tests
- **Phase 5: Verification** — Run suite, confirm coverage improvement, document strategy

## Skills Used

- `e2e-testing-patterns` — E2E testing methodology and patterns
- `testing-patterns` — Unit/integration/E2E patterns
- `testing-workflow` — Testing workflow
- `quality-gates` — Quality gates
- `code-review` — Code review patterns
- Command: `test-feature` — Single-feature test generation

## Trigger Phrases

- "write tests for [feature/module]"
- "test this [file/directory]"
- "improve test coverage"
- "add tests for [component]"
- "testing strategy for [project]"
- "set up testing infrastructure"

## Installation

### Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.ai-skills/agents/testing .cursor/rules/testing-agent
```

### Claude Code (per-project)

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/testing .claude/agents/testing
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/testing ~/.claude/agents/testing
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
