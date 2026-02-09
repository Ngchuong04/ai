# Docker Security Checklist

Comprehensive security hardening guide for containerized applications.

---

## 1. Non-Root User Configuration

Running containers as root is a critical security risk. Always create and use a dedicated user.

### Checklist

- [ ] Create a dedicated user with specific UID/GID (not default)
- [ ] Set USER directive before CMD/ENTRYPOINT
- [ ] Use numeric UID for Kubernetes compatibility
- [ ] Ensure file ownership matches the user

### Pattern: Alpine Linux

```dockerfile
# Create user with specific UID/GID
RUN addgroup -g 1001 -S appgroup && \
    adduser -S appuser -u 1001 -G appgroup

# Set ownership during COPY
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER 1001
```

### Pattern: Debian/Ubuntu

```dockerfile
# Create user with specific UID/GID
RUN groupadd -g 1001 appgroup && \
    useradd -r -u 1001 -g appgroup appuser

# Set ownership
COPY --chown=appuser:appgroup . .

# Switch to non-root user
USER 1001
```

### Why UID 1001?

- Avoids collision with system users (typically < 1000)
- Works well with Kubernetes security contexts
- Easy to reference in security policies

---

## 2. Secrets Management

Never store secrets in images or environment variables visible in `docker inspect`.

### Checklist

- [ ] No secrets in Dockerfile (API keys, passwords, tokens)
- [ ] No secrets in ENV instructions
- [ ] Use build-time secrets for private dependencies
- [ ] Use runtime secrets for application credentials
- [ ] Secrets not visible in image layers (`docker history`)

### Pattern: Build-Time Secrets (BuildKit)

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine

# Mount secret during build - not persisted in layer
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) \
    npm config set //registry.npmjs.org/:_authToken=$NPM_TOKEN && \
    npm ci && \
    npm config delete //registry.npmjs.org/:_authToken
```

Build command:
```bash
DOCKER_BUILDKIT=1 docker build \
  --secret id=npm_token,src=./.npm_token \
  -t myapp .
```

### Pattern: Runtime Secrets (Docker Swarm)

```yaml
# docker-compose.yml
services:
  app:
    image: myapp
    secrets:
      - db_password
    environment:
      DB_PASSWORD_FILE: /run/secrets/db_password

secrets:
  db_password:
    external: true
```

### Pattern: Runtime Secrets (Kubernetes)

```yaml
# Mount secret as file, not env var
volumes:
  - name: secrets
    secret:
      secretName: app-secrets
volumeMounts:
  - name: secrets
    mountPath: /run/secrets
    readOnly: true
```

---

## 3. Base Image Security

The base image is your foundation. Keep it minimal and updated.

### Checklist

- [ ] Use official images from trusted registries
- [ ] Pin specific versions (not `latest`)
- [ ] Use minimal base images (Alpine, distroless, scratch)
- [ ] Regularly update base images
- [ ] Scan images for vulnerabilities

### Base Image Comparison

| Base Image | Size | Use Case | Security |
|------------|------|----------|----------|
| `scratch` | 0 MB | Static Go binaries | Best - no OS |
| `gcr.io/distroless/static` | ~2 MB | Static binaries | Excellent - minimal |
| `gcr.io/distroless/base` | ~20 MB | Dynamic binaries | Excellent |
| `alpine` | ~5 MB | General purpose | Good - small attack surface |
| `debian-slim` | ~80 MB | Compatibility | Moderate |
| `ubuntu` | ~80 MB | Development | Lower - more packages |

### Pattern: Version Pinning

```dockerfile
# Bad - unpredictable
FROM node:latest
FROM node:20

# Good - predictable, patchable
FROM node:20.10.0-alpine3.19

# Best - use digest for reproducibility
FROM node:20.10.0-alpine3.19@sha256:abc123...
```

### Pattern: Image Scanning

```bash
# Docker Scout (built-in)
docker scout quickview myapp:latest
docker scout cves myapp:latest

# Trivy (open source)
trivy image myapp:latest

