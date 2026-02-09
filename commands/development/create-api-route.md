---
name: create-api-route
model: standard
description: Scaffold an API endpoint with validation, error handling, and tests
usage: /create-api-route <endpoint> [--method GET|POST|PUT|DELETE|PATCH] [--auth] [--paginated]
---

# /create-api-route

Scaffold a production-ready API endpoint with input validation, structured error handling, and a companion test file.

## Usage

```
/create-api-route <endpoint> [--method GET|POST|PUT|DELETE|PATCH] [--auth] [--paginated]
```

**Arguments:**
- `endpoint` — Route path such as `/users/:id` or `users` (leading slash optional)
- `--method` — HTTP method to handle (default: `POST`). Accepts `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- `--auth` — Include authentication middleware and guard logic
- `--paginated` — Add cursor or offset pagination (applies only to list endpoints returning arrays)

## Examples

```
/create-api-route /users --method GET --paginated
/create-api-route /users/:id --method PUT --auth
/create-api-route /orders --method POST --auth
/create-api-route /products/:id --method DELETE --auth
/create-api-route /search --method GET --paginated
```

## When to Use

- Adding a new REST endpoint to an existing API service
- Replacing a placeholder or stub route with a production implementation
- Standardizing route structure across a codebase that has inconsistent patterns
- Bootstrapping CRUD operations for a new resource
- Generating the boilerplate so you can focus on business logic

## What It Does

1. **Parses** the endpoint path and flags into structured parameters
2. **Detects** the backend framework and validation library in use
3. **Scaffolds** the route handler with the correct framework conventions
4. **Adds** request validation using the project's existing validation library
5. **Adds** structured error handling with proper HTTP status codes
6. **Generates** a test file covering the happy path and common failure cases
7. **Reports** all created and modified files

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Input

Extract structured parameters from the command arguments:

| Parameter | Source | Default |
|-----------|--------|---------|
| Resource name | Last non-parameter segment of the endpoint (e.g., `users`) | Required |
| Route path | Full endpoint string, normalized with leading `/` | Required |
| Path parameters | Segments prefixed with `:` (e.g., `:id`) | None |
| HTTP method | `--method` flag | `POST` |
| Auth required | Presence of `--auth` flag | `false` |
| Paginated | Presence of `--paginated` flag | `false` |

Validate that `--paginated` is only used with `GET` method. Warn and ignore if combined with `POST`, `PUT`, `DELETE`, or `PATCH`.

### Phase 2: Detect Framework

Use `Glob` and `Grep` to identify the backend framework. Check files in order and stop at the first match:

| Framework | Detection Signal |
|-----------|-----------------|
| **Express** | `app.ts`, `server.ts`, or `app.js` importing `express` |
| **Fastify** | File importing `fastify` or containing `Fastify` instance |
| **Next.js** | `app/api/` directory or `pages/api/` directory |
| **Hono** | File importing `hono` or `Hono` constructor |
| **Flask** | `app.py` importing `flask` or `Flask(__name__)` |
| **Django** | `urls.py` with `urlpatterns` and `views.py` present |
| **Go net/http** | `main.go` importing `"net/http"` |
| **Rust Actix** | `main.rs` or `lib.rs` importing `actix_web` |

If no framework is detected, ask the user which framework to target before proceeding.

Also detect the existing project structure conventions by scanning for patterns:
- Route file location (e.g., `src/routes/`, `app/api/`, `internal/handler/`)
- Controller vs handler pattern
- Middleware directory location
- Test file location and naming convention (`*.test.ts`, `*_test.go`, `test_*.py`)

### Phase 3: Scaffold Route Handler

Create the route handler file following the detected framework conventions.

Use `Glob` to find existing route files and `Read` one as a reference for style, imports, and structure. The generated handler must include:

1. **Imports** matching the project's existing import style
2. **Route registration** using the framework's idiom (`app.get()`, `router.HandleFunc()`, `@app.route()`, etc.)
3. **Request parsing** for path params, query params, and body (method-dependent)
4. **Auth middleware** attachment if `--auth` was specified
5. **Pagination parameters** (`limit`, `offset` or `cursor`) if `--paginated` was specified
6. **A placeholder comment** for business logic: `// TODO: Implement business logic`
7. **Response formatting** consistent with existing endpoints

Use `Edit` to write the handler file. If the project uses a route index or registration file, use `Read` then `Edit` to add the new route import and registration.

### Phase 4: Add Validation

Detect the validation library in use and generate a schema for the endpoint:

| Library | Detection | File Pattern |
|---------|-----------|-------------|
| **Zod** | `zod` in `package.json` or existing `.ts` imports | `src/schemas/<resource>.schema.ts` |
| **Joi** | `joi` in `package.json` or existing imports | `src/schemas/<resource>.schema.ts` |
| **Pydantic** | `pydantic` in `requirements.txt` or existing imports | `schemas/<resource>.py` |
| **validator** (Go) | `go-playground/validator` in `go.mod` | `internal/dto/<resource>.go` with struct tags |

