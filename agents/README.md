# Agents

16 autonomous workflow agents that orchestrate skills and commands into end-to-end workflows. Each agent is a multi-phase process that loads relevant skills for domain knowledge and can invoke slash commands for structured sub-tasks.

**Note:** Agents are specific to this repository. They are not published to [skills.sh](https://skills.sh); use the project's `skills` CLI or manual copy to install them into Cursor or Claude Code.

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

### Using the project's `skills` CLI

From the skills repo root (or after `npm link` from another project with `SKILLS_HOME` set):

```bash
# Initialize for Cursor (writes to .cursor/rules/)
skills init cursor

# Initialize for Claude Code (writes to .agents/skills/)
skills init agents

# Add one or more agents by name
skills add api
skills add frontend debugging
skills add --category agents   # add all agents (if supported)
```

The CLI copies the agent directory (e.g. `ai/agents/api/`) into your project's rules/skills directory so the agent's `AGENT.md` is available as context.

### Manual installation (Cursor)

Use agents as Cursor rules so the agent gets the workflow as context:

```bash
# From your project root; clone the repo first if needed
git clone <repo-url> ~/.skills
# Copy a single agent
cp -r ~/.skills/ai/agents/api .cursor/rules/api-agent
# Or create .cursor/rules first
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/frontend .cursor/rules/frontend-agent
```

Cursor will load `.cursor/rules/*` as rule context. Naming the folder with a `-agent` suffix helps distinguish agents from skill rules.

### Manual installation (Claude Code)

Use agents as project-level skills so Claude Code can load the workflow:

```bash
# From your project root
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/api .claude/skills/api-agent
```

Or install globally for Claude Code:

```bash
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/api ~/.claude/skills/api-agent
```

Claude Code discovers skills in `.claude/skills/` (project) or `~/.claude/skills/` (global). Each agent directory should contain `AGENT.md`; the folder name (e.g. `api-agent`) is how you refer to it.

### Not on skills.sh

Agents are not published to [skills.sh](https://skills.sh). The Vercel `npx skills` CLI only supports skills (repos with `SKILL.md` files). To use these agents you must use this repo's `skills` CLI or copy the `ai/agents/<name>/` directories manually as above.

---

## How Agents Work

Each agent is defined in `ai/agents/<name>/AGENT.md` and follows a consistent pattern:

1. **Skills** — The agent loads relevant skills from `ai/skills/` for domain knowledge (listed in "Before Starting").
2. **Commands** — The agent can invoke slash commands from `ai/commands/` for structured sub-workflows.
3. **Workflow** — A multi-phase process with checkpoints and quality gates (design, implementation, verification, etc.).

When you install an agent as a rule or skill, you're giving the AI the full `AGENT.md` so it can follow that workflow. For best results, also install the skills that agent references (see each agent's README for the list).

---

## Model Tiers

Each agent declares per-phase model tier recommendations in its YAML frontmatter (`models:`). This allows different phases to use different model tiers for cost/speed. See the root [MODEL-TIERS.md](../../MODEL-TIERS.md) for the tier reference.

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
| Skills catalog | [../skills/](../skills/) | 118 skills by category |
| Commands reference | [../COMMANDS.md](../COMMANDS.md) | 50 slash commands |
| Model tiers | [../../MODEL-TIERS.md](../../MODEL-TIERS.md) | Tier definitions and platform mapping |
| Agent template | [../templates/agent-template.md](../templates/agent-template.md) | Template for creating new agents |
