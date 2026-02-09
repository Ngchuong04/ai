# Skill Creator

Guide for creating effective AI agent skills — modular packages that extend agent capabilities with specialized knowledge, workflows, and tools. Skills transform agents from general-purpose into specialized, equipped with procedural knowledge.

## What's Inside

- Skill anatomy (SKILL.md, scripts/, references/, assets/)
- YAML frontmatter format (WHAT, WHEN, KEYWORDS)
- Creation workflow (understand, plan, initialize, edit, package, iterate)
- Bundled resource patterns (scripts, references, assets)
- Progressive disclosure patterns for keeping SKILL.md lean
- Degrees of freedom calibration (high/medium/low specificity)
- Quality checklist
- Init and packaging scripts

## When to Use

- User wants to create, write, author, or update a skill
- User asks about skill structure, SKILL.md format, or how to package domain knowledge for AI agents
- Triggered by: "create a skill", "make a skill", "new skill", "skill template", "SKILL.md", "agent skill", "write a skill", "skill structure"

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/tools/skill-creator
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/tools/skill-creator .cursor/skills/skill-creator
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/tools/skill-creator ~/.cursor/skills/skill-creator
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/tools/skill-creator .claude/skills/skill-creator
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/tools/skill-creator ~/.claude/skills/skill-creator
```

## Related Skills

- **skill-judge** — Evaluate skill quality after creation
- **find-skills** — Discover existing skills before creating new ones

---

Part of the [Tools](..) skill category.
