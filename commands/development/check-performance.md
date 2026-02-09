---
name: check-performance
model: standard
description: Comprehensive performance audit — bundles, runtime, memory, network, and Core Web Vitals
usage: /check-performance [target]
---

# /check-performance

Audit application performance across bundles, runtime, memory, network, database queries, and Core Web Vitals.

## Usage

```
/check-performance [target]
```

**Arguments:**
- `target` (optional) — File path, directory, URL, route, or area to audit (e.g., `src/app/dashboard`, `/api/orders`, `homepage`)

## Examples

```
/check-performance src/app/dashboard          # Audit bundle and runtime for the dashboard route
/check-performance /api/orders                # Profile API response times and query performance
/check-performance homepage                   # Measure Core Web Vitals for the homepage
/check-performance src/components/DataTable   # Analyze rendering performance of a component
/check-performance                            # Full application-wide performance audit
```

## What It Does

1. **Detects** the project's bundler, framework, and runtime environment
2. **Analyzes** bundle size and composition using the appropriate bundle analysis tool
3. **Identifies** large dependencies, duplicated modules, and tree-shaking failures
4. **Profiles** runtime performance — long tasks, excessive re-renders, blocking operations
5. **Scans** for memory leaks — detached DOM nodes, unclosed listeners, growing collections
6. **Evaluates** network waterfall — request count, payload sizes, sequenced fetches, missing compression
7. **Measures** Core Web Vitals (LCP, FID, CLS, INP, TTFB) against threshold targets
8. **Inspects** database queries for N+1 patterns, missing indexes, and slow query signatures
9. **Checks** API response times — P50, P95, P99 latency and payload efficiency
10. **Audits** static assets — unoptimized images, unsubsetted fonts, unminified CSS/JS
11. **Scores** each category and ranks findings by estimated user impact
12. **Generates** a prioritized report with concrete fixes and expected improvement per fix

## Implementation Steps

Use `TodoWrite` to track progress through each phase.

### Phase 1: Environment Detection

Detect the project's bundler and framework to select the right analysis tools.

**Bundler detection:**

| Indicator | Bundler | Analysis Tool |
|-----------|---------|---------------|
| `webpack.config.*` or `next.config.*` with webpack | Webpack | `webpack-bundle-analyzer` |
| `vite.config.*` | Vite | `rollup-plugin-visualizer` |
| `rollup.config.*` | Rollup | `rollup-plugin-visualizer` |
| `esbuild` in `package.json` scripts | esbuild | `esbuild-analyzer` or `source-map-explorer` |
| `turbo.json` with Next.js 13+ | Turbopack | `@next/bundle-analyzer` |
| `.parcelrc` or `parcel` in scripts | Parcel | `parcel-bundle-analyzer` |

**Framework detection:**

| Indicator | Framework | Performance Tools |
|-----------|-----------|-------------------|
| `next.config.*` | Next.js | `@next/bundle-analyzer`, `next build --profile`, `next/reporting` |
| `nuxt.config.*` | Nuxt | `nuxt build --analyze`, `@nuxt/devtools` |
| `angular.json` | Angular | `ng build --stats-json`, `webpack-bundle-analyzer` |
| `svelte.config.*` | SvelteKit | `rollup-plugin-visualizer`, `vite-plugin-inspect` |
| `remix.config.*` or `@remix-run` | Remix | `source-map-explorer`, Remix DevTools |
| `astro.config.*` | Astro | `astro build --stats`, `source-map-explorer` |
| `package.json` with `react-scripts` | CRA | `source-map-explorer`, `cra-bundle-analyzer` |

**Runtime/backend detection:**

| Indicator | Runtime | Profiling Tool |
|-----------|---------|----------------|
| `package.json` (Node) | Node.js | `--prof`, `clinic.js`, `0x` |
| `requirements.txt` / `pyproject.toml` | Python | `cProfile`, `py-spy`, `scalene` |
| `go.mod` | Go | `pprof`, `go tool trace` |
| `Cargo.toml` | Rust | `cargo flamegraph`, `perf` |
| `Gemfile` | Ruby | `rack-mini-profiler`, `stackprof` |

### Phase 2: Bundle Analysis

1. **Run** the appropriate build with analysis flags:
   ```
   # Next.js
   ANALYZE=true next build

   # Vite
   npx vite build && npx source-map-explorer dist/assets/*.js

   # Webpack
   npx webpack --profile --json > stats.json && npx webpack-bundle-analyzer stats.json
   ```
2. **Parse** the output to extract:
   - Total bundle size (raw and gzipped)
   - Per-route chunk sizes
   - Top 10 largest modules by size
   - Duplicated packages (same library bundled multiple times)
   - Tree-shaking failures (side-effect imports pulling in full libraries)
3. **Compare** against budgets:

| Metric | Target | Warning | Critical |
|--------|--------|---------|----------|
| Initial JS (gzipped) | < 100 KB | 100–200 KB | > 200 KB |
| Per-route chunk | < 50 KB | 50–100 KB | > 100 KB |
| Total CSS | < 50 KB | 50–100 KB | > 100 KB |
| Largest single module | < 30 KB | 30–60 KB | > 60 KB |
| Duplicated packages | 0 | 1–2 | > 2 |

