# Performance Agent

Autonomous workflow for systematic performance profiling, bottleneck analysis, incremental optimization with measurement, and ongoing monitoring setup. Covers bundle size, runtime speed, memory, database queries, API response times, and Core Web Vitals.

## Workflow Phases

- **Phase 1: Profiling** — Detect project type and tooling, collect baseline metrics (bundle, runtime, memory, network, DB)
- **Phase 2: Analysis** — Identify bottlenecks, rank by user impact and effort-to-fix
- **Phase 3: Optimization** — Apply optimizations incrementally with before/after measurement
- **Phase 4: Verification** — Confirm improvements hold, no regressions
- **Phase 5: Monitoring** — Set up ongoing monitoring to detect future degradation

## Skills Used

- `clean-code` — Clean code principles during optimization
- `react-performance` — React performance optimization patterns
- `react-best-practices` — React best practices and patterns
- Command: `check-performance` — Single-check performance with structured output

## Trigger Phrases

- "optimize performance of [module/app]"
- "why is this so slow"
- "reduce bundle size"
- "fix this memory leak"
- "improve page speed / Core Web Vitals"
- "profile this [function/endpoint/page]"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add performance
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/performance .cursor/rules/performance-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/performance .claude/skills/performance-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/performance ~/.claude/skills/performance-agent
```

For best results, also install the skills this agent references (see Skills Used above). Ensure the app builds and runs and git is clean before profiling.

---

Part of the [Agents](../) directory.
