---
name: migrate-deps
model: standard
description: Dependency upgrades with breaking change analysis and migration steps
usage: /migrate-deps <package> [--to <version>] [--dry-run] [--all-outdated]
---

# /migrate-deps

Upgrade dependencies safely with breaking change analysis, automated migration, and verification.

## Usage

```
/migrate-deps <package> [--to <version>] [--dry-run] [--all-outdated]
```

**Arguments:**
- `package` — Package name to upgrade (e.g., `react`, `django`, `tokio`)
- `--to <version>` — Target version (default: latest stable)
- `--dry-run` — Preview the upgrade plan without making changes
- `--all-outdated` — Upgrade all outdated packages instead of a single one

## Examples

```
/migrate-deps react --to 19                    # Upgrade React to v19
/migrate-deps django                           # Upgrade Django to latest
/migrate-deps tokio --to 1.40 --dry-run        # Preview Tokio upgrade
/migrate-deps --all-outdated                   # Upgrade everything outdated
/migrate-deps next --to 15                     # Upgrade Next.js to v15
/migrate-deps flask --to 3.1                   # Upgrade Flask to 3.1
```

## When to Use

- Upgrading a major version of a core dependency
- Security advisories require bumping a dependency
- A new feature you need is only available in a newer version
- Keeping dependencies current as part of regular maintenance
- Migrating an entire project's outdated dependency tree

## What It Does

1. **Parses** the input to determine target package(s) and desired version
2. **Detects** the package manager and lockfile format
3. **Analyzes** the current dependency state (installed version, dependents, constraints)
4. **Researches** breaking changes between current and target versions
5. **Plans** the migration with ordered steps and code changes
6. **Executes** the upgrade and applies necessary code modifications
7. **Verifies** the upgrade with tests, type checks, and build

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Input

Determine what to upgrade and to which version.

- If `package` is provided, use it as the target. Normalize the name (e.g., `@scope/pkg`).
- If `--to` is specified, parse the version string. Accept semver (`3.2.1`), major-only (`19`), or range (`^5.0`).
- If `--all-outdated` is set, skip single-package logic — collect all outdated packages in Phase 3.
- If `--dry-run` is set, flag the session as read-only — no writes, no installs.
- If no arguments are provided, ask the user what package to upgrade.

### Phase 2: Detect Package Manager

Identify the package manager by scanning project root files with `Glob`.

| Indicator File | Package Manager | Lockfile |
|----------------|----------------|----------|
| `package.json` + `package-lock.json` | npm | `package-lock.json` |
| `package.json` + `yarn.lock` | yarn | `yarn.lock` |
| `package.json` + `pnpm-lock.yaml` | pnpm | `pnpm-lock.yaml` |
| `requirements.txt` or `requirements/*.txt` | pip | — |
| `pyproject.toml` with `[tool.poetry]` | poetry | `poetry.lock` |
| `pyproject.toml` with `[project]` | uv / pip | `uv.lock` |
| `Cargo.toml` | cargo | `Cargo.lock` |
| `go.mod` | go mod | `go.sum` |
| `composer.json` | composer | `composer.lock` |
| `Gemfile` | bundler | `Gemfile.lock` |

If multiple indicators are found (e.g., both `yarn.lock` and `package-lock.json`), prefer the lockfile that exists. If ambiguous, ask the user.

### Phase 3: Analyze Current State

Gather information about the current dependency situation.

**3a. Current version**

Read the manifest file (`package.json`, `pyproject.toml`, etc.) to find the currently specified version constraint. Then read the lockfile to find the exact installed version.

**3b. Target version**

If `--to` was specified, use that version. Otherwise, query the latest stable version:

```
npm view <pkg> version
pip index versions <pkg>
cargo search <pkg> --limit 1
go list -m -versions <module>
composer show <pkg> --available
gem search <pkg> --versions
```

**3c. Semver analysis**

Compare current and target versions to classify the upgrade:

| Change Type | Semver | Risk Level | Typical Impact |
|-------------|--------|------------|----------------|
| Patch | `1.2.3` → `1.2.4` | Low | Bug fixes only |
| Minor | `1.2.3` → `1.3.0` | Low–Medium | New features, no breaking changes |
| Major | `1.2.3` → `2.0.0` | High | Breaking changes expected |
| Pre-release | `1.2.3` → `2.0.0-rc.1` | Very High | Unstable API, incomplete changes |