# Snyk
snyk container test myapp:latest
```

---

## 4. Runtime Security

Limit what containers can do at runtime.

### Checklist

- [ ] Drop unnecessary Linux capabilities
- [ ] Use read-only root filesystem where possible
- [ ] Set resource limits (CPU, memory)
- [ ] Disable privilege escalation
- [ ] Use seccomp profiles

### Pattern: Docker Compose Security

```yaml
services:
  app:
    image: myapp
    security_opt:
      - no-new-privileges:true
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE  # Only if binding to ports < 1024
    read_only: true
    tmpfs:
      - /tmp
      - /var/run
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
```

### Pattern: Docker Run Security

```bash
docker run \
  --read-only \
  --tmpfs /tmp \
  --cap-drop ALL \
  --security-opt no-new-privileges:true \
  --memory 512m \
  --cpus 0.5 \
  myapp
```

### Linux Capabilities Reference

| Capability | Purpose | Usually Needed |
|------------|---------|----------------|
| `NET_BIND_SERVICE` | Bind to ports < 1024 | Rarely |
| `CHOWN` | Change file ownership | Rarely |
| `SETUID/SETGID` | Change user/group | Never in production |
| `SYS_ADMIN` | Administrative operations | Never |
| `ALL` | All capabilities | Drop this |

---

## 5. Network Security

Minimize network exposure and isolate services.

### Checklist

- [ ] Only expose necessary ports
- [ ] Use internal networks for backend services
- [ ] Implement health checks
- [ ] Use TLS for external communications
- [ ] Avoid host network mode

### Pattern: Network Isolation

```yaml
services:
  frontend:
    networks:
      - frontend
      - backend
    ports:
      - "443:3000"  # Only frontend exposed

  api:
    networks:
      - backend
    # No ports exposed to host

  database:
    networks:
      - backend
    # No ports exposed to host

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access
```

### Pattern: Health Checks

```dockerfile
# HTTP health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1

# TCP health check (no curl/wget)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD nc -z localhost 3000 || exit 1
```

---

## 6. Build Security

Secure the build process itself.

### Checklist

- [ ] Use `.dockerignore` to exclude sensitive files
- [ ] Don't install unnecessary packages
- [ ] Remove package manager caches
- [ ] Verify downloaded files (checksums)
- [ ] Use multi-stage builds to exclude build tools

### Pattern: Secure Package Installation

```dockerfile
# Alpine - verify and clean
RUN apk add --no-cache \
    package1 \
    package2 && \
    rm -rf /var/cache/apk/*

# Debian - verify and clean
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    package1 \
    package2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

### Pattern: Verify Downloads

```dockerfile
# Download with checksum verification
ARG TOOL_VERSION=1.2.3
ARG TOOL_SHA256=abc123...
RUN wget -O /tmp/tool.tar.gz \
    https://example.com/tool-${TOOL_VERSION}.tar.gz && \
    echo "${TOOL_SHA256}  /tmp/tool.tar.gz" | sha256sum -c - && \
    tar -xzf /tmp/tool.tar.gz -C /usr/local/bin && \
    rm /tmp/tool.tar.gz
```

---

## 7. Quick Security Audit

Run these commands to audit an existing image:

```bash
# Check if running as root
docker run --rm myapp whoami
# Should NOT return "root"

# Check for secrets in history
docker history --no-trunc myapp | grep -iE "password|secret|key|token"
# Should return nothing

# Check image layers for secrets
docker save myapp | tar -xO | strings | grep -iE "password|secret|api_key"
# Should return nothing

# Check capabilities
docker run --rm myapp capsh --print
# Should show minimal capabilities

# Scan for vulnerabilities
docker scout cves myapp
# Fix any HIGH or CRITICAL vulnerabilities
```

---

## Summary Checklist

| Category | Critical Items |
|----------|---------------|
| **User** | Non-root user with specific UID |
| **Secrets** | No secrets in image, use mounted secrets |
| **Base Image** | Minimal, pinned version, regularly scanned |
| **Runtime** | Drop capabilities, resource limits |
| **Network** | Minimal exposure, internal networks |
| **Build** | .dockerignore, clean caches, verify downloads |
