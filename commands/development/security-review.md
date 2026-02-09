---
name: security-review
model: standard
description: Quick security review of code against OWASP Top 10 and common vulnerability patterns
usage: /security-review <file-or-directory> [--severity critical|high|medium|low] [--fix]
---

# /security-review

Scan code for security vulnerabilities against OWASP Top 10 categories, auth patterns, rate limiting, and data exposure risks. Produces a severity-rated report with specific remediation guidance.

## Usage

```
/security-review <file-or-directory> [--severity critical|high|medium|low] [--fix]
```

**Arguments:**
- `file-or-directory` — Path to scan. Can be a single file, a directory, or a glob pattern
- `--severity` — Minimum severity to report (default: `low`). Use `critical` or `high` to reduce noise
- `--fix` — Automatically apply safe fixes for low-risk findings (adds `// SECURITY:` comments for manual-fix items)

## Examples

```
/security-review src/
/security-review src/auth/ --severity high
/security-review src/routes/payments.ts
/security-review src/api/ --fix
/security-review . --severity critical
```

## When to Use

- Before merging a PR that touches authentication, authorization, or payment logic
- After adding new API endpoints or user input handling
- Periodic review of a service or module for security drift
- When onboarding to an unfamiliar codebase and assessing security posture
- Before a production deployment of sensitive features
- After a dependency update to check for new exposure patterns

## What It Does

1. **Scans** target files for vulnerability patterns
2. **Checks** against OWASP Top 10 categories
3. **Reviews** authentication and authorization patterns
4. **Inspects** rate limiting on public endpoints
5. **Validates** error handling for information leakage
6. **Generates** a severity-rated report with fix suggestions

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Identify Scan Targets

Use `Glob` to expand the target path into a list of files. Filter to code files only:

| Stack | File Extensions |
|-------|----------------|
| **Node.js / TypeScript** | `.ts`, `.tsx`, `.js`, `.jsx`, `.mjs` |
| **Python** | `.py` |
| **Go** | `.go` |
| **Rust** | `.rs` |
| **Config** | `.env`, `.yml`, `.yaml`, `.json`, `.toml` (check for secrets) |
| **Docker** | `Dockerfile`, `docker-compose.yml` (check for misconfig) |

Exclude test files, `node_modules`, `vendor`, and build output directories.

Use `Read` to load each file for analysis. For large directories, prioritize files matching high-risk patterns:
- Files with `auth`, `login`, `session`, `token`, `password`, `secret`, `admin`, `payment`, `billing` in the name
- Route handlers and controllers
- Middleware files
- Configuration files

### Phase 2: Check OWASP Top 10

Scan each file using `Grep` and `Read` against the following vulnerability categories:

#### A01: Broken Access Control

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Missing auth middleware | Route handlers without authentication checks | Critical |
| Missing authorization | Actions without role/permission verification | Critical |
| IDOR vulnerabilities | Direct use of user-supplied IDs without ownership check | High |
| Path traversal | File operations using unsanitized user input | Critical |
| CORS misconfiguration | `Access-Control-Allow-Origin: *` with credentials | High |

Search patterns:
```
# Missing auth on routes
Grep: route/handler definitions without auth middleware
Grep: app.get|app.post|router.* without requireAuth|authenticate|isAuthenticated

# IDOR
Grep: req.params.id|request.args.get.*id used directly in DB queries

# Path traversal
Grep: path.join|os.path.join|filepath.Join with user input
Grep: fs.readFile|open\(.*req\.|os.Open.*request
```

#### A02: Cryptographic Failures

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Weak hashing | MD5 or SHA1 for passwords | Critical |
| Hardcoded secrets | API keys, passwords, tokens in source code | Critical |
| Missing encryption | Sensitive data stored or transmitted in plaintext | High |
| Weak JWT config | No expiration, `none` algorithm, weak secret | Critical |

Search patterns:
```
Grep: md5|sha1.*password|createHash\(['"]md5
Grep: password\s*[:=]\s*['"][^'"]+|api_key\s*[:=]\s*['"][^'"]+|secret\s*[:=]\s*['"][^'"]+
Grep: algorithm.*none|alg.*none
Grep: jwt.sign.*expiresIn|jwt.encode.*exp
```

