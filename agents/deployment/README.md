# Deployment Agent

Autonomous workflow for configuring CI/CD pipelines, containerizing applications, and automating deployments with environment management, secret handling, and health check verification.

## Workflow Phases

- **Phase 1: Assessment** — Detect CI/CD platform, cloud provider, deployment target, container registry
- **Phase 2: Pipeline setup** — Configure GitHub Actions, GitLab CI, or other CI/CD
- **Phase 3: Build configuration** — Dockerfile, multi-stage builds, optimization
- **Phase 4: Deployment configuration** — Environment promotion, secrets, health checks
- **Phase 5: Verification** — Smoke tests, monitoring setup

## Skills Used

- `docker` — Docker best practices for container builds
- `k8s-manifest-generator` — Kubernetes manifest generation patterns
- `prometheus` — Monitoring and alerting configuration

## Trigger Phrases

- "set up CI/CD for this project"
- "create a deployment pipeline"
- "containerize this application"
- "configure deployment to [cloud provider]"
- "set up GitHub Actions for deploy"
- "automate deployments to production"

## Installation

### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/agents
cp -r ~/.ai-skills/agents/deployment .cursor/agents/deployment
```

### Cursor (global)

```bash
mkdir -p ~/.cursor/agents
cp -r ~/.ai-skills/agents/deployment ~/.cursor/agents/deployment
```

### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/agents
cp -r ~/.ai-skills/agents/deployment .claude/agents/deployment
```

### Claude Code (global)

```bash
mkdir -p ~/.claude/agents
cp -r ~/.ai-skills/agents/deployment ~/.claude/agents/deployment
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
