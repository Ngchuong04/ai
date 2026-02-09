# Architecture Decision Records (ADRs)

Lightweight documentation capturing the context, decision, and consequences of significant technical choices. ADRs become the institutional memory of why things are built the way they are.

## What's Inside

- Quick decision guide for when to write an ADR vs skip
- ADR lifecycle management (Proposed → Accepted → Deprecated → Superseded)
- Standard ADR template (context, decision, consequences)
- MADR (Markdown Any Decision Records) extended template
- Lightweight and superseded ADR templates
- Directory structure conventions and tooling (`adr-tools`)
- Review checklist for ADR quality

## When to Use

- Adopting new frameworks or technologies
- Choosing between architectural approaches
- Making database or infrastructure decisions
- Defining API design patterns
- Any decision that would be hard to reverse or understand later

## Installation

```bash
skills add adr-patterns
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/documentation/adr-patterns .cursor/skills/adr-patterns
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/documentation/adr-patterns ~/.cursor/skills/adr-patterns
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/documentation/adr-patterns .claude/skills/adr-patterns
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/documentation/adr-patterns ~/.claude/skills/adr-patterns
```

---

Part of the [Documentation](..) skill category.
