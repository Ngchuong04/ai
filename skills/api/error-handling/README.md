# Error Handling Patterns

Error handling patterns across languages and layers — operational vs programmer errors, retry strategies, circuit breakers, error boundaries, HTTP responses, graceful degradation, and structured logging. Use when designing error strategies, building resilient APIs, or reviewing error management.

## What's Inside

- Error Handling Philosophy — fail fast, fail loud, handle at boundaries, be specific, provide context
- Error Types — operational errors vs programmer errors
- Language Patterns — JavaScript, Python, Go, Rust error handling idioms
- Error Boundaries — Express error middleware, React error boundary
- Retry Patterns — exponential backoff with jitter, circuit breaker, bulkhead, timeout
- HTTP Error Responses — status codes, standard error envelope
- Graceful Degradation — fallback values, feature flags, cached responses, partial responses
- Logging & Monitoring — structured logging, error tracking, alert thresholds, correlation IDs
- Anti-Patterns — swallowing errors, generic catch-all, stringly-typed errors, and more

## When to Use

- Designing error handling strategies for APIs or applications
- Building resilient systems with retry and circuit breaker patterns
- Implementing error boundaries in Express or React
- Standardizing error response formats across endpoints
- Adding graceful degradation for non-critical services
- Setting up structured error logging and monitoring

## Installation

```bash
skills add error-handling
```

### Manual Installation

Copy this directory to your project:

```bash
# Cursor
cp -r ~/.skills/ai/skills/api/error-handling .cursor/rules/error-handling

# Claude Code  
cp -r ~/.skills/ai/skills/api/error-handling .agents/skills/error-handling
```

## Related Skills

- `api-design` — Error response format and status code usage
- `rate-limiting` — Rate limit errors (429) and retry handling
- `caching` — Never cache error responses

---

Part of the [API](..) skill category.
