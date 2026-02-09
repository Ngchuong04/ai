# Docker

Container optimization, security hardening, multi-stage builds, and production deployment patterns for Docker and Docker Compose.

## What's Inside

- Multi-stage build patterns (deps → build → production)
- Security-hardened containers (non-root users, capability drops, read-only filesystem)
- Production Docker Compose with health checks, secrets, resource limits, and network isolation
- Comprehensive `.dockerignore` template
- Build cache optimization with BuildKit mount caches
- Build-time secrets (never stored in image layers)
- Multi-architecture builds with buildx
- Framework-specific Dockerfiles (Next.js, Python FastAPI, Go distroless)
- Troubleshooting guide (image size, build performance, debugging)
- Review checklist for Dockerfile, security, and Compose

## When to Use

- Optimizing Dockerfiles for image size and build speed
- Debugging container issues
- Security hardening containers for production
- Setting up Docker Compose for development and production
- Configuring networking, health checks, and secrets

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/devops/docker
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/devops/docker .cursor/skills/docker
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/devops/docker ~/.cursor/skills/docker
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/devops/docker .claude/skills/docker
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/devops/docker ~/.claude/skills/docker
```

## Related Skills

- [kubernetes](../kubernetes/) — Kubernetes manifest generation and deployment
- [prometheus](../prometheus/) — Monitoring and alerting for containerized services

---

Part of the [DevOps](..) skill category.
