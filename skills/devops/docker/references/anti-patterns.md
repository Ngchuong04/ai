# Docker Anti-Patterns

Common Docker mistakes with explanations and fixes.

---

## 1. Running as Root

**Problem**: Containers run as root by default, which is a security risk. If an attacker compromises the container, they have root access.

```dockerfile
# ❌ Bad - runs as root
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm ci
CMD ["node", "server.js"]
```

```dockerfile
# ✅ Good - runs as non-root user
FROM node:20-alpine
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

COPY --chown=nextjs:nodejs . .
RUN npm ci

# Switch to non-root user
USER 1001
CMD ["node", "server.js"]
```

---

## 2. Installing Dev Dependencies in Production

**Problem**: Dev dependencies increase image size and attack surface without providing runtime value.

```dockerfile
# ❌ Bad - installs everything
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "server.js"]
```

```dockerfile
# ✅ Good - production only
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force
COPY . .
CMD ["node", "server.js"]
```

---

## 3. Storing Secrets in Image

**Problem**: Secrets in ENV or COPY are visible in image layers and `docker history`.

```dockerfile
# ❌ Bad - secret visible in layer
FROM node:20-alpine
ENV API_KEY=sk-1234567890abcdef
COPY .env /app/.env
```

```dockerfile
# ✅ Good - mount secrets at runtime
FROM node:20-alpine
# No secrets in image

# At runtime:
# docker run -v /path/to/secrets:/run/secrets:ro myapp
```

```dockerfile
# ✅ Good - build-time secrets (not persisted)
# syntax=docker/dockerfile:1.4
FROM node:20-alpine
RUN --mount=type=secret,id=api_key \
    API_KEY=$(cat /run/secrets/api_key) ./configure.sh
```

---

## 4. Poor Layer Caching

**Problem**: Copying all files before installing dependencies invalidates cache on every code change.

```dockerfile
# ❌ Bad - cache invalidated on any file change
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm ci
```

```dockerfile
# ✅ Good - dependencies cached separately
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
```

**Rule**: Copy dependency files → Install dependencies → Copy source code

---

## 5. Not Using .dockerignore

**Problem**: Without `.dockerignore`, Docker sends unnecessary files to the build context, slowing builds and potentially including secrets.

```dockerfile
# ❌ Bad - sends everything including node_modules, .git, .env
COPY . .
```

```gitignore
# ✅ Good - create .dockerignore
node_modules
.git
.env
.env.*
*.log
.DS_Store
coverage
.next
dist
```

**Check context size**:
```bash
# See what's being sent to Docker
docker build --no-cache . 2>&1 | grep "Sending build context"
# Should be < 10MB for most apps
```

---

## 6. Using `latest` Tag

**Problem**: `latest` is mutable and unpredictable. Builds can break unexpectedly when the image updates.

```dockerfile
# ❌ Bad - unpredictable
FROM node:latest
FROM node:20
```

```dockerfile
# ✅ Good - specific version
FROM node:20.10.0-alpine3.19

# ✅ Best - pinned with digest
FROM node:20.10.0-alpine3.19@sha256:abc123...
```

---

## 7. Not Pinning Package Versions

**Problem**: Package versions can change between builds, causing inconsistencies.

```dockerfile
# ❌ Bad - versions can change
RUN apt-get update && apt-get install -y \
    curl \
    wget
```

```dockerfile
# ✅ Good - pinned versions
RUN apt-get update && apt-get install -y \
    curl=7.88.1-10+deb12u5 \
    wget=1.21.3-1+b1
```

**Note**: This creates maintenance burden. Balance with regular updates.

---

## 8. Giant Images

**Problem**: Large images are slow to pull, push, and start. They also have larger attack surfaces.

```dockerfile
# ❌ Bad - 1GB+ image with build tools in production
FROM node:20
RUN apt-get update && apt-get install -y build-essential python3
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

```dockerfile
# ✅ Good - multi-stage, minimal production image
FROM node:20 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/server.js"]
```

**Image size comparison**:
| Base | Typical Size |
|------|--------------|
| `node:20` | ~1 GB |
| `node:20-slim` | ~200 MB |
| `node:20-alpine` | ~130 MB |
| `distroless/nodejs20` | ~120 MB |

---

## 9. Ignoring Health Checks

**Problem**: Without health checks, orchestrators can't detect unhealthy containers.

```dockerfile
# ❌ Bad - no health check
FROM node:20-alpine
CMD ["node", "server.js"]
```

```dockerfile
# ✅ Good - health check defined
FROM node:20-alpine
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:3000/health || exit 1
CMD ["node", "server.js"]
```

---

## 10. Not Cleaning Package Caches

**Problem**: Package manager caches remain in the layer, increasing image size.

```dockerfile
# ❌ Bad - cache remains (adds 50-200MB)
RUN apt-get update && apt-get install -y curl
```

```dockerfile
# ✅ Good - clean in same layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

