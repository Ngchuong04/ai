# Skill Judge

Evaluate Agent Skill quality against official specifications. Scores skills across 8 dimensions (120 points total) and provides specific, actionable improvement suggestions based on patterns derived from 17+ official examples.

## What's Inside

- Core philosophy: Good Skill = Expert-only Knowledge minus What the Model Already Knows
- 8 evaluation dimensions: Knowledge Delta, Mindset + Procedures, Anti-Pattern Quality, Specification Compliance, Progressive Disclosure, Freedom Calibration, Pattern Recognition, Practical Usability
- Evaluation protocol (knowledge delta scan, structure analysis, scoring, grading)
- Grade scale (A through F with percentage thresholds)
- Common failure patterns with fixes (Tutorial, Dump, Orphan References, Checkbox Procedure, and more)
- Report template for structured evaluation output

## When to Use

- Reviewing or auditing a SKILL.md file
- Improving an existing skill's design
- Checking if a skill follows best practices
- Before publishing a skill to the ecosystem
- Triggered by: "review skill", "evaluate skill", "audit skill", "improve skill", "skill quality", "SKILL.md review"

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/tools/skill-judge
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install skill-judge
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/tools/skill-judge .cursor/skills/skill-judge
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/tools/skill-judge ~/.cursor/skills/skill-judge
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/tools/skill-judge .claude/skills/skill-judge
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/tools/skill-judge ~/.claude/skills/skill-judge
```

## Related Skills

- **skill-creator** — Create skills that score well on evaluation
- **find-skills** — Discover existing skills to evaluate

---

Part of the [Tools](..) skill category.
