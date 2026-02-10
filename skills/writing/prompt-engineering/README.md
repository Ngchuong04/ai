# Prompt Engineering

Master advanced prompt engineering techniques to maximize LLM performance, reliability, and controllability in production. Covers core techniques, key patterns, and optimization strategies for building AI-powered features.

## What's Inside

- Core techniques: Few-Shot Learning, Chain-of-Thought, Structured Outputs, System Prompt Design, Template Systems
- Key patterns: Structured Output with Validation, CoT with Self-Verification, Progressive Disclosure, Error Recovery and Fallback, Role-Based System Prompts, RAG Integration
- Performance optimization (token efficiency, prompt caching)
- Best practices and success metrics
- Common pitfalls with fixes
- Integration patterns (validation, confidence scoring)
- Reference files for each technique (CoT, few-shot, optimization, templates, system prompts)
- Prompt template library and optimization script
- Eval cases for testing prompts

## When to Use

- Designing complex prompts for production LLM applications
- Optimizing prompt performance and consistency
- Implementing structured reasoning patterns (chain-of-thought, tree-of-thought)
- Building few-shot learning systems with dynamic example selection
- Creating reusable prompt templates with variable interpolation
- Debugging prompts that produce inconsistent outputs
- Implementing system prompts for specialized AI assistants

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/writing/prompt-engineering
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install prompt-engineering
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/writing/prompt-engineering .cursor/skills/prompt-engineering
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/writing/prompt-engineering ~/.cursor/skills/prompt-engineering
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/writing/prompt-engineering .claude/skills/prompt-engineering
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/writing/prompt-engineering ~/.claude/skills/prompt-engineering
```

## Related Skills

- **clear-writing** — Write clear prose within prompts and documentation
- **schema-markup** — Structured data concepts apply to structured outputs

---

Part of the [Writing](..) skill category.