#### A03: Injection

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| SQL injection | String concatenation in SQL queries | Critical |
| Command injection | `exec`, `spawn`, `system` with user input | Critical |
| Template injection | User input in template strings rendered server-side | High |
| NoSQL injection | Unvalidated objects passed to MongoDB queries | High |

Search patterns:
```
Grep: \$\{.*req\.|\.query\(.*\+.*req\.|f".*SELECT.*{|\.format\(.*SELECT
Grep: exec\(.*req\.|spawn\(.*req\.|system\(.*request|os.system\(.*input
Grep: render_template_string|eval\(|Function\(
Grep: \$where|\$regex.*req\.|\.find\(.*req\.body
```

#### A04: Insecure Design

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| No rate limiting | Public endpoints without throttling | Medium |
| No input limits | Missing max length on string inputs, missing file size limits | Medium |
| Predictable tokens | `Math.random()`, `random.random()` for security tokens | High |

#### A05: Security Misconfiguration

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Debug mode in production | `DEBUG=true`, `NODE_ENV=development` in production configs | High |
| Default credentials | `admin/admin`, `root/root`, default database passwords | Critical |
| Verbose errors | Stack traces or internal paths in API responses | Medium |
| Missing security headers | No CSP, HSTS, X-Frame-Options, X-Content-Type-Options | Medium |

Search patterns:
```
Grep: DEBUG\s*=\s*[Tt]rue|debug\s*:\s*true
Grep: password.*admin|password.*root|password.*123|password.*password
Grep: stack.*trace|stackTrace|err\.stack|traceback
```

#### A06: Vulnerable Components

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Outdated dependencies | Known CVEs in `package.json`, `requirements.txt`, `go.mod` | Varies |
| Unpinned versions | `*` or `latest` in dependency versions | Low |

#### A07: Authentication Failures

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| No brute force protection | Login endpoint without rate limiting or account lockout | High |
| Weak password policy | No minimum length or complexity requirements | Medium |
| Session fixation | Session ID not regenerated after login | High |
| Missing token expiration | JWT or session tokens without TTL | High |

#### A08: Data Integrity Failures

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Insecure deserialization | `JSON.parse`, `pickle.loads`, `yaml.load` on user input without validation | High |
| Missing integrity checks | Downloaded files or updates without checksum verification | Medium |

#### A09: Logging & Monitoring Failures

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Sensitive data in logs | Passwords, tokens, PII logged | High |
| No audit logging | Auth events, admin actions, data changes not logged | Medium |
| Missing request logging | No middleware for request/response logging | Low |

Search patterns:
```
Grep: console.log.*password|log.*token|logger.*secret|print.*api_key
Grep: console.log.*req\.body|log.*request\.data
```

#### A10: SSRF

| Pattern | What to Look For | Severity |
|---------|-----------------|----------|
| Unvalidated URLs | User-supplied URLs passed to `fetch`, `axios`, `requests` without allowlist | High |
| Internal network access | No restriction on `localhost`, `127.0.0.1`, `10.*`, `172.16.*`, `192.168.*` | High |

### Phase 3: Check Auth Patterns

Review authentication and authorization implementation:

| Check | What to Verify |
|-------|---------------|
| Token storage | JWT in `httpOnly` cookie, not `localStorage` |
| Token validation | Signature verification on every request, not just parsing |
| Password storage | bcrypt/scrypt/argon2 with appropriate cost factor |
| Session management | Secure, HttpOnly, SameSite cookie attributes |
| CSRF protection | Anti-CSRF tokens on state-changing requests |
| OAuth implementation | State parameter validation, PKCE for public clients |

### Phase 4: Check Rate Limiting

Use `Grep` to find public-facing endpoints and verify rate limiting:

| Endpoint Type | Expected Limit | Finding if Missing |
|---------------|---------------|-------------------|
| Login / auth | 5-10 per minute per IP | Critical |
| Registration | 3-5 per hour per IP | High |
| Password reset | 3-5 per hour per email | High |
| API endpoints | 100-1000 per minute per key | Medium |
| File upload | 10-50 per hour per user | Medium |
| Webhook receivers | Based on expected volume | Low |

