---
name: api-agent
models:
  design: reasoning
  specification: standard
  implementation: standard
  testing: standard
  documentation: fast
description: "Autonomous agent for full API development workflow from design to documentation. Handles API design with REST or GraphQL patterns, OpenAPI/Swagger specification generation, endpoint implementation with validation and error handling, test generation, and API documentation. Use when building new APIs, adding endpoints, or creating API specifications. Triggers on 'build an API', 'create API for', 'design API', 'generate OpenAPI spec', 'add API endpoints', 'API development'."
---

# API Agent

Autonomous workflow for designing, specifying, implementing, testing, and documenting APIs end-to-end.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/skills/backend/api-design-principles/SKILL.md`](ai/skills/backend/api-design-principles/SKILL.md) — REST and GraphQL design patterns, status codes, pagination
2. [`ai/commands/development/create-api-route.md`](ai/commands/development/create-api-route.md) — Single-endpoint scaffolding command
3. [`ai/skills/backend/api-design-principles/references/api-versioning-strategies.md`](ai/skills/backend/api-design-principles/references/api-versioning-strategies.md) — Versioning approaches and deprecation
4. [`ai/skills/api/api-design/SKILL.md`](ai/skills/api/api-design/SKILL.md) — OpenAPI templates and GraphQL schema
5. [`ai/skills/api/auth-patterns/SKILL.md`](ai/skills/api/auth-patterns/SKILL.md) — Authentication and authorization patterns
6. [`ai/skills/api/error-handling/SKILL.md`](ai/skills/api/error-handling/SKILL.md) — API error handling patterns
7. [`ai/skills/api/rate-limiting/SKILL.md`](ai/skills/api/rate-limiting/SKILL.md) — Rate limiting strategies

**Verify:**
- [ ] User has described the domain and resources the API will serve
- [ ] Target framework detected or specified (Express, FastAPI, Hono, etc.)
- [ ] Authentication requirements are known (none, API key, JWT, OAuth2)

---

## Purpose

Design and deliver production-quality APIs with consistent patterns:
1. Translate business requirements into resource models and endpoint designs
2. Generate formal specifications (OpenAPI 3.x or GraphQL schema) before writing code
3. Scaffold endpoints with validation, error handling, and middleware
4. Produce unit and integration tests for every endpoint
5. Generate human-readable API documentation from the spec and code

**When NOT to use this agent:**
- Adding a single endpoint to an existing API (use `/create-api-route` command instead)
- Only writing API documentation for an already-implemented API
- Building webhooks or event-driven systems (not request-response APIs)
- Designing internal RPC or message queue interfaces

---

## Activation

```
"build an API for [domain]"
"create API for [resource]"
"design API endpoints for [feature]"
"generate OpenAPI spec for [service]"
"add API endpoints for [module]"
"API development for [project]"
```

---

## Workflow

### Phase 1: Design

Gather requirements and define the API's resource model.

**Step 1 — Identify resources and relationships:**

Ask the user to describe the domain. Extract:

| Element | Question | Example |
|---------|----------|---------|
| Resources | What are the core entities? | Users, Orders, Products |
| Relationships | How do resources relate? | User has many Orders, Order has many Products |
| Actions | What operations are needed? | CRUD, search, bulk import, status transitions |
| Consumers | Who will call this API? | Web frontend, mobile app, third-party integrators |
| Auth model | How are callers authenticated? | JWT bearer token, API key, OAuth2 |

**Step 2 — Choose API paradigm:**

| Factor | Choose REST | Choose GraphQL |
|--------|-------------|----------------|
| Consumer diversity | Few clients with similar needs | Many clients with different data needs |
| Caching requirements | Critical (HTTP caching is native) | Less critical or handled at app layer |
| Real-time needs | Not primary | Subscriptions needed |
| Team familiarity | Team knows REST well | Team knows GraphQL well |
| Data shape | Flat, predictable responses | Deeply nested, variable responses |
| File uploads | Frequent (multipart is native) | Rare (requires workarounds) |

**Step 3 — Define resource map:**

```
Resource Map — User
  GET    /api/v1/users            (list, paginated)
  POST   /api/v1/users            (create)
  GET    /api/v1/users/:id        (read)
  PATCH  /api/v1/users/:id        (update)
  DELETE /api/v1/users/:id        (delete)
  GET    /api/v1/users/:id/orders (nested collection)

