# Meme Factory

Generate memes using the free memegen.link API and textual Markdown meme formats. Supports 100+ image templates and 15+ textual meme formats — no API key required.

**Note:** Image meme URLs point to the third-party service `api.memegen.link`; no requests are made by this skill until a generated URL is used (e.g. embedded or opened in a browser).

## What's Inside

- URL structure and text encoding for memegen.link API
- Popular template selection guide with contextual matching
- Image format options and platform-specific dimensions
- Textual Markdown meme formats (greentext, copypasta, ASCII art, Tumblr chains, and more)
- Custom backgrounds and mixing text + image memes
- Python helper script for programmatic generation
- Validation checklist and embedding guidelines

## When to Use

- User wants to create memes or add humor to content
- Generating visual aids for social media
- Triggered by: "make a meme", "create meme", "meme about", "meme factory", or requests for humor/visual comedy

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/tools/meme-factory
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install meme-factory
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/tools/meme-factory .cursor/skills/meme-factory
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/tools/meme-factory ~/.cursor/skills/meme-factory
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/tools/meme-factory .claude/skills/meme-factory
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/tools/meme-factory ~/.claude/skills/meme-factory
```

---

Part of the [Tools](..) skill category.