### Phase 3: Runtime Performance Profiling

1. **Scan** source code for common runtime anti-patterns:

| Anti-Pattern | Detection Method | Impact |
|-------------|-----------------|--------|
| Synchronous blocking in main thread | Search for `fs.readFileSync`, `execSync`, heavy `for` loops | High — blocks UI/event loop |
| Unthrottled event handlers | Search for `scroll`, `resize`, `mousemove` without `throttle`/`debounce` | High — jank and frame drops |
| Unnecessary re-renders | React: components missing `memo`, inline object/array props | Medium — wasted CPU cycles |
| Layout thrashing | Interleaved DOM reads and writes (`offsetHeight` inside loops) | High — forces synchronous layout |
| Expensive computed values | Missing `useMemo`/`useCallback` on costly operations | Medium — redundant computation |
| Unbounded list rendering | Large arrays rendered without virtualization | High — DOM node explosion |
| Blocking `<script>` tags | Scripts without `async` or `defer` in `<head>` | High — delays page render |
| Excessive DOM depth | Deeply nested component trees (> 32 levels) | Medium — slower style calculations |
| Synchronous XHR | `XMLHttpRequest` with `false` async flag | High — freezes main thread |
| Unoptimized animations | Animating `width`/`height`/`top`/`left` instead of `transform`/`opacity` | Medium — triggers layout/paint |
| Large JSON serialization | `JSON.stringify` on large objects in hot paths | Medium — blocks event loop |
| Missing web worker offload | CPU-heavy operations (crypto, parsing, sorting) on main thread | High — UI unresponsive |

2. **Check** for server-side performance issues:
   - Missing response streaming (Next.js `loading.tsx`, React `<Suspense>`)
   - Sequential `await` calls that could be parallelized (`Promise.all`)
   - Missing cache headers on API responses
   - Absent request deduplication

### Phase 4: Memory Leak Detection

Scan for common memory leak patterns:

| Pattern | What to Search For |
|---------|--------------------|
| Event listener leaks | `addEventListener` without corresponding `removeEventListener` in cleanup |
| Interval/timeout leaks | `setInterval`/`setTimeout` without `clearInterval`/`clearTimeout` |
| Subscription leaks | Observable `.subscribe()` without `.unsubscribe()` in teardown |
| Detached DOM references | Storing DOM nodes in variables that outlive the node's lifecycle |
| Closure captures | Closures in long-lived scopes capturing large objects |
| Growing Maps/Sets | `Map` or `Set` that only adds entries, never deletes |
| Unclosed connections | Database/WebSocket connections opened but never closed |
| React state on unmounted | State updates after component unmount (missing cleanup in `useEffect`) |

### Phase 5: Network and Asset Analysis

1. **Audit** static assets:

| Asset Type | Check | Fix |
|-----------|-------|-----|
| Images | Format (prefer WebP/AVIF), dimensions vs display size, missing `width`/`height` | Convert format, resize, add dimensions |
| Fonts | Subset, `font-display`, number of variants, self-hosted vs CDN | Subset with `glyphhanger`, use `font-display: swap` |
| CSS | Unused rules, render-blocking stylesheets, file count | PurgeCSS, inline critical CSS, concat files |
| JavaScript | Unused code, render-blocking scripts, missing code splitting | Tree-shake, add `defer`, dynamic `import()` |

2. **Check** network patterns:
   - Sequential API calls that should be batched or parallelized
   - Missing compression (`Content-Encoding: gzip`/`br`)
   - Missing caching headers (`Cache-Control`, `ETag`)
   - Excessive request count (> 50 requests on initial load)
   - Large payloads without pagination (> 1 MB JSON responses)
   - Missing `preconnect`/`preload` hints for critical resources

### Phase 6: Core Web Vitals Assessment

Evaluate each vital against Google's thresholds:

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | ≤ 2.5s | 2.5–4.0s | > 4.0s |
| FID (First Input Delay) | ≤ 100ms | 100–300ms | > 300ms |
| CLS (Cumulative Layout Shift) | ≤ 0.1 | 0.1–0.25 | > 0.25 |
| INP (Interaction to Next Paint) | ≤ 200ms | 200–500ms | > 500ms |
| TTFB (Time to First Byte) | ≤ 800ms | 800–1800ms | > 1800ms |

For each metric, identify contributing factors:

- **LCP:** Hero image size, server response time, render-blocking resources, client-side rendering delays
- **FID/INP:** Long tasks (> 50ms), heavy JavaScript execution, main-thread blocking
- **CLS:** Images/ads without dimensions, dynamically injected content, web font FOUT/FOIT
- **TTFB:** Slow server, missing CDN, no edge caching, heavy server-side computation

### Phase 7: Database and API Performance

