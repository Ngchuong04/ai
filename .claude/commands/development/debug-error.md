---
name: debug-error
model: standard
description: Structured error debugging and root cause analysis
usage: /debug-error <error>
---

# /debug-error

Systematically debug an error through structured analysis, root cause investigation, and ranked fix suggestions.

## Usage

```
/debug-error <error>
```

**Arguments:**
- `error` — Error message, stack trace, or description (paste directly, quote, or describe)

## Examples

```
/debug-error "TypeError: Cannot read properties of undefined (reading 'map')"
/debug-error "ECONNREFUSED 127.0.0.1:5432"
/debug-error "panic: runtime error: index out of range [3] with length 2"
/debug-error "error[E0382]: borrow of moved value: `data`"
/debug-error the build fails with a module not found error on line 42 of server.ts
```

## What It Does

1. **Captures** error context from the argument, clipboard paste, or recent terminal output
2. **Parses** the error message, error code, and stack trace into structured components
3. **Classifies** the error type (runtime, compile, type, network, permission, dependency, syntax)
4. **Locates** the failing code by extracting file paths and line numbers from the stack trace
5. **Reads** the failing source file and surrounding context (50 lines above and below)
6. **Checks** recent git changes with `git log --oneline -20` and `git diff` on the failing file
7. **Searches** the codebase for related error patterns and similar failures
8. **Determines** whether the error originates in project code or in dependencies
9. **Generates** a ranked list of hypotheses with reasoning for each
10. **Provides** concrete code fixes for each hypothesis, ranked by likelihood
11. **Suggests** verification steps and test commands for each fix
12. **Recommends** prevention measures (tests, types, linting rules)

## Implementation Steps

Use TodoWrite to track each debugging phase. Mark each step in_progress before starting and completed when done.

### Phase 1: Error Capture and Classification

Parse the error input and extract structured fields:

| Field | Extract From |
|-------|-------------|
| Error message | First line or summary of the error |
| Error code | Named code like ENOENT, E0382, TS2345 |
| Error type | Runtime, compile, type, network, permission, syntax, dependency |
| Language/runtime | Node.js, Python, Go, Rust, etc. — infer from stack trace format |
| File path | Absolute or relative path from stack trace |
| Line number | Line and column from stack trace |
| Function name | Function or method where the error occurred |
| Full stack trace | Complete call chain for context |

### Phase 2: Context Gathering

1. **Read the failing file.** Open the file from the stack trace. Read at least 50 lines above and below the error line to understand the surrounding logic.
2. **Check project vs dependency.** If the file path contains `node_modules/`, `site-packages/`, `vendor/`, or similar, trace back up the stack to the first project-owned frame.
3. **Read related files.** Follow imports and function calls from the failing line to understand data flow.
4. **Check recent changes.** Run `git log --oneline -20 -- <failing-file>` and `git diff HEAD~5 -- <failing-file>` to find recent modifications.
5. **Search for patterns.** Grep the codebase for the same error message, similar error handling, or related function calls.
6. **Check dependencies.** If the error involves a module or package, verify versions in `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, or equivalent.

### Phase 3: Root Cause Analysis

Apply the **common error pattern table** below to match known patterns before forming hypotheses:

| Pattern | Likely Cause | First Check |
|---------|-------------|-------------|
| `ENOENT` / `FileNotFoundError` | Missing file or wrong path | Verify the path exists, check cwd |
| `ECONNREFUSED` | Service not running | Check if the target service is up |
| `EADDRINUSE` | Port conflict | Find and stop the process on that port |
| `TypeError: Cannot read properties of undefined` | Null/undefined access on object chain | Trace the variable back to its source |
| `TypeError: X is not a function` | Wrong import, typo, or version mismatch | Check import statement and export name |
| `SyntaxError` | Malformed code or wrong file format | Check the exact line for typos or encoding |
| `ModuleNotFoundError` / `Cannot find module` | Missing install or wrong path | Run install command, check import path |
| `ENOMEM` / `heap out of memory` | Memory leak or dataset too large | Profile memory, check for unbounded growth |
| `EPERM` / `PermissionError` | Insufficient file/network permissions | Check file ownership and process user |
| `panic: runtime error` (Go) | Nil pointer, index out of range, or type assertion | Check the variable at the panic line |
| `error[E0382]` (Rust) | Borrow checker — use after move | Track ownership of the moved value |
| `TS2345` / `TS2322` (TypeScript) | Type mismatch | Compare expected vs actual types |
| `segfault` / `SIGSEGV` | Null pointer dereference or buffer overflow | Run with address sanitizer if possible |

### Phase 4: Hypothesis Formation

Generate 2-5 hypotheses. For each one, include:

```
### Hypothesis [N]: [Short title]
**Likelihood:** High | Medium | Low
**Reasoning:** [Why this could be the cause — reference specific code or patterns]
**Evidence:** [What in the error or code supports this]
**Counter-evidence:** [What argues against this, if anything]
```

Rank hypotheses from most to least likely.

### Phase 5: Fix Suggestions

For each hypothesis, provide a concrete fix:

```
### Fix for Hypothesis [N]: [Title]
**File:** [path/to/file.ext]
**Change:** [Description of what to change]

