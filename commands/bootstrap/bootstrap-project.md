---
name: bootstrap-project
model: standard
description: Scaffold a new project with opinionated setup
usage: /bootstrap-project
---

# /bootstrap-project

Interactive project scaffolding with docs-first methodology.

## Usage

```
/bootstrap-project
```

## Examples

```
/bootstrap-project             # Interactive scaffolding
```

## When to Use

- Starting a **brand new project** from scratch
- Need full project scaffold with docs, tests, CI/CD
- Want opinionated structure following docs-first methodology
- **NOT** for existing projects — use `/bootstrap-docs` instead

## What It Does

1. **Asks** for project type (Monorepo, App, Service, Library)
2. **Asks** for stack preferences (Next.js, Go, Node.js, etc.)
3. **Asks** for features (Docker, Testing, CI/CD)
4. **Creates** directory structure based on project type
5. **Initializes** documentation in `docs/`
6. **Creates** Makefile with standard targets
7. **Generates** initial ADR for tech decisions
8. **Sets up** roadmap template
9. **Initializes** git with initial commit

## Interactive Questions

1. **Project type?** Monorepo, App, Service, Library
2. **Stack?** Next.js, Go, Node.js, Python, etc.
3. **Features?** Docker, Testing, CI/CD, Docs

## Output Locations

```
project/
├── .github/workflows/ci.yml   # CI/CD (if selected)
├── docker/                    # Docker files (if selected)
├── docs/
│   ├── architecture/
│   ├── planning/
│   │   ├── roadmap.md
│   │   └── specs/
│   ├── decisions/
│   │   └── 001-tech-stack.md
│   ├── product/
│   │   └── personas/
│   └── runbooks/
├── src/                       # (structure varies by type)
├── tests/
├── Makefile
└── README.md
```

## After Bootstrap

1. Define personas in `docs/product/personas/`
2. Write initial PRD in `docs/product/`
3. Review ADR-001 tech decisions
4. Populate roadmap in `docs/planning/`

## Related

- **Agent:** [`ai/agents/bootstrap/`](ai/agents/bootstrap/)
- **Docs-only:** `/bootstrap-docs` (add docs to existing project)
- **Design system:** `/bootstrap-design-system` (add design system)
- **Methodology:** [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
