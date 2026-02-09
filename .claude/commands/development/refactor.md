---
name: refactor
model: reasoning
description: Systematic code refactoring with safety checks and incremental verification
usage: /refactor <target>
---

# /refactor

Refactor code systematically with safety guarantees — never break working code.

## Usage

```
/refactor <target>
```

**Arguments:**
- `target` — File path, function name, class name, or description of what to refactor

## Examples

```
/refactor src/utils/auth.ts                    # Refactor entire file
/refactor processPayment                       # Refactor a specific function
/refactor "the validation logic in UserForm"   # Refactor by description
/refactor src/api/handlers.py::create_order    # Refactor specific function in file
```

## When to Use

- Code smells detected (long functions, deep nesting, duplication)
- Before adding new features to tangled code
- After a feature is working but the implementation is messy
- When test coverage is sufficient to refactor safely
- When code review feedback requests structural changes

## What It Does

1. **Locates** target code and maps its dependencies
2. **Verifies** safety baseline (tests pass, types check, git clean)
3. **Analyzes** code smells and improvement opportunities
4. **Plans** refactoring steps and presents for approval
5. **Executes** changes incrementally with test verification after each step
6. **Validates** final state (tests, types, linter, diff summary)
7. **Reports** what changed and why

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Identify Target

- Read the `target` argument — resolve to specific file(s) and code regions.
- Use `Grep` and `Glob` to locate the code if a function name or description is given.
- Use `Read` to examine the target code and surrounding context.
- Identify the language and framework in use.

### Phase 2: Pre-Refactoring Safety Checks

Run all three checks. All must pass before proceeding.

**2a. Git status**
```
git status
git diff --stat
```
Verify the working tree is clean. If there are uncommitted changes, stop and warn:
> "Uncommitted changes detected. Commit or stash before refactoring."

**2b. Test baseline**

Detect the project's test runner automatically:

| Indicator | Runner |
|-----------|--------|
| `package.json` with `jest` | `npx jest` |
| `package.json` with `vitest` | `npx vitest run` |
| `pytest.ini` or `pyproject.toml` [tool.pytest] | `pytest` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |
| `Makefile` with `test` target | `make test` |

Run the test suite. If any test fails, stop and warn:
> "Baseline tests failing. Fix tests before refactoring."

**2c. Type checking**

Detect and run the type checker if present:

| Indicator | Checker |
|-----------|---------|
| `tsconfig.json` | `npx tsc --noEmit` |
| `mypy.ini` or `pyproject.toml` [tool.mypy] | `mypy .` |
| `pyrightconfig.json` | `pyright` |

If type checking fails, warn but allow the user to decide whether to proceed.

### Phase 3: Analyze the Code

Use `Read` to examine the target code thoroughly. Identify:

- **Code smells** — long methods, deep nesting, duplicated logic, god objects, feature envy, primitive obsession, shotgun surgery
- **Dependencies** — use `Grep` to find all callers and imports of the target
- **Scope** — list every file that will be affected by the refactoring
- **Complexity** — count branches, nesting depth, function length

Present findings as a brief summary:

```
Refactoring Analysis: processPayment()
=======================================
Location:     src/services/payment.ts:42-138
Lines:        96 (recommended max: 20)
Complexity:   12 branches, 4 levels deep
Callers:      3 files (checkout.ts, subscription.ts, retry.ts)
Code smells:  Long method, deep nesting, mixed abstraction levels

Suggested refactorings:
  1. Extract validatePaymentInput() — lines 45-67
  2. Extract callPaymentGateway() — lines 68-95
  3. Extract handlePaymentResult() — lines 96-130
  4. Simplify conditional at line 72 (guard clause)
```

### Phase 4: Plan and Get Approval

Choose from these refactoring patterns (reference `clean-code` skill for principles):

