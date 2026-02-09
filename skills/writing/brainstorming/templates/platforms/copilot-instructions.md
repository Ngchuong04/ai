# Brainstorming — Copilot Instructions

## Instructions

When the user has an idea for a feature, component, or behavior change, follow this collaborative brainstorming process before writing any implementation code.

## Phase 1: Understand the Idea

Start by checking the project context (files, docs, commits). Then ask questions to refine the idea:

```
# Ask ONE question at a time
# Prefer multiple-choice format when possible

Q: "What's the primary goal of this feature?"
  a) Improve user onboarding
  b) Add a new data visualization
  c) Optimize an existing workflow
  d) Something else — describe it
```

Focus each question on: purpose, constraints, user needs, or success criteria. Never ask more than one question per message.

## Phase 2: Explore Approaches

Always present 2–3 approaches with trade-offs:

```markdown
## Approach A: [Name] ⭐ Recommended
- Pros: ...
- Cons: ...
- Why I recommend this: ...

## Approach B: [Name]
- Pros: ...
- Cons: ...

## Approach C: [Name]
- Pros: ...
- Cons: ...
```

Lead with your recommendation and reasoning. Let the user choose.

## Phase 3: Present the Design

Break the design into 200–300 word sections covering:
- Architecture and components
- Data flow and state management
- Error handling and edge cases
- Testing strategy

After each section, ask: "Does this look right so far?"

## Key Principles

- One question per message — never overwhelm
- YAGNI ruthlessly — cut unnecessary features
- Always explore alternatives before committing
- Validate each section incrementally
- Write the final design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Ask before moving to implementation
