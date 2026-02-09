# Content Agent

Autonomous workflow for creating professional written content — from brainstorming through drafting, editing, and publishing. Covers documentation, blog posts, social media, professional communications, and technical writing.

## Workflow Phases

- **Phase 1: Discovery** — Content brief: audience, purpose, format, tone, length, platform
- **Phase 2: Brainstorming** — Ideas, angles, outlines using the brainstorming skill
- **Phase 3: Research** — Facts, examples, and data to support the content
- **Phase 4: Drafting** — Draft following clear writing principles
- **Phase 5: Editing** — Cut filler, activate voice, sharpen sentences
- **Phase 6: Enhancement** — Diagrams, illustrations, schema markup, SEO
- **Phase 7: Review** — Quality, audience fit, factual accuracy

## Skills Used

- `brainstorming` — Idea generation and creative exploration
- `clear-writing` — Concise prose, Strunk's Elements of Style
- `professional-communication` — Email, messaging, meeting communication
- `article-illustrator` — Article illustration generation
- `persona-docs` — Target audience documentation
- `mermaid-diagrams` — Technical diagrams and visualizations
- `prompt-engineering` — Prompt optimization for content generation
- `schema-markup` — SEO structured data and schema.org
- `social-content` — Platform-specific social media content
- `copywriting` — Marketing copy frameworks

## Trigger Phrases

- "write a blog post about [topic]"
- "create documentation for [project/feature]"
- "draft an email to [audience] about [topic]"
- "write content for [page/section]"
- "create a README for [project]"
- "write a guide on [topic]"
- "create social posts for [announcement]"
- "write a report on [subject]"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add content
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/content .cursor/rules/content-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/content .claude/skills/content-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/content ~/.claude/skills/content-agent
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
