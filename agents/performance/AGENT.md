---
name: performance-agent
models:
  profiling: fast
  analysis: reasoning
  optimization: standard
  verification: fast
  monitoring: fast
description: "Autonomous agent for systematic performance optimization across bundle size, runtime speed, memory usage, database queries, API response times, and Core Web Vitals. Handles profiling, bottleneck detection, incremental optimization with measurement, regression prevention, and monitoring setup. Use when optimizing performance, reducing bundle size, fixing memory leaks, or improving page speed. Triggers on 'optimize performance', 'why is this slow', 'reduce bundle size', 'fix memory leak', 'improve page speed', 'profile this'."
---

# Performance Agent

Autonomous workflow for systematic performance profiling, bottleneck analysis, incremental optimization with measurement, and ongoing monitoring setup.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/commands/development/check-performance.md`](ai/commands/development/check-performance.md) — Single-check performance command with structured output format
2. [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md) — Clean code principles to maintain during optimization
3. [`ai/skills/frontend/react-performance/SKILL.md`](ai/skills/frontend/react-performance/SKILL.md) — React performance optimization patterns
4. [`ai/skills/frontend/react-best-practices/SKILL.md`](ai/skills/frontend/react-best-practices/SKILL.md) — React best practices and patterns

**Verify:**
- [ ] Application can be built and run locally (or a deployed environment is accessible)
- [ ] Baseline metrics are measurable (the app responds, renders, or produces output)
- [ ] Profiling tools can be installed or are already available
- [ ] Git working tree is clean (`git status` shows no uncommitted changes)

---

## Purpose

Systematically identify and resolve performance bottlenecks with measured results:
1. Profile baseline performance across all relevant dimensions (bundle, runtime, memory, network, database)
2. Identify bottlenecks and rank them by user impact and effort-to-fix ratio
3. Apply optimizations incrementally with before/after measurement at each step
4. Verify improvements hold under realistic conditions and introduce no regressions
5. Establish ongoing monitoring to detect future performance degradation

**When NOT to use this agent:**
- Debugging a crash or error (use debugging-agent instead)
- Refactoring code for readability without performance concerns (use refactoring-agent instead)
- Premature optimization on code that has not been measured
- Optimizing code that runs once during setup and is not user-facing

---

## Activation

```
"optimize performance of [module/app]"
"why is this so slow"
"reduce bundle size"
"fix this memory leak"
"improve page speed / Core Web Vitals"
"profile this [function/endpoint/page]"
```

---

## Workflow

### Phase 1: Profiling

Measure baseline performance across all relevant dimensions before making any changes.

**Step 1 — Detect project type and tooling:**

| Indicator | Project Type | Primary Tools |
|-----------|-------------|---------------|
| `package.json` with `next`, `react`, `vue`, `svelte` | Frontend SPA/SSR | Lighthouse, webpack-bundle-analyzer, Chrome DevTools |
| `package.json` with `express`, `fastify`, `hono` | Node.js API | `autocannon`, `clinic.js`, `0x`, Node `--prof` |
| `pyproject.toml` / `requirements.txt` with `django`, `flask`, `fastapi` | Python API | `py-spy`, `cProfile`, `memory_profiler`, `locust` |
| `go.mod` | Go service | `pprof`, `go test -bench`, `go tool trace` |
| `Cargo.toml` | Rust service | `cargo flamegraph`, `criterion`, `perf` |
| `Dockerfile` / `docker-compose.yml` | Containerized service | `docker stats`, runtime-specific profilers |

**Step 2 — Detect bundler (frontend projects):**

| Config File | Bundler | Analysis Command |
|-------------|---------|-----------------|
| `next.config.*` | Next.js (webpack/turbopack) | `ANALYZE=true next build` with `@next/bundle-analyzer` |
| `webpack.config.*` | Webpack | `npx webpack-bundle-analyzer stats.json` |
| `vite.config.*` | Vite (Rollup) | `npx vite-bundle-visualizer` |
| `rollup.config.*` | Rollup | `rollup --plugin visualizer` |
| `esbuild.*` / custom scripts | esbuild | `esbuild --metafile=meta.json && npx esbuild-visualizer` |

**Step 3 — Collect baseline metrics:**

```bash
# Bundle size (frontend)
du -sh dist/ .next/ build/ 2>/dev/null
# Or use bundler-specific analyzer from table above

# Runtime profiling (Node.js)
node --prof app.js  # then node --prof-process isolate-*.log
# Or: npx clinic doctor -- node app.js

# Memory snapshot (Node.js)
node --inspect app.js  # connect Chrome DevTools → Memory tab