**3d. Dependency tree impact**

Use `Grep` to find every file that imports or references the package. Count the number of direct usages across the codebase to estimate migration scope.

If `--all-outdated`, run the package manager's outdated command to collect the full list:

```
npm outdated --json
pip list --outdated --format=json
cargo outdated (if installed)
go list -m -u all
composer outdated --format=json
bundle outdated
```

### Phase 4: Research Breaking Changes

For major and minor upgrades, research what changed between versions.

**4a. Changelog and release notes**

Use `Bash` to fetch changelog information:

```
# Check local changelog first
cat CHANGELOG.md | head -200
# Or from the package's repository
gh release list --repo <owner>/<repo> --limit 20
gh release view <tag> --repo <owner>/<repo>
```

Use `WebSearch` or `WebFetch` if the changelog is hosted online (e.g., GitHub releases page, migration guide URL).

**4b. Migration guide**

Search for official migration guides. Common locations:

- `MIGRATION.md` or `UPGRADE.md` in the repository
- Docs site (e.g., `reactjs.org/blog`, `docs.djangoproject.com/en/stable/releases/`)
- GitHub release body for the major version tag

**4c. Classify breaking changes**

Organize findings into a migration impact table:

| Change Category | Description | Detection Method |
|----------------|-------------|------------------|
| API changes | Function signatures renamed, parameters added/removed | `Grep` for old function names |
| Config format changes | Configuration keys renamed, restructured, or removed | `Read` config files, compare to new schema |
| Import path changes | Module paths moved or reorganized | `Grep` for old import paths |
| Removed features | Functions, classes, or options deleted entirely | `Grep` for removed APIs |
| Default behavior changes | Existing options now produce different results | Review changelog, test output differences |
| Type signature changes | TypeScript/type annotation incompatibilities | Run type checker after upgrade |
| Peer dependency changes | Required companion packages added or version-bumped | Read `peerDependencies` in new version |

### Phase 5: Plan Migration

Build an ordered migration plan based on findings from Phase 4.

For each breaking change identified:

1. List every file affected (from Phase 3d grep results).
2. Describe the exact code transformation required.
3. Note whether the change is mechanical (find-and-replace) or requires judgment.

Present the plan to the user:

```
Migration Plan: react 18.2.0 → 19.0.0
=======================================
Risk level:    High (major version)
Files affected: 23
Breaking changes: 4

Step 1: Update import paths (12 files) — mechanical
  - `import { render } from 'react-dom'` → `import { createRoot } from 'react-dom/client'`

Step 2: Replace deprecated API calls (8 files) — mechanical
  - `ReactDOM.render(...)` → `createRoot(...).render(...)`

Step 3: Update type definitions (3 files) — requires review
  - `React.FC` children prop no longer implicit

Step 4: Update config (1 file) — mechanical
  - Add `react-dom/client` to jest moduleNameMapper
```

If `--dry-run` is set, output the plan and stop here. Do not proceed to Phase 6.

### Phase 6: Execute Upgrade

Execute the plan step by step with verification between each step.

**6a. Update the manifest**

Run the package manager's upgrade command:

```
npm install <pkg>@<version>
yarn add <pkg>@<version>
pnpm add <pkg>@<version>
pip install <pkg>==<version>
poetry add <pkg>@<version>
cargo update -p <pkg>
go get <module>@<version>
composer require <pkg>:<version>
bundle update <pkg>
```

**6b. Apply code changes**

For each step in the migration plan:

1. Use `Edit` to apply the code transformation.
2. Prefer `replace_all` for mechanical find-and-replace changes across a file.
3. For complex changes, edit one occurrence first, verify it compiles, then apply to remaining files.
4. Update the `TodoWrite` list after each step.

**6c. Update companion dependencies**

If the upgrade requires bumping peer dependencies or companion packages (e.g., `@types/react`, `react-dom`, `django-rest-framework`), install those as well.

### Phase 7: Verify and Report

Run the full verification suite to confirm the upgrade succeeded.

**7a. Install and resolve**

```
npm install   # or equivalent
```

Verify the lockfile updated cleanly with no unresolved conflicts.

**7b. Type check**

Detect and run the type checker:

