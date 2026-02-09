# API

Comprehensive API design and development patterns. Covers REST and GraphQL design principles, full API lifecycle orchestration, versioning strategies, authentication and authorization, caching layers, database migrations, error handling, and rate limiting — everything needed to build robust, production-grade APIs.

## Skills

| Skill | Description |
|-------|-------------|
| [api-design](api-design/) | REST and GraphQL API design principles — resource modeling, HTTP semantics, pagination, error handling, and schema design |
| [api-development](api-development/) | Meta-skill orchestrating the full API development lifecycle — from design through documentation |
| [api-versioning](api-versioning/) | API versioning strategies — URL path, header, query param, content negotiation — with deprecation timelines and migration patterns |
| [auth-patterns](auth-patterns/) | Authentication and authorization patterns — JWT, OAuth 2.0, sessions, RBAC/ABAC, password security, and MFA |
| [caching](caching/) | Caching strategies, invalidation, eviction policies, HTTP caching, distributed caching, and anti-patterns |
| [database-migrations](database-migrations/) | Safe, zero-downtime database migration strategies — schema evolution, rollback planning, and data migration |
| [error-handling](error-handling/) | Error handling across languages and layers — retry strategies, circuit breakers, error boundaries, and graceful degradation |
| [rate-limiting](rate-limiting/) | Rate limiting algorithms, implementation strategies, HTTP conventions, tiered limits, and distributed patterns |

## Installation

```bash
# Add all API skills
npx skills add api-design
npx skills add api-development
npx skills add api-versioning
npx skills add auth-patterns
npx skills add caching
npx skills add database-migrations
npx skills add error-handling
npx skills add rate-limiting

# Or add individual skills
npx skills add api-design
npx skills add auth-patterns
```

## See Also

- [All Skills](../) — Complete skills catalog
- [Agents](../../agents/) — Workflow agents
