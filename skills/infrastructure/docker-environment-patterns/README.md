# Docker Environment Patterns

Docker containerization expertise — multi-stage builds, image optimization, security hardening, Docker Compose orchestration, and production deployment patterns. Covers everything from writing your first Dockerfile to optimizing production images for size, security, and performance.

## What's Inside

- Multi-stage build patterns for minimal production images
- Image optimization (layer caching, .dockerignore, cache cleaning)
- Security hardening (non-root users, read-only filesystems, secret management)
- Docker Compose orchestration with health checks and dependency ordering
- Framework-specific patterns (Node.js, Python, Go, Rust, Java)
- Troubleshooting guide for common container issues
- Production review checklist

## When to Use

- Creating or optimizing Dockerfiles for any application
- Debugging container startup failures, image size problems, or networking issues
- Setting up Docker Compose for local development or production
- Hardening container security (non-root, secrets, health checks)
- Building CI/CD pipelines with Docker

## Installation

```bash
skills add docker-environment-patterns
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/docker-environment-patterns .cursor/skills/docker-environment-patterns
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/docker-environment-patterns ~/.cursor/skills/docker-environment-patterns
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/infrastructure/docker-environment-patterns .claude/skills/docker-environment-patterns
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/infrastructure/docker-environment-patterns ~/.claude/skills/docker-environment-patterns
```

---

Part of the [Infrastructure](..) skill category.
