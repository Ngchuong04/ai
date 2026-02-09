# API Design Principles

REST and GraphQL API design principles — resource modeling, HTTP semantics, pagination, error handling, HATEOAS, schema design, and DataLoader patterns. Use when designing new APIs, reviewing specs, or establishing team API standards.

## What's Inside

- REST Design Principles — resource-oriented architecture, collection design, HTTP methods
- Pagination — offset-based and cursor-based strategies
- Filtering, Sorting, and Search patterns
- Error Response Format and Status Code Usage
- HATEOAS and Idempotency patterns
- GraphQL Design Principles — schema-first development, mutations, union error pattern
- DataLoader N+1 Prevention
- Schema Evolution with `@deprecated`
- REST vs GraphQL vs gRPC comparison
- Best Practices and Anti-Patterns

## When to Use

- Designing new REST or GraphQL APIs
- Refactoring existing APIs for better usability
- Establishing API design standards for a team
- Reviewing API specifications before implementation
- Migrating between API paradigms (REST ↔ GraphQL)
- Optimizing APIs for specific consumers (mobile, third-party)

## Installation

```bash
npx skills add api-design
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/api/api-design .cursor/skills/api-design
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/api/api-design ~/.cursor/skills/api-design
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/api/api-design .claude/skills/api-design
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/api/api-design ~/.claude/skills/api-design
```

## Related Skills

- `api-versioning` — Version lifecycle, deprecation, migration patterns
- `auth-patterns` — JWT, OAuth2, sessions, RBAC, MFA
- `error-handling` — Error types, retry patterns, circuit breakers, HTTP errors
- `rate-limiting` — Algorithms, HTTP headers, tiered limits, distributed limiting
- `caching` — Cache strategies, HTTP caching, invalidation, Redis patterns

---

Part of the [API](..) skill category.