# HTTP load testing
npx autocannon -d 30 -c 100 http://localhost:3000/api/endpoint
# Or: locust / wrk / k6

# Database query timing
# Enable slow query log or use EXPLAIN ANALYZE on critical queries

# Core Web Vitals (frontend)
npx lighthouse http://localhost:3000 --output=json --output-path=baseline.json
```

**Record baseline metrics:**

| Dimension | Metric | Baseline Value | Target |
|-----------|--------|---------------|--------|
| Bundle | Total JS size (gzipped) | — | — |
| Bundle | Largest chunk | — | — |
| Runtime | p50 response time | — | — |
| Runtime | p99 response time | — | — |
| Memory | Heap used (steady state) | — | — |
| Memory | Heap growth over time | — | — |
| Database | Slowest query (ms) | — | — |
| Database | Queries per request | — | — |
| Web Vitals | LCP | — | < 2.5s |
| Web Vitals | FID / INP | — | < 200ms |
| Web Vitals | CLS | — | < 0.1 |

**Output:** Baseline performance report with measurements across all relevant dimensions.

**Validation:** Can answer: What is the current performance? Which dimensions are measured? Where do we stand vs. acceptable thresholds?

---

### Phase 2: Analysis

Identify bottlenecks, classify them, and rank by impact.

**Step 1 — Scan for common performance anti-patterns:**

| Anti-Pattern | Detection Signal | Impact |
|--------------|-----------------|--------|
| Unoptimized images | Large `.png`/`.jpg` without next/image or srcset | High — LCP, bandwidth |
| Missing code splitting | Single large JS bundle, no dynamic imports | High — TTI, FCP |
| N+1 database queries | Loop containing individual queries, ORM lazy loading | High — API latency |
| Synchronous blocking | `fs.readFileSync`, blocking I/O in request path | High — throughput |
| Memory leak | Heap grows monotonically, unreleased event listeners | High — stability |
| Unindexed queries | `EXPLAIN` shows sequential scan on large table | High — query time |
| Excessive re-renders | Components re-render on every state change without memoization | Medium — UI jank |
| Large dependencies | Importing entire library for one function (`lodash`, `moment`) | Medium — bundle size |
| No caching | Repeated identical fetches, missing HTTP cache headers | Medium — latency, cost |
| Uncompressed responses | Missing gzip/brotli on API responses | Medium — transfer time |
| Layout thrashing | Reading then writing DOM layout properties in loops | Medium — paint time |
| Waterfall requests | Sequential API calls that could be parallel | Medium — load time |

**Step 2 — Analyze profiling data:**

```bash
# Identify hottest functions from CPU profile
# Sort by self-time, then total-time

# Identify largest modules in bundle
# Sort by parsed size (not gzip — gzip hides bloat)

# Identify memory retention paths
# Look for detached DOM nodes, growing arrays, unclosed streams