Generate validation rules based on the endpoint:

- **Path parameters** — required, type-checked (e.g., UUID, integer)
- **Query parameters** — optional with defaults for pagination (`limit` default 20, max 100)
- **Request body** (POST/PUT/PATCH) — required fields with types, optional fields marked explicitly
- **Response shape** — typed response object or struct

Use `Grep` to find existing validation schemas and follow the same structure. Write the schema file with `Edit`.

### Phase 5: Add Error Handling

Add structured error responses following the project's existing error patterns. Use this HTTP status code reference:

| Status Code | Meaning | When to Use |
|-------------|---------|-------------|
| `200 OK` | Success | GET, PUT, PATCH returning data |
| `201 Created` | Resource created | POST that creates a new resource |
| `204 No Content` | Success, no body | DELETE, or PUT/PATCH with no return body |
| `400 Bad Request` | Malformed input | Validation failure, missing required fields |
| `401 Unauthorized` | Not authenticated | Missing or invalid auth token |
| `403 Forbidden` | Not authorized | Valid auth but insufficient permissions |
| `404 Not Found` | Resource missing | ID lookup returned no result |
| `409 Conflict` | State conflict | Duplicate creation, concurrent edit conflict |
| `422 Unprocessable Entity` | Semantic error | Valid syntax but business rule violation |
| `500 Internal Server Error` | Server fault | Unhandled exception, database failure |

Use `Grep` to find existing error handling patterns (search for `catch`, `error`, `HttpException`, `HTTPException`, `AppError`, etc.) and follow the same pattern. If the project has a custom error class, reuse it.

### Phase 6: Generate Tests

Create a test file alongside the handler using the project's test framework.

Use `Glob` to find existing test files and `Read` one to match the test style. Generate tests for:

1. **Happy path** — valid request returns expected status and body
2. **Validation failure** — missing required field returns 400 or 422
3. **Not found** — request for nonexistent resource returns 404 (for endpoints with path params)
4. **Auth failure** — request without token returns 401 (if `--auth`)
5. **Auth forbidden** — request with insufficient permissions returns 403 (if `--auth`)
6. **Pagination** — verify limit/offset or cursor behavior (if `--paginated`)
7. **Duplicate/conflict** — creation with existing unique key returns 409 (for POST)

Write the test file with `Edit`. Use `Bash` to run the test suite once and confirm the new tests are discovered (not necessarily passing, since business logic is a placeholder).

### Phase 7: Report

Print a summary listing:

```
Created/Modified Files
======================

  Created:  src/routes/users.ts          (route handler)
  Created:  src/schemas/users.schema.ts  (validation schema)
  Created:  src/routes/__tests__/users.test.ts (test file)
  Modified: src/routes/index.ts          (route registration)

Next Steps
==========

  1. Implement business logic in the handler (replace TODO comment)
  2. Run tests: npm test -- --grep "users"
  3. Add database queries or service calls
  4. Review generated validation schema for domain-specific rules
```

## NEVER Do

| Rule | Reason |
|------|--------|
| Never invent a framework convention | Always match existing project patterns discovered during detection |
| Never skip validation | Every endpoint must validate input, even simple GET requests with path params |
| Never return stack traces in error responses | Leak internal details to clients; log them server-side instead |
| Never hardcode authentication secrets or keys | Auth middleware must read from environment variables or config |
| Never create a route without a test file | Untested endpoints are a liability; always generate the companion test |
| Never ignore existing error handling patterns | Inconsistent error formats break API clients; reuse the project's error structure |
| Never register a route that shadows an existing one | Use `Grep` to verify no route conflict before writing the registration |

## Error Handling

| Situation | Action |
|-----------|--------|
| Framework not detected | Ask the user to specify the framework before proceeding |
| Validation library not found | Default to inline validation and suggest installing Zod, Joi, or Pydantic |
| Route path already exists | Warn the user and ask whether to overwrite or create alongside |
| Test framework not detected | Skip test generation and warn the user to add tests manually |
| Auth middleware not found in project | Generate a placeholder middleware file and note it needs implementation |
| Route registration file not found | Create the handler as a standalone file and instruct the user to register it |

## Output

- **Route handler file** placed in the project's existing route directory
- **Validation schema file** placed in the project's existing schema directory
- **Test file** placed alongside the handler or in the project's test directory
- **Updated route registration** in the framework's routing entry point

## Related

- **API design:** `api-design-principles` skill (for RESTful conventions and naming)
- **Feature workflow:** `/new-feature` (when the endpoint is part of a larger feature)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
