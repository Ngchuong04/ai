---
name: debugging-agent
models:
  error_capture: fast
  context_gathering: fast
  root_cause_analysis: reasoning
  fix_application: standard
  prevention: standard
description: "Autonomous agent for systematic error diagnosis, root cause analysis, and verified fix application. Handles stack trace parsing, context gathering, hypothesis formation, incremental fix verification, and recurrence prevention. Use when debugging errors, investigating failures, or diagnosing unexpected behavior. Triggers on 'debug this', 'why is this failing', 'fix this error', 'investigate this bug', 'diagnose this issue'."
---

# Debugging Agent

Autonomous workflow for systematic error diagnosis, root cause analysis, fix application with verification, and recurrence prevention.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/commands/development/debug-error.md`](ai/commands/development/debug-error.md) — Single-error debugging command with structured output format
2. [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md) — Clean code principles for writing quality fixes
3. [`ai/skills/testing/debugging/SKILL.md`](ai/skills/testing/debugging/SKILL.md) — Debugging techniques and strategies
4. [`ai/skills/tools/logging-observability/SKILL.md`](ai/skills/tools/logging-observability/SKILL.md) — Structured logging and observability patterns

**Verify:**
- [ ] Error is reproducible or a stack trace / error message is available
- [ ] Access to the failing codebase (files can be read and edited)
- [ ] Test runner is available or manual reproduction steps are known

---

## Purpose

Systematically diagnose and resolve errors with verified fixes:
1. Capture and classify errors into structured, actionable components
2. Gather surrounding context — source code, git history, dependencies, and related patterns
3. Perform root cause analysis using common error pattern matching and hypothesis ranking
4. Apply fixes incrementally with verification at each step
5. Prevent recurrence through tests, types, linting, and monitoring recommendations

**When NOT to use this agent:**
- Single obvious error with a clear fix (use `/debug-error` command instead)
- Writing tests for working code (use testing-agent instead)
- Refactoring code that works but is messy (use refactoring-agent instead)
- Performance optimization without errors (profile and benchmark directly)

---

## Activation

```
"debug this error"
"why is this failing"
"fix this error in [file/module]"
"investigate this bug"
"diagnose this issue"
"this keeps crashing, help"
```

---

## Workflow

### Phase 1: Error Capture

Parse the error input and extract structured fields for analysis.

**Capture from all available sources:**
```bash
# Check recent terminal output for errors
# Read the error message, stack trace, or description provided by the user
# If the user pasted a partial trace, search for the full output in terminal history
```

**Extract structured fields:**
| Field | Extract From | Example |
|-------|-------------|---------|
| Error message | First line or summary of the error | `TypeError: Cannot read properties of undefined (reading 'map')` |
| Error code | Named code (ENOENT, E0382, TS2345, etc.) | `ECONNREFUSED` |
| Error type | Classify into category | Runtime, compile, type, network, permission, syntax, dependency |
| Language/runtime | Infer from stack trace format and file extensions | Node.js, Python, Go, Rust, Java |
| File path | Absolute or relative path from stack trace | `src/services/auth.ts` |
| Line number | Line and column from stack trace | `42:17` |
| Function name | Function or method where the error occurred | `AuthService.validateToken` |
| Full stack trace | Complete call chain | All frames from error origin to entry point |

**Classify the error type:**
| Type | Indicators | Urgency |
|------|-----------|---------|
| Runtime | `TypeError`, `ReferenceError`, `panic`, `NullPointerException` | High — app crashes |
| Compile | `tsc`, `cargo check`, `go build` failures | High — app won't build |
| Type | `TS2345`, `TS2322`, `error[E0308]`, mypy errors | Medium — type mismatch |
| Network | `ECONNREFUSED`, `ETIMEDOUT`, `502`, `503` | High — service unavailable |
| Permission | `EPERM`, `EACCES`, `PermissionError`, `403` | Medium — access denied |
| Dependency | `ModuleNotFoundError`, `Cannot find module`, version conflicts | Medium — missing or incompatible package |
| Syntax | `SyntaxError`, `unexpected token`, parse failures | Low — typo or formatting |
| Data | `ValidationError`, constraint violations, malformed input | Medium — bad data in pipeline |

**Output:** Structured error record with all extracted fields populated.

**Validation:** Can answer: What is the exact error? What type is it? Where does it originate? What language/runtime is involved?

---

### Phase 2: Context Gathering

Build a comprehensive picture of the code and environment surrounding the error.

**Step 1 — Read the failing file:**
```bash
# Read the file referenced in the stack trace
# Include at least 50 lines above and below the error line for context
# If no file is referenced, search by error message
```

**Step 2 — Determine origin:**
| Path Contains | Origin | Action |
|---------------|--------|--------|
| `node_modules/`, `site-packages/`, `vendor/` | Dependency | Trace up the stack to the first project-owned frame |
| Project source directories | Project code | Analyze directly |
| Generated files (`dist/`, `build/`, `.next/`) | Build output | Find the corresponding source file |

**Step 3 — Check git history:**
```bash
# Recent changes to the failing file
git log --oneline -15 -- <failing-file>

