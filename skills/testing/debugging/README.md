# Debugging Methodology

A systematic, scientific approach to finding and fixing bugs — replacing guesswork with method. Covers structured techniques, common bug categories, git bisect, time-boxing, prevention strategies, and anti-patterns.

## What's Inside

- Debugging philosophy (observe → hypothesize → test → conclude)
- Systematic methods (binary search, hypothesis testing, minimal reproduction, trace analysis, rubber duck, divide and conquer)
- Six-step debugging workflow (reproduce → isolate → diagnose → fix → verify → prevent)
- Debugging toolkit (debugger, logging, profiler, network inspector, memory analyzer)
- Common bug categories with symptoms and first checks (null reference, off-by-one, race conditions, memory leaks, timezone issues, and more)
- Git bisect guide with automated bisect
- "Questions to ask when stuck" checklist
- Time-boxing strategies
- Prevention practices (regression tests, improved types, monitoring)

## When to Use

- Investigating bugs and diagnosing failures
- Stuck on a problem and need a structured approach
- Establishing debugging practices for a team
- Teaching systematic debugging methodology

## Installation

```bash
npx skills add debugging
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/testing/debugging .cursor/skills/debugging
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/testing/debugging ~/.cursor/skills/debugging
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/testing/debugging .claude/skills/debugging
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/testing/debugging ~/.claude/skills/debugging
```

## Related Skills

- [testing-patterns](../testing-patterns/) — Write regression tests after fixing bugs
- [clean-code](../clean-code/) — Code quality that prevents bugs
- [testing-workflow](../testing-workflow/) — Routes debugging needs within the testing orchestration

---

Part of the [Testing](..) skill category.