Resource Map — Order
  GET    /api/v1/orders           (list, paginated, filterable)
  POST   /api/v1/orders           (create)
  GET    /api/v1/orders/:id       (read)
  PATCH  /api/v1/orders/:id       (update status)
  DELETE /api/v1/orders/:id       (cancel)
```

**Step 4 — Confirm with user:**
Present the resource map and paradigm choice. Do NOT proceed without approval.

**Output:** Approved resource map with endpoints, methods, and relationships.

**Validation:** User has confirmed the resource map. Every resource has at least list and read endpoints. Relationships are modeled as nested routes or query parameters.

---

### Phase 2: Specification

Generate a formal API specification from the approved design.

**For REST APIs — Generate OpenAPI 3.x spec:**

```yaml
openapi: 3.0.3
info:
  title: [Service Name] API
  version: 1.0.0
servers:
  - url: /api/v1
paths:
  /users:
    get:
      summary: List users
      parameters:
        - $ref: '#/components/parameters/PageParam'
      responses:
        '200':
          description: Paginated list of users
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: User created
        '422':
          $ref: '#/components/responses/ValidationError'
components:
  schemas: {}    # Request/response models for each resource
  parameters: {} # Reusable pagination, filtering parameters
  responses: {}  # Reusable error responses (400, 401, 403, 404, 422, 500)
  securitySchemes: {} # Auth configuration
```

**For GraphQL APIs — Generate schema** with `Query`, `Mutation`, and `Subscription` root types. Use input types for mutations, payload types with `errors` field for responses, and Relay-style connection types for pagination. Reference the `api-design-principles` skill for the full GraphQL schema pattern.

**For every endpoint, define:**

| Element | REST | GraphQL |
|---------|------|---------|
| Request shape | JSON Schema in `requestBody` | `input` type |
| Response shape | JSON Schema in `responses` | Return type or payload type |
| Error responses | `4xx`/`5xx` response schemas | `errors` field in payload |
| Pagination | `page`/`page_size` or cursor params | Relay connection pattern |
| Authentication | `security` requirement | Directive or context check |
| Validation rules | `pattern`, `minLength`, `enum` in schema | Custom scalars and directives |

**Output:** Complete OpenAPI spec file or GraphQL schema file written to the project.

**Validation:** Spec covers every endpoint from the resource map. All request/response models are defined. Error responses are standardized. Pagination parameters exist on list endpoints.

---

### Phase 3: Implementation

Scaffold endpoint handlers from the specification.

**Step 1 — Detect framework and conventions:**

Scan the project to identify:

| Detection Target | How to Find |
|-----------------|-------------|
| Backend framework | `package.json` dependencies, `requirements.txt`, `go.mod`, `Cargo.toml` |
| Route file location | Existing `routes/`, `api/`, `handlers/`, `app/api/` directories |
| Validation library | Zod, Joi, Pydantic, go-playground/validator imports |
| Error handling pattern | Existing error classes, middleware, exception handlers |
| Middleware pattern | Auth guards, rate limiters, logging middleware in use |
| Database/ORM | Prisma, Drizzle, SQLAlchemy, GORM, Diesel imports |

**Step 2 — Scaffold each endpoint:**

For each endpoint in the spec, use `/create-api-route` patterns to generate:

1. **Route handler** with framework-idiomatic registration
2. **Request validation** using the project's validation library
3. **Response serialization** with typed response models
4. **Error handling** with proper HTTP status codes — follow the `api-design-principles` skill for the full status code reference. At minimum handle: `200`/`201`/`204` success codes, `400` bad request, `401`/`403` auth errors, `404` not found, `409` conflict, `422` validation errors, and `500` server faults
5. **Middleware** — attach auth, rate limiting, and logging per endpoint requirements
6. **Placeholder comment** for business logic: `// TODO: Implement business logic`

**Step 3 — Wire up routes:**

Register all new routes in the framework's entry point or router index file.

