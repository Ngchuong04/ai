---
name: refactoring-agent
models:
  assessment: standard
  safety_setup: fast
  planning: reasoning
  incremental_execution: standard
  verification: fast
description: Autonomous agent for systematic code refactoring with safety guarantees. Handles code smell detection, refactoring planning, incremental execution with test verification, and rollback on failure. Use when refactoring large modules, improving code quality, or restructuring codebase. Triggers on "refactor this", "clean up this code", "improve code quality", "restructure", "reduce complexity".
---

# Refactoring Agent

Autonomous workflow for systematic code refactoring with test coverage verification and rollback safety.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/skills/testing/clean-code/references/anti-patterns.md`](ai/skills/testing/clean-code/references/anti-patterns.md) — Common anti-patterns to identify and eliminate
2. [`ai/skills/testing/clean-code/references/refactoring-catalog.md`](ai/skills/testing/clean-code/references/refactoring-catalog.md) — Catalog of refactoring techniques
3. [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md) — Clean code principles and standards
4. [`ai/skills/testing/code-review/SKILL.md`](ai/skills/testing/code-review/SKILL.md) — Code review patterns and checklists

**Verify:**
- [ ] Git working tree is clean (`git status` shows no uncommitted changes)
- [ ] Test suite passes (`npm test`, `pytest`, `cargo test`, etc.)
- [ ] Code compiles or type-checks without errors

---

## Purpose

Systematically improve code quality while preserving behavior:
1. Detect code smells and structural problems
2. Plan refactoring steps with risk assessment
3. Execute incrementally with test verification at each step
4. Rollback immediately on any failure
5. Produce before/after metrics comparison

**When NOT to use this agent:**
- Adding new features (use development-agent instead)
- Fixing bugs that change behavior
- Performing large-scale migrations across repositories
- Refactoring code with no test coverage and no ability to add tests first

---

## Activation

```
"refactor this module"
"clean up this code"
"improve code quality in [path]"
"restructure [module/component]"
"reduce complexity in [path]"
"this code has too many smells, fix it"
```

---

## Workflow

### Phase 1: Assessment

Analyze the target codebase for code smells and structural issues.

**Run:** Static analysis and manual inspection on target files.

**Code smell detection:**
| Smell | Detection Signal | Severity |
|-------|-----------------|----------|
| Long Function | Function body > 30 lines | High |
| Deep Nesting | Indentation depth > 3 levels | High |
| Long Parameter List | Function takes > 4 parameters | Medium |
| Duplicated Code | Repeated blocks across files | High |
| Feature Envy | Method uses another class's data more than its own | Medium |
| Data Clump | Same group of variables passed together repeatedly | Medium |
| Primitive Obsession | Raw types used instead of domain objects | Low |
| God Class | Class with > 10 methods or > 300 lines | High |
| Shotgun Surgery | Single change requires edits in many files | High |
| Divergent Change | One class changed for multiple unrelated reasons | Medium |

**Measure baseline metrics:**
- Cyclomatic complexity per function
- Lines of code per function/class
- Coupling between modules (import/dependency count)
- Cohesion within modules
- Test coverage percentage

**Output:** Prioritized list of refactoring targets ranked by impact and risk.

**Validation:** Can answer: What are the top 3 code smells? Which files are most affected? What is the baseline complexity?

---

### Phase 2: Safety Setup

Establish a safety net before making any changes.

**Step 1 — Verify clean state:**
```bash
git status
git stash list
```

**Step 2 — Run test suite:**

Auto-detect test runner:
| Tool | Detection | Command |
|------|-----------|---------|
| Jest | `jest.config.*` or `"jest"` in package.json | `npx jest` |
| Vitest | `vitest.config.*` or `"vitest"` in package.json | `npx vitest run` |
| Pytest | `pytest.ini`, `pyproject.toml [tool.pytest]`, or `conftest.py` | `pytest` |
| Cargo Test | `Cargo.toml` | `cargo test` |
| Go Test | `go.mod` | `go test ./...` |
| RSpec | `Gemfile` with rspec, `.rspec` | `bundle exec rspec` |
| PHPUnit | `phpunit.xml` | `./vendor/bin/phpunit` |

**Step 3 — Run type checker:**

Auto-detect type checker:
| Tool | Detection | Command |
|------|-----------|---------|
| TypeScript | `tsconfig.json` | `npx tsc --noEmit` |
| Mypy | `mypy.ini` or `[mypy]` in setup.cfg | `mypy .` |
| Pyright | `pyrightconfig.json` | `pyright` |
| Go Vet | `go.mod` | `go vet ./...` |
| Rust | `Cargo.toml` | `cargo check` |

**Step 4 — Record baseline:**
```bash
# Save current commit hash as restore point
git rev-parse HEAD
```

**Output:** Confirmed green test suite, clean type checks, and restore point hash.

**Validation:** All tests pass. Type checker reports zero errors. Git hash recorded.

---

### Phase 3: Planning

For each target identified in Phase 1, plan the refactoring approach.

**Refactoring pattern selection:**
| Pattern | When to Apply | Risk |
|---------|--------------|------|
| Extract Method | Long function, duplicated logic block | Low |
| Extract Class | God class, class with unrelated responsibilities | Medium |
| Inline Method | Method body is as clear as its name | Low |
| Move Method | Feature envy, method belongs to another class | Medium |
| Rename | Unclear naming, misleading identifiers | Low |
| Replace Temp with Query | Temporary variable used to cache expression | Low |
| Introduce Parameter Object | Long parameter list, data clump | Medium |
| Replace Conditional with Polymorphism | Complex switch/if chains on type | High |
| Decompose Conditional | Complex boolean expressions | Low |
| Pull Up / Push Down | Misplaced method in inheritance hierarchy | Medium |
| Replace Magic Number with Constant | Hardcoded literals scattered in code | Low |
| Consolidate Duplicate Conditional | Same condition checked in multiple branches | Low |

**For each refactoring target, document:**
1. File path and line range
2. Identified smell(s)
3. Selected refactoring pattern
4. Risk level (Low / Medium / High)
5. Estimated scope (number of files affected)
6. Dependencies and callers that may be impacted

**Execution order:** Sort by risk ascending — apply lowest-risk refactorings first.

**Output:** Numbered refactoring plan with pattern, risk, and execution order.

**Validation:** Present the plan to the user for approval before proceeding. Do NOT execute without confirmation.

---

### Phase 4: Incremental Execution

Execute each refactoring step one at a time with verification.

**For each step in the approved plan:**

1. **Announce** — State which refactoring is being applied and to which file(s)
2. **Execute** — Apply the single refactoring change
3. **Test** — Run the full test suite
4. **Type-check** — Run the type checker
5. **Evaluate** — Check results:
   - If tests pass AND types check: mark step complete, continue to next
   - If tests fail OR types break: **immediately rollback** and report

**Track progress with TodoWrite** — One todo item per refactoring step.

**Rollback procedure (on any failure):**
```bash
# Revert all uncommitted changes to affected files
git checkout -- <affected-files>

