# Backend

Backend architecture patterns and infrastructure skills. Covers API design principles, architecture decision records, Clean/Hexagonal/DDD patterns, event sourcing, Go concurrency, microservices decomposition, monorepo management, Node.js backend patterns, PostgreSQL job queues, service layer architecture, and Postgres performance optimization.

## Skills

| Skill | Description |
|-------|-------------|
| [api-design-principles](api-design-principles/) | Design intuitive, scalable REST and GraphQL APIs — resource modeling, HTTP semantics, pagination, and versioning |
| [architecture-decision-records](architecture-decision-records/) | Lightweight documentation capturing context, decisions, and consequences of significant technical choices |
| [architecture-patterns](architecture-patterns/) | Clean Architecture, Hexagonal Architecture, and Domain-Driven Design for maintainable, testable systems |
| [event-store](event-store/) | Event store design for event-sourced systems — event schemas, projections, snapshotting, and CQRS integration |
| [go-concurrency](go-concurrency/) | Production Go concurrency patterns — goroutines, channels, sync primitives, context, worker pools, and pipelines |
| [microservices-patterns](microservices-patterns/) | Distributed system patterns — service decomposition, inter-service communication, data management, and resilience |
| [monorepo](monorepo/) | Monorepo management with Turborepo, Nx, and pnpm workspaces — task orchestration, caching, and CI/CD |
| [nodejs-patterns](nodejs-patterns/) | Production Node.js backend patterns — Express/Fastify, layered architecture, middleware, validation, and database integration |
| [postgres-job-queue](postgres-job-queue/) | PostgreSQL-based job queue with priority scheduling, batch claiming, and progress tracking using SKIP LOCKED |
| [service-layer-architecture](service-layer-architecture/) | Controller-service-query layered API architecture with data enrichment and parallel fetching |
| [supabase-postgres](supabase-postgres/) | Postgres performance optimization — indexing, connection management, RLS security, schema design, and monitoring |

## Installation

```bash
# Add all backend skills
skills add api-design-principles
skills add architecture-decision-records
skills add architecture-patterns
skills add event-store
skills add go-concurrency
skills add microservices-patterns
skills add monorepo
skills add nodejs-patterns
skills add postgres-job-queue
skills add service-layer-architecture
skills add supabase-postgres

# Or add individual skills
skills add architecture-patterns
skills add nodejs-patterns
```

## See Also

- [All Skills](../) — Complete skills catalog
- [Agents](../../agents/) — Workflow agents