[Exact code diff or edit to apply]

**Why this fixes it:** [Explanation connecting the fix to the root cause]
```

### Phase 6: Verification

For each fix, provide:

1. **Manual test** — a specific command to run or action to take
2. **Automated test** — a test case to add that guards against regression
3. **Smoke check** — the simplest possible way to confirm the fix worked

```
# Verify fix N
[specific command, e.g., npm test, go test ./..., cargo check]

# Reproduce the original error (should now pass)
[command that originally triggered the error]
```

### Phase 7: Prevention

Suggest at least one measure from each category when applicable:

| Category | Example |
|----------|---------|
| **Type safety** | Add TypeScript strict mode, Go interface checks, Rust lifetime annotations |
| **Tests** | Unit test for the failing function, integration test for the flow |
| **Linting** | ESLint rule, clippy lint, golangci-lint check |
| **Runtime guards** | Input validation, null checks, error boundary |
| **Monitoring** | Error tracking, structured logging at the failure point |

## Output

All output goes to the terminal. No files are created unless a fix is applied.

The final output follows this structure:

```
Error Analysis
==============

Error:     [parsed error message]
Type:      [error classification]
Location:  [file:line:column]
Runtime:   [language/runtime detected]
Origin:    [project code | dependency]

Root Cause
----------
[Most likely explanation in 1-2 sentences]

Hypotheses (ranked)
-------------------
1. [High]   — [title and one-line summary]
2. [Medium] — [title and one-line summary]
3. [Low]    — [title and one-line summary]

Recommended Fix
---------------
[Code diff for the highest-ranked hypothesis]

Verification
------------
[Commands to run]

Prevention
----------
[Specific recommendations]
```

## NEVER Do

- **Never modify code without understanding the error first.** Read and analyze before proposing any change.
- **Never assume the error location is the root cause.** The stack trace shows where it failed, not always why.
- **Never ignore dependency errors.** If the error is in `node_modules` or `vendor`, trace back to the project code that called into it.
- **Never skip the git history check.** A recent change is the most common cause of a new error.
- **Never apply multiple fixes at once.** Suggest them in ranked order. Apply one, verify, then move to the next if needed.
- **Never suppress or catch the error without fixing the underlying issue.** A `try/catch` or `recover` is not a fix.
- **Never delete or rewrite large blocks of code to "fix" an error.** Targeted, minimal changes only.

## Error Handling

- If no stack trace is provided, ask for one or search the codebase for the error message.
- If the file referenced in the stack trace does not exist locally, note it and check if it is from a dependency or generated code.
- If the error is too vague to classify (e.g., "it doesn't work"), ask specific follow-up questions: what command was run, what was the expected behavior, what happened instead.
- If multiple unrelated errors appear, pick the first one (usually the root cause) and note the others for later.

## Related

- **Feature development:** `/new-feature` (if the error blocks a feature)
- **Architecture decisions:** `/new-adr` (if the fix requires an architectural change)
- **Agent:** [`ai/agents/development/`](ai/agents/development/)
