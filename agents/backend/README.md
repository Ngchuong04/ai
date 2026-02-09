# Backend Agent

Autonomous workflow for designing, implementing, and hardening production-grade backend services end-to-end. Handles architecture decisions, database design, service layers, authentication, caching, and production readiness.

## Workflow Phases

- **Phase 1: Architecture** — Gather requirements, choose architecture pattern (monolith/microservices/serverless), document ADRs
- **Phase 2: Data modeling** — Database schemas, indexing, constraints, migration paths
- **Phase 3: Service layer** — Implementation with validation, error handling, auth, and authorization
- **Phase 4: Infrastructure** — Logging, caching, rate limiting, health checks
- **Phase 5: Production hardening** — Security review, monitoring, graceful shutdown
- **Phase 6: Documentation** — Runbooks and operational docs

## Skills Used

- `architecture-patterns` — Clean, Hexagonal, DDD, layered
- `nodejs-patterns` — Node.js backend patterns and middleware
- `supabase-postgres` — Postgres best practices, indexing, query optimization
- `auth-patterns` — Authentication and authorization
- `error-handling` — API error handling patterns
- `rate-limiting` — Rate limiting strategies
- `caching` — Caching patterns and invalidation
- `logging-observability` — Structured logging and distributed tracing
- `production-readiness` — Production readiness checklist

## Trigger Phrases

- "build a backend for [domain]"
- "create a service for [feature]"
- "design the architecture for [system]"
- "implement the backend for [project]"
- "build the API layer for [application]"
- "create a microservice for [capability]"
- "set up the server for [project]"

## Installation

### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/backend .cursor/agents/backend
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/backend ~/.cursor/agents/backend
```

### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/backend .claude/agents/backend
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/backend ~/.claude/agents/backend
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
