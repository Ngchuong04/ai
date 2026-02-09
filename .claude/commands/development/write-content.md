---
name: write-content
model: reasoning
description: Create professional written content — blog posts, docs, guides, tutorials — following clear-writing principles
usage: /write-content [type] [topic] [--audience <audience>] [--length <short|medium|long>]
---

# /write-content

Create polished, well-structured written content following clear-writing principles from The Elements of Style.

## Usage

```
/write-content [type] [topic] [--audience <audience>] [--length <short|medium|long>]
```

**Arguments:**
- `type` — Content type: `blog-post`, `documentation`, `guide`, `tutorial`, `readme`, `email`, `announcement`
- `topic` — The subject to write about
- `--audience <audience>` — Target reader (e.g., `developers`, `executives`, `beginners`, `users`)
- `--length <length>` — Content length: `short` (~500 words), `medium` (~1500 words), `long` (~3000+ words). Default: `medium`

## Examples

```
/write-content blog-post "Why We Migrated to Server Components" --audience developers --length long
/write-content documentation "Authentication API" --audience developers
/write-content guide "Setting Up CI/CD with GitHub Actions" --audience beginners --length medium
/write-content tutorial "Build a REST API with Express" --audience beginners --length long
/write-content readme "Project overview" --audience developers --length short
/write-content announcement "v2.0 Release" --audience users --length short
/write-content email "Security incident post-mortem" --audience executives --length short
```

## When to Use

- Writing a blog post or technical article
- Creating documentation for an API, library, or feature
- Writing a step-by-step guide or tutorial
- Drafting a project README
- Composing a release announcement or email update
- Any time you need clear, structured prose — not just bullet points

## What It Does

1. **Defines** audience, purpose, tone, and format
2. **Brainstorms** angles and builds a structured outline
3. **Drafts** following clear-writing principles (active voice, concrete language, no filler)
4. **Structures** with proper headings, lists, and code blocks
5. **Adds** diagrams for technical content where they aid understanding
6. **Adds** schema markup for web-published content
7. **Edits** in a final pass to tighten prose and improve flow

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Define Content Parameters

Establish the following before writing:

| Parameter | How to Determine |
|-----------|-----------------|
| **Audience** | Use `--audience` flag, or infer from project context and content type |
| **Purpose** | What should the reader know, feel, or do after reading? |
| **Tone** | Match audience: technical for developers, accessible for beginners, concise for executives |
| **Format** | Determined by `type` — each has a distinct structure (see Phase 3) |
| **Length** | Use `--length` flag: short ~500 words, medium ~1500, long ~3000+ |

### Phase 2: Brainstorm and Outline

- Generate 3–5 possible angles for the topic.
- Select the strongest angle based on audience relevance and uniqueness.
- Build a hierarchical outline:
  - H2 sections for major themes
  - H3 subsections for supporting points
  - Note where code examples, diagrams, or callouts are needed

For technical content, consider:
- What does the reader need to know first? (prerequisites)
- What's the logical progression from concept to application?
- Where will the reader get stuck? (address proactively)

### Phase 3: Draft Content

Write the first draft following the outline. Apply structure rules per content type:

| Type | Structure |
|------|-----------|
| `blog-post` | Hook → Context → Main argument → Supporting points → Conclusion → CTA |
| `documentation` | Overview → Prerequisites → API/Usage → Parameters → Examples → Errors → Related |
| `guide` | Goal → Prerequisites → Step-by-step instructions → Verification → Troubleshooting |
| `tutorial` | What you'll build → Setup → Step-by-step with code → Testing → Next steps |
| `readme` | Title → Description → Installation → Quick start → Usage → API → Contributing → License |
| `email` | Subject line → Key message (first sentence) → Context → Action required → Timeline |
| `announcement` | Headline → What's new → Why it matters → How to get started → What's next |

### Phase 4: Apply Clear-Writing Principles

Run every paragraph through these rules from The Elements of Style:

