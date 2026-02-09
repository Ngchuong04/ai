# Skills

118 modular AI agent skills organized into 19 categories. Each skill is a self-contained knowledge module that gives AI agents domain expertise, coding patterns, and decision frameworks.

## Installation

### With [skills.sh](https://skills.sh)

The fastest way to install individual skills using the [skills.sh](https://skills.sh/docs) CLI:

```bash
npx skills add <skill-name>
```

See [skills.sh docs](https://skills.sh/docs) to browse, search, and list skills.

### Manual Installation

Clone this repo and copy skills into your project:

```bash
# Clone the repo
git clone https://github.com/wpank/ai ~/.ai-skills
```

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/frontend/nextjs .cursor/skills/nextjs
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/frontend/nextjs ~/.cursor/skills/nextjs
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/frontend/nextjs .claude/skills/nextjs
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/frontend/nextjs ~/.claude/skills/nextjs
```

---

## Categories

| Category | Skills | Description |
|----------|--------|-------------|
| [ai-chat](ai-chat/) | 10 | AI chat interfaces — streaming, personas, tool composition, system prompts |
| [api](api/) | 8 | API design, versioning, auth, caching, rate limiting, error handling |
| [backend](backend/) | 12 | Architecture patterns, microservices, databases, Node.js, Go concurrency |
| [creative](creative/) | 1 | Generative art and algorithmic design |
| [design-systems](design-systems/) | 10 | Design tokens, component architecture, theming, financial UIs |
| [devops](devops/) | 6 | Docker, Kubernetes, Prometheus, Turborepo, Solidity security |
| [extraction](extraction/) | 1 | Pattern mining from codebases into reusable skills |
| [frontend](frontend/) | 15 | React, Next.js, Expo, Tailwind, shadcn/ui, responsive design |
| [marketing](marketing/) | 8 | Copywriting, CRO, content strategy, startup metrics |
| [meta](meta/) | 17 | Meta-skills that orchestrate other skills into workflows |
| [product](product/) | 1 | Startup metrics and KPI frameworks |
| [realtime](realtime/) | 4 | WebSockets, SSE, Kafka, Redis pub/sub, resilient connections |
| [refinement](refinement/) | 1 | Staged content refinement and consolidation |
| [testing](testing/) | 9 | Unit/integration/E2E testing, code review, debugging, clean code |
| [tools](tools/) | 9 | CLI tools, skill management, session handoff, release workflows |
| [writing](writing/) | 9 | Technical writing, diagrams, prompt engineering, communication |

---

## Skill Structure

Each skill is a directory containing:

```
skill-name/
├── SKILL.md          # Main skill file (required)
├── README.md         # Human-readable overview
├── references/       # Supporting docs, deep-dives
├── templates/        # Starter templates and scaffolds
├── data/             # Data files (CSV, JSON)
└── scripts/          # Automation scripts
```

The `SKILL.md` file contains:
- **YAML frontmatter** — name, model tier, description, trigger keywords
- **When to Use** — scenarios where the skill applies
- **Patterns** — code examples, decision frameworks, checklists
- **Anti-patterns** — what to avoid
- **Related Skills** — links to complementary skills

---

## Model Tiers

Skills declare a recommended model tier in their frontmatter:

| Tier | Use Case |
|------|----------|
| `fast` | Quick lookups, simple patterns, file scanning |
| `standard` | Code generation, implementation patterns |
| `reasoning` | Architecture decisions, complex tradeoffs |

---

## See Also

- [Agents](../agents/) — 16 workflow agents that use these skills
- [Commands](../commands/) — 48 slash commands