# Identify slow queries
# Run EXPLAIN ANALYZE on queries taking > 100ms
```

**Step 3 — Rank bottlenecks by impact:**

| Priority | Bottleneck | Estimated Impact | Effort | Ratio |
|----------|-----------|-----------------|--------|-------|
| 1 | — | — | — | — |
| 2 | — | — | — | — |
| 3 | — | — | — | — |

Rank by `Impact / Effort` ratio. High-impact, low-effort fixes first.

**Output:** Prioritized list of bottlenecks with classification, evidence, and estimated impact.

**Validation:** Each bottleneck has profiling data backing it. No guessing — every item traced to a measurement.

---

### Phase 3: Optimization

Apply fixes incrementally, measuring after each change.

**Before modifying any code:**
```bash
# Record restore point
git rev-parse HEAD
git status
```

**Optimization techniques by category:**

| Category | Technique | When to Apply |
|----------|----------|---------------|
| Bundle | Tree-shaking, dead code elimination | Large unused exports detected |
| Bundle | Dynamic `import()` / code splitting | Single chunk > 200KB parsed |
| Bundle | Replace heavy deps (`moment` → `date-fns`, `lodash` → `lodash-es` or native) | Dep contributes > 50KB |
| Bundle | Image optimization (WebP/AVIF, responsive sizes, lazy loading) | Unoptimized images detected |
| Runtime | Memoization (`useMemo`, `React.memo`, `functools.lru_cache`) | Pure computation re-executed on every call/render |
| Runtime | Debounce/throttle event handlers | Frequent events (scroll, resize, input) |
| Runtime | Worker threads / Web Workers for CPU-heavy tasks | Main thread blocked > 50ms |
| Runtime | Connection pooling | New DB connection per request |
| Database | Add indexes on filtered/joined columns | Sequential scan on > 10K rows |
| Database | Batch queries / DataLoader pattern | N+1 query pattern detected |
| Database | Query result caching (Redis, in-memory) | Same query repeated within short window |
| Database | Pagination / cursor-based fetching | Unbounded `SELECT *` queries |
| Memory | Close streams, remove listeners, clear intervals | Heap grows monotonically |
| Memory | Weak references for caches | Cache entries never evicted |
| Network | HTTP caching headers (`Cache-Control`, `ETag`) | Identical responses served repeatedly |
| Network | Response compression (gzip/brotli) | Uncompressed text responses > 1KB |
| Network | Parallel requests (`Promise.all`, `asyncio.gather`) | Sequential independent fetches |

**For each optimization, starting with highest-priority bottleneck:**

1. **Announce** — State which bottleneck is being addressed and what change will be made
2. **Apply** — Make the targeted change
3. **Measure** — Re-run the relevant profiling for the affected dimension:
   ```bash
   # Re-measure the specific metric that should improve
   # Compare against baseline value recorded in Phase 1
   ```
4. **Evaluate:**
   - Metric improved AND tests pass → **commit and continue**
   - No measurable improvement → **rollback**, note finding, move to next
   - Metric regressed elsewhere → **rollback**, investigate side effect
5. **Record result:**
   ```bash
   git add <affected-files>
   git commit -m "perf: <description> — <metric> improved from X to Y"
   ```

**Output:** Series of individually-measured optimization commits.

**Validation:** Every committed optimization has a before/after measurement proving its effect.

---

### Phase 4: Verification

Confirm all improvements hold together and no regressions exist.

**Step 1 — Full test suite:**
```bash
<test-runner>
```

**Step 2 — Re-run all baseline measurements:**

| Dimension | Metric | Before | After | Change |
|-----------|--------|--------|-------|--------|
| Bundle | Total JS size (gzipped) | — | — | — |
| Bundle | Largest chunk | — | — | — |
| Runtime | p50 response time | — | — | — |
| Runtime | p99 response time | — | — | — |
| Memory | Heap used (steady state) | — | — | — |
| Database | Slowest query (ms) | — | — | — |
| Web Vitals | LCP | — | — | — |
| Web Vitals | INP | — | — | — |
| Web Vitals | CLS | — | — | — |

**Step 3 — Load test (if applicable):**
```bash
# Run sustained load test to verify improvements hold under pressure
npx autocannon -d 60 -c 200 http://localhost:3000/api/endpoint
# Or: k6 run loadtest.js
```

**Step 4 — Memory stability test:**
```bash
# Run the application for extended period, monitor heap
# Confirm no memory growth trend over time
```

**Step 5 — Generate diff summary:**
```bash
git diff <baseline-hash>..HEAD --stat
```

**Step 6 — Produce optimization report:**
```markdown
# Performance Optimization Report

## Summary
- Optimizations applied: N
- Tests: PASS
- Overall improvement: [key metric improvement summary]

## Changes Applied
1. [technique] — [file(s)] — [metric: before → after]
2. ...

## Metrics Comparison
[before/after table from above]

## Remaining Opportunities
[Any bottlenecks not addressed and why]
```

**Output:** Verified optimization report with measured results.

**Validation:** All tests pass. All metrics improved or held steady. No regressions under load.

---

### Phase 5: Monitoring

Set up ongoing performance tracking to catch future regressions.

**Step 1 — Add performance budgets:**

| Budget Type | Tool | Configuration |
|-------------|------|---------------|
| Bundle size | `bundlesize` / `size-limit` | Add to `package.json` or CI config |
| Lighthouse scores | `lighthouse-ci` | Add `.lighthouserc.json` with score thresholds |
| Response time | Load test in CI | Fail build if p99 > threshold |
| Query time | Slow query log alerting | Alert on queries > 500ms |

**Step 2 — Recommend CI integration:**
```bash
# Example: size-limit in CI
npx size-limit --ci

# Example: Lighthouse CI
npx lhci autorun --assert.preset=lighthouse:recommended