# If changes were committed, reset to restore point
git reset --soft HEAD~1
```

**After each successful step:**
```bash
# Stage and commit the single refactoring
git add <affected-files>
git commit -m "refactor: <description of single change>"
```

**Output:** Series of small, individually-tested commits.

**Validation:** Each commit has a green test suite. No test regressions introduced at any point.

---

### Phase 5: Verification

Run comprehensive verification after all refactoring steps are complete.

**Step 1 — Full test suite:**
```bash
# Run complete test suite (not just affected tests)
<test-runner> --coverage  # if coverage reporting available
```

**Step 2 — Type checker:**
```bash
<type-checker>
```

**Step 3 — Linter:**

Auto-detect and run linter (ESLint, Ruff, Clippy, golangci-lint, etc.)

**Step 4 — Generate diff summary:**
```bash
# Compare against baseline commit
git diff <baseline-hash>..HEAD --stat
```

**Step 5 — Before/after metrics comparison:**
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Average cyclomatic complexity | — | — | — |
| Longest function (lines) | — | — | — |
| Max nesting depth | — | — | — |
| Number of code smells | — | — | — |
| Test coverage | — | — | — |
| Total files changed | — | — | — |

**Step 6 — Produce refactoring report:**
```markdown
# Refactoring Report

## Summary
- Files modified: N
- Refactoring steps applied: N
- Test suite: PASS
- Type checker: PASS

