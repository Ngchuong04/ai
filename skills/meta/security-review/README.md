# Security Review

Meta-skill that orchestrates a comprehensive security review by coordinating auth, input validation, secrets management, API security, and infrastructure hardening skills into a single, repeatable workflow.

## What's Inside

- Six-step orchestration flow (auth & authz → input & errors → dependencies → API security → smart contracts → infrastructure)
- Skill routing table for each security concern
- Security checklist (OWASP Top 10, input validation, auth/sessions, cryptography, error handling, data protection)
- Severity classification (Critical, High, Medium, Low) with response times
- Security review report template

## When to Use

- Before release — final security gate before code ships
- After auth changes — auth regressions are high-severity by default
- During security audit — structured walkthrough for auditors
- New API endpoints — every new surface area needs review
- Handling user input — input validation is the #1 attack vector
- Dependency updates — new deps may introduce vulnerabilities
- Infrastructure changes — container, K8s, or network config changes

## Installation

```bash
npx add https://github.com/wpank/ai/tree/main/skills/meta/security-review
```

### Manual Installation

#### Cursor (per-project)

From your project root:

```bash
mkdir -p .cursor/skills
cp -r ~/.ai-skills/skills/meta/security-review .cursor/skills/security-review
```

#### Cursor (global)

```bash
mkdir -p ~/.cursor/skills
cp -r ~/.ai-skills/skills/meta/security-review ~/.cursor/skills/security-review
```

#### Claude Code (per-project)

From your project root:

```bash
mkdir -p .claude/skills
cp -r ~/.ai-skills/skills/meta/security-review .claude/skills/security-review
```

#### Claude Code (global)

```bash
mkdir -p ~/.claude/skills
cp -r ~/.ai-skills/skills/meta/security-review ~/.claude/skills/security-review
```

## Related Skills

- `auth-patterns` — Authentication & authorization patterns
- `error-handling-patterns` — Input validation & error handling
- `quality-gates` — Dependency scanning & security gates
- `api-design-principles` — API security & endpoint hardening
- `solidity-security` — Smart contract vulnerabilities
- `docker-expert` — Container security
- `k8s-manifest-generator` — Kubernetes security

---

Part of the [Meta](..) skill category.