```dockerfile
# ✅ Alpine version
RUN apk add --no-cache curl
```

---

## 11. Multiple RUN Commands for Related Operations

**Problem**: Each RUN creates a layer. Splitting related operations creates unnecessary layers and can leave artifacts.

```dockerfile
# ❌ Bad - 3 layers, rm doesn't reduce size
RUN apt-get update
RUN apt-get install -y curl
RUN rm -rf /var/lib/apt/lists/*
```

```dockerfile
# ✅ Good - 1 layer, cleanup effective
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
```

---

## 12. ADD Instead of COPY

**Problem**: `ADD` has magic behavior (auto-extraction, URL fetching) that's rarely needed and can be surprising.

```dockerfile
# ❌ Bad - unclear behavior
ADD app.tar.gz /app/
ADD https://example.com/file.txt /app/
```

```dockerfile
# ✅ Good - explicit behavior
COPY app.tar.gz /tmp/
RUN tar -xzf /tmp/app.tar.gz -C /app/ && rm /tmp/app.tar.gz

RUN wget -O /app/file.txt https://example.com/file.txt
```

**Rule**: Use `COPY` unless you specifically need `ADD`'s auto-extraction.

---

## 13. Not Using Multi-Stage Builds

**Problem**: Build tools, source code, and intermediate artifacts remain in the production image.

```dockerfile
# ❌ Bad - Go compiler in production image (800MB+)
FROM golang:1.22
WORKDIR /app
COPY . .
RUN go build -o server
CMD ["./server"]
```

```dockerfile
# ✅ Good - only binary in production (~10MB)
FROM golang:1.22 AS builder
WORKDIR /app
COPY . .
RUN CGO_ENABLED=0 go build -o server

FROM scratch
COPY --from=builder /app/server /server
CMD ["/server"]
```

---

## 14. Hardcoding Ports

**Problem**: Hardcoding ports reduces flexibility and causes conflicts.

```dockerfile
# ❌ Bad - hardcoded
FROM node:20-alpine
ENV PORT=3000
EXPOSE 3000
CMD ["node", "server.js"]
```

```dockerfile
# ✅ Good - configurable
FROM node:20-alpine
ARG PORT=3000
ENV PORT=${PORT}
EXPOSE ${PORT}
CMD ["node", "server.js"]
```

---

## 15. Using WORKDIR Instead of cd

**Problem**: `cd` in RUN doesn't persist. Use WORKDIR.

```dockerfile
# ❌ Bad - cd doesn't persist
RUN cd /app && npm install
RUN npm run build  # This runs in / not /app
```

```dockerfile
# ✅ Good - WORKDIR persists
WORKDIR /app
RUN npm install
RUN npm run build  # This runs in /app
```

---

## 16. Not Setting SHELL

**Problem**: Default shell on Alpine is `/bin/sh` which has limited features.

```dockerfile
# ❌ Bad on Alpine - pipefail not supported
RUN curl -s https://example.com | sh
```

```dockerfile
# ✅ Good - explicit shell with pipefail
SHELL ["/bin/sh", "-o", "pipefail", "-c"]
RUN curl -s https://example.com | sh

# Or for bash
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
```

---

## Quick Reference

| Anti-Pattern | Fix |
|--------------|-----|
| Running as root | `USER 1001` |
| Dev deps in prod | `npm ci --only=production` |
| Secrets in image | Mount at runtime |
| COPY . . first | Copy package files first |
| No .dockerignore | Create one |
| `latest` tag | Pin specific version |
| Giant images | Multi-stage builds |
| No health check | Add HEALTHCHECK |
| Uncleaned caches | Clean in same RUN |
| Many RUN layers | Combine related RUNs |
| ADD over COPY | Use COPY |
| No multi-stage | Separate build/runtime |
