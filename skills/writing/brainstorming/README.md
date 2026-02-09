# Brainstorming Ideas Into Designs

Explore ideas before implementation through collaborative dialogue. Turns ideas into fully formed designs and specs through structured conversation, ensuring you explore the problem space before jumping to solutions.

## What's Inside

- Four-phase process: Understand the Idea, Explore Approaches, Present the Design, After the Design
- Question-asking guidelines (one at a time, prefer multiple choice)
- Approach presentation format with trade-offs and recommendations
- Incremental design validation (200-300 word sections)
- Common brainstorming contexts (new feature, refactoring, architecture decision, complex bug fix)
- Platform-specific templates (Claude, GitHub Copilot, Cursor)
- Key principles (YAGNI, explore alternatives, incremental validation)
- Anti-patterns to avoid

## When to Use

- Before any creative work — creating features, building components, adding functionality
- Modifying existing behavior or architecture
- When the user has an idea but no clear spec
- When requirements are ambiguous or incomplete
- Before any implementation that involves design decisions

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/writing/brainstorming
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/writing/brainstorming .cursor/skills/brainstorming
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/writing/brainstorming ~/.cursor/skills/brainstorming
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/writing/brainstorming .claude/skills/brainstorming
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/writing/brainstorming ~/.claude/skills/brainstorming
```

---

Part of the [Writing](..) skill category.