| Principle | Check |
|-----------|-------|
| **Use active voice** | "The team built the feature" not "The feature was built by the team" |
| **Omit needless words** | Cut "in order to" → "to", "at this point in time" → "now", "due to the fact that" → "because" |
| **Use specific, concrete language** | "Reduced latency by 40ms" not "Significantly improved performance" |
| **Parallel construction** | List items and headings follow the same grammatical pattern |
| **Put statements in positive form** | "Forgot to" not "Did not remember to" |
| **Use definite language** | "This approach fails when…" not "This approach might possibly fail in some cases when…" |
| **One paragraph, one idea** | Each paragraph makes a single point and then stops |
| **Strong openings** | Every section opens with its main point, not with throat-clearing |

### Phase 5: Add Diagrams

For technical content, identify where a diagram aids understanding better than prose:

| Content | Diagram Type |
|---------|-------------|
| Architecture or system design | C4 or flowchart |
| API or code flow | Sequence diagram |
| Data models or relationships | Entity-relationship diagram |
| Processes or algorithms | Flowchart |
| State transitions | State diagram |
| Project timeline | Gantt chart |

Generate diagrams in Mermaid syntax so they render in markdown. Follow the mermaid-diagrams skill for best practices: max 15 nodes, clear labels, logical grouping.

### Phase 6: Add Schema Markup

For web-published content (blog posts, documentation, guides), generate appropriate JSON-LD schema:

| Content Type | Schema Type |
|-------------|-------------|
| `blog-post` | `Article` or `BlogPosting` |
| `documentation` | `TechArticle` |
| `guide` / `tutorial` | `HowTo` |
| `readme` | `SoftwareSourceCode` |
| `announcement` | `NewsArticle` |

### Phase 7: Final Edit Pass

Review the complete draft against this checklist:

- [ ] Every section has a clear purpose — remove any that don't
- [ ] No filler words or phrases remain
- [ ] All claims are specific and provable
- [ ] Code examples are correct and runnable
- [ ] Headings are parallel and scannable
- [ ] Flow between sections is logical — each follows naturally from the last
- [ ] Introduction and conclusion match — the piece delivers what it promises
- [ ] Length matches the `--length` target (±20%)

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER start with "In this article, we will…"** | Weak opening that delays the value. Start with the insight or the problem. |
| **NEVER use filler phrases** | "It is worth noting that" and "It is important to mention" add nothing |
| **NEVER use passive voice without purpose** | Active voice is almost always clearer and more direct |
| **NEVER write walls of text** | Use headings, lists, code blocks, and diagrams to break up prose |
| **NEVER assume knowledge without stating prerequisites** | If the reader needs to know something first, say so explicitly |
| **NEVER leave code examples untested** | Every code block should be runnable or clearly marked as pseudocode |
| **NEVER pad content to hit a word count** | Say what needs saying and stop. Shorter is better than longer if both are complete. |

## Output

Complete content piece in markdown format, ready to publish or commit:

```
[Title]
=======
Audience: [target reader]
Length:   [word count]
Type:     [content type]

[Full content in markdown with headings, code blocks, diagrams, and callouts]
```

For web content, a separate `schema.json` block with the appropriate JSON-LD markup.

## Related

- **Skill:** [`clear-writing`](ai/skills/writing/clear-writing/SKILL.md) — Elements of Style principles for professional prose
- **Skill:** [`brainstorming`](ai/skills/writing/brainstorming/SKILL.md) — structured ideation for angles and outlines
- **Skill:** [`mermaid-diagrams`](ai/skills/writing/mermaid-diagrams/SKILL.md) — diagram generation for technical content
- **Skill:** [`schema-markup`](ai/skills/writing/schema-markup/SKILL.md) — structured data for web-published content
- **Agent:** [`content`](ai/agents/content/AGENT.md) — content creation agent
- **Command:** `/create-diagram` — generate standalone Mermaid diagrams
- **Command:** `/write-copy` — for marketing copy rather than editorial content