# Diff of recent changes
git diff HEAD~5 -- <failing-file>

# Who last touched the failing lines
git blame -L <start>,<end> -- <failing-file>
```

**Step 4 — Search the codebase for related patterns:**
```bash
# Search for the same error message elsewhere
rg "<error-message>" --type-add 'src:*.{ts,py,go,rs,java}' -t src

# Find all callers of the failing function
rg "<function-name>" --type-add 'src:*.{ts,py,go,rs,java}' -t src

# Check for similar error handling patterns
rg "catch|except|recover|rescue" -- <failing-file>
```

**Step 5 — Check dependencies (if relevant):**
| File | Check |
|------|-------|
| `package.json` / `package-lock.json` | Node.js dependency versions and peer deps |
| `requirements.txt` / `pyproject.toml` | Python package versions |
| `go.mod` / `go.sum` | Go module versions |
| `Cargo.toml` / `Cargo.lock` | Rust crate versions |
| `Gemfile` / `Gemfile.lock` | Ruby gem versions |

**Step 6 — Check environment and configuration:**
- Verify environment variables referenced in the failing code
- Check configuration files (`.env`, `config.yaml`, etc.) for missing or invalid values
- Confirm runtime version matches project requirements

**Output:** Full context dossier — source code, git history, dependency state, and environment.

**Validation:** Can answer: What does the code do at the failure point? What changed recently? Are dependencies correct? Is the environment configured properly?

---

### Phase 3: Root Cause Analysis

Apply pattern matching and logical reasoning to identify the most likely cause.

**Match against common error patterns:**
| Pattern | Likely Cause | First Check |
|---------|-------------|-------------|
| `Cannot read properties of undefined` | Null/undefined in object chain | Trace variable to its assignment; check if async data loaded |
| `X is not a function` | Wrong import, typo, or version mismatch | Verify import statement and exported name |
| `ENOENT` / `FileNotFoundError` | Missing file or incorrect path | Verify path exists, check working directory |
| `ECONNREFUSED` | Target service not running | Check if database/API/service is up |
| `EADDRINUSE` | Port already in use | Find process on port: `lsof -i :<port>` |
| `ModuleNotFoundError` / `Cannot find module` | Missing install or wrong import path | Run install, check import path and tsconfig paths |
| `ENOMEM` / `heap out of memory` | Memory leak or unbounded data | Profile memory, check for infinite loops or large datasets |
| `EPERM` / `PermissionError` | Insufficient permissions | Check file ownership, process user, and chmod |
| `SyntaxError` / `unexpected token` | Malformed code, wrong file format, encoding | Check exact line for typos, BOM characters, mixed tabs/spaces |
| `TS2345` / `TS2322` | TypeScript type mismatch | Compare expected vs actual types at the call site |
| `panic: runtime error` (Go) | Nil pointer, index out of range | Check variable initialization and slice bounds |
| `error[E0382]` (Rust) | Use after move — borrow checker | Track ownership chain of the moved value |
| `CORS` / `Access-Control-Allow-Origin` | Cross-origin request blocked | Check server CORS configuration and request origin |
| `SIGKILL` / `OOMKilled` | Container or process exceeded memory limit | Check resource limits, optimize memory usage |

**Form hypotheses (generate 2–5):**

For each hypothesis, document:
```
### Hypothesis [N]: [Short title]
**Likelihood:** High | Medium | Low
**Reasoning:** [Why this could be the cause — reference specific code or patterns]
**Evidence:** [What in the error, code, or history supports this]
**Counter-evidence:** [What argues against this, if anything]
**Test:** [How to confirm or rule out this hypothesis]
```

**Rank hypotheses** by likelihood. Weight these signals:
| Signal | Weight |
|--------|--------|
| Recent git change touching the failing line | Highest |
| Error pattern matches a known cause exactly | High |
| Dependency version changed recently | High |
| Environment or configuration differs from expected | Medium |
| Code has no tests covering the failing path | Medium |
| Error only occurs in certain conditions (race, load, data) | Lower (harder to confirm) |

**Output:** Ranked list of hypotheses with evidence and test plan for each.

**Validation:** Each hypothesis is falsifiable — there is a concrete way to confirm or rule it out.

---

### Phase 4: Fix Application

Apply the most likely fix incrementally with verification at each step.

**Before modifying any code:**
```bash
# Record restore point
git stash list
git rev-parse HEAD

