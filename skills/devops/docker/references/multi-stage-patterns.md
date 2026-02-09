# Multi-Stage Build Patterns

Advanced patterns for efficient, secure Docker builds.

---

## Core Concept

Multi-stage builds use multiple `FROM` statements. Each stage can:
- Use a different base image
- Copy artifacts from previous stages
- Be targeted independently with `--target`

**Benefits**:
- Smaller production images (no build tools)
- Better security (fewer packages)
- Faster deployments (smaller images to pull)
- Cleaner separation of concerns

---

## Pattern 1: Builder Pattern

The most common pattern: compile in one stage, run in another.

### Node.js Example

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app

# Install dependencies (cached layer)
COPY package*.json ./
RUN npm ci

# Build application
COPY . .
RUN npm run build

# Stage 2: Production
FROM node:20-alpine AS production
WORKDIR /app

# Create non-root user
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Copy only production artifacts
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/package.json ./

USER 1001
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Go Example (Extreme Minimization)

```dockerfile
# Stage 1: Build
FROM golang:1.22-alpine AS builder
WORKDIR /app

# Download dependencies (cached layer)
COPY go.mod go.sum ./
RUN go mod download

# Build static binary
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-w -s" -o /server

# Stage 2: Production (scratch = empty image)
FROM scratch
COPY --from=builder /server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

**Result**: ~10MB image vs ~800MB with full Go image.

---

## Pattern 2: Development vs Production Targets

Use `--target` to build different variants from the same Dockerfile.

```dockerfile
# Base stage with common setup
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

# Development target
FROM base AS development
RUN npm install
COPY . .
EXPOSE 3000 9229
CMD ["npm", "run", "dev"]

# Builder stage (for production)
FROM base AS builder
RUN npm ci
COPY . .
RUN npm run build && npm prune --production

# Production target
FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

USER 1001
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

**Usage**:
```bash
# Development build
docker build --target development -t myapp:dev .

# Production build
docker build --target production -t myapp:prod .
```

---

## Pattern 3: Test Stage Inclusion

Run tests during build to catch failures early.

```dockerfile
FROM node:20-alpine AS base
WORKDIR /app
COPY package*.json ./

FROM base AS dependencies
RUN npm ci

FROM dependencies AS development
COPY . .
CMD ["npm", "run", "dev"]

# Test stage - run during CI
FROM dependencies AS test
COPY . .
RUN npm run lint
RUN npm run test
RUN npm run type-check

# Build stage - only runs if tests pass
FROM dependencies AS builder
COPY . .
RUN npm run build && npm prune --production

FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist
COPY --from=builder --chown=nextjs:nodejs /app/node_modules ./node_modules

USER 1001
CMD ["node", "dist/index.js"]
```

**CI Usage**:
```bash
# Run tests (fails build if tests fail)
docker build --target test -t myapp:test .

# Build production (only if tests passed)
docker build --target production -t myapp:prod .
```

---

## Pattern 4: Build Cache Optimization

Use BuildKit cache mounts to speed up builds.

### Node.js with npm cache

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./

# Cache npm packages between builds
RUN --mount=type=cache,target=/root/.npm \
    npm ci

COPY . .
RUN npm run build
```

### Python with pip cache

```dockerfile
# syntax=docker/dockerfile:1.4
FROM python:3.12-slim AS builder
WORKDIR /app

COPY requirements.txt .

# Cache pip packages between builds
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .
```

### Go with module cache

```dockerfile
# syntax=docker/dockerfile:1.4
FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./

# Cache Go modules between builds
RUN --mount=type=cache,target=/go/pkg/mod \
    go mod download

COPY . .
RUN --mount=type=cache,target=/root/.cache/go-build \
    CGO_ENABLED=0 go build -o /server
```

---

## Pattern 5: Cross-Platform Builds

Build for multiple architectures using BuildKit.

```dockerfile
FROM --platform=$BUILDPLATFORM golang:1.22-alpine AS builder

# Build arguments for cross-compilation
ARG TARGETOS
ARG TARGETARCH

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=${TARGETOS} GOARCH=${TARGETARCH} \
    go build -o /server

FROM scratch
COPY --from=builder /server /server
ENTRYPOINT ["/server"]
```

**Build for multiple platforms**:
```bash
# Create builder for multi-arch
docker buildx create --name multiarch --use

# Build and push for amd64 and arm64
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myregistry/myapp:latest \
  --push .
```

---

## Pattern 6: Dependency-Only Stage

Separate dependency installation for maximum cache reuse.

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine AS dev-deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM dev-deps AS builder
COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

# Use production deps from deps stage
COPY --from=deps --chown=nextjs:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=nextjs:nodejs /app/dist ./dist

USER 1001
CMD ["node", "dist/index.js"]
```

---

## Pattern 7: External Binary Injection

Copy binaries from other images for additional tools.

```dockerfile
# Get static binaries from external images
FROM curlimages/curl:latest AS curl
FROM busybox:uclibc AS busybox

FROM node:20-alpine AS production
WORKDIR /app

# Copy curl for health checks
COPY --from=curl /usr/bin/curl /usr/bin/curl

# Copy shell utilities if needed
COPY --from=busybox /bin/sh /bin/sh
COPY --from=busybox /bin/wget /bin/wget

COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

---

## Pattern 8: Secrets in Build

Handle secrets securely during build (BuildKit required).

```dockerfile
# syntax=docker/dockerfile:1.4
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./

# Mount secret - NOT stored in layer
RUN --mount=type=secret,id=npm_token \
    NPM_TOKEN=$(cat /run/secrets/npm_token) && \
    echo "//registry.npmjs.org/:_authToken=${NPM_TOKEN}" > .npmrc && \
    npm ci && \
    rm .npmrc

COPY . .
RUN npm run build

FROM node:20-alpine AS production
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
CMD ["node", "dist/index.js"]
```

**Build with secret**:
```bash
docker build --secret id=npm_token,src=.npm_token -t myapp .
```

---

## Stage Naming Conventions

| Stage Name | Purpose |
|------------|---------|
| `base` | Common setup, shared by other stages |
| `deps` / `dependencies` | Install production dependencies |
| `dev-deps` | Install all dependencies including dev |
| `builder` / `build` | Compile/build application |
| `test` / `testing` | Run tests and linting |
| `development` | Development target with hot reload |
| `production` / `runtime` | Final production image |

---

## Build Commands Reference

```bash
# Build specific target
docker build --target development -t myapp:dev .

# Build with build args
docker build --build-arg NODE_ENV=production -t myapp:prod .

# Build with secrets (BuildKit)
DOCKER_BUILDKIT=1 docker build \
  --secret id=token,src=./token.txt \
  -t myapp .

# Build with cache mount (BuildKit)
DOCKER_BUILDKIT=1 docker build -t myapp .

# Multi-platform build
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  -t myapp:latest .

# Build with no cache
docker build --no-cache -t myapp .

# Build with progress output
docker build --progress=plain -t myapp .
```

---

## Image Size Comparison

| Strategy | Node.js App | Go App |
|----------|------------|--------|
| No multi-stage | ~1.2 GB | ~800 MB |
| Multi-stage (alpine) | ~150 MB | ~15 MB |
| Multi-stage (distroless) | ~130 MB | ~8 MB |
| Multi-stage (scratch) | N/A | ~5 MB |
