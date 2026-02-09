---
name: create-service
model: standard
description: Scaffold a new backend service with proper architecture, containerization, and dev tooling
usage: /create-service <service-name> [--type rest|graphql|grpc] [--stack node|python|go]
---

# /create-service

Scaffold a production-ready backend service with architecture patterns, structured logging, health checks, containerization, and development tooling.

## Usage

```
/create-service <service-name> [--type rest|graphql|grpc] [--stack node|python|go]
```

**Arguments:**
- `service-name` — Name of the service (e.g., `user-service`, `billing-api`). Used for directory name, package name, and Docker image name
- `--type` — API style (default: `rest`). Accepts `rest`, `graphql`, `grpc`
- `--stack` — Language and ecosystem (default: auto-detected from workspace). Accepts `node`, `python`, `go`

## Examples

```
/create-service user-service --type rest --stack node
/create-service analytics-engine --type graphql --stack python
/create-service notification-service --type grpc --stack go
/create-service payment-gateway --type rest
/create-service search-service --stack node
```

## When to Use

- Starting a new microservice from scratch
- Adding a service to an existing monorepo or multi-service architecture
- Replacing a prototype with a properly structured service
- Bootstrapping a backend for a new project with production-ready defaults
- Standardizing service structure across a team

## What It Does

1. **Detects or asks** for service type, language/framework, and database needs
2. **Selects** an architecture pattern based on domain complexity
3. **Scaffolds** directory structure matching the chosen pattern
4. **Generates** boilerplate files with production-ready defaults
5. **Adds** containerization and development tooling
6. **Reports** all created files and next steps

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Input and Detect Context

Extract structured parameters from the command arguments:

| Parameter | Source | Default |
|-----------|--------|---------|
| Service name | First positional argument | Required |
| API type | `--type` flag | `rest` |
| Stack | `--stack` flag | Auto-detect from workspace |
| Database | Detected from existing config or asked | None |

Use `Glob` and `Grep` to detect the workspace context:
- Existing services (look for `docker-compose.yml`, `Dockerfile`, service directories)
- Monorepo structure (look for `turbo.json`, `pnpm-workspace.yaml`, `go.work`)
- Database already in use (look for Prisma schema, Drizzle config, SQLAlchemy models, GORM imports)
- Shared libraries or packages that the new service should import

If stack cannot be auto-detected, ask the user before proceeding.

### Phase 2: Choose Architecture Pattern

Select the architecture based on the service's expected complexity. Ask the user if unclear:

| Complexity Signal | Pattern | When to Use |
|-------------------|---------|-------------|
| Simple CRUD, few entities | **Layered / MVC** | REST APIs with straightforward data access, admin panels, simple services |
| Complex domain rules, multiple bounded contexts | **Clean Architecture / Hexagonal** | Services with rich business logic, multiple integrations, domain invariants |
| Event-driven, audit trail needed | **Event Sourcing + CQRS** | Financial systems, collaboration tools, anything needing full change history |

Reference the `architecture-patterns` skill for detailed pattern guidance. Map the chosen pattern to a directory structure:

**Layered / MVC (Node.js example):**
```
src/
  routes/
  controllers/
  services/
  models/
  middleware/
  config/
```

**Clean Architecture (Node.js example):**
```
src/
  domain/
    entities/
    value-objects/
  application/
    use-cases/
    ports/
  infrastructure/
    repositories/
    external-services/
  interfaces/
    http/
      routes/
      controllers/
      middleware/
  config/
```

**Event Sourcing (Node.js example):**
```
src/
  domain/
    aggregates/
    events/
    commands/
  application/
    command-handlers/
    event-handlers/
    query-handlers/
  infrastructure/
    event-store/
    projections/
    messaging/
  interfaces/
    http/
  config/
```

Adapt directory names to language conventions (`internal/`, `pkg/` for Go; top-level modules for Python).

### Phase 3: Scaffold Directory Structure

Create all directories for the chosen pattern. Use `Bash` with `mkdir -p` to create the full tree in one call.

### Phase 4: Generate Boilerplate Files

Generate the following files, adapting to the chosen stack and framework:

#### Entry Point
- **Node.js:** `src/index.ts` or `src/main.ts` with Express/Fastify/Hono setup
- **Python:** `main.py` or `app/__init__.py` with Flask/FastAPI setup
- **Go:** `cmd/server/main.go` with `net/http` or Gin/Echo setup

Must include:
- Graceful shutdown handling (listen for `SIGINT`, `SIGTERM`)
- Server configuration from environment variables
- Startup logging with service name, port, and environment

#### Health Check Endpoint
- `GET /health` returning `{ "status": "ok", "service": "<name>", "version": "<version>" }`
- `GET /ready` returning `{ "ready": true }` (checks database connection, external dependencies)