1. **Scan** for database query anti-patterns:

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| N+1 queries | Loop containing individual queries (e.g., `for ... await db.find(id)`) | Batch with `WHERE id IN (...)` or use DataLoader |
| Missing indexes | `WHERE`/`ORDER BY` on columns without indexes | Add composite index |
| SELECT * | Fetching all columns when few are needed | Select only required fields |
| Unbounded queries | Missing `LIMIT` on list queries | Add pagination |
| Missing connection pooling | New connection per request | Use pool (e.g., `pg.Pool`, SQLAlchemy pool) |
| Redundant queries | Same query executed multiple times per request | Cache or deduplicate |

2. **Check** API response efficiency:
   - Over-fetching (response contains fields the client doesn't use)
   - Under-fetching (client makes multiple requests for related data)
   - Missing response compression
   - Missing pagination on list endpoints

## Output

All output goes to the terminal. No files are created unless the user requests a saved report.

```
Performance Audit Report
========================

Target:    [target description or "full application"]
Framework: [detected framework]
Bundler:   [detected bundler]
Runtime:   [detected runtime]

Score: [0-100] / 100

Bundle Analysis                                     [PASS | WARN | FAIL]
------------------------------------------------------------------------
Total JS (gzipped):    87 KB                        [PASS]
Largest chunk:         42 KB                        [PASS]
Duplicated packages:   1 (lodash)                   [WARN]
Tree-shaking issues:   0                            [PASS]

Runtime Performance                                 [PASS | WARN | FAIL]
------------------------------------------------------------------------
Blocking operations:   2 found                      [WARN]
Re-render issues:      3 components                 [WARN]
Virtualization needed: 1 list                       [FAIL]

Memory                                              [PASS | WARN | FAIL]
------------------------------------------------------------------------
Listener leaks:        0                            [PASS]
Subscription leaks:    1 found                      [WARN]

Network & Assets                                    [PASS | WARN | FAIL]
------------------------------------------------------------------------
Unoptimized images:    4 files                      [FAIL]
Missing compression:   2 routes                     [WARN]
Render-blocking:       1 stylesheet                 [WARN]

Core Web Vitals (estimated)                         [PASS | WARN | FAIL]
------------------------------------------------------------------------
LCP:   ~2.1s                                        [PASS]
INP:   ~180ms                                       [PASS]
CLS:   ~0.14                                        [WARN]
TTFB:  ~620ms                                       [PASS]

Database & API                                      [PASS | WARN | FAIL]
------------------------------------------------------------------------
N+1 queries:           2 detected                   [FAIL]
Missing indexes:       1 likely                     [WARN]
Unbounded queries:     0                            [PASS]

Prioritized Fixes (by estimated impact)
---------------------------------------
1. [HIGH]   Fix N+1 in OrderService.getAll()        — est. -400ms P95
2. [HIGH]   Virtualize ProductList (2,400 items)     — est. -200ms INP
3. [HIGH]   Optimize 4 hero images to WebP/AVIF      — est. -800ms LCP
4. [MEDIUM] Remove duplicate lodash bundle            — est. -24 KB JS
5. [MEDIUM] Add font subsetting (Inter)              — est. -60 KB
6. [LOW]    Add debounce to search input handler     — reduces layout work
```

## NEVER Do

- **Never run destructive commands.** Performance analysis is read-only. Do not modify source files, database schemas, or build configs without explicit user approval.
- **Never install tools globally** without asking. Prefer `npx` for one-off analysis tools.
- **Never trust a single metric in isolation.** Bundle size means nothing if runtime is the bottleneck. Correlate findings across categories.
- **Never report estimated vitals as measured values.** Clearly label static-analysis estimates vs real measurements from Lighthouse or CrUX.
- **Never ignore the backend.** A slow API makes every frontend optimization irrelevant. Always check server-side performance.
- **Never recommend premature optimization.** Only flag issues that have measurable user impact or exceed defined thresholds.
- **Never skip the bundler/framework detection step.** Using the wrong analysis tool produces misleading results.
- **Never benchmark on a development build.** Always analyze production builds with minification and optimizations enabled.

## Error Handling

- If no bundler is detected, fall back to `source-map-explorer` on any `.js` output files, or note that bundle analysis is not applicable.
- If the project has no build step (vanilla HTML/JS), skip bundle analysis and focus on network, asset, and runtime checks.
- If the target route or file does not exist, list available routes or files and ask for clarification.
- If analysis tools are not installed, suggest installation commands and offer to run with `npx`.
- If the project uses a monorepo, ask which package or app to audit before proceeding.
- If no database layer is detected, skip Phase 7 database checks silently.
- If build fails during analysis, report the build error and suggest running `/debug-error` on it.

## Related

- **Bundle deep-dive:** `source-map-explorer`, `webpack-bundle-analyzer`
- **Debugging:** `/debug-error` (if performance issues surface runtime errors)
- **Code quality:** `/review-code` (performance dimension covers some overlap)
- **Refactoring:** `/refactor` (for restructuring code after identifying bottlenecks)
- **Skill:** `clean-code` (avoiding anti-patterns that degrade performance)
- **Skill:** [`react-performance`](ai/skills/frontend/react-performance/SKILL.md) (React-specific performance optimization)
- **Skill:** [`react-best-practices`](ai/skills/frontend/react-best-practices/SKILL.md) (React patterns that prevent performance issues)
