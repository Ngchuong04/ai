---
name: generate-docs
model: standard
description: Auto-generate documentation from code comments and structure
usage: /generate-docs <target> [--format markdown|jsdoc|docstring] [--output <path>] [--update]
---

# /generate-docs

Auto-generate documentation from code comments, type signatures, and project structure.

## Usage

```
/generate-docs <target> [--format markdown|jsdoc|docstring] [--output <path>] [--update]
```

**Arguments:**
- `target` — File path, directory path, or module name to document
- `--format` — Output format: `markdown` (default), `jsdoc`, `docstring`
- `--output` — Destination path for generated docs (default: `docs/api/`)
- `--update` — Refresh existing documentation without overwriting manual edits

## Examples

```
/generate-docs src/auth/                          # Document entire auth module as markdown
/generate-docs src/utils/parser.ts                # Document a single file
/generate-docs src/api/ --format jsdoc            # Generate JSDoc annotations
/generate-docs lib/ --output docs/reference/      # Custom output directory
/generate-docs src/models/ --update               # Refresh existing docs, preserve manual edits
/generate-docs src/ --format markdown --output .   # Docs alongside source files
```

## When to Use

- Bootstrapping documentation for an undocumented codebase
- Generating API reference docs from type signatures and comments
- Adding inline doc comments (JSDoc, docstrings) to source files
- Refreshing stale documentation after a refactor
- Producing a coverage report of what is and is not documented
- Onboarding onto a new project that lacks written documentation

## What It Does

1. **Parses** the target argument and resolves file paths
2. **Detects** the language and documentation convention in use
3. **Analyzes** code structure: exports, classes, functions, types, constants
4. **Extracts** existing comments, annotations, and doc blocks
5. **Generates** documentation in the requested format
6. **Writes** output files and produces a coverage report

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Parse Input and Resolve Target

1. Use `Glob` to expand the target into a list of source files
2. Filter out non-source files (images, lockfiles, vendored code, generated files)
3. Detect whether `--update` mode applies by checking for existing docs at the output path
4. If `--update`, use `Read` to load existing documentation so manual edits are preserved

**File type filter — include only:**

| Extension | Language |
|-----------|----------|
| `.js`, `.jsx`, `.ts`, `.tsx`, `.mjs`, `.cjs` | JavaScript / TypeScript |
| `.py`, `.pyi` | Python |
| `.rs` | Rust |
| `.go` | Go |
| `.java` | Java |
| `.cs` | C# |
| `.rb` | Ruby |
| `.php` | PHP |

### Phase 2: Analyze Code Structure

1. Use `Read` to load each source file
2. Use `Grep` to locate exported symbols, class declarations, function signatures, and type definitions
3. Build a symbol table for each file:
   - Module-level exports and re-exports
   - Classes and their public methods, properties, and constructors
   - Standalone functions and arrow-function constants
   - Interfaces, type aliases, and enums
   - Constants and configuration objects
   - API route handlers and endpoint definitions

**Documentation type detection:**

| Language | Convention | Trigger Pattern |
|----------|-----------|-----------------|
| JavaScript / TypeScript | JSDoc | `/** ... */` blocks above declarations |
| Python | Docstrings | Triple-quoted strings after `def` / `class` |
| Rust | RustDoc | `///` and `//!` comment lines |
| Go | GoDoc | Comment block directly preceding `func` / `type` |
| Java | Javadoc | `/** ... */` with `@param`, `@return` tags |
| C# | XML comments | `///` with `<summary>`, `<param>` elements |
| Ruby | YARD | `#` comment blocks with `@param`, `@return` |
| PHP | PHPDoc | `/** ... */` with `@param`, `@return` tags |

### Phase 3: Extract Existing Documentation

1. For each symbol, extract any existing doc comment or annotation
2. Parse structured tags (`@param`, `@returns`, `@throws`, `@example`, `@deprecated`)
3. Identify undocumented symbols and flag them for generation
4. Record coverage metrics: documented vs. undocumented symbols per file

**Extractable elements:**

| Element | What to Capture |
|---------|----------------|
| Functions / methods | Description, parameters, return type, thrown errors, examples |
| Classes / structs | Purpose, constructor args, public interface summary |
| Interfaces / types | Purpose, property descriptions, usage context |
| Enums | Variant descriptions, intended usage |
| Constants | Value, purpose, where it is consumed |
| Module-level docs | Package or file-level overview comment |
| API endpoints | HTTP method, path, request/response shape, auth requirements |

### Phase 4: Generate Documentation

1. For undocumented symbols, infer documentation from:
   - Function name and parameter names
   - Type annotations and return types
   - Usage patterns found via `Grep` across the codebase
   - Surrounding comments or related test files
