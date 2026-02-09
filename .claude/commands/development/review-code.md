---
name: review-code
model: reasoning
description: AI-assisted code review with multi-dimensional best-practice analysis
usage: /review-code [target]
---

# /review-code

Perform a structured, multi-dimensional code review with actionable findings.

## Usage

```
/review-code [target]
```

**Arguments:**
- `target` (optional) — File path, directory path, branch name, or PR number

## Examples

```
/review-code src/auth/login.ts          # Review a single file
/review-code src/api/                    # Review all files in a directory
/review-code feature/payment-flow        # Review diff against main for a branch
/review-code #142                        # Review PR #142 diff
/review-code                             # Review staged changes or last commit
```

## What It Does

1. **Determines** scope of review based on the target argument:
   - File or directory path: read and review that code directly
   - Branch name: diff the branch against `main` (or default branch)
   - PR number (prefixed with `#`): fetch the PR diff via `gh pr diff`
   - No argument: review staged changes (`git diff --cached`); if none, review the last commit (`git diff HEAD~1`)
2. **Gathers** project context before reviewing:
   - Read config files for conventions (`.editorconfig`, `.eslintrc`, `tsconfig.json`, `biome.json`, `.prettierrc`, `pyproject.toml`, etc.)
   - Check for `CONTRIBUTING.md`, `docs/code-style.md`, or similar guides
   - Identify the language, framework, and test runner in use
3. **Analyzes** the code across six dimensions (see Review Dimensions below)
4. **Categorizes** every finding by severity with a concrete fix
5. **Generates** a structured review report (see Output Format below)

## Review Dimensions

Evaluate every piece of code under review against all six dimensions. Skip a dimension only when it is genuinely irrelevant to the change.

### Correctness
- Logic errors, off-by-one mistakes, wrong operator precedence
- Null/undefined handling — missing guards, unsafe optional chaining
- Race conditions, deadlocks, or unhandled async edge cases
- Incorrect error propagation (swallowed errors, wrong error types)
- Boundary conditions and type coercion surprises

### Security
- Unsanitized user input flowing into SQL, HTML, shell commands, or file paths
- Missing or incorrect authentication and authorization checks
- Sensitive data (tokens, passwords, PII) logged, exposed in URLs, or committed
- Insecure cryptographic defaults (weak hashing, hardcoded secrets)
- CORS misconfiguration, CSRF gaps, insecure deserialization

### Performance
- N+1 query patterns or unbounded database fetches
- Unnecessary iterations, redundant computations inside loops
- Missing pagination on list endpoints or UI renders
- Memory leaks (unclosed streams, dangling listeners, growing caches)
- Absent caching where repeated expensive work is obvious

### Maintainability
- Cyclomatic complexity — functions doing too many things
- Poor naming (ambiguous variables, misleading function names)
- Code duplication that should be extracted
- Tight coupling between unrelated modules
- Magic numbers or strings without constants or enums

### Testing
- Are new code paths covered by tests?
- Are edge cases and error paths tested?
- Is mocking appropriate (not mocking the thing under test)?
- Are assertions specific (not just "does not throw")?
- Snapshot tests that mask real behavior changes

### Documentation
- Are public API functions and types documented?
- Is complex or non-obvious logic explained with comments?
- Are breaking changes noted in changelogs or migration guides?
- Do README or usage docs reflect the current behavior?

## Implementation Steps

Follow these steps in order. Do not skip the context-gathering phase.

### Step 1 — Resolve the Review Target

```
IF target is a file or directory path:
  Read the files directly
ELSE IF target starts with '#':
  Run: gh pr diff <number>
ELSE IF target looks like a branch name:
  Run: git diff main...<branch>
ELSE (no argument):
  Run: git diff --cached
  IF empty:
    Run: git diff HEAD~1
```

### Step 2 — Gather Project Context

