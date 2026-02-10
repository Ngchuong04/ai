# DevOps

Skills for DevOps and infrastructure — containerization, orchestration, monitoring, monorepo build systems, and smart contract security.

## Skills

| Skill | Description |
|-------|-------------|
| [docker](docker/) | Docker containerization expertise — multi-stage builds, image optimization, security hardening, and Compose orchestration. |
| [kubernetes](kubernetes/) | Kubernetes manifest generation for Deployments, StatefulSets, CronJobs, Services, Ingresses, and ConfigMaps. |
| [k8s-manifest-generator](kubernetes/k8s-manifest-generator/) | Create production-ready Kubernetes manifests following best practices and security standards. |
| [prometheus](prometheus/) | Prometheus monitoring — scrape configuration, service discovery, recording rules, and alert rules. |
| [solidity-security](solidity-security/) | Smart contract security patterns, vulnerability prevention, gas optimization, and audit preparation for Solidity. |
| [turborepo](turborepo/) | Turborepo monorepo build system — caching, task pipelines, and parallel execution for JS/TS projects. |

## Installation

```bash
# Add individual skills
npx add https://github.com/wpank/ai/tree/main/skills/devops/docker
npx add https://github.com/wpank/ai/tree/main/skills/devops/kubernetes
npx add https://github.com/wpank/ai/tree/main/skills/devops/prometheus
```

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install docker
npx clawhub@latest install kubernetes
npx clawhub@latest install k8s-manifest-generator
npx clawhub@latest install prometheus
npx clawhub@latest install solidity-security
npx clawhub@latest install turborepo
```

## See Also

- [All Skills](../) — Complete skills catalog
- [Agents](../../agents/) — Workflow agents
