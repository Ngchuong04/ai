---
name: new-adr
model: reasoning
description: Create a new Architecture Decision Record
usage: /new-adr <title>
---

# /new-adr

Create a new Architecture Decision Record.

## Usage

```
/new-adr <title>
```

**Arguments:**
- `title` — Decision title (kebab-case, descriptive)

## Examples

```
/new-adr authentication-approach
/new-adr database-selection
/new-adr caching-strategy
/new-adr api-versioning
```

## What It Does

1. **Scans** `docs/decisions/` to determine next ADR number
2. **Creates** new file `docs/decisions/[number]-[title].md`
3. **Fills** in template with title and number
4. **Prompts** for context (what problem are we solving?)
5. **Guides** through decision capture

## ADR Template

```markdown
# ADR-[NUMBER]: [Title]

## Status
Proposed | Accepted | Deprecated | Superseded

## Context
[What is the issue we're solving? What constraints exist?]

## Decision
[What did we decide? Be specific about the choice made.]

## Consequences
[Results - positive and negative. What becomes easier? Harder?]

## Alternatives Considered
[Other options evaluated and why they were rejected]
```

## Status Lifecycle

| Status | Meaning |
|--------|---------|
| Proposed | Under discussion |
| Accepted | Implemented and active |
| Deprecated | No longer recommended |
| Superseded | Replaced by another ADR |

## Output Locations

- ADR file → `docs/decisions/[number]-[title].md`

## Related

- **Feature development:** `/new-feature` (often triggers ADR)
- **Docs structure:** `/bootstrap-docs` (sets up decisions/)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