# Ensure we can rollback
git status
```

**For each hypothesis, starting with the highest ranked:**

1. **Announce** — State which hypothesis is being tested and what change will be made
2. **Apply** — Make the minimal, targeted code change
3. **Verify** — Run the reproduction steps to confirm the error is resolved:
   ```bash
   # Re-run the command or action that triggered the error
   <original-failing-command>

   # Run the test suite to check for regressions
   <test-runner>

   # Run the type checker if applicable
   <type-checker>
   ```
4. **Evaluate results:**
   - If error is resolved AND tests pass: **fix confirmed** — proceed to Phase 5
   - If error persists: **rollback**, move to next hypothesis
   - If error changes: **document the new error**, assess whether it is progress or a new issue

**Rollback procedure (on failure):**
```bash
# Revert uncommitted changes
git checkout -- <affected-files>

# If a commit was made, reset
git reset --soft HEAD~1
```

**Fix quality requirements:**
| Requirement | Rationale |
|------------|-----------|
| Minimal change — fewest lines possible | Reduces risk of introducing new bugs |
| No suppressing the error (no bare `try/catch`) | Catching without fixing masks the real problem |
| No deleting or rewriting large code blocks | Surgical fixes only; refactoring is a separate concern |
| Matches project code style and conventions | Fix should be indistinguishable from existing code |
| Includes a comment only if the fix is non-obvious | Explain *why*, not *what*, when warranted |

**After confirmed fix:**
```bash
# Stage and commit the fix
git add <affected-files>
git commit -m "fix: <concise description of what was fixed and why>"
```

**Output:** Verified fix committed to git with passing tests.

**Validation:** The original error no longer occurs. All tests pass. No new errors introduced.

---

### Phase 5: Prevention

Ensure the same class of error cannot recur undetected.

**Add targeted tests:**
```bash
# Write a test that reproduces the original error scenario
# The test should FAIL without the fix and PASS with it
# Include edge cases discovered during diagnosis
```

**Prevention measures by category:**
| Category | Action | Example |
|----------|--------|---------|
| Test coverage | Add unit test for the failing function | `it("handles undefined user gracefully", ...)` |
| Type safety | Add stricter types or null checks | `user: User \| null` with explicit null handling |
| Input validation | Add runtime validation at entry points | Zod schema, JSON schema, or manual validation |
| Error boundaries | Add structured error handling | React Error Boundary, Go error wrapping, Rust `Result<T, E>` |
| Linting rules | Enable or add lint rule catching the pattern | `@typescript-eslint/no-unsafe-member-access`, `clippy::unwrap_used` |
| Monitoring | Add logging or alerting at the failure point | Structured log with error context, Sentry breadcrumb |
| Documentation | Document the failure mode and fix | Code comment explaining the edge case |

**Verify prevention measures:**
```bash
# Run the new test(s)
<test-runner> --testPathPattern="<new-test-file>"

# Confirm the test fails when the fix is reverted (optional but recommended)
# Revert fix → run test → confirm failure → re-apply fix

