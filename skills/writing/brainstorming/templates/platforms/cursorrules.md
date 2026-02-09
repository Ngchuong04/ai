# Brainstorming — Cursor Rules

# Collaborative design process: explore ideas before implementation.

## When to Use
- Before any creative work: features, components, new functionality
- When modifying behavior or architecture significantly
- When the user has an idea but no clear spec

## Process — Understanding the Idea
- Check the current project state first (files, docs, recent commits)
- Ask questions ONE AT A TIME — never overwhelm with multiple questions
- Prefer multiple-choice questions when possible
- Focus on understanding: purpose, constraints, success criteria
- If a topic needs more exploration, break it into follow-up questions

## Process — Exploring Approaches
- Always propose 2–3 different approaches with trade-offs
- Lead with your recommended option and explain why
- Present options conversationally, not as a wall of text
- Let the user pick before proceeding

## Process — Presenting the Design
- Present the design in sections of 200–300 words
- Ask after EACH section: "Does this look right so far?"
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't fit

## Key Principles
- One question at a time — never batch questions
- Multiple choice preferred over open-ended
- Apply YAGNI ruthlessly — remove unnecessary features
- Always explore alternatives before settling
- Validate incrementally — confirm each section before moving on
- Be flexible — revisit earlier decisions when needed

## After the Design
- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git
- Ask "Ready to set up for implementation?" before coding

## Never
- Never skip the brainstorming phase for creative work
- Never present the entire design at once — break it into sections
- Never assume requirements — ask when unclear
- Never jump to implementation without a validated design
