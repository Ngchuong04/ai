# Agents

16 autonomous workflow agents that orchestrate skills and commands into end-to-end workflows. Each agent is a multi-phase process that loads relevant skills for domain knowledge and can invoke slash commands for structured sub-tasks.

> **Note:** Agents are not published to [skills.sh](https://skills.sh). Install them by cloning this repo and copying the agent directory into your project.

---

## Agent Catalog

| Agent | Description | Triggers |
|-------|-------------|----------|
| [api](api/) | Full API development — design, OpenAPI specs, endpoint implementation, tests, and documentation | "build an API", "create API for", "design API", "generate OpenAPI spec", "add API endpoints" |
| [backend](backend/) | Production backend services — architecture decisions, database design, service layers, and operational readiness | "build a backend", "create a service", "design the architecture", "implement the backend", "create a microservice" |
| [bootstrap](bootstrap/) | Project scaffolding with opinionated structure, documentation, and tooling | "bootstrap new project", "scaffold project", "create new project" |
| [content](content/) | Professional written content — docs, blog posts, social media, emails, guides, and technical writing | "write a blog post", "create documentation", "draft an email", "write content for", "create a README" |
| [debugging](debugging/) | Systematic error diagnosis — stack trace parsing, hypothesis formation, incremental fix verification | "debug this", "why is this failing", "fix this error", "investigate this bug", "diagnose this issue" |
| [deployment](deployment/) | CI/CD pipelines, container builds, cloud deployment, environment promotion, and monitoring setup | "deploy", "set up CI/CD", "create pipeline", "containerize", "set up GitHub Actions" |
| [design-system](design-system/) | Design token extraction from codebases or reference sites, Tailwind + CSS variable generation | "extract design system", "analyze design tokens", "create design system from" |
| [development](development/) | Docs-first feature development — planning, spec creation, ADRs, and implementation tracking | "new feature", "develop feature", "add feature", "implement feature" |
| [extraction](extraction/) | Pattern mining from codebases into reusable skills and documentation | "extract patterns from", "analyze this project", "extract from this repo", "capture patterns" |
| [frontend](frontend/) | Production frontend interfaces — component design, styling, accessibility, and performance | "build a component", "create a page", "design the UI for", "build the frontend", "create a landing page" |
| [marketing](marketing/) | Marketing pages, copy, conversion funnels, CRO analysis, and measurement setup | "create marketing page", "write copy for", "optimize conversions", "marketing strategy", "CRO audit" |
| [migration](migration/) | Multi-step migrations with rollback planning — database schemas, framework upgrades, architecture changes | "migrate", "upgrade", "migration plan", "migrate database", "zero-downtime migration" |
| [performance](performance/) | Performance optimization — bundles, runtime, memory, queries, API response times, Core Web Vitals | "optimize performance", "why is this slow", "reduce bundle size", "fix memory leak", "profile this" |
| [refactoring](refactoring/) | Systematic code refactoring — smell detection, planning, incremental execution with test verification | "refactor this", "clean up this code", "improve code quality", "restructure", "reduce complexity" |
| [refinement](refinement/) | Consolidate extracted skills from staging into production-ready, project-agnostic patterns | "refine staged content", "consolidate skills", "process staging" |
| [testing](testing/) | Comprehensive test suites — strategy, generation, coverage analysis, and testing infrastructure | "write tests for", "test this", "improve test coverage", "add tests", "testing strategy" |

---

## Installation

### Step 1: Clone this repo

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Step 2: Copy agents into your project

#### Cursor (per-project)

From your project root:

```bash
# Single agent
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/api .cursor/agents/api

# All agents
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/* .cursor/agents/
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/api ~/.cursor/agents/api
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/api .claude/agents/api
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/api ~/.claude/agents/api
```

> Each agent directory contains `AGENT.md` (the workflow definition) and `README.md`. For best results, also install the skills each agent references — see the agent's README for the list.

---

## How Agents Work

Each agent is defined in `agents/<name>/AGENT.md` and follows a consistent pattern:

1. **Skills** — The agent loads relevant skills from `skills/` for domain knowledge (listed in "Before Starting").
2. **Commands** — The agent can invoke slash commands from `commands/` for structured sub-workflows.
3. **Workflow** — A multi-phase process with checkpoints and quality gates (design, implementation, verification, etc.).

When you install an agent as a rule or skill, you're giving the AI the full `AGENT.md` so it can follow that workflow. For best results, also install the skills that agent references (see each agent's README for the list).

---

## Model Tiers

Each agent declares per-phase model tier recommendations in its YAML frontmatter (`models:`). This allows different phases to use different model tiers for cost/speed.

| Phase type | Typical tier | Rationale |
|------------|--------------|-----------|
| Discovery / assessment | `fast` | File reading, scanning, structure analysis |
| Planning / design | `reasoning` | Architecture decisions, tradeoff analysis |
| Execution / implementation | `standard` | Code generation with patterns |
| Verification / completion | `fast` | Running checks, formatting output |

---

## See Also

| Resource | Path | Description |
|----------|------|-------------|
| Skills catalog | [../skills/](../skills/) | 115 skills by category |
| Commands reference | [../commands/](../commands/) | 48 slash commands |