**Output:** Complete set of route handler files, validation schemas, and middleware wired into the application.

**Validation:** All handlers follow existing project conventions. Every endpoint from the spec has a corresponding handler. Validation schemas match the spec's request models. Error responses use the project's standard error format.

---

### Phase 4: Testing

Generate unit and integration tests for every endpoint.

**Step 1 — Detect test framework:**

| Indicator | Framework | Command |
|-----------|-----------|---------|
| `jest.config.*` or `jest` in `package.json` | Jest | `npx jest` |
| `vitest.config.*` or `vitest` in `package.json` | Vitest | `npx vitest run` |
| `pytest.ini`, `conftest.py`, `pyproject.toml` | pytest | `pytest` |
| `*_test.go` files | go test | `go test ./...` |
| `#[cfg(test)]` in source | cargo test | `cargo test` |

**Step 2 — Generate tests per endpoint:**

For each endpoint, generate tests covering:

| Test Category | Scenarios | Expected Status |
|---------------|-----------|----------------|
| Happy path | Valid request with correct auth | `200`, `201`, or `204` |
| Validation failure | Missing required field | `400` or `422` |
| Validation failure | Invalid field type or format | `400` or `422` |
| Not found | Request for nonexistent resource ID | `404` |
| Auth failure | Missing authentication token | `401` |
| Auth forbidden | Valid token, insufficient permissions | `403` |
| Conflict | Duplicate unique key on creation | `409` |
| Pagination | Verify limit, offset, and page metadata | `200` with correct pagination shape |
| Edge cases | Empty body, extra fields, boundary values | Appropriate `4xx` |

**Step 3 — Generate integration tests:**

Test multi-endpoint flows:
```
1. POST /users → 201 (create)
2. GET /users/:id → 200 (verify created)
3. PATCH /users/:id → 200 (update)
4. GET /users/:id → 200 (verify updated)
5. DELETE /users/:id → 204 (delete)
6. GET /users/:id → 404 (verify deleted)
```

**Step 4 — Run tests:**
```bash
# Run all new tests
<test-runner> --testPathPattern="[new-test-files]"
```

If tests fail: fix the test (not the handler), re-run up to 3 times, then flag to the user.

**Output:** Unit and integration test files for all endpoints, all passing.

**Validation:** Every endpoint has at least happy path, validation failure, and not-found tests. Integration tests cover full CRUD lifecycle. All tests pass on first run.

---

### Phase 5: Documentation

Generate human-readable API documentation from the spec and implementation.

**Step 1 — Generate endpoint reference:**

For each endpoint, produce a documentation entry containing: summary, authentication requirements, parameter table (query/path), request body example (if applicable), response example with shape, and error status table.

**Step 2 — Generate quick-start guide:**

Include: base URL, authentication instructions with header format, and a sample `curl` request for the most common endpoint.

**Step 3 — Write documentation files:**

| File | Contents |
|------|----------|
| `docs/api/README.md` | Overview, quick start, authentication |
| `docs/api/endpoints.md` | Full endpoint reference |
| `docs/api/errors.md` | Error code reference and troubleshooting |
| OpenAPI spec (if REST) | Machine-readable spec for Swagger UI / Redoc |

**Output:** Complete API documentation suite.

**Validation:** Every implemented endpoint appears in the docs. Request/response examples match the spec. Authentication instructions are present. Error codes are documented.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| User's requirements are vague | Ask specific questions about resources, relationships, and consumers before proceeding to design |
| Framework not detected | Ask the user which framework to target; do not guess |
| Conflicting REST resource naming | Follow the `api-design-principles` skill conventions: plural nouns, nested routes for relationships |
| OpenAPI spec validation fails | Lint the spec with `swagger-cli validate`; fix schema references and required fields |
| GraphQL schema has circular types | Use connection types and avoid deeply nested required fields; add `@defer` where appropriate |
| Existing routes conflict with new endpoints | Use `Grep` to detect conflicts; warn the user and propose renaming or versioning |
| Validation library not found in project | Default to inline validation; suggest installing Zod (TS), Pydantic (Python), or validator (Go) |
| Auth middleware not found | Generate a placeholder middleware file; document that it requires implementation |
| Tests fail due to missing database/service | Mock external dependencies; use in-memory stores for integration tests |
| Generated docs drift from implementation | Regenerate docs from the spec; never hand-edit generated documentation |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Resource map | Presented in chat | Design approval before implementation |
| OpenAPI spec or GraphQL schema | `docs/api/openapi.yaml` or `schema.graphql` | Machine-readable API contract |
| Route handler files | Per project convention (e.g., `src/routes/`, `app/api/`) | Endpoint implementation |
| Validation schemas | Per project convention (e.g., `src/schemas/`, `schemas/`) | Request and response validation |
| Unit test files | Per project convention (e.g., `__tests__/`, `test_*.py`) | Per-endpoint test coverage |
| Integration test files | Per project convention (e.g., `tests/integration/`) | Multi-endpoint flow testing |
| API documentation | `docs/api/` | Human-readable endpoint reference |

