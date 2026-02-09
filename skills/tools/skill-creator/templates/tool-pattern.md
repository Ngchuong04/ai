---
name: your-skill-name
description: <!-- CUSTOMIZE: Describe the tool expertise this skill provides. Include the tool name, common tasks, and trigger phrases. Example: "Docker containerization expert with deep knowledge of [areas]. Use PROACTIVELY for [specific problems]." Tool skills should trigger when users work with specific technologies. -->
---

# <!-- CUSTOMIZE: Skill Title -->

<!-- CUSTOMIZE: One sentence positioning this skill as a tool expert. Example: "You are an advanced [tool] expert with comprehensive knowledge of [key areas]." -->

## Initial Assessment

<!-- CUSTOMIZE: Tool skills start by detecting the current environment and project state. This section defines what to check before taking action. -->

1. **Scope check** - If the issue falls outside this tool's domain, recommend the right skill:
   <!-- CUSTOMIZE: List adjacent tools/skills and when to redirect -->
   - <!-- CUSTOMIZE: Adjacent domain --> -> <!-- CUSTOMIZE: other skill -->
   - <!-- CUSTOMIZE: Adjacent domain --> -> <!-- CUSTOMIZE: other skill -->

2. **Detect environment:**

   ```bash
   # <!-- CUSTOMIZE: Replace with actual detection commands for your tool -->
   # Tool version and availability
   <!-- CUSTOMIZE: tool --> --version 2>/dev/null || echo "Not installed"

   # Project file detection
   find . -name "<!-- CUSTOMIZE: config file pattern -->" -type f | head -10

   # Current state
   <!-- CUSTOMIZE: status/info commands -->
   ```

3. **Adapt approach** based on detection:
   - Match existing configuration patterns and conventions
   - <!-- CUSTOMIZE: What to respect in existing setup -->
   - <!-- CUSTOMIZE: What to account for (environments, versions, etc.) -->

## Command Reference

<!-- CUSTOMIZE: A quick-lookup table of the most important commands or operations. Keep to 8-12 rows covering daily use. -->

| Command | Purpose | Example |
|---------|---------|---------|
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |
| `<!-- CUSTOMIZE -->` | <!-- CUSTOMIZE --> | `<!-- CUSTOMIZE -->` |

## Core Patterns

<!-- CUSTOMIZE: 3-5 sections covering the most important usage patterns. Each pattern includes a description and a concrete, copy-pasteable configuration or code example. -->

### Pattern 1: <!-- CUSTOMIZE: Pattern Name -->

<!-- CUSTOMIZE: Brief description of when and why to use this pattern. -->

```<!-- CUSTOMIZE: language -->
# <!-- CUSTOMIZE: Replace with a production-ready example -->
```

### Pattern 2: <!-- CUSTOMIZE: Pattern Name -->

<!-- CUSTOMIZE: Brief description. -->

```<!-- CUSTOMIZE: language -->
# <!-- CUSTOMIZE: Replace with a production-ready example -->
```

### Pattern 3: <!-- CUSTOMIZE: Pattern Name -->

<!-- CUSTOMIZE: Brief description. -->

```<!-- CUSTOMIZE: language -->
# <!-- CUSTOMIZE: Replace with a production-ready example -->
```

## Configuration Templates

<!-- CUSTOMIZE: Pre-built configurations for common scenarios. Link to templates/ files for full versions; inline short ones (under 20 lines). -->

| Template | Purpose | Location |
|----------|---------|----------|
| **<!-- CUSTOMIZE -->** | <!-- CUSTOMIZE --> | [templates/<!-- CUSTOMIZE -->](templates/<!-- CUSTOMIZE -->) |
| **<!-- CUSTOMIZE -->** | <!-- CUSTOMIZE --> | [templates/<!-- CUSTOMIZE -->](templates/<!-- CUSTOMIZE -->) |
| **<!-- CUSTOMIZE -->** | <!-- CUSTOMIZE --> | [templates/<!-- CUSTOMIZE -->](templates/<!-- CUSTOMIZE -->) |

## Validation

<!-- CUSTOMIZE: How to verify that the tool configuration is correct. Include specific commands to run. -->

After applying changes, validate:

```bash
# <!-- CUSTOMIZE: Build/compile/lint validation -->

# <!-- CUSTOMIZE: Runtime validation -->

# <!-- CUSTOMIZE: Security or quality check -->
```

## Review Checklist

<!-- CUSTOMIZE: A checklist for reviewing tool configurations. Organize by concern area. -->

### <!-- CUSTOMIZE: Area 1 (e.g., Performance, Security, Configuration) -->
- [ ] <!-- CUSTOMIZE: Check 1 -->
- [ ] <!-- CUSTOMIZE: Check 2 -->
- [ ] <!-- CUSTOMIZE: Check 3 -->

### <!-- CUSTOMIZE: Area 2 -->
- [ ] <!-- CUSTOMIZE: Check 1 -->
- [ ] <!-- CUSTOMIZE: Check 2 -->
- [ ] <!-- CUSTOMIZE: Check 3 -->

### <!-- CUSTOMIZE: Area 3 -->
- [ ] <!-- CUSTOMIZE: Check 1 -->
- [ ] <!-- CUSTOMIZE: Check 2 -->
- [ ] <!-- CUSTOMIZE: Check 3 -->

## Troubleshooting

<!-- CUSTOMIZE: Common issues, their symptoms, root causes, and fixes. Tool skills frequently encounter the same errors. -->

### <!-- CUSTOMIZE: Issue Category 1 -->
**Symptoms**: <!-- CUSTOMIZE: What the user sees -->
**Root causes**: <!-- CUSTOMIZE: Why it happens -->
**Solutions**: <!-- CUSTOMIZE: How to fix it -->

### <!-- CUSTOMIZE: Issue Category 2 -->
**Symptoms**: <!-- CUSTOMIZE -->
**Root causes**: <!-- CUSTOMIZE -->
**Solutions**: <!-- CUSTOMIZE -->

## Resources

<!-- CUSTOMIZE: Tool skills benefit from reference files for advanced patterns and template files for ready-to-use configurations. -->

### references/

- [<!-- CUSTOMIZE -->](references/<!-- CUSTOMIZE -->) - <!-- CUSTOMIZE: What it covers and when to read it -->
- [<!-- CUSTOMIZE -->](references/<!-- CUSTOMIZE -->) - <!-- CUSTOMIZE -->

### templates/

| Template | Purpose |
|----------|---------|
| [<!-- CUSTOMIZE -->](templates/<!-- CUSTOMIZE -->) | <!-- CUSTOMIZE: Production-ready config --> |
| [<!-- CUSTOMIZE -->](templates/<!-- CUSTOMIZE -->) | <!-- CUSTOMIZE: Production-ready config --> |
