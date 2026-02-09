---
name: deploy
model: standard
description: Deployment workflow with environment selection, safety checks, and rollback
usage: /deploy <environment> [--strategy rolling|blue-green|canary] [--skip-tests] [--dry-run]
---

# /deploy

Execute a safe, verified deployment with pre-flight checks, health verification, and automatic rollback on failure.

## Usage

```
/deploy <environment> [--strategy rolling|blue-green|canary] [--skip-tests] [--dry-run]
```

**Arguments:**
- `environment` — Target environment: `dev`, `staging`, or `production`
- `--strategy` — Deployment strategy (default: `rolling` for dev/staging, `blue-green` for production)
- `--skip-tests` — Skip the test suite during pre-flight (forbidden for production)
- `--dry-run` — Run all checks and build without actually deploying

## Examples

```
/deploy dev                                    # Deploy to dev with defaults
/deploy staging --strategy canary              # Canary deploy to staging
/deploy production --strategy blue-green       # Blue-green deploy to production
/deploy production --dry-run                   # Validate everything without deploying
/deploy staging --skip-tests                   # Deploy to staging, skip test suite
```

## What It Does

1. **Validates** the target environment and flags, blocking dangerous combinations
2. **Checks** git status for clean working tree, correct branch, and no uncommitted changes
3. **Runs** the test suite and type checker as pre-flight verification
4. **Detects** the CI/CD platform, container registry, and cloud provider in use
5. **Builds** the application and verifies the artifact or image
6. **Tags** the release with a version or commit SHA
7. **Pushes** the artifact to the appropriate registry
8. **Deploys** using the selected strategy (rolling, blue-green, or canary)
9. **Runs** health checks against the deployed instance with retry backoff
10. **Executes** post-deployment smoke tests against the live environment
11. **Rolls back** automatically if health checks or smoke tests fail
12. **Reports** deployment status, duration, and artifact details

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse and Validate Input

| Parameter | Source | Default | Constraints |
|-----------|--------|---------|-------------|
| Environment | Positional argument | Required | `dev`, `staging`, `production` |
| Strategy | `--strategy` flag | `rolling` (dev/staging), `blue-green` (production) | `rolling`, `blue-green`, `canary` |
| Skip tests | `--skip-tests` flag | `false` | Forbidden for `production` |
| Dry run | `--dry-run` flag | `false` | Allowed for all environments |

Reject if `--skip-tests` is used with `production`. Reject `--strategy canary` with `dev` (requires traffic splitting).

### Phase 2: Pre-Deployment Safety Checks

**2a. Git status** — verify clean working tree. For `production`: branch must be `main` or `release/*`. For `staging`: `main`, `release/*`, or `develop`. For `dev`: any branch.

**2b. Test suite** — detect and run unless `--skip-tests`:

| Indicator | Runner |
|-----------|--------|
| `package.json` with `jest` | `npx jest --ci` |
| `package.json` with `vitest` | `npx vitest run` |
| `pytest.ini` or `pyproject.toml` [tool.pytest] | `pytest` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |
| `Makefile` with `test` target | `make test` |

**2c. Type checking** — run if present (`tsc --noEmit`, `mypy`, `pyright`). Failures block `production`; warn-only for other environments.

### Phase 3: Detect Infrastructure

Use `Glob` and `Grep` to identify CI/CD, registry, and cloud provider.

**CI/CD Platform:**

| Platform | Detection Signal |
|----------|-----------------|
| **GitHub Actions** | `.github/workflows/*.yml` |
| **GitLab CI** | `.gitlab-ci.yml` |
| **CircleCI** | `.circleci/config.yml` |
| **Jenkins** | `Jenkinsfile` |
| **Vercel** | `vercel.json` or `.vercel/` |
| **Netlify** | `netlify.toml` |
| **AWS CodePipeline** | `buildspec.yml` or `appspec.yml` |
| **Google Cloud Build** | `cloudbuild.yaml` |
| **Azure DevOps** | `azure-pipelines.yml` |
| **Fly.io** | `fly.toml` |

**Container Registry:**

| Registry | Detection Signal |
|----------|-----------------|
| **Docker Hub** | No registry prefix in image refs |
| **GitHub (ghcr.io)** | Image refs containing `ghcr.io` |
| **AWS ECR** | Image refs containing `.dkr.ecr.` |
| **Google Artifact Registry** | Image refs containing `gcr.io` or `*-docker.pkg.dev` |
| **Azure ACR** | Image refs containing `.azurecr.io` |
| **GitLab Registry** | Image refs containing `registry.gitlab.com` |

**Cloud Provider:**