# Run full suite to ensure nothing broke
<test-runner>
```

**Output:** Prevention measures applied and verified.

**Validation:** At least one new test guards against the original error. Prevention measures are appropriate to the error category.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No stack trace provided | Ask the user for one; search terminal history; grep the codebase for the error message |
| Error is not reproducible | Gather environment details, check for race conditions, review logs for intermittent patterns |
| File from stack trace does not exist locally | Check if it is from a dependency, generated code, or a different branch; locate the source equivalent |
| Error is too vague ("it doesn't work") | Ask: what command was run, what was expected, what happened instead, when did it last work |
| Multiple unrelated errors appear | Isolate the first error (usually the root cause); note the others for sequential investigation |
| Fix resolves the error but breaks tests | Rollback; analyze why the tests fail; the fix may be incorrect or tests may need updating (update tests only if they test the wrong behavior) |
| Error is in a dependency, not project code | Check for known issues in the dependency; verify version compatibility; consider pinning or upgrading |
| Error only occurs in CI / production | Compare environment differences; check env vars, OS, runtime version, and resource limits |
| Hypothesis testing is inconclusive | Gather more data — add logging, use a debugger, bisect with `git bisect` to find the introducing commit |
| Fix requires architectural change | Document the issue and proposed architectural change; escalate to the user rather than making sweeping changes |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Structured error analysis | Presented in chat | Classified error with extracted fields and context |
| Ranked hypotheses | Presented in chat | Transparent reasoning for the diagnosis |
| Verified code fix | Original source file(s) | Minimal change resolving the root cause |
| Fix commit | Git history | Traceable, reversible fix with descriptive message |
| Regression test | Test file per project convention | Guards against recurrence of the same error |
| Prevention recommendations | Presented in chat | Long-term measures to avoid the error class |

---

## Quality Checklist

Before marking the debugging workflow complete:

- [ ] Error is fully classified with structured fields (message, type, location, runtime)
- [ ] Context gathered from source code, git history, and dependencies
- [ ] At least 2 hypotheses formed with evidence and ranking
- [ ] Root cause identified and documented with reasoning
- [ ] Fix is minimal and targeted — no unnecessary changes
- [ ] Original error no longer occurs after fix
- [ ] Full test suite passes with no regressions
- [ ] Fix is committed with a descriptive message
- [ ] At least one regression test added for the failure scenario
- [ ] Prevention measures recommended appropriate to the error category
- [ ] No errors suppressed with bare try/catch or equivalent
- [ ] User informed of root cause, fix, and prevention steps

---

## Related

- **Command:** [`ai/commands/development/debug-error.md`](ai/commands/development/debug-error.md)
- **Skill:** [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md)
- **Skill:** [`ai/skills/testing/debugging/SKILL.md`](ai/skills/testing/debugging/SKILL.md)
- **Skill:** [`ai/skills/tools/logging-observability/SKILL.md`](ai/skills/tools/logging-observability/SKILL.md)
- **Agent:** [`ai/agents/testing/AGENT.md`](ai/agents/testing/AGENT.md)
- **Agent:** [`ai/agents/refactoring/AGENT.md`](ai/agents/refactoring/AGENT.md)

---

## NEVER Do

- **Never modify code before understanding the error** — Read the stack trace, gather context, and form hypotheses first. Blind changes waste time and introduce new bugs.
- **Never assume the error location is the root cause** — The stack trace shows where the error surfaced, not necessarily where it originated. Trace back through the call chain.
- **Never suppress errors without fixing the underlying issue** — Adding a `try/catch`, `recover`, or `rescue` block without resolving the cause hides the bug and makes future debugging harder.
- **Never apply multiple fixes simultaneously** — Test one hypothesis at a time. If multiple changes are applied, you cannot determine which one resolved the error.
- **Never skip the git history check** — A recent change is the most common cause of a new error. Always check `git log` and `git diff` on the failing file.
- **Never ignore dependency errors** — If the stack trace passes through `node_modules/`, `site-packages/`, or `vendor/`, trace back to the project code that invoked it. The bug is usually in how the dependency is called, not in the dependency itself.
- **Never delete or rewrite large blocks of code as a fix** — Debugging requires surgical, minimal changes. Large rewrites belong in a refactoring workflow with proper test coverage.
- **Never skip verification after applying a fix** — Always re-run the failing command and the full test suite. An unverified fix is no fix at all.
- **Never leave debugging without a prevention step** — Every resolved error is an opportunity to add a test, type guard, or lint rule that prevents the same class of bug from recurring.