### Phase 5: Check Error Handling

Verify that error responses do not leak internal details:

| Pattern | Severity | Fix |
|---------|----------|-----|
| Stack traces in responses | Medium | Catch and return generic message; log full error server-side |
| Database error messages in responses | High | Wrap database errors; never expose query details |
| File paths in responses | Medium | Sanitize error messages |
| Internal IP addresses in responses | Medium | Strip internal addresses |
| Version numbers in headers | Low | Remove `X-Powered-By`, server version headers |

### Phase 6: Generate Report

Compile all findings into a structured report:

```
Security Review: src/
=====================

Scanned: 47 files
Duration: 12 seconds

  Critical:  2 findings
  High:      5 findings
  Medium:    8 findings
  Low:       3 findings

─────────────────────────────────────────

[CRITICAL] SQL Injection — src/routes/users.ts:42
  Category: A03 Injection
  Pattern:  String concatenation in SQL query
  Code:     const result = await db.query(`SELECT * FROM users WHERE id = ${req.params.id}`)
  Fix:      Use parameterized query: db.query('SELECT * FROM users WHERE id = $1', [req.params.id])

[CRITICAL] Hardcoded Secret — src/config/auth.ts:8
  Category: A02 Cryptographic Failures
  Pattern:  API key hardcoded in source code
  Code:     const API_KEY = 'sk-live-abc123...'
  Fix:      Move to environment variable: process.env.API_KEY

[HIGH] Missing Auth Middleware — src/routes/admin.ts:15
  Category: A01 Broken Access Control
  Pattern:  Admin route without authentication
  Code:     router.get('/admin/users', listAllUsers)
  Fix:      Add auth middleware: router.get('/admin/users', requireAuth, requireRole('admin'), listAllUsers)

[HIGH] Sensitive Data in Logs — src/middleware/logger.ts:23
  Category: A09 Logging Failures
  Pattern:  Request body logged including passwords
  Code:     logger.info('Request body:', req.body)
  Fix:      Sanitize sensitive fields before logging: logger.info('Request body:', sanitize(req.body))

... (additional findings)

─────────────────────────────────────────

Recommendations
===============

  1. [IMMEDIATE] Fix 2 critical injection and secret exposure issues
  2. [THIS SPRINT] Add auth middleware to 3 unprotected admin routes
  3. [THIS SPRINT] Sanitize log output to remove sensitive data
  4. [BACKLOG] Add rate limiting to login and registration endpoints
  5. [BACKLOG] Add security headers middleware (CSP, HSTS, X-Frame-Options)
```

## NEVER Do

| Rule | Reason |
|------|--------|
| Never auto-fix critical or high severity issues without review | Automated fixes for auth and injection can break functionality; always require human review |
| Never report secrets or full key values in the output | Redact to first 4-8 characters when showing hardcoded secrets |
| Never skip config files during scan | `.env`, `docker-compose.yml`, and CI configs often contain secrets or misconfigurations |
| Never assume a dependency is safe because it's popular | Check for known CVEs regardless of download count |
| Never treat test files as production code | Skip test directories to avoid false positives on intentional test fixtures |
| Never report without remediation guidance | Every finding must include a specific, actionable fix |

## Error Handling

| Situation | Action |
|-----------|--------|
| Target path does not exist | Error with clear message and suggest valid paths |
| No code files found in target | Warn and list the file types found |
| File too large to analyze | Warn and offer to scan specific functions or sections |
| Unknown framework or language | Apply language-agnostic checks (secrets, config) and note limited coverage |
| Too many findings (> 50) | Group by category and severity; show top 20 with note about remaining |

## Output

- **Security report** with severity-rated findings, affected file and line, and remediation steps
- **Summary counts** by severity level
- **Prioritized recommendations** grouped by urgency
- **Auto-fix comments** in code if `--fix` flag was used (safe fixes only)

## Related

- **Auth patterns:** `solidity-security` skill (for smart contract security)
- **Error handling:** `logging-observability` skill (for secure logging practices)
- **Docker security:** `docker-expert` skill (for container hardening)
- **Code review:** `/review-code` (for general code quality review)
- **Feature workflow:** `/new-feature` (to include security review as part of feature development)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