| Provider | Detection Signal |
|----------|-----------------|
| **AWS** | `samconfig.toml`, `cdk.json`, `serverless.yml` with `provider: aws` |
| **GCP** | `app.yaml`, `cloudbuild.yaml`, `gcloud` references |
| **Azure** | `azure-pipelines.yml`, `host.json`, `.azure/` |
| **Vercel** | `vercel.json` or Vercel-specific config in `next.config.*` |
| **Netlify** | `netlify.toml` with `[build]` section |
| **Fly.io** | `fly.toml` with `[deploy]` section |
| **Heroku** | `Procfile`, `app.json`, or `heroku.yml` |
| **Render** | `render.yaml` |
| **DigitalOcean** | `.do/app.yaml` |

If no platform is detected, ask the user to specify the deployment target.

### Phase 4: Build and Verify

| Build System | Detection | Command |
|--------------|-----------|---------|
| **npm/yarn/pnpm** | `package.json` with `build` script | `npm run build` |
| **Docker** | `Dockerfile` present | `docker build -t <app>:<tag> .` |
| **Go** | `go.mod` | `go build -o ./bin/<app> ./cmd/<app>` |
| **Rust** | `Cargo.toml` | `cargo build --release` |
| **Make** | `Makefile` with `build` target | `make build` |

After build: verify artifact exists, record commit SHA via `git rev-parse --short HEAD`. If build fails, stop and report.

### Phase 5: Tag, Push, and Deploy

Generate tag: `dev-<sha>` for dev, `staging-<sha>` for staging, `v<semver>` or `prod-<sha>` for production. Push artifact to the detected registry. For `--dry-run`, print commands without executing.

**Strategy execution:**

- **Rolling** — replace instances one at a time; health check each before continuing
- **Blue-Green** — deploy to inactive environment, health check, swap traffic atomically
- **Canary** — route 5-10% traffic to new version, monitor for 5 min, gradually increase to 100%

### Phase 6: Health Checks and Smoke Tests

```bash
# Health check with exponential backoff (4 attempts: 5s, 10s, 20s, 40s)
for delay in 5 10 20 40; do
  curl -sf --max-time 10 "$DEPLOY_URL/health" && break
  sleep $delay
done
```

Post-deploy smoke tests: root URL returns 200, health endpoint responds, critical API path works, static assets load. If any check fails, trigger rollback.

### Phase 7: Rollback Procedure

```bash
# Kubernetes
kubectl rollout undo deployment/<app> -n <namespace>

# Vercel / Fly.io
vercel rollback
fly releases rollback

# Docker — retag previous image as latest and push
docker tag <registry>/<app>:<previous-tag> <registry>/<app>:latest
docker push <registry>/<app>:latest
```

After rollback: re-run health checks, report failure details, preserve failed artifact for debugging.

## Output

```
Deployment Report
=================

Environment:  <environment>
Strategy:     <strategy>
Status:       ✓ SUCCESS | ✗ FAILED (rolled back)
Duration:     <elapsed>

Build
-----
  Commit:     <sha> (<message>)
  Branch:     <branch>
  Artifact:   <registry/path:tag>

Checks
------
  Tests:      <passed> passed, <failed> failed
  Types:      Clean | <N> errors
  Git:        <status>

Health:       Passed (attempt <N>/4)
Smoke:        <passed>/<total> passed
URL:          <deployed-url>

Next Steps
----------
  1. Monitor error rates for 15 minutes
  2. Verify key user flows manually
  3. Announce the release in #deployments
```

## NEVER Do

- **NEVER deploy to production from a feature branch** — production must come from `main` or `release/*`
- **NEVER skip tests for production deployments** — untested deploys risk customer-facing outages
- **NEVER deploy with uncommitted changes** — unreproducible builds make rollback impossible
- **NEVER continue after failed health checks** — rollback immediately
- **NEVER delete the previous deployment artifact** — it is your rollback safety net
- **NEVER force-push tags to overwrite a failed release** — tag history is an audit trail
- **NEVER expose secrets in deployment logs** — mask env vars and redact tokens from output
- **NEVER deploy without a rollback plan** — every deploy needs a documented path back

## Error Handling

- **Dirty working tree** — stop and instruct user to commit or stash
- **Tests fail** — stop and report failing tests; block deployment
- **Build fails** — stop and display build errors; do not proceed
- **Registry push fails** — retry once; if still failing, check auth and network
- **Health checks timeout** — trigger automatic rollback; report last response
- **Smoke tests fail** — trigger automatic rollback; report which tests failed
- **Rollback fails** — alert immediately; provide manual rollback commands
- **No CI/CD detected** — ask user to specify target; provide manual steps
- **Production deploy** — prompt for explicit confirmation before proceeding

## Related

- **Pre-deploy review:** `/review-code` (review changes before deploying)
- **Testing:** `/test-feature` (run targeted tests before deployment)
- **Debugging deploys:** `/debug-error` (investigate deployment failures)
- **Infrastructure:** [`docker`](ai/skills/devops/docker/SKILL.md) skill, [`kubernetes`](ai/skills/devops/kubernetes/SKILL.md) skill
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
