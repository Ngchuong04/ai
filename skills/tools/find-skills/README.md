# Find Skills

Discover and install agent skills from the open skills ecosystem using `npx skills`. Helps users find and install modular skill packages that extend agent capabilities with specialized knowledge, workflows, and tools.

## What's Inside

- Skill discovery workflow (identify need, search, present, install)
- Common skill categories (Web Development, Testing, DevOps, Documentation, Code Quality, Design)
- Key commands reference (`find`, `add`, `check`, `update`, `init`)
- Handling "no skills found" scenarios
- Search query mapping from user requests

## When to Use

- User asks "how do I do X" where X might have an existing skill
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is a specialized capability
- User wants to extend agent capabilities
- User mentions wishing they had help with a specific domain

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/tools/find-skills
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/tools/find-skills .cursor/skills/find-skills
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/tools/find-skills ~/.cursor/skills/find-skills
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/tools/find-skills .claude/skills/find-skills
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/tools/find-skills ~/.claude/skills/find-skills
```

---

Part of the [Tools](..) skill category.
