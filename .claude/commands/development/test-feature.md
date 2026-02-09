---
name: test-feature
model: standard
description: Generate comprehensive tests for a feature from its implementation
usage: /test-feature <feature>
---

# /test-feature

Generate tests for a feature based on its implementation.

## Usage

```
/test-feature <feature>
```

**Arguments:**
- `feature` — Feature name, file path, or short description of what to test

## Examples

```
/test-feature user-authentication
/test-feature src/services/payment.ts
/test-feature "the cart checkout flow"
/test-feature --recent                   # Test most recently changed files
```

## When to Use

- After implementing a new feature that lacks test coverage
- When adding tests to existing untested code
- Before submitting a PR to ensure adequate coverage
- When refactoring code and needing regression tests
- After fixing a bug (write a test that would have caught it)

## What It Does

1. **Identifies** the feature to test from the argument or recent git changes
2. **Reads** source files and analyzes function signatures, types, dependencies, and control flow
3. **Scans** the project for existing test patterns (framework, naming, directory structure, assertion style)
4. **Detects** the test framework from project configuration files
5. **Generates** comprehensive tests covering all code paths
6. **Writes** test files following the project's established conventions
7. **Runs** the tests to verify they pass
8. **Reports** results and coverage summary if tooling is available

## Implementation Steps

### Step 1: Resolve the Feature

Determine what source files to test.

- If the argument is a **file path**, use it directly. Confirm the file exists with Glob.
- If the argument is a **feature name**, search the codebase with Grep for modules, classes, or directories matching that name.
- If the argument is `--recent`, run `git diff --name-only HEAD~3` to find recently changed source files. Exclude test files, configs, and documentation from the list.
- If no argument is provided, ask the user what feature to test.

Use TodoWrite to create a task list tracking progress through all subsequent steps.

### Step 2: Analyze the Implementation

Read every source file identified in Step 1. For each file, extract:

- **Exported functions and classes** — names, parameter types, return types
- **Control flow branches** — if/else, switch, try/catch, early returns
- **Edge cases** — null checks, empty collections, boundary values, type guards
- **Error handling** — thrown exceptions, error returns, fallback behavior
- **External dependencies** — imports from other modules, API calls, database access, file I/O
- **Side effects** — mutations, event emissions, logging, state changes

Build a mental model of what the code does, not just what it looks like. Understand the contract each function fulfills.

### Step 3: Detect the Test Framework and Conventions

Search for test configuration in this priority order:

| Language | Config Files | Common Frameworks |
|----------|-------------|-------------------|
| JavaScript/TypeScript | `package.json`, `jest.config.*`, `vitest.config.*`, `.mocharc.*` | Jest, Vitest, Mocha |
| Python | `pyproject.toml`, `setup.cfg`, `pytest.ini`, `tox.ini` | pytest, unittest |
| Rust | `Cargo.toml` | built-in (`#[cfg(test)]`) |
| Go | `go.mod` | built-in (`testing`) |
| Java/Kotlin | `build.gradle*`, `pom.xml` | JUnit, TestNG |

Then scan existing test files to detect project conventions:

- **Test directory structure** — colocated (`__tests__/`, `*.test.*` next to source) or separate (`tests/`, `test/`)
- **Naming pattern** — `*.test.ts`, `*_test.go`, `test_*.py`, `*Test.java`
- **Assertion library** — built-in asserts, Chai, Jest matchers, AssertJ
- **Mocking approach** — Jest mocks, unittest.mock, testify mocks, manual fakes
- **Setup/teardown patterns** — beforeEach, fixtures, test factories
- **Import style** — relative vs absolute, path aliases

Match every convention exactly. New tests must look like they belong in the project.

### Step 4: Generate Tests

Write tests in this priority order:

#### 1. Happy Path Tests
Cover the primary use case for each public function. Verify correct output given valid input.

#### 2. Edge Case Tests
Cover boundary conditions and special inputs:
- Empty strings, zero values, empty arrays/maps
- Maximum and minimum values
- Single-element collections
- Unicode, special characters, whitespace
- Concurrent access (if applicable)

