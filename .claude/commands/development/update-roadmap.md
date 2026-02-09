---
name: update-roadmap
model: fast
description: Add todos and update sprint status in roadmap
usage: /update-roadmap [action]
---

# /update-roadmap

Manage the project roadmap with todos and sprint status.

## Usage

```
/update-roadmap [action]
```

**Actions:**
- `add` — Add new todos to roadmap (default)
- `complete` — Mark todos as complete
- `move` — Move todos between sections
- `review` — Show current roadmap status

## Examples

```
/update-roadmap                    # Interactive: add todos
/update-roadmap add               # Add new todos
/update-roadmap complete          # Mark items done
/update-roadmap move              # Move between sprints
/update-roadmap review            # Show current status
```

## When to Use

- Starting work on a new task (add to roadmap first)
- Completing tasks (mark as done)
- Sprint planning (move items to current sprint)
- Checking project status (review)
- Breaking down features into tasks

## What It Does

### `add` (default)
1. **Reads** current `docs/planning/roadmap.md`
2. **Prompts** for new todos
3. **Asks** for placement (Current Sprint, Backlog, etc.)
4. **Breaks down** complex tasks into smaller todos
5. **Adds** todos in correct section
6. **Orders** by dependencies

### `complete`
1. **Shows** unchecked todos
2. **Prompts** for which to complete
3. **Marks** as done: `- [x]`
4. **Optionally** moves to Completed section

### `move`
1. **Shows** todos by section
2. **Prompts** for which to move
3. **Asks** for target section
4. **Reorders** maintaining dependencies

### `review`
1. **Reads** roadmap
2. **Counts** todos by section and status
3. **Shows** summary

## Roadmap Format

```markdown
# Roadmap

## In Progress
- [ ] Currently working on this

## Current Sprint
- [ ] Next priority
- [ ] Following item

## Backlog
- [ ] Future work
- [ ] More future work

## Completed
- [x] Done item (with date)
```

## Good Todo Practices

| Good | Bad |
|------|-----|
| "Add POST /auth/login endpoint" | "Implement authentication" |
| "Create LoginForm component" | "Build the login UI" |
| "Add JWT token generation" | "Handle tokens" |

**Break down** complex tasks into:
- Smallest completable units
- Clear, specific descriptions
- Ordered by dependencies

## Output Locations

- Roadmap → `docs/planning/roadmap.md`

## Related

- **New feature:** `/new-feature` (creates spec + roadmap entries)
- **Bootstrap docs:** `/bootstrap-docs` (creates roadmap template)
- **Development agent:** [`ai/agents/development/`](ai/agents/development/)