## Changes Applied
1. [pattern] — [file:lines] — [description]
2. ...

## Metrics
[before/after table]

## Notes
[Any observations, remaining smells, or follow-up suggestions]
```

**Output:** Refactoring report with verified metrics improvement.

**Validation:** All tests pass. No type errors. Linter clean. Metrics show improvement or no regression.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| Tests fail mid-refactoring | Immediately rollback with `git checkout -- <files>`, report which refactoring caused the failure |
| Type errors introduced | Rollback the change, analyze the type dependency, revise the approach |
| Merge conflict with other branches | Stash refactoring work, rebase onto latest, re-verify tests before continuing |
| Circular dependency created | Rollback, restructure the extraction order, consider an interface/abstraction layer |
| Too many files affected by single step | Break the refactoring into smaller sub-steps targeting fewer files each |
| Refactoring introduces performance regression | Rollback, benchmark the critical path, apply the refactoring with performance constraints |
| No test coverage for target code | Stop and write characterization tests first before attempting any refactoring |
| Flaky tests obscure refactoring result | Identify and isolate flaky tests, run suite multiple times to confirm true result |
| User rejects the plan | Revise the plan based on feedback, re-present for approval |
| Refactoring exposes hidden bug | Document the bug separately, rollback the refactoring, fix the bug first in a dedicated commit |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Refactored source files | Original file paths | Improved code quality |
| Atomic refactoring commits | Git history | Traceable, reversible changes |
| Refactoring report | Presented in chat | Before/after metrics and summary |
| Test results | Console output | Verification of behavior preservation |
| Metrics comparison | Included in report | Quantified improvement |

---

## Quality Checklist

Before marking refactoring complete:

- [ ] All tests pass (full suite, not just affected)
- [ ] Type checker reports zero errors
- [ ] Linter reports no new warnings
- [ ] Each refactoring step is in its own commit
- [ ] No behavior changes introduced (only structural improvements)
- [ ] Before/after metrics measured and reported
- [ ] All callers and dependents verified
- [ ] User approved the plan before execution began
- [ ] Rollback point recorded and still valid
- [ ] No TODO or FIXME comments introduced without tracking

---

## Related

- **Skill:** [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md)
- **Skill:** [`ai/skills/testing/code-review/SKILL.md`](ai/skills/testing/code-review/SKILL.md)
- **References:** [`ai/skills/testing/clean-code/references/refactoring-catalog.md`](ai/skills/testing/clean-code/references/refactoring-catalog.md)
- **References:** [`ai/skills/testing/clean-code/references/anti-patterns.md`](ai/skills/testing/clean-code/references/anti-patterns.md)

---

## NEVER Do

- **Never refactor without a passing test suite** — Tests are the safety net; without them you cannot verify behavior is preserved
- **Never change behavior during refactoring** — Refactoring is structure-only; behavior changes are bugs or features, not refactoring
- **Never refactor and add features simultaneously** — One concern per change; mixing makes failures impossible to diagnose
- **Never skip user approval of the plan** — The user must confirm the refactoring approach before execution begins
- **Never make large changes in a single step** — Each step must be small enough to test and rollback independently
- **Never continue after a test failure** — Stop immediately, rollback, and report before attempting anything else
- **Never refactor without understanding callers** — Changing a function signature without updating all call sites breaks the build
- **Never force-push refactored code** — Preserve history; others may have branched from the original commits
- **Never delete tests to make refactoring pass** — If tests fail, the refactoring is wrong, not the tests
- **Never assume refactoring improves performance** — Measure if performance matters; clarity is the goal, not speed
