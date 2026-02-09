---
name: brainstorm
model: reasoning
description: Run a structured brainstorming session to generate, filter, and expand ideas for features, solutions, or designs
usage: /brainstorm [topic] [--mode <diverge|converge|both>]
---

# /brainstorm

Run a structured brainstorming session that generates diverse ideas, filters them by impact and feasibility, and expands the top picks into actionable proposals.

## Usage

```
/brainstorm [topic] [--mode <diverge|converge|both>]
```

**Arguments:**
- `topic` — The problem, opportunity, or question to brainstorm around
- `--mode <mode>` — Session mode: `diverge` (generate ideas only), `converge` (filter and rank existing ideas), `both` (full session, default)

## Examples

```
/brainstorm "How can we reduce onboarding time from 10 minutes to under 2?"
/brainstorm "New features for Q3 roadmap" --mode diverge
/brainstorm "Architecture for real-time collaboration" --mode both
/brainstorm "Monetization strategies for free tier users" --mode converge
/brainstorm "Reduce API response time below 100ms"
```

## When to Use

- Starting a new feature and need to explore approaches before committing
- Stuck on a problem and need fresh angles
- Planning a roadmap and need to generate feature candidates
- Evaluating tradeoffs between multiple solutions
- Exploring how to 10x an existing experience
- Before any significant architecture or product decision

## What It Does

1. **Defines** the problem or opportunity with clear boundaries
2. **Diverges** to generate 10+ ideas using multiple creative lenses
3. **Converges** to filter and rank ideas by impact and effort
4. **Expands** the top 3 ideas into structured proposals with user stories, requirements, and risks
5. **Presents** ranked recommendations with clear rationale

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Define the Problem

Before generating ideas, frame the problem clearly:

| Element | Question |
|---------|----------|
| **Problem statement** | What exactly are we trying to solve or improve? |
| **Current state** | What exists today? What's working? What's not? |
| **Success criteria** | How will we know the solution worked? |
| **Constraints** | What are the non-negotiables? (timeline, budget, tech stack, team size) |
| **Scope** | What's in bounds? What's explicitly out of bounds? |

Write a one-sentence problem statement in this format:
> "How might we [desired outcome] for [target user] given [key constraint]?"

### Phase 2: Diverge — Generate Ideas

Generate at least 10 ideas. Quantity matters more than quality at this stage. Use multiple lenses to force diversity:

| Lens | Prompt |
|------|--------|
| **User perspective** | What would the user wish this could do? |
| **10x thinking** | What if we made this 10x better, not 10% better? |
| **Inversion** | What's the opposite approach? What if we removed this entirely? |
| **Analogy** | How do other industries/products solve a similar problem? |
| **Constraint removal** | If we had unlimited time/money/engineers, what would we build? |
| **Simplification** | What's the simplest possible solution that still works? |
| **Composition** | Can we combine two existing features to create something new? |
| **Automation** | What's currently manual that could be automated? |
| **Edge cases** | What would power users want? What about complete beginners? |
| **Competitor** | What would [top competitor] do? What would they never do? |

Rules for divergence:
- No judging ideas during this phase
- Write each idea in one sentence
- Include wild ideas — they often spark practical ones
- Build on previous ideas ("Yes, and…")
- Aim for at least 10, push to 15+ if the topic is rich

### Phase 3: Converge — Filter and Rank

Score each idea on two dimensions:

| Dimension | Scale | Criteria |
|-----------|-------|----------|
| **Impact** | 1–5 | How much does this move the needle on the success criteria? |
| **Effort** | 1–5 | How much time, complexity, and risk does this involve? (1 = low effort) |

Calculate priority score: `Impact × (6 - Effort)` — this naturally surfaces high-impact, low-effort ideas.

Create a 2×2 matrix:

```
         High Impact
              │
   Quick Wins │ Big Bets
   (do first) │ (plan carefully)
──────────────┼──────────────
   Fill-ins   │ Money Pits
   (do if easy)│ (avoid)
              │
         Low Impact
    Low Effort ──── High Effort
```

Select the top 3 ideas (prioritizing Quick Wins, then Big Bets).

### Phase 4: Expand Top Ideas

For each of the top 3 ideas, develop a structured proposal:

**User Story:**
```
As a [type of user],
I want to [action/capability],
so that [benefit/outcome].
```

**Key Requirements:**
- 3–5 must-have requirements
- 2–3 nice-to-have requirements

**Technical Considerations:**
- Architecture implications
- Dependencies on existing systems
- Data model changes
- API changes
- Third-party integrations needed

**Risks and Tradeoffs:**

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk description] | Low/Med/High | Low/Med/High | [how to reduce] |

**Estimated Effort:**
- T-shirt size: XS / S / M / L / XL
- Key milestones and rough timeline

### Phase 5: Present Recommendations

Rank the top 3 ideas with a clear recommendation:

| Rank | Idea | Impact | Effort | Recommendation |
|------|------|--------|--------|---------------|
| 1 | [name] | [score] | [score] | [why this is #1] |
| 2 | [name] | [score] | [score] | [why this is #2] |
| 3 | [name] | [score] | [score] | [why this is #3] |

Include a "Start with…" recommendation — the single next action to take.

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER judge ideas during divergence** | Premature filtering kills creative thinking and reduces idea diversity |
| **NEVER stop at the first good idea** | The best idea is rarely the first one. Push for volume. |
| **NEVER skip the problem definition** | Brainstorming without a clear problem produces unfocused, unusable ideas |
| **NEVER present ideas without ranking** | Unranked lists create decision paralysis. Always prioritize. |
| **NEVER ignore feasibility** | Even in divergent thinking, note obviously impossible ideas so convergence is efficient |
| **NEVER expand more than 3 ideas** | Deep analysis of too many ideas wastes effort. Go deep on the best few. |

## Output

```
Brainstorm: [topic]
===================
Problem: [one-sentence problem statement]
Mode:    [diverge | converge | both]

All Ideas (ranked):
  1. [idea] — Impact: X, Effort: X, Score: X
  2. [idea] — Impact: X, Effort: X, Score: X
  ...

Top 3 Expanded:

#1: [Idea Name]
  User Story: As a [user], I want [capability], so that [benefit]
  Requirements: [list]
  Technical: [considerations]
  Risks: [table]
  Effort: [t-shirt size]

#2: [Idea Name]
  ...

#3: [Idea Name]
  ...

Recommendation: Start with [#1] because [rationale].
Next action: [specific first step].
```

## Related

- **Skill:** [`brainstorming`](ai/skills/writing/brainstorming/SKILL.md) — structured ideation frameworks
- **Skill:** [`game-changing-features`](ai/skills/writing/game-changing-features/SKILL.md) — finding 10x product opportunities
- **Skill:** [`decision-frameworks`](ai/skills/meta/decision-frameworks/SKILL.md) — structured decision-making tools
- **Agent:** [`development`](ai/agents/development/AGENT.md) — development agent
- **Command:** `/new-feature` — take a brainstormed idea into implementation
- **Command:** `/write-content` — write up a brainstorm outcome as a proposal document
