---
name: bootstrap-docs
model: fast
description: Add documentation structure to existing project
usage: /bootstrap-docs
---

# /bootstrap-docs

Add docs-first documentation structure to an existing project.

## Usage

```
/bootstrap-docs
```

## Examples

```
/bootstrap-docs                # Add docs/ structure to current project
```

## When to Use

- Adding documentation to an **existing project** that lacks `docs/`
- Project already has source code but no structured docs
- Want docs-first methodology without recreating project
- **NOT** for new projects — use `/bootstrap-project` instead

## What It Does

1. **Creates** `docs/` directory structure
2. **Generates** template files for each section
3. **Creates** ADR template (001-template.md)
4. **Initializes** roadmap with sections
5. **Creates** persona template
6. **Sets up** runbook templates (local-dev, deploy)

## Output Locations

```
docs/
├── architecture/
│   └── README.md              # Architecture overview
├── planning/
│   ├── roadmap.md             # Sprint tracking
│   └── specs/                 # Feature specs go here
├── decisions/
│   └── 001-template.md        # ADR template
├── product/
│   ├── overview.md            # Product overview
│   └── personas/              # User personas
└── runbooks/
    ├── local-dev.md           # Local development setup
    └── deploy.md              # Deployment procedures
```

## Templates Created

| File | Purpose |
|------|---------|
| `decisions/001-template.md` | ADR template with Status, Context, Decision, Consequences |
| `planning/roadmap.md` | Sprint tracking with Current/Backlog sections |
| `runbooks/local-dev.md` | Prerequisites, setup steps, common tasks |
| `runbooks/deploy.md` | Deployment checklist, rollback procedures |

## Related

- **Full project:** `/bootstrap-project` (creates entire project)
- **Design system:** `/bootstrap-design-system` (add design tokens)
- **New feature:** `/new-feature` (use docs structure)
- **New ADR:** `/new-adr` (create decision record)