2. Apply the correct format template based on `--format` and detected language
3. For `--update` mode, merge generated content with existing manual docs — never discard human-written sections

**Format templates:**

**Markdown (default):**
```markdown
## `functionName(param1, param2)`

Description inferred from code and context.

**Parameters:**
| Name | Type | Description |
|------|------|-------------|
| `param1` | `string` | What this parameter controls |
| `param2` | `number` | What this parameter controls |

**Returns:** `ReturnType` — Description of return value

**Example:**
\`\`\`ts
const result = functionName("input", 42);
\`\`\`
```

**JSDoc (inline):**
```js
/**
 * Description inferred from code and context.
 * @param {string} param1 - What this parameter controls
 * @param {number} param2 - What this parameter controls
 * @returns {ReturnType} Description of return value
 * @example
 * const result = functionName("input", 42);
 */
```

**Python docstring (inline):**
```python
def function_name(param1: str, param2: int) -> ReturnType:
    """Description inferred from code and context.

    Args:
        param1: What this parameter controls.
        param2: What this parameter controls.

    Returns:
        Description of return value.

    Example:
        >>> result = function_name("input", 42)
    """
```

### Phase 5: Write Output

1. For markdown format, write files to the `--output` path using `Write`:
   - One file per module or directory, mirroring the source tree
   - An `index.md` linking to all generated docs
2. For inline formats (jsdoc, docstring), use `Edit` to insert doc comments directly above each symbol in the source file
3. In `--update` mode, use `Edit` to replace only the auto-generated sections, leaving manual content untouched

### Phase 6: Report

1. Print a summary table to the console using `Bash`:
   - Files processed
   - Symbols documented (new + updated)
   - Symbols skipped (already documented, in update mode)
   - Coverage percentage (before and after)
2. List any symbols that could not be documented automatically, with reasons

**Quality checks applied before writing:**

| Check | Criteria |
|-------|----------|
| Parameter descriptions present | Every parameter has a non-empty description |
| Return types documented | Return type and description are specified |
| Examples included | At least one usage example per public function |
| Edge cases noted | Thrown errors and failure modes are documented |
| Links valid | Cross-references point to real symbols |
| No placeholder text | No `TODO`, `FIXME`, or `[describe]` left in output |

## NEVER Do

| Rule | Reason |
|------|--------|
| Never fabricate behavior | Document only what the code actually does; do not guess at side effects or undeclared behavior |
| Never document internal-only symbols in public docs | Private helpers, unexported functions, and underscore-prefixed names stay out of external API docs |
| Never overwrite manual documentation in update mode | Human-written sections are authoritative; merge around them, never replace them |
| Never include secrets or credentials found in code | Redact any tokens, keys, or passwords encountered during analysis |
| Never generate docs for vendored or generated code | Skip `node_modules/`, `vendor/`, `__generated__/`, `.min.js`, and similar paths |
| Never produce vague descriptions | "Does stuff" is not documentation; every description must be specific and actionable |
| Never skip the coverage report | The user needs to know what was documented and what was missed |
| Never invent parameter types | If the type cannot be determined from annotations or inference, mark it as `unknown` and flag it |

## Error Handling

| Situation | Action |
|-----------|--------|
| Target path does not exist | Print error with the resolved path, suggest checking for typos |
| No source files found in target | List the file types found, ask if the filter should be broadened |
| File cannot be parsed (syntax errors) | Skip the file, log a warning, continue with remaining files |
| Output directory does not exist | Create it automatically, inform the user |
| Existing docs conflict in update mode | Show a diff of the conflict, ask the user which version to keep |
| Unsupported language detected | Skip the file, list it in the report as unsupported |
| Symbol type cannot be inferred | Document the symbol with `unknown` type, flag it in the coverage report |
| Target is too large (>500 files) | Process in batches, prioritize public API surface, note partial coverage |

## Output

- **Markdown format:** Documentation files in the output directory, plus an `index.md` table of contents
- **Inline format:** Updated source files with doc comments inserted above each symbol
- **Coverage report:** Printed to console — files processed, symbols documented, coverage percentage before and after
- **Warnings list:** Symbols that could not be auto-documented, with reasons

## Related

- **Code review:** `/review-code` (reviews documentation quality as part of its analysis)
- **Writing style:** `writing-clearly-and-concisely` skill (apply to generated prose)
- **Skill:** [`clear-writing`](ai/skills/writing/clear-writing/SKILL.md) (concise, clear documentation writing)
- **Skill:** [`mermaid-diagrams`](ai/skills/writing/mermaid-diagrams/SKILL.md) (diagrams for architecture and flow documentation)
- **Architecture docs:** `/new-adr` (for documenting design decisions, not code-level API)
- **Runbooks:** `/create-runbook` (for operational procedures, not code reference)