| Pattern | When to Use |
|---------|-------------|
| **Extract Method** | Long function, mixed abstraction levels |
| **Extract Variable** | Complex expression, unclear intent |
| **Inline** | Over-abstracted, single-use wrapper |
| **Rename** | Name does not reveal intent |
| **Move** | Function in wrong module/class |
| **Guard Clause** | Deep nesting from conditionals |
| **Replace Conditional with Polymorphism** | Switch/if chains on type |
| **Decompose Conditional** | Complex boolean logic |
| **Consolidate Duplicate** | Same logic in multiple places |
| **Replace Magic Number** | Unnamed literals |

Present the plan as numbered steps. Wait for user approval before proceeding:

> "Here is the refactoring plan. Approve to proceed, or suggest changes."

### Phase 5: Execute Incrementally

For each step in the approved plan:

1. Make the change using `Edit` (prefer small, focused edits).
2. Run the test suite with `Bash`.
3. If tests pass, move to the next step.
4. If tests fail, **immediately roll back** the change and report:
   > "Tests failed after [step]. Rolling back. Here is the failure: ..."

Keep the `TodoWrite` list updated after each step completes.

### Phase 6: Post-Refactoring Verification

Run the full verification suite:

1. **Tests** — run the full test suite (same runner as Phase 2b).
2. **Type checker** — run if available (same as Phase 2c).
3. **Linter** — detect and run:

| Indicator | Linter |
|-----------|--------|
| `.eslintrc*` or `eslint.config.*` | `npx eslint .` |
| `ruff.toml` or `pyproject.toml` [tool.ruff] | `ruff check .` |
| `pylintrc` or `.pylintrc` | `pylint` |
| `.golangci.yml` | `golangci-lint run` |
| `clippy` (Rust) | `cargo clippy` |

4. **Diff summary** — run `git diff --stat` to show what changed.

### Phase 7: Report Results

Output a summary:

```
Refactoring Complete
====================
Target:        processPayment() in src/services/payment.ts
Steps:         4 of 4 completed
Tests:         47 passed, 0 failed
Type check:    Clean
Linter:        Clean

Changes:
  src/services/payment.ts       | 96 → 28 lines (extracted 3 functions)
  src/services/payment-utils.ts | +68 lines (new helper module)

Patterns applied:
  - Extract Method (x3)
  - Guard Clause (x1)
```

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER refactor without a passing test suite** | No safety net means no safe refactoring |
| **NEVER change behavior** | Refactoring preserves external behavior by definition |
| **NEVER refactor and add features simultaneously** | One change type at a time — refactor, then feature |
| **NEVER skip the approval step** | The user must review the plan before changes begin |
| **NEVER make large changes in a single step** | Incremental changes with test runs after each step |
| **NEVER continue after a test failure** | Stop, roll back, report, and reassess |
| **NEVER refactor without understanding callers** | Changing signatures breaks downstream code |

## Error Handling

| Situation | Action |
|-----------|--------|
| Dirty working tree | Stop. Instruct user to commit or stash. |
| Baseline tests fail | Stop. Instruct user to fix tests first. |
| No tests found | Warn strongly. Ask user whether to proceed without safety net. |
| Tests fail mid-refactor | Roll back the last change. Report the failure. Ask how to proceed. |
| Type errors introduced | Roll back. Investigate the type mismatch before retrying. |
| Merge conflict in target file | Stop. Instruct user to resolve conflicts first. |

### Rollback Procedure

If any step fails and changes need to be undone:

```
git checkout -- <affected-files>
```

Then re-run the test suite to confirm the rollback restored a passing state.

## Output

- No files created — modifies existing files in place
- All changes visible via `git diff` after completion

## Related

- **Skill:** [`clean-code`](ai/skills/testing/clean-code/SKILL.md) (refactoring patterns and code quality principles)
- **Skill:** [`reducing-entropy`](ai/skills/testing/reducing-entropy/SKILL.md) (minimize codebase complexity and size)
- **Command:** `/new-feature` (for when refactoring leads to new capability)
- **Command:** `/update-roadmap` (to track refactoring tasks)
