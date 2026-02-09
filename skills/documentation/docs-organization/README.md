# Project Documentation Organization

Complete workflow for setting up and maintaining project documentation. Follows a docs-first philosophy — start every project with documentation, not code — covering directory structure, documentation types, quality gates, and the critical separation between current-state and future-state docs.

## What's Inside

- Docs-first philosophy and workflow
- Standard directory structure for project documentation
- Critical separation: current-state docs vs future-state planning
- Documentation types (ADRs, PRDs, Personas, Runbooks, Guides)
- Roadmap format and maintenance patterns
- Quality gates and anti-patterns
- New project documentation checklist

## When to Use

- Starting a new project and need docs structure
- Improving documentation on an existing project
- Setting up ADRs, PRDs, or persona docs
- Want consistent documentation across projects

## Installation

```bash
npx skills add docs-organization
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/documentation/docs-organization .cursor/skills/docs-organization
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/documentation/docs-organization ~/.cursor/skills/docs-organization
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/documentation/docs-organization .claude/skills/docs-organization
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/documentation/docs-organization ~/.claude/skills/docs-organization
```

---

Part of the [Documentation](..) skill category.
