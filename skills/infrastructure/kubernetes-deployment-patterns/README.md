# Kubernetes Deployment Patterns

Production-ready Kubernetes manifest generation covering Deployments, StatefulSets, CronJobs, Services, Ingresses, ConfigMaps, Secrets, and PVCs with security contexts, health checks, and resource management.

## What's Inside

- Workload selection guide (Deployment vs StatefulSet vs Job vs CronJob vs DaemonSet)
- Deployment manifests with rolling updates, probes, and resource limits
- Service types (ClusterIP, LoadBalancer) and Ingress with TLS
- ConfigMap and Secret management patterns
- Persistent storage with PVCs and StorageClasses
- Security context configuration (non-root, read-only, capabilities)
- Standard labeling conventions and manifest organization
- Validation commands and troubleshooting quick reference

## When to Use

- Creating deployment manifests for new microservices
- Defining networking resources (Services, Ingress with TLS)
- Managing configuration with ConfigMaps and Secrets
- Setting up stateful workloads with StatefulSets and PVCs
- Configuring scheduled jobs with CronJobs
- Organizing multi-environment configs with Kustomize overlays

## Installation

```bash
npx skills add kubernetes-deployment-patterns
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/kubernetes-deployment-patterns .cursor/skills/kubernetes-deployment-patterns
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/kubernetes-deployment-patterns ~/.cursor/skills/kubernetes-deployment-patterns
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/infrastructure/kubernetes-deployment-patterns .claude/skills/kubernetes-deployment-patterns
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/infrastructure/kubernetes-deployment-patterns ~/.claude/skills/kubernetes-deployment-patterns
```

---

Part of the [Infrastructure](..) skill category.
