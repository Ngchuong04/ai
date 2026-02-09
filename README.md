# AI Agent Skills, Agents & Commands

A curated collection of **115 skills**, **16 agents**, and **48 commands** for [Claude Code](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) and [Cursor](https://cursor.sh). Extend your AI coding assistant with domain expertise, autonomous workflows, and structured development processes.

## What's Inside

| Type | Count | Description |
|------|-------|-------------|
| [**Skills**](#skills) | 115 | Modular knowledge modules — patterns, frameworks, and decision guides |
| [**Agents**](#agents) | 16 | Autonomous multi-phase workflow agents |
| [**Commands**](#commands) | 48 | Slash commands for structured development tasks |

---

## Quick Start

### Install Skills with [skills.sh](https://skills.sh)

The fastest way to install a skill from this repo:

```bash
npx add https://github.com/wpank/ai/tree/main/skills/<category>/<skill-name>
```

Example: `npx add https://github.com/wpank/ai/tree/main/skills/api/api-design`

### Clone the Full Repo

For access to everything — skills, agents, and commands:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

Then copy what you need into your projects (see Installation below).

---

## Installation

### Skills via [skills.sh](https://skills.sh)

Install a skill from this repo by URL:

```bash
npx add https://github.com/wpank/ai/tree/main/skills/<category>/<skill-name>
```

Example: `npx add https://github.com/wpank/ai/tree/main/skills/api/api-design`

### Agents & Commands (Manual Copy)

Agents and commands are **not** published to skills.sh. Clone this repo and copy what you need into your project's `.cursor/` or `.claude/` directory.

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

#### Cursor (per-project)

From your project root:

```bash
# Skills
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/<category>/<skill-name> .cursor/skills/

# Agents
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/<agent-name> .cursor/agents/

# Commands
mkdir -p .cursor/commands
cp -r ~/.ai-skills/commands/* .cursor/commands/
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills ~/.cursor/agents ~/.cursor/commands
cp -r ~/.ai-skills/skills/<category>/<skill-name> ~/.cursor/skills/
cp -r ~/.ai-skills/agents/<agent-name> ~/.cursor/agents/
cp -r ~/.ai-skills/commands/* ~/.cursor/commands/
```

#### Claude Code (per-project)

From your project root:

```bash
# Skills
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/<category>/<skill-name> .claude/skills/

# Agents
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/<agent-name> .claude/agents/

# Commands
mkdir -p .claude/commands
cp -r ~/.ai-skills/commands/* .claude/commands/
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills ~/.claude/agents ~/.claude/commands
cp -r ~/.ai-skills/skills/<category>/<skill-name> ~/.claude/skills/
cp -r ~/.ai-skills/agents/<agent-name> ~/.claude/agents/
cp -r ~/.ai-skills/commands/* ~/.claude/commands/
```

---

## Skills

115 modular AI agent skills organized across 17 categories. Each skill is a self-contained `SKILL.md` with patterns, code examples, anti-patterns, and decision frameworks.

### API (8 skills)

Designing, securing, and scaling APIs.

| Skill | Description |
|-------|-------------|
| [api-design](skills/api/api-design/) | REST & GraphQL design — resources, pagination, error handling |
| [api-development](skills/api/api-development/) | Full API lifecycle orchestration from design to docs |
| [api-versioning](skills/api/api-versioning/) | Versioning strategies, deprecation timelines, migration patterns |
| [auth-patterns](skills/api/auth-patterns/) | JWT, OAuth 2.0, sessions, RBAC/ABAC, MFA |
| [caching](skills/api/caching/) | Cache strategies, invalidation, eviction, distributed caching |
| [database-migrations](skills/api/database-migrations/) | Zero-downtime schema migrations with rollback planning |
| [error-handling](skills/api/error-handling/) | Error strategies — retries, circuit breakers, graceful degradation |
| [rate-limiting](skills/api/rate-limiting/) | Algorithms, tiered limits, distributed patterns |

### Backend (12 skills)

Server-side architecture, databases, and infrastructure patterns.

| Skill | Description |
|-------|-------------|
| [api-design-principles](skills/backend/api-design-principles/) | REST & GraphQL principles for backend services |
| [architecture-decision-records](skills/backend/architecture-decision-records/) | Lightweight ADRs capturing context, decision, and consequences |
| [architecture-patterns](skills/backend/architecture-patterns/) | Clean Architecture, Hexagonal, DDD with templates |
| [event-store](skills/backend/event-store/) | Event sourcing, projections, snapshotting, CQRS |
| [go-concurrency](skills/backend/go-concurrency/) | Goroutines, channels, worker pools, graceful shutdown |
| [microservices-patterns](skills/backend/microservices-patterns/) | Service decomposition, communication, data management |
| [monorepo](skills/backend/monorepo/) | Turborepo, Nx, pnpm workspaces — structure and caching |
| [nodejs-patterns](skills/backend/nodejs-patterns/) | Express/Fastify, middleware, validation, auth, database integration |
| [postgres-job-queue](skills/backend/postgres-job-queue/) | PostgreSQL job queue with SKIP LOCKED and priority scheduling |
| [service-layer-architecture](skills/backend/service-layer-architecture/) | Controller-service-query architecture with data enrichment |
| [supabase-postgres](skills/backend/supabase-postgres/) | Postgres optimization — indexing, RLS, connection management |

### Design Systems (10 skills)

Token architecture, theming, component patterns, and visual design.

| Skill | Description |
|-------|-------------|
| [animated-financial-display](skills/design-systems/animated-financial-display/) | Spring-physics number animations for financial dashboards |
| [design-system-components](skills/design-systems/design-system-components/) | Surface primitives, CVA variants, consistent styling |
| [design-system-patterns](skills/design-systems/design-system-patterns/) | Token hierarchies, theming, Style Dictionary, multi-brand |
| [distinctive-design-systems](skills/design-systems/distinctive-design-systems/) | Design systems with personality — aesthetics, color, typography |
| [financial-data-visualization](skills/design-systems/financial-data-visualization/) | Dark-themed financial charts, gain/loss color scales |
| [loading-state-patterns](skills/design-systems/loading-state-patterns/) | Skeleton loaders, shimmer effects, progressive loading |
| [theme-factory](skills/design-systems/theme-factory/) | 10+ curated color & typography themes for styled artifacts |
| [ui-design](skills/design-systems/ui-design/) | Layout, typography, color, spacing, accessibility, motion |
| [ui-ux-pro-max](skills/design-systems/ui-ux-pro-max/) | 50+ styles, 97 palettes, 57 font pairings, 99 UX rules |
| [web-design](skills/design-systems/web-design/) | CSS patterns for layout, typography, and responsive design |

### DevOps (6 skills)

Containers, orchestration, monitoring, and build systems.

| Skill | Description |
|-------|-------------|
| [docker](skills/devops/docker/) | Multi-stage builds, security hardening, Compose orchestration |
| [kubernetes](skills/devops/kubernetes/) | Deployments, StatefulSets, Services, Ingress, security contexts |
| [k8s-manifest-generator](skills/devops/kubernetes/k8s-manifest-generator/) | Production-ready K8s manifest generation |
| [prometheus](skills/devops/prometheus/) | Scrape config, service discovery, recording & alert rules |
| [solidity-security](skills/devops/solidity-security/) | Smart contract security, gas optimization, audit prep |
| [turborepo](skills/devops/turborepo/) | Caching, task pipelines, parallel execution for monorepos |

### Extraction (1 skill)

| Skill | Description |
|-------|-------------|
| [extraction](skills/extraction/) | Mine patterns from codebases into reusable skills and docs |

### Frontend (15 skills)

React, Next.js, mobile, styling, and component architecture.

| Skill | Description |
|-------|-------------|
| [composition-patterns](skills/frontend/composition-patterns/) | Compound components, context providers, explicit variants |
| [expo-native-ui](skills/frontend/expo-native-ui/) | Expo Router, native tabs, animations, SF Symbols |
| [frontend-design](skills/frontend/frontend-design/) | Distinctive production interfaces — avoid generic aesthetics |
| [native-ui](skills/frontend/native-ui/) | React Native with Expo Router, Apple HIG conventions |
| [nextjs](skills/frontend/nextjs/) | App Router, Server Components, streaming, Server Actions |
| [react-best-practices](skills/frontend/react-best-practices/) | 57 performance rules from Vercel Engineering |
| [react-composition](skills/frontend/react-composition/) | Scalable component architecture with composition patterns |
| [react-modernization](skills/frontend/react-modernization/) | Class-to-hooks migration, concurrent features adoption |
| [react-performance](skills/frontend/react-performance/) | Bundle optimization, re-render reduction, server components |
| [responsive-design](skills/frontend/responsive-design/) | Container queries, fluid typography, CSS Grid, mobile-first |
| [shadcn-ui](skills/frontend/shadcn-ui/) | shadcn/ui + Radix + Tailwind — forms, themes, components |
| [tailwind-design-system](skills/frontend/tailwind-design-system/) | CVA, compound components, design tokens with Tailwind |
| [tailwind-v4-shadcn](skills/frontend/tailwind-v4-shadcn/) | Tailwind v4 + shadcn/ui production setup |

### Marketing (8 skills)

Copy, conversion optimization, content strategy, and metrics.

| Skill | Description |
|-------|-------------|
| [content-strategy](skills/marketing/content-strategy/) | Content planning aligned with personas and journey stages |
| [copywriting](skills/marketing/copywriting/) | Marketing copy for landing pages, pricing, features |
| [marketing-ideas](skills/marketing/marketing-ideas/) | 139 proven SaaS marketing tactics with guidance |
| [marketing-psychology](skills/marketing/marketing-psychology/) | 70+ mental models and cognitive biases for marketing |
| [onboarding-cro](skills/marketing/onboarding-cro/) | Post-signup activation, first-run experience optimization |
| [page-cro](skills/marketing/page-cro/) | Page-level conversion rate optimization analysis |
| [signup-flow-cro](skills/marketing/signup-flow-cro/) | Signup form optimization and registration friction reduction |
| [social-content](skills/marketing/social-content/) | Social media content creation for LinkedIn, X, Instagram |
| [startup-metrics](skills/marketing/startup-metrics/) | SaaS metrics, CAC/LTV, burn multiple, churn analysis |

### Meta (17 skills)

Orchestration skills that coordinate other skills into complete workflows.

| Skill | Description |
|-------|-------------|
| [10x-patterns](skills/meta/10x-patterns/) | Patterns that dramatically accelerate development velocity |
| [ai-chat-application](skills/meta/ai-chat-application/) | End-to-end AI chat app with Vercel AI SDK |
| [auto-context](skills/meta/auto-context/) | Auto-load project context before major actions |
| [context-driven-development](skills/meta/context-driven-development/) | Structured context docs for AI-assisted development |
| [decision-frameworks](skills/meta/decision-frameworks/) | Library selection, build vs buy, architecture decisions |
| [design-system-creation](skills/meta/design-system-creation/) | Complete design system creation workflow |
| [estimation-patterns](skills/meta/estimation-patterns/) | Task estimation — decomposition, multipliers, bias awareness |
| [feature-specification](skills/meta/feature-specification/) | Convert personas into feature specs with acceptance criteria |
| [full-stack-feature](skills/meta/full-stack-feature/) | End-to-end feature orchestration from research to deploy |
| [planning-with-files](skills/meta/planning-with-files/) | File-based planning to survive context resets |
| [production-readiness](skills/meta/production-readiness/) | Pre-launch checklist across logging, security, monitoring |
| [project-documentation](skills/meta/project-documentation/) | ADRs, PRDs, personas, and docs organization |
| [realtime-dashboard](skills/meta/realtime-dashboard/) | Real-time dashboards with streaming and live updates |
| [security-review](skills/meta/security-review/) | Comprehensive security audit orchestration |
| [subagent-development](skills/meta/subagent-development/) | Execute plans with independent subagent tasks |
| [workflow-patterns](skills/meta/workflow-patterns/) | TDD, phase checkpoints, and structured commits |

### Product (1 skill)

| Skill | Description |
|-------|-------------|
| [startup-metrics](skills/product/startup-metrics/) | KPIs and unit economics from seed through Series A |

### Realtime (4 skills)

WebSockets, SSE, event streaming, and resilient connections.

| Skill | Description |
|-------|-------------|
| [dual-stream-architecture](skills/realtime/dual-stream-architecture/) | Kafka + Redis Pub/Sub for durability + low-latency |
| [realtime-react-hooks](skills/realtime/realtime-react-hooks/) | React hooks for SSE, WebSocket, and SWR integration |
| [resilient-connections](skills/realtime/resilient-connections/) | Retry logic, circuit breakers, graceful degradation |
| [websocket-hub-patterns](skills/realtime/websocket-hub-patterns/) | Horizontally-scalable WebSocket hub with Redis |

### Refinement (1 skill)

| Skill | Description |
|-------|-------------|
| [refinement](skills/refinement/) | Consolidate extracted skills into project-agnostic patterns |

### Testing (9 skills)

Quality assurance, code review, debugging, and standards.

| Skill | Description |
|-------|-------------|
| [clean-code](skills/testing/clean-code/) | Naming, functions, structure, anti-patterns, safety checks |
| [code-review](skills/testing/code-review/) | Systematic review — security, performance, maintainability |
| [debugging](skills/testing/debugging/) | Scientific debugging, git bisect, time-boxing, prevention |
| [e2e-testing-patterns](skills/testing/e2e-testing-patterns/) | Playwright & Cypress — critical journeys, flaky test fixes |
| [quality-gates](skills/testing/quality-gates/) | Pre-commit through post-deploy quality checkpoints |
| [reducing-entropy](skills/testing/reducing-entropy/) | Minimize codebase size through ruthless simplification |
| [testing-patterns](skills/testing/testing-patterns/) | Unit, integration, E2E with framework-specific guidance |
| [testing-workflow](skills/testing/testing-workflow/) | Orchestrate comprehensive testing across a project |

### Tools (9 skills)

CLI tools, skill management, session lifecycle, and releases.

| Skill | Description |
|-------|-------------|
| [command-creator](skills/tools/command-creator/) | Create reusable slash commands for AI workflows |
| [find-skills](skills/tools/find-skills/) | Discover and install skills from the ecosystem |
| [finishing-branch](skills/tools/finishing-branch/) | Complete dev work — merge, PR, or cleanup options |
| [logging-observability](skills/tools/logging-observability/) | Structured logging, OpenTelemetry, Prometheus/Grafana |
| [meme-factory](skills/tools/meme-factory/) | Generate memes via memegen.link API + textual formats |
| [release-skills](skills/tools/release-skills/) | Semantic versioning, changelogs, git tagging |
| [session-handoff](skills/tools/session-handoff/) | Handoff documents for seamless agent context transfer |
| [skill-creator](skills/tools/skill-creator/) | Guide for creating well-structured SKILL.md files |
| [skill-judge](skills/tools/skill-judge/) | 8-dimension skill quality evaluation (120-point scoring) |
| [subagent-driven-development](skills/tools/subagent-driven-development/) | Dispatch subagents per task with two-stage review |

### Writing (9 skills)

Technical writing, diagrams, prompts, and communication.

| Skill | Description |
|-------|-------------|
| [article-illustrator](skills/writing/article-illustrator/) | Add illustrations to articles with 20+ visual styles |
| [brainstorming](skills/writing/brainstorming/) | Structured ideation before implementation |
| [clear-writing](skills/writing/clear-writing/) | Documentation, READMEs, error messages, commit messages |
| [game-changing-features](skills/writing/game-changing-features/) | Find 10x product opportunities and high-leverage features |
| [mermaid-diagrams](skills/writing/mermaid-diagrams/) | Software diagrams — class, sequence, flow, ERD, C4, state |
| [persona-docs](skills/writing/persona-docs/) | User persona documentation with journey maps |
| [professional-communication](skills/writing/professional-communication/) | Emails, Slack messages, meeting agendas, status updates |
| [prompt-engineering](skills/writing/prompt-engineering/) | Advanced prompt techniques for production LLM systems |
| [schema-markup](skills/writing/schema-markup/) | JSON-LD structured data and schema.org optimization |

---

## Agents

16 autonomous workflow agents that orchestrate skills and commands into end-to-end processes. Each agent is a multi-phase workflow defined in `AGENT.md`.

| Agent | Description |
|-------|-------------|
| [api](agents/api/) | Full API development — design, OpenAPI specs, implementation, tests, docs |
| [backend](agents/backend/) | Production backend services — architecture, database design, service layers |
| [bootstrap](agents/bootstrap/) | Project scaffolding with opinionated structure and tooling |
| [content](agents/content/) | Professional content — docs, blog posts, social, technical writing |
| [debugging](agents/debugging/) | Systematic error diagnosis — stack traces, hypothesis, incremental fixes |
| [deployment](agents/deployment/) | CI/CD pipelines, containers, cloud deployment, environment promotion |
| [design-system](agents/design-system/) | Design token extraction and Tailwind + CSS variable generation |
| [development](agents/development/) | Docs-first feature development with planning and tracking |
| [extraction](agents/extraction/) | Pattern mining from codebases into reusable skills |
| [frontend](agents/frontend/) | Production frontend — components, styling, accessibility, performance |
| [marketing](agents/marketing/) | Marketing pages, copy, conversion funnels, CRO analysis |
| [migration](agents/migration/) | Multi-step migrations with rollback planning and zero-downtime |
| [performance](agents/performance/) | Performance optimization — bundles, runtime, memory, queries |
| [refactoring](agents/refactoring/) | Systematic refactoring — smell detection, safe incremental changes |
| [refinement](agents/refinement/) | Consolidate extracted skills into production-ready patterns |
| [testing](agents/testing/) | Comprehensive test suites — strategy, generation, coverage analysis |

---

## Commands

48 slash commands organized in 8 groups. Each command is a markdown file with usage, examples, and implementation steps.

### Bootstrap (3)

| Command | Description |
|---------|-------------|
| [bootstrap-project](commands/bootstrap/bootstrap-project.md) | Scaffold a new project with opinionated setup |
| [bootstrap-design-system](commands/bootstrap/bootstrap-design-system.md) | Initialize design system structure |
| [bootstrap-docs](commands/bootstrap/bootstrap-docs.md) | Add documentation structure to an existing project |

### Development (31)

| Command | Description |
|---------|-------------|
| [accessibility-audit](commands/development/accessibility-audit.md) | WCAG 2.1 AA accessibility audit |
| [brainstorm](commands/development/brainstorm.md) | Structured brainstorming session |
| [check-performance](commands/development/check-performance.md) | Performance audit — bundles, runtime, Core Web Vitals |
| [complete-task](commands/development/complete-task.md) | Mark task done, generate completion artifacts |
| [context-reset](commands/development/context-reset.md) | Archive stale context, reset to fresh templates |
| [create-api-route](commands/development/create-api-route.md) | Scaffold API endpoint with validation and tests |
| [create-component](commands/development/create-component.md) | Scaffold UI component with variants and a11y |
| [create-diagram](commands/development/create-diagram.md) | Generate Mermaid diagrams |
| [create-landing-page](commands/development/create-landing-page.md) | Scaffold landing page with copy and design system |
| [create-migration](commands/development/create-migration.md) | Database migration with safety checks and rollback |
| [create-service](commands/development/create-service.md) | Scaffold backend service with containers and tooling |
| [daily-standup](commands/development/daily-standup.md) | Auto-generate standup from git history and TODOs |
| [debug-error](commands/development/debug-error.md) | Structured error debugging and root cause analysis |
| [deploy](commands/development/deploy.md) | Deployment with environment selection and rollback |
| [design-ui](commands/development/design-ui.md) | Design and implement UI with design system |
| [handoff-and-resume](commands/development/handoff-and-resume.md) | Session handoff and resume documents |
| [intent](commands/development/intent.md) | Quick intent capture at session start |
| [migrate-deps](commands/development/migrate-deps.md) | Dependency upgrades with breaking change analysis |
| [new-adr](commands/development/new-adr.md) | Create Architecture Decision Record |
| [new-feature](commands/development/new-feature.md) | Docs-first feature development |
| [progress](commands/development/progress.md) | Show progress across TODOs, roadmap, commits |
| [refactor](commands/development/refactor.md) | Systematic refactoring with safety checks |
| [review-code](commands/development/review-code.md) | Multi-dimensional code review |
| [security-review](commands/development/security-review.md) | OWASP Top 10 security review |
| [session-summary](commands/development/session-summary.md) | End-of-session summary with next steps |
| [sprint-review](commands/development/sprint-review.md) | Sprint review summary with retrospective |
| [start-task](commands/development/start-task.md) | Document task intent and establish context |
| [test-feature](commands/development/test-feature.md) | Generate comprehensive tests for a feature |
| [update-roadmap](commands/development/update-roadmap.md) | Add TODOs and update sprint status |
| [workflow](commands/development/workflow.md) | Full development workflow with stage gates |
| [write-content](commands/development/write-content.md) | Professional written content — blogs, guides, tutorials |

### Docs (3)

| Command | Description |
|---------|-------------|
| [create-persona](commands/docs/create-persona.md) | Create user persona document |
| [create-prd](commands/docs/create-prd.md) | Create Product Requirements Document |
| [create-runbook](commands/docs/create-runbook.md) | Create operations runbook |

### Documentation (1)

| Command | Description |
|---------|-------------|
| [generate-docs](commands/documentation/generate-docs.md) | Auto-generate docs from code comments and structure |

### Extraction (1)

| Command | Description |
|---------|-------------|
| [extract-patterns](commands/extraction/extract-patterns.md) | Mine reusable patterns from the current project |

### Marketing (2)

| Command | Description |
|---------|-------------|
| [cro-audit](commands/marketing/cro-audit.md) | Conversion rate optimization audit with scoring |
| [write-copy](commands/marketing/write-copy.md) | Marketing copy with persona targeting and A/B variants |

### Refinement (2)

| Command | Description |
|---------|-------------|
| [promote-skill](commands/refinement/promote-skill.md) | Move skill from staging to active |
| [refine-staged](commands/refinement/refine-staged.md) | Process and consolidate all staged content |

### Skills (5)

| Command | Description |
|---------|-------------|
| [create-skill](commands/skills/create-skill.md) | Guided skill creation with quality criteria |
| [update-skill](commands/skills/update-skill.md) | Update an existing skill with improvements |
| [validate-skill](commands/skills/validate-skill.md) | Check skill against quality criteria |
| [check-overlaps](commands/skills/check-overlaps.md) | Find redundant or overlapping skills |
| [archive-skill](commands/skills/archive-skill.md) | Move deprecated skill to archive |

### Common Workflows

```
# New project
/bootstrap-project → /bootstrap-design-system → /bootstrap-docs

# Feature end-to-end
/new-feature → /create-component → /create-api-route → /test-feature → /review-code

# UI development
/design-ui → /create-component → /accessibility-audit → /check-performance

# Backend service
/create-service → /create-migration → /create-api-route → /test-feature

# Ship it
/check-performance → /security-review → /deploy staging → /deploy production

# Session lifecycle
/intent → /start-task → /workflow → /complete-task → /session-summary
```

---

## Repo Structure

```
.
├── skills/                  # 115 skills organized by category
│   ├── ai-chat/             #   AI chat interfaces and streaming
│   ├── api/                 #   API design, auth, caching
│   ├── backend/             #   Architecture, databases, Node.js, Go
│   ├── design-systems/      #   Tokens, theming, components
│   ├── devops/              #   Docker, K8s, Prometheus, Turborepo
│   ├── documentation/       #   ADRs, PRDs, docs organization
│   ├── extraction/          #   Pattern mining
│   ├── frontend/            #   React, Next.js, Expo, Tailwind
│   ├── infrastructure/     #   Docker env, K8s, Prometheus observability
│   ├── marketing/           #   Copy, CRO, content strategy
│   ├── meta/                #   Orchestration and workflow skills
│   ├── product/             #   Startup metrics
│   ├── realtime/            #   WebSocket, SSE, Kafka, Redis
│   ├── refinement/          #   Skill consolidation
│   ├── testing/             #   Testing, review, debugging
│   ├── tools/               #   CLI, releases, session management
│   └── writing/             #   Technical writing, diagrams, prompts
├── agents/                  # 16 autonomous workflow agents
│   ├── api/
│   ├── backend/
│   ├── bootstrap/
│   ├── content/
│   ├── debugging/
│   ├── deployment/
│   ├── design-system/
│   ├── development/
│   ├── extraction/
│   ├── frontend/
│   ├── marketing/
│   ├── migration/
│   ├── performance/
│   ├── refactoring/
│   ├── refinement/
│   └── testing/
├── commands/                # 48 slash commands
│   ├── bootstrap/           #   Project scaffolding (3)
│   ├── development/         #   Day-to-day workflows (31)
│   ├── docs/                #   Documentation artifacts (3)
│   ├── documentation/       #   Doc generation (1)
│   ├── extraction/          #   Pattern mining (1)
│   ├── marketing/           #   CRO and copy (2)
│   ├── refinement/          #   Skill promotion (2)
│   └── skills/              #   Skill management (5)
└── .claude/                 # Active installation for Claude Code
    ├── skills/              #   Runtime-loaded skills
    ├── agents/              #   Runtime-loaded agents
    └── commands/            #   Runtime-loaded commands
```

---

## Skill Anatomy

Each skill is a directory with a required `SKILL.md` and optional supporting files:

```
skill-name/
├── SKILL.md              # Required — patterns, examples, anti-patterns
├── README.md             # Human-readable overview
├── references/           # Deep-dive docs and supporting material
├── templates/            # Starter templates and scaffolds
├── data/                 # Data files (CSV, JSON)
└── scripts/              # Automation scripts
```

The `SKILL.md` contains:
- **YAML frontmatter** — name, model tier, description, trigger keywords
- **When to Use** — scenarios where the skill applies
- **Patterns** — code examples, decision frameworks, checklists
- **Anti-patterns** — common mistakes to avoid
- **Related Skills** — links to complementary skills

---

## Agent Anatomy

Each agent is defined in `AGENT.md` with:

1. **Skills** — Domain knowledge loaded from `skills/`
2. **Commands** — Slash commands from `commands/` for sub-workflows
3. **Workflow** — Multi-phase process with checkpoints and quality gates
4. **Model Tiers** — Per-phase model recommendations (fast/standard/reasoning)

| Phase Type | Typical Tier | Rationale |
|------------|--------------|-----------|
| Discovery / assessment | `fast` | File reading, scanning, structure analysis |
| Planning / design | `reasoning` | Architecture decisions, tradeoff analysis |
| Execution / implementation | `standard` | Code generation with patterns |
| Verification / completion | `fast` | Running checks, formatting output |

---

## Contributing

### Creating a New Skill

1. Create a directory under the appropriate category in `skills/`
2. Write a `SKILL.md` following the structure above
3. Add a `README.md` with a human-readable overview
4. Use the [skill-creator](skills/tools/skill-creator/) skill or [create-skill](commands/skills/create-skill.md) command for guidance
5. Validate with the [skill-judge](skills/tools/skill-judge/) skill (120-point scoring)

### Creating a New Agent

1. Create a directory under `agents/`
2. Write an `AGENT.md` with YAML frontmatter, skills list, and phased workflow
3. Add a `README.md`
4. Reference existing skills and commands in the workflow

### Creating a New Command

1. Create a `.md` file under the appropriate group in `commands/`
2. Include: Usage, Examples, When to Use, Implementation Steps, Output format

---

## License

MIT
