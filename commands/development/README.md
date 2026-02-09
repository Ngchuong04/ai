# Development commands

Day-to-day coding, debugging, deployment, and workflow. Scaffolding, testing, review, deployment, and session management.

## Commands

| Command | Description | Usage |
|---------|-------------|-------|
| [accessibility-audit](accessibility-audit.md) | Audit against WCAG 2.1 AA accessibility standards | `/accessibility-audit <file-or-component> [--level AA\|AAA] [--fix]` |
| [brainstorm](brainstorm.md) | Structured brainstorming — generate, filter, and expand ideas | `/brainstorm [topic] [--mode diverge\|converge\|both]` |
| [check-performance](check-performance.md) | Performance audit — bundles, runtime, memory, network, Core Web Vitals | `/check-performance [target]` |
| [complete-task](complete-task.md) | Mark task done, generate changelog, update roadmap | `/complete-task <task>` |
| [context-reset](context-reset.md) | Archive stale context files and reset to fresh templates | `/context-reset [--dry-run] [--no-confirm]` |
| [create-api-route](create-api-route.md) | Scaffold API endpoint with validation, error handling, and tests | `/create-api-route <endpoint> [--method GET\|POST\|PUT\|DELETE\|PATCH] [--auth] [--paginated]` |
| [create-component](create-component.md) | Scaffold UI component with variants, props, and accessibility | `/create-component <name> [--variant] [--interactive] [--with-tests] [--with-story]` |
| [create-diagram](create-diagram.md) | Generate Mermaid diagrams for docs, architecture, or code | `/create-diagram [type] [topic]` |
| [create-landing-page](create-landing-page.md) | Scaffold landing page with copy, design system, and implementation | `/create-landing-page <product-name> [--style <style>] [--stack <stack>]` |
| [create-migration](create-migration.md) | Database migration with safety checks, rollback, and verification | `/create-migration <migration-name> [--type schema\|data\|index]` |
| [create-service](create-service.md) | Scaffold backend service with architecture and containerization | `/create-service <service-name> [--type rest\|graphql\|grpc] [--stack node\|python\|go]` |
| [daily-standup](daily-standup.md) | Auto-generate daily standup from git history and TODOs | `/daily-standup [--since <timestamp\|duration>] [--save]` |
| [debug-error](debug-error.md) | Structured error debugging and root cause analysis | `/debug-error <error>` |
| [deploy](deploy.md) | Deployment with safety checks, health verification, and rollback | `/deploy <environment> [--strategy rolling\|blue-green\|canary] [--skip-tests] [--dry-run]` |
| [design-ui](design-ui.md) | Design and implement UI with design system, a11y, and responsive behavior | `/design-ui <component-or-page-name> [--style <style>] [--device <device>]` |
| [handoff-and-resume](handoff-and-resume.md) | Create handoff document with resume instructions | `/handoff-and-resume [--resume <path>] [--save]` |
| [intent](intent.md) | Quick intent capture at the start of a work session | `/intent <goal>` |
| [migrate-deps](migrate-deps.md) | Dependency upgrade with breaking change analysis and migration steps | `/migrate-deps <package> [--to <version>] [--dry-run] [--all-outdated]` |
| [new-adr](new-adr.md) | Create an Architecture Decision Record | `/new-adr <title>` |
| [new-feature](new-feature.md) | Docs-first feature development workflow | `/new-feature <name>` |
| [progress](progress.md) | Show progress dashboard across tracking files | `/progress [--days <N>] [--roadmap <path>]` |
| [refactor](refactor.md) | Systematic refactoring with safety checks and verification | `/refactor <target>` |
| [review-code](review-code.md) | AI-assisted multi-dimensional code review | `/review-code [target]` |
| [security-review](security-review.md) | Security review against OWASP Top 10 and vulnerability patterns | `/security-review <file-or-directory> [--severity critical\|high\|medium\|low] [--fix]` |
| [session-summary](session-summary.md) | Generate end-of-session summary | `/session-summary [--since <timestamp\|duration>] [--save]` |
| [sprint-review](sprint-review.md) | Generate sprint review with metrics and retrospective | `/sprint-review [--days <N>] [--save] [--team]` |
| [start-task](start-task.md) | Document intent and create plan before coding | `/start-task <task>` |
| [test-feature](test-feature.md) | Generate comprehensive tests for a feature | `/test-feature <feature>` |
| [update-roadmap](update-roadmap.md) | Manage roadmap with todos and sprint status | `/update-roadmap [action]` |
| [workflow](workflow.md) | Full lifecycle: Intent → Plan → Execute → Test → Document → Complete | `/workflow <task> [--type feature\|bugfix\|refactor] [--skip-plan] [--resume]` |
| [write-content](write-content.md) | Create professional written content — blog posts, docs, guides | `/write-content [type] [topic] [--audience <audience>] [--length short\|medium\|long]` |

## Installation

First, clone the repo:

```bash
git clone https://github.com/wpank/ai ~/.ai-skills
```

### Cursor (per-project)

```bash
mkdir -p .cursor/commands/development
cp ~/.ai-skills/commands/development/*.md .cursor/commands/development/
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/commands/development
cp ~/.ai-skills/commands/development/*.md ~/.cursor/commands/development/
```

### Claude Code (per-project)

```bash
mkdir -p .claude/commands/development
cp ~/.ai-skills/commands/development/*.md .claude/commands/development/
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/commands/development
cp ~/.ai-skills/commands/development/*.md ~/.claude/commands/development/
```

---

Part of the [Commands](../) directory.