#### 3. Error Handling Tests
Verify every error path behaves correctly:
- Invalid input types and shapes
- Missing required fields
- Network failures and timeouts (mock these)
- Permission errors
- Malformed data

#### 4. Integration Point Tests
Mock external dependencies and verify interactions:
- Database calls return expected shapes
- API clients are called with correct arguments
- Event emitters fire expected events
- File I/O operations use correct paths

For each test:
- Write a descriptive name that states the scenario and expected outcome
- Follow the Arrange-Act-Assert pattern
- Keep each test focused on one behavior
- Avoid testing implementation details — test the contract

### Step 5: Write Test Files

Place test files according to the project's detected convention.

- Use Glob to verify the target directory exists before writing.
- If unsure about placement, check where existing tests for similar modules live.
- Include all necessary imports, mocks, and setup at the top of the file.
- Group related tests in describe/context blocks (or equivalent).

### Step 6: Run and Verify

Run the test suite using the project's test command:

```
# Detect from package.json scripts, Makefile, or standard commands
npm test
pytest
cargo test
go test ./...
```

Scope the run to only the new test files when possible to get fast feedback.

- If tests **pass**: report the results and proceed to coverage.
- If tests **fail**: read the failure output, fix the test (not the source code), and re-run.
- If the test runner is **not found**: inform the user and provide the test files for manual verification.

### Step 7: Report Results

Summarize what was generated:

```
Tests Generated
===============
Feature:     user-authentication
Files:       2 created
Tests:       14 total (8 unit, 6 integration)
Pass/Fail:   14 passed, 0 failed
Coverage:    src/auth/login.ts — 92% lines

New files:
  - src/auth/__tests__/login.test.ts
  - src/auth/__tests__/session.test.ts
```

Run coverage tools if available (`--coverage`, `pytest --cov`, `go test -cover`) and report uncovered lines.

## NEVER Do

- **NEVER modify source code** to make tests pass. Tests adapt to the implementation, not the reverse. If a test cannot pass without source changes, flag it to the user.
- **NEVER generate tests that test implementation details** (private methods, internal state). Test public interfaces and observable behavior only.
- **NEVER hardcode secrets, credentials, or real API keys** in test files. Use fixtures, environment stubs, or clearly fake values like `test-api-key-000`.
- **NEVER skip or `.only` tests** in the committed output. Every generated test must run as part of the suite.
- **NEVER create snapshot tests** unless the project already uses them. Snapshot tests are brittle and should be an explicit choice.
- **NEVER generate tests that depend on execution order.** Each test must pass in isolation.
- **NEVER ignore the project's existing patterns.** If the project uses `describe`/`it`, do not switch to `test()`. If fixtures go in `conftest.py`, do not inline them.
- **NEVER write trivial tests** that only assert `true === true` or test getter/setter boilerplate. Every test must verify meaningful behavior.

## Error Handling

| Problem | Resolution |
|---------|------------|
| Feature argument matches no files | Ask the user to provide a specific file path or broader description |
| No test framework detected | Check for a `Makefile`, `scripts/` directory, or ask the user what framework to use |
| Tests fail on first run | Read error output carefully. Fix mock setup, imports, or assertions. Do not modify source. Re-run up to 3 times. |
| No existing test patterns found | Use the framework's standard conventions as a baseline and inform the user |
| Source file has no exports or public API | Test the module's side effects or ask the user which internal functions to cover |
| Circular dependencies block mocking | Restructure mocks to break the cycle, or use dependency injection stubs |

## Output Locations

- Test files placed according to project convention (e.g., `__tests__/`, `tests/`, colocated)
- No other files created

## Related

- **New feature:** `/new-feature` (create a feature before testing it)
- **Skill:** [`testing-patterns`](ai/skills/testing/testing-patterns/SKILL.md) (test design and assertion patterns)
- **Skill:** [`e2e-testing-patterns`](ai/skills/testing/e2e-testing-patterns/SKILL.md) (end-to-end testing with Playwright and Cypress)
- **Development agent:** [`ai/agents/development/`](ai/agents/development/)
- **Methodology:** [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
