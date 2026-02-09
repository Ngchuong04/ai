---
name: create-persona
model: reasoning
description: Create a user persona document
usage: /create-persona <name>
---

# /create-persona

Create a user persona document for product development.

## Usage

```
/create-persona <name>
```

**Arguments:**
- `name` — Persona name (e.g., "alex-developer", "sam-startup-founder")

## Examples

```
/create-persona alex-developer
/create-persona sam-startup-founder
/create-persona casey-casual-user
```

## When to Use

- **Before `/new-feature`** for persona-driven development
- Starting a new product (define users first)
- When features lack clarity about target user
- Adding a new user type to existing product
- Stakeholder alignment on who you're building for

## What It Does

1. **Creates** persona file at `docs/product/personas/[name].md`
2. **Prompts** for persona details (name, role, goals)
3. **Asks** about frustrations and needs
4. **Guides** through scenario creation
5. **Generates** structured persona document

## Persona Template

```markdown
# Persona: [Name]

## Overview
**Name:** [Full name]
**Role:** [Job title / description]
**Experience:** [Beginner / Intermediate / Expert]

## Goals
- [What they're trying to achieve]
- [Primary motivation]

## Frustrations
- [Current pain points]
- [What blocks them today]

## Needs
- [What they need from our product]
- [Key features they care about]

## Scenario
[A day-in-the-life story using the product]

## Quotes
> "[Something they might say that captures their mindset]"

## Technical Profile
- **Devices:** [Desktop, Mobile, etc.]
- **Tech comfort:** [Low / Medium / High]
- **Tools they use:** [Related tools]
```

## Why Personas Matter

| Without Personas | With Personas |
|-----------------|---------------|
| Build for "everyone" | Build for specific needs |
| Features lack focus | Features solve real problems |
| Debates are opinion-based | Decisions reference users |
| Easy to scope creep | Clear what's out of scope |

## Output Locations

- Persona → `docs/product/personas/[name].md`

## Related

- **Docs structure:** `/bootstrap-docs` (creates personas/)
- **New feature:** `/new-feature` (references personas)
- **Skill:** [`persona-docs`](ai/skills/writing/persona-docs/SKILL.md) (persona documentation templates and methodology)
- **Skill:** [`marketing-psychology`](ai/skills/marketing/marketing-psychology/SKILL.md) (psychological models for understanding user behavior)
- **Methodology:** [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md)
