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

### Using the skills CLI

```bash
skills init cursor   # or: skills init agents
skills add deployment
```

### Manual: Cursor

```bash
mkdir -p .cursor/rules
cp -r ~/.skills/ai/agents/deployment .cursor/rules/deployment-agent
```

### Manual: Claude Code

```bash
# Project
mkdir -p .claude/skills
cp -r ~/.skills/ai/agents/deployment .claude/skills/deployment-agent

# Global
mkdir -p ~/.claude/skills
cp -r ~/.skills/ai/agents/deployment ~/.claude/skills/deployment-agent
```

For best results, also install the skills this agent references (see Skills Used above).

---

Part of the [Agents](../) directory.