Scan the repository root and common locations for:
- Linter and formatter configs
- `CONTRIBUTING.md` or code-style docs
- `tsconfig.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, or equivalent
- Test directory structure and test runner configuration

Use this context to calibrate findings. Do not flag style issues that contradict the project's own configuration.

### Step 3 — Perform the Review

Walk through the code or diff methodically. For each finding:
1. Identify the dimension it falls under
2. Assign a severity level
3. Reference the specific file and line
4. Describe the problem in one sentence
5. Provide a concrete fix (code snippet or clear instruction)

### Step 4 — Compile Praise

Identify at least one positive aspect of the code. Look for:
- Clean abstractions or well-chosen patterns
- Thorough error handling
- Good test coverage
- Clear naming or helpful comments
- Smart use of language or framework features

### Step 5 — Assemble the Report

Format the output according to the Output Format section below.

## Output Format

```markdown
# Code Review: [target description]

## Summary

[1-3 sentence overall assessment. State whether the code is ready to merge,
needs minor fixes, or requires significant rework.]

**Scope:** [files reviewed or diff range]
**Findings:** [X critical, Y warnings, Z suggestions]

## Praise

- [Specific positive observations about the code]

## Findings

### Critical

#### 1. [Short title] — `path/to/file.ts:42`
**Dimension:** [Correctness | Security | Performance | ...]
**Problem:** [One sentence describing the issue]
**Suggested fix:**
\```diff
- problematic code
+ corrected code
\```

### Warnings

#### 1. [Short title] — `path/to/file.ts:87`
**Dimension:** [dimension]
**Problem:** [description]
**Suggested fix:**
\```diff
- current code
+ improved code
\```

### Suggestions

#### 1. [Short title] — `path/to/file.ts:15`
**Dimension:** [dimension]
**Problem:** [description]
**Suggested fix:** [description or code snippet]

## Checklist

- [ ] All critical findings addressed
- [ ] Warning-level items reviewed
- [ ] Tests pass after changes
- [ ] No new linter violations introduced
```

## Severity Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| Critical | Bugs, security holes, data loss risks | Must fix before merge |
| Warning | Performance issues, poor patterns, missing validation | Should fix; justify if skipping |
| Suggestion | Style improvements, minor refactors, nice-to-haves | Consider for follow-up |

## Handling Large Diffs

When the diff exceeds 500 lines:
1. **Prioritize** critical and warning findings — skip low-value suggestions
2. **Focus** on new or heavily modified files over minor edits
3. **Group** repeated instances of the same issue instead of listing each one
4. **State** in the summary that the review focused on high-impact findings
5. **Recommend** a follow-up review for areas not covered

## NEVER Do

- **Never rubber-stamp.** If the code has problems, say so clearly.
- **Never flag style preferences** that contradict the project's own linter or formatter config.
- **Never produce vague findings.** "This could be improved" is not a finding. Every item needs a specific problem and a specific fix.
- **Never ignore the test dimension.** If changes lack tests, flag it.
- **Never review generated or vendored code** (e.g., `node_modules/`, `vendor/`, lockfiles, `.min.js`). Skip these silently.
- **Never pile on.** If the same mistake repeats ten times, note it once and say "repeated N times across X files."
- **Never omit praise.** Every review includes at least one positive observation.

## Error Handling

| Scenario | Action |
|----------|--------|
| Target file not found | Print error, suggest checking the path |
| Branch does not exist | List available branches, ask for clarification |
| PR number invalid | Verify with `gh pr list`, show recent PRs |
| No staged changes and no recent commits | Inform the user, suggest specifying a target |
| Binary files in diff | Skip binary files, note them in the summary |
| `gh` CLI not available (PR review) | Fall back to `git log --oneline` and manual diff |

## Related

- **Clean code standards:** [`clean-code`](ai/skills/testing/clean-code/SKILL.md) skill
- **Code review checklist:** [`code-review`](ai/skills/testing/code-review/SKILL.md) skill
- **Quality gates:** [`quality-gates`](ai/skills/testing/quality-gates/SKILL.md) skill
- **Architecture review:** `/new-adr` (for decisions surfaced during review)
- **Feature workflow:** `/new-feature` (pairs well with pre-merge review)