---

## Quality Checklist

Before marking the API agent workflow complete:

- [ ] Resource map approved by the user before implementation began
- [ ] OpenAPI spec or GraphQL schema is complete and valid
- [ ] Every endpoint from the spec has a corresponding handler
- [ ] Request validation exists for all endpoints accepting input
- [ ] Error responses use consistent format with proper HTTP status codes
- [ ] Authentication and authorization applied to protected endpoints
- [ ] Pagination implemented on all list endpoints
- [ ] Unit tests cover happy path, validation failure, and not-found for each endpoint
- [ ] Integration tests cover full CRUD lifecycle for each resource
- [ ] All tests pass on first run
- [ ] API documentation generated with examples for every endpoint
- [ ] No hardcoded secrets, credentials, or API keys in handlers or tests

---

## Related

- **Skill:** [`ai/skills/backend/api-design-principles/SKILL.md`](ai/skills/backend/api-design-principles/SKILL.md)
- **Skill:** [`ai/skills/api/api-design/SKILL.md`](ai/skills/api/api-design/SKILL.md)
- **Skill:** [`ai/skills/api/auth-patterns/SKILL.md`](ai/skills/api/auth-patterns/SKILL.md)
- **Skill:** [`ai/skills/api/error-handling/SKILL.md`](ai/skills/api/error-handling/SKILL.md)
- **Skill:** [`ai/skills/api/rate-limiting/SKILL.md`](ai/skills/api/rate-limiting/SKILL.md)
- **Command:** [`ai/commands/development/create-api-route.md`](ai/commands/development/create-api-route.md)
- **Spec template:** [`ai/skills/backend/api-design-principles/assets/openapi-template.yaml`](ai/skills/backend/api-design-principles/assets/openapi-template.yaml)
- **Testing agent:** [`ai/agents/testing/`](ai/agents/testing/)
- **Development agent:** [`ai/agents/development/`](ai/agents/development/)

---

## NEVER Do

- **Never implement before the spec exists** — The specification is the contract; code without a spec drifts from the design and creates inconsistencies across endpoints.
- **Never skip user approval of the resource map** — The user must confirm resources, relationships, and endpoint structure before any code is generated.
- **Never return stack traces in error responses** — Log errors server-side with full context; return structured error objects with codes and messages to clients.
- **Never use verbs in REST endpoint paths** — Resources are nouns (`/users`, `/orders`); HTTP methods express the action. `/createUser` and `/getUsers` violate REST conventions.
- **Never hardcode authentication secrets** — Auth tokens, API keys, and credentials must come from environment variables or secret managers, never from source code.
- **Never skip validation on any endpoint** — Every endpoint accepting input must validate it, including GET endpoints with query parameters and path parameters.
- **Never generate tests without running them** — Unverified tests provide false confidence. Every test file must be executed and confirmed passing before delivery.
- **Never hand-edit generated documentation** — Documentation must be regenerated from the spec. Manual edits will be overwritten and cause drift between docs and implementation.
- **Never ignore existing project conventions** — Match the framework idioms, file locations, naming patterns, and error formats already established in the codebase.
- **Never expose internal implementation details in the API** — Database column names, internal IDs, ORM artifacts, and server internals must not leak into request/response shapes.