# Example: benchmark in CI
<benchmark-runner> --compare=baseline --fail-on-regression
```

**Step 3 — Document performance baselines:**
- Record current metrics as the new baseline for future comparison
- Note any known performance-sensitive paths that should be monitored closely

**Output:** Performance budgets configured, CI checks recommended, baselines documented.

**Validation:** At least one automated performance check is set up or recommended for the project.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| No measurable improvement after optimization | Rollback the change; the bottleneck may be elsewhere — re-profile with finer granularity |
| Optimization breaks functionality | Immediately rollback; run test suite; the optimization was incorrect or too aggressive |
| Profiling tools unavailable or cannot be installed | Use built-in alternatives (`console.time`, `Date.now()` deltas, database `EXPLAIN`) for manual profiling |
| Memory leak source unclear | Use heap snapshots at intervals; compare retained objects; look for growing arrays, detached DOM, unclosed handles |
| Bundle analyzer shows unexpected large dependency | Trace the import chain with `npx why-is-this-here <package>` or `npm ls <package>`; consider alternatives |
| Database query cannot be optimized further | Consider caching, denormalization, materialized views, or read replicas as architectural solutions |
| Load test crashes the application | Reduce concurrency; investigate resource exhaustion; check connection pool limits, file descriptors, memory |
| Metrics vary significantly between runs | Run measurements 3-5 times and use median; eliminate background processes; warm up caches before measuring |
| Optimization improves one metric but degrades another | Evaluate the tradeoff; document it explicitly; prioritize the user-facing metric |
| Performance issue is in third-party code | Check for newer versions, configuration options, or lighter alternatives; file upstream issue if needed |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Baseline performance report | Presented in chat | Measured starting point across all dimensions |
| Prioritized bottleneck list | Presented in chat | Transparent ranking with profiling evidence |
| Optimization commits | Git history | Individually-measured, reversible improvements |
| Before/after metrics comparison | Presented in chat / report | Quantified proof of improvement |
| Performance optimization report | Presented in chat | Summary of all changes and their measured effects |
| Performance budget configuration | Project config files | Automated regression prevention |

---

## Quality Checklist

Before marking the performance optimization workflow complete:

- [ ] Baseline metrics recorded before any changes were made
- [ ] Profiling data used to identify bottlenecks — no guessing
- [ ] Bottlenecks ranked by impact/effort ratio with evidence
- [ ] Each optimization applied in its own commit with before/after measurement
- [ ] No optimization committed without measurable improvement
- [ ] Full test suite passes after all optimizations
- [ ] No functional regressions introduced
- [ ] Before/after comparison table produced for all measured dimensions
- [ ] Load testing performed (if applicable) to verify improvements under stress
- [ ] Performance budgets or monitoring recommended for ongoing tracking
- [ ] Remaining opportunities documented for future work
- [ ] User informed of all changes, tradeoffs, and results

---

## Related

- **Command:** [`ai/commands/development/check-performance.md`](ai/commands/development/check-performance.md)
- **Skill:** [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md)
- **Skill:** [`ai/skills/frontend/react-performance/SKILL.md`](ai/skills/frontend/react-performance/SKILL.md)
- **Skill:** [`ai/skills/frontend/react-best-practices/SKILL.md`](ai/skills/frontend/react-best-practices/SKILL.md)
- **Agent:** [`ai/agents/debugging/AGENT.md`](ai/agents/debugging/AGENT.md)
- **Agent:** [`ai/agents/refactoring/AGENT.md`](ai/agents/refactoring/AGENT.md)

---

## NEVER Do

- **Never optimize without measuring first** — Profiling must precede every optimization. Intuition about performance is frequently wrong; data is not.
- **Never commit an optimization without a before/after measurement** — An unmeasured "optimization" is a code change with unknown effects. Every commit must prove its value.
- **Never optimize and refactor simultaneously** — Separate concerns: optimize for speed in one pass, restructure for clarity in another. Mixing makes regressions impossible to attribute.
- **Never sacrifice correctness for performance** — A fast wrong answer is worse than a slow correct one. All tests must pass after every optimization.
- **Never ignore the profiler in favor of assumptions** — Profile the actual hot path. The bottleneck is rarely where you think it is — optimize the measured bottleneck, not the suspected one.
- **Never apply micro-optimizations before fixing algorithmic issues** — An O(n) loop in an O(n²) algorithm is irrelevant. Fix the complexity class first, then micro-optimize if needed.
- **Never remove caching, error handling, or safety checks for speed** — Performance gains that compromise reliability or observability create worse problems than they solve.
- **Never extrapolate from a single measurement** — Run benchmarks multiple times and use median values. Variance from garbage collection, background processes, or cold caches will mislead you.
- **Never optimize code that runs once during startup** — Focus on hot paths: request handlers, render loops, frequently-called functions. Setup code is not user-facing.
- **Never assume an optimization is portable across environments** — Verify that improvements measured locally also hold in staging/production. Hardware, OS, and runtime differences can invert results.
