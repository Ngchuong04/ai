# Prometheus Observability

Production Prometheus setup covering scrape configuration, service discovery, recording rules, alert rules, and operational best practices for infrastructure and application monitoring.

## What's Inside

- Architecture overview (scraping, AlertManager, Grafana, long-term storage)
- Installation via Helm on Kubernetes
- Core scrape configuration and job setup
- Service discovery (Kubernetes, file-based, static targets)
- Recording rules for pre-computing expensive PromQL queries
- Alert rules with SLO-based patterns for availability and latency
- Validation commands and configuration testing
- Best practices and troubleshooting quick reference

## When to Use

- Setting up metrics collection for a new service
- Configuring service discovery for Kubernetes pods or static targets
- Creating recording rules to pre-compute expensive queries
- Designing SLO-based alert rules for availability and latency
- Deploying Prometheus in HA mode with retention and storage planning
- Troubleshooting scraping issues (targets down, metrics missing, relabeling)

## Installation

```bash
npx skills add prometheus-observability
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/prometheus-observability .cursor/skills/prometheus-observability
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/infrastructure/prometheus-observability ~/.cursor/skills/prometheus-observability
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/infrastructure/prometheus-observability .claude/skills/prometheus-observability
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/infrastructure/prometheus-observability ~/.claude/skills/prometheus-observability
```

---

Part of the [Infrastructure](..) skill category.