#### Error Handler Middleware
- Centralized error handler that catches all unhandled errors
- Structured JSON error responses: `{ "error": { "code": "...", "message": "..." } }`
- No stack traces or internal details in production responses
- Logs full error details server-side

#### Logger Setup
- Structured JSON logging (pino for Node.js, structlog for Python, zerolog/zap for Go)
- Request ID propagation via middleware
- Log levels configurable via environment variable (`LOG_LEVEL`)
- Request/response logging middleware with duration

#### Database Connection (if applicable)
- Connection pooling with configurable pool size
- Connection retry logic with backoff
- Graceful disconnect on shutdown
- Health check integration

#### Environment Config
- `.env.example` with all required variables documented
- Config loader that validates required variables at startup and fails fast
- Typed config object or struct

### Phase 5: Add Containerization

Generate a multi-stage `Dockerfile`:
- Build stage with only build dependencies
- Production stage with minimal base image
- Non-root user
- Health check instruction
- `.dockerignore` file

Generate `docker-compose.yml`:
- Service definition with port mapping
- Database service if applicable (Postgres, Redis, etc.)
- Volume mounts for local development
- Environment file reference

### Phase 6: Add Development Tooling

Generate a `Makefile` (or `Taskfile.yml` if the project already uses Task) with targets:

| Target | Command | Description |
|--------|---------|-------------|
| `dev` | Start with hot reload | `nodemon`, `air`, `uvicorn --reload` |
| `build` | Compile / bundle | `tsc`, `go build`, `pip install` |
| `test` | Run test suite | `jest`, `pytest`, `go test` |
| `lint` | Run linter | `eslint`, `ruff`, `golangci-lint` |
| `format` | Auto-format code | `prettier`, `black`, `gofmt` |
| `docker-up` | Start containers | `docker compose up -d` |
| `docker-down` | Stop containers | `docker compose down` |
| `migrate` | Run database migrations | Framework-specific |

### Phase 7: Report

Print a summary listing:

```
Created Files
=============

  src/index.ts                 (entry point with graceful shutdown)
  src/routes/health.ts         (health check endpoints)
  src/middleware/error.ts       (error handler)
  src/middleware/logger.ts      (request logging)
  src/middleware/request-id.ts  (request ID propagation)
  src/config/env.ts            (environment config)
  src/config/database.ts       (database connection)
  Dockerfile                   (multi-stage build)
  docker-compose.yml           (local development)
  .dockerignore                (Docker ignore rules)
  .env.example                 (environment template)
  Makefile                     (dev tooling)

Next Steps
==========

  1. Copy .env.example to .env and fill in values
  2. Run: make docker-up   (start database)
  3. Run: make dev          (start service with hot reload)
  4. Visit: http://localhost:3000/health
  5. Add your first route: /create-api-route /your-resource --method POST
```

## NEVER Do

| Rule | Reason |
|------|--------|
| Never hardcode secrets or credentials | All sensitive values must come from environment variables |
| Never skip graceful shutdown | Abrupt termination causes connection leaks and data corruption |
| Never use `latest` tags in Dockerfile | Non-reproducible builds; always pin base image versions |
| Never run containers as root | Security risk; always create and use a non-root user |
| Never skip health checks | Orchestrators need health endpoints to manage the service lifecycle |
| Never log sensitive data | PII, tokens, and passwords must never appear in logs |
| Never ignore existing workspace conventions | Match the project's existing structure, naming, and tooling |

## Error Handling

| Situation | Action |
|-----------|--------|
| Stack not detected and not specified | Ask the user which stack to use |
| Service name conflicts with existing directory | Warn and ask whether to overwrite or choose a different name |
| Database type unclear | Ask the user; suggest Postgres as default for relational needs |
| Monorepo detected but structure unclear | Ask where to place the new service directory |
| Unsupported type + stack combination | Warn the user and suggest the closest supported alternative |

## Output

- **Complete service directory** with architecture-appropriate structure
- **Boilerplate files** for entry point, health checks, error handling, logging, and config
- **Dockerfile and docker-compose.yml** for containerized development
- **Makefile** with standard development targets
- **Environment template** documenting all required configuration

## Related

- **Architecture:** `architecture-patterns` skill (for Clean Architecture, Hexagonal, Event Sourcing guidance)
- **Node.js patterns:** `nodejs-backend-patterns` skill (for Express/Fastify conventions)
- **Logging:** `logging-observability` skill (for structured logging and tracing setup)
- **Docker:** `docker-expert` skill (for Dockerfile optimization and container security)
- **API routes:** `/create-api-route` (to add endpoints after scaffolding)
- **Feature workflow:** `/new-feature` (when the service is part of a larger feature)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