| Indicator | Command |
|-----------|---------|
| `tsconfig.json` | `npx tsc --noEmit` |
| `mypy.ini` or `pyproject.toml` [tool.mypy] | `mypy .` |
| `pyrightconfig.json` | `pyright` |

**7c. Test suite**

Run the project's test suite:

| Indicator | Command |
|-----------|---------|
| `package.json` with `jest` | `npx jest` |
| `package.json` with `vitest` | `npx vitest run` |
| `pytest.ini` or `pyproject.toml` [tool.pytest] | `pytest` |
| `Cargo.toml` | `cargo test` |
| `go.mod` | `go test ./...` |
| `Makefile` with `test` target | `make test` |

**7d. Build**

Run the build command if one exists:

```
npm run build
cargo build
go build ./...
```

**7e. Report**

Output a final summary:

```
Migration Complete
==================
Package:       react 18.2.0 → 19.0.0
Risk level:    High (major version)
Files changed: 23
Code changes:  47 edits across 4 migration steps

Verification:
  Install:     Clean (0 warnings)
  Types:       Clean
  Tests:       142 passed, 0 failed
  Build:       Success

Migration notes:
  - Replaced ReactDOM.render with createRoot API (12 files)
  - Updated implicit children prop in React.FC types (3 files)
  - Bumped @types/react to 19.0.0 and react-dom to 19.0.0
  - Updated jest config for new react-dom/client entry point
```

## NEVER Do

| Rule | Reason |
|------|--------|
| **NEVER upgrade without checking the current test baseline** | A failing test suite before the upgrade makes it impossible to verify the migration |
| **NEVER skip breaking change research for major versions** | Blindly upgrading a major version leads to runtime failures and subtle bugs |
| **NEVER upgrade all packages at once without `--all-outdated`** | Bulk upgrades make it impossible to isolate which package caused a failure |
| **NEVER delete the lockfile to resolve conflicts** | Lockfiles ensure reproducible builds — regenerating from scratch can introduce unrelated version changes |
| **NEVER force-install with `--legacy-peer-deps` or `--force` without warning** | These flags hide real incompatibilities that will surface at runtime |
| **NEVER modify test assertions to make them pass after an upgrade** | If tests fail, the migration has a problem — fix the migration, not the tests |
| **NEVER upgrade to pre-release or unstable versions without explicit user consent** | Pre-release versions may have incomplete features or undocumented breaking changes |
| **NEVER proceed past Phase 5 when `--dry-run` is set** | Dry run means read-only — no installs, no file edits, no side effects |

## Error Handling

| Situation | Action |
|-----------|--------|
| Package not found in registry | Verify the package name and registry URL. Check for scope prefix (`@org/pkg`) or typos. |
| Dependency version conflict | Display the conflict tree. Suggest compatible version ranges. Try resolving with `--legacy-peer-deps` only after user approval. |
| Peer dependency mismatch | List the peer requirements of the new version. Upgrade peer dependencies first, then retry. |
| Lockfile merge conflict | Run `git checkout --theirs <lockfile>` then re-run install. Verify resolved versions match expectations. |
| Tests fail after upgrade | Diff the test output against baseline. Identify whether failures are from removed APIs, changed defaults, or type mismatches. Apply targeted fixes. |
| Build fails after upgrade | Check compiler output for deprecated APIs or changed module paths. Cross-reference with Phase 4 findings. |
| Type errors after upgrade | Run the type checker and collect all errors. Group by root cause (e.g., a single changed type definition may cascade). Fix the root type first. |
| Network failure during install | Retry once. If persistent, check registry availability and proxy settings. Suggest `--offline` if cached packages are available. |
| Circular dependency introduced | Display the cycle. Check if the new version restructured its exports. May require import path adjustments. |

## Output

- Updated dependency manifest (`package.json`, `pyproject.toml`, `Cargo.toml`, etc.)
- Updated lockfile (`package-lock.json`, `poetry.lock`, `Cargo.lock`, etc.)
- Modified source files with migration changes applied
- Migration summary listing every change made and why
- Test and build results confirming the upgrade is stable

## Related

- **Command:** `/refactor` (for structural code changes triggered by a migration)
- **Command:** `/test-feature` (to verify affected features after an upgrade)
- **Command:** `/debug-error` (when migration introduces runtime errors)
- **Command:** `/new-adr` (to document significant dependency upgrade decisions)
