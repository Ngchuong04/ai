# API Agent

Autonomous workflow for designing, specifying, implementing, testing, and documenting APIs end-to-end. Handles API design with REST or GraphQL patterns, OpenAPI/Swagger specification generation, endpoint implementation with validation and error handling, test generation, and API documentation.

## Workflow Phases

- **Phase 1: Design** — Gather requirements, define resource model, choose REST vs GraphQL, confirm resource map
- **Phase 2: Specification** — Generate OpenAPI 3.x or GraphQL schema
- **Phase 3: Implementation** — Scaffold endpoints with validation, error handling, and middleware
- **Phase 4: Testing** — Unit and integration tests for every endpoint
- **Phase 5: Documentation** — Human-readable API docs from spec and code

## Skills Used

- `api-design-principles` — REST and GraphQL design patterns, status codes, pagination
- `api-design` — OpenAPI templates and GraphQL schema
- `auth-patterns` — Authentication and authorization
- `error-handling` — API error handling patterns
- `rate-limiting` — Rate limiting strategies
- Command: `create-api-route` — Single-endpoint scaffolding

## Trigger Phrases

- "build an API for [domain]"
- "create API for [resource]"
- "design API endpoints for [feature]"
- "generate OpenAPI spec for [service]"
- "add API endpoints for [module]"
- "API development for [project]"

## Installation

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add api
```

### Manual: Cursor

Copy this agent into your project as a rule so the AI gets the workflow as context:

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/api .cursor/rules/api-agent
```

### Manual: Claude Code

Copy into project or global skills so Claude Code can load the workflow:

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/api .claude/skills/api-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/api ~/.claude/skills/api-agent
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
