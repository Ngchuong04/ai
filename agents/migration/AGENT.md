---
name: migration-agent
models:
  assessment: fast
  planning: reasoning
  preparation: standard
  execution: standard
  verification: fast
description: "Autonomous agent for multi-step migrations with rollback planning and zero-downtime execution. Handles database schema migrations, framework and library version upgrades, language version upgrades, architecture migrations (monolith to microservices), data format migrations, and API version migrations. Use when planning or executing complex migrations across systems or versions. Triggers on 'migrate', 'upgrade', 'migration plan', 'migrate database', 'upgrade framework', 'migration strategy', 'zero-downtime migration', 'rollback plan'."
---

# Migration Agent

Autonomous workflow for planning and executing multi-step migrations with rollback safety, zero-downtime strategies, and verification at every stage.

---

## Before Starting

**Mandatory references to read:**
1. [`ai/commands/development/migrate-deps.md`](ai/commands/development/migrate-deps.md) — Single-dependency upgrade command with breaking change analysis
2. [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md) — Clean code principles for writing migration code
3. [`ai/skills/backend/architecture-patterns/SKILL.md`](ai/skills/backend/architecture-patterns/SKILL.md) — Architecture patterns for structural migrations
4. [`ai/skills/api/database-migrations/SKILL.md`](ai/skills/api/database-migrations/SKILL.md) — Database migration patterns and strategies

**Verify:**
- [ ] Git working tree is clean (`git status` shows no uncommitted changes)
- [ ] Current test suite passes — baseline must be green before any migration
- [ ] Backup strategy is in place for data-carrying migrations (database, file formats)
- [ ] Stakeholders are aware of the migration scope and timeline
- [ ] Rollback criteria are defined (what constitutes a failed migration)

---

## Purpose

Plan and execute complex migrations safely with verifiable rollback at every step:
1. Assess the current state, identify migration scope, and map all dependencies
2. Create a step-by-step migration plan with explicit rollback points and risk assessment
3. Prepare safety nets — backups, feature flags, compatibility layers, and shadow systems
4. Execute incrementally with verification checkpoints at each step
5. Verify completeness through comprehensive testing, data integrity checks, and performance comparison

**When NOT to use this agent:**
- Upgrading a single dependency (use `/migrate-deps` command instead)
- Fixing a bug in existing code (use debugging-agent instead)
- Refactoring code without changing underlying technology (use refactoring-agent instead)
- Writing new features from scratch (use development-agent instead)

---

## Activation

```
"migrate the database schema"
"upgrade to [framework] v[version]"
"create a migration plan for [system]"
"migrate from monolith to microservices"
"zero-downtime migration for [component]"
"plan rollback strategy for [migration]"
```

---

## Workflow

### Phase 1: Assessment

Analyze the current state of the system to determine migration scope and risk.

**Step 1 — Classify the migration type:**

| Migration Type | Description | Typical Risk | Rollback Complexity |
|----------------|-------------|-------------|---------------------|
| Database schema | Add/remove/alter tables, columns, indexes, constraints | High | High — data loss possible |
| Framework upgrade | Major version bump of core framework (Next.js, Django, Rails) | High | Medium — code changes reversible |
| Library upgrade | Major version bump of dependency (React, SQLAlchemy, Tokio) | Medium | Low — use `/migrate-deps` |
| Language version | Upgrade runtime (Python 3.11→3.13, Node 18→22, Go 1.21→1.23) | Medium | Medium — syntax/stdlib changes |
| Architecture | Monolith→microservices, MVC→hexagonal, REST→GraphQL | Very High | Very High — structural redesign |
| Data format | JSON→Protobuf, CSV→Parquet, XML→JSON | Medium | Medium — requires dual-write period |
| API version | v1→v2, breaking contract changes, deprecation of endpoints | High | Medium — requires versioned routing |

**Step 2 — Map dependencies and blast radius:**

```bash
# Identify all files importing/using the migrating component
rg "<migration-target>" --type-add 'src:*.{ts,py,go,rs,java,rb}' -t src -l

# Check configuration files referencing the target
rg "<migration-target>" --glob '*.{json,yaml,yml,toml,ini,cfg,env}'

# Review git history for recent changes to affected files
git log --oneline -20 -- <affected-paths>
```

**Step 3 — Assess risk:**

| Risk Factor | Low | Medium | High |
|-------------|-----|--------|------|
| Files affected | < 10 | 10–50 | > 50 |
| Data at risk | None (stateless) | Cached/regenerable | Persistent user data |
| Downtime tolerance | Hours acceptable | Minutes acceptable | Zero-downtime required |
| Rollback window | Days | Hours | Minutes |
| Test coverage of affected code | > 80% | 40–80% | < 40% |
| Number of breaking changes | 0–2 | 3–8 | > 8 |
| External consumers | None | Internal teams | Public API users |

**Output:** Migration classification, dependency map, blast radius count, and risk assessment matrix.

**Validation:** Can answer: What type of migration is this? How many files/systems are affected? What is the overall risk level? What data is at risk?

---

### Phase 2: Planning

Create a detailed, step-by-step migration plan with rollback points at every stage.

**Step 1 — Select migration strategy:**

| Strategy | When to Use | Downtime | Complexity |
|----------|------------|----------|------------|
| Big bang | Small scope, low risk, downtime acceptable | Yes | Low |
| Rolling | Stateless services, container orchestration available | Minimal | Medium |
| Blue-green | Full environment duplication possible, instant rollback needed | Zero | High |
| Canary | Gradual traffic shift desired, metrics-driven validation | Zero | High |
| Strangler fig | Legacy system replacement, long-running migration | Zero | Very High |
| Parallel run | Data migrations requiring integrity verification | Zero | High |
| Expand-contract | Database schema changes, backward-compatible first | Zero | Medium |

**Step 2 — Define rollback strategy per migration type:**

| Migration Type | Rollback Strategy | Rollback Mechanism |
|----------------|------------------|--------------------|
| Database schema (additive) | Drop new columns/tables | Reverse migration script |
| Database schema (destructive) | Restore from backup | Point-in-time recovery, backup restore |
| Framework upgrade | Revert commits, reinstall old version | `git revert`, lockfile restore |
| Language version | Switch runtime version back | Version manager (nvm, pyenv, rustup) |
| Architecture | Route traffic back to old service | Load balancer config, DNS switch |
| Data format | Dual-read from old format | Feature flag toggling format reader |
| API version | Keep old version running | Versioned routing, deprecation headers |

**Step 3 — Build the migration plan:**

For each step, document:
1. **Action** — What exactly will be done
2. **Precondition** — What must be true before this step runs
3. **Verification** — How to confirm the step succeeded
4. **Rollback** — How to undo this specific step
5. **Point of no return** — Whether this step is reversible (mark clearly if not)

```
Migration Plan: PostgreSQL 14 → 16
====================================
Risk level:     High (database, persistent data)
Strategy:       Expand-contract with parallel run
Estimated time: 4 hours
Rollback window: 2 hours after cutover

Step 1: [REVERSIBLE] Add new columns with defaults
  Precondition: Backup verified within last 1 hour
  Verification: Schema diff shows only additions
  Rollback:     DROP COLUMN statements

Step 2: [REVERSIBLE] Deploy dual-write application code
  Precondition: Step 1 verified
  Verification: Both old and new columns populated on writes
  Rollback:     Revert application deployment

Step 3: [REVERSIBLE] Backfill new columns from old data
  Precondition: Dual-write confirmed working for > 30 minutes
  Verification: COUNT mismatches = 0 between old and new columns
  Rollback:     Truncate new columns, revert to step 2

Step 4: [REVERSIBLE] Switch reads to new columns
  Precondition: Backfill verified, data integrity confirmed
  Verification: Application reads from new columns, monitors green
  Rollback:     Feature flag to switch reads back to old columns

Step 5: [POINT OF NO RETURN] Drop old columns
  Precondition: New columns serving 100% of reads for > 24 hours
  Verification: Schema diff shows only removals
  Rollback:     Restore from backup (full rollback only)
```

**Step 4 — Present plan and get approval:**

Do NOT proceed without explicit user approval. Highlight all points of no return.

**Output:** Numbered migration plan with strategy, rollback points, and estimated timeline.

**Validation:** Every step has a rollback strategy. Points of no return are clearly marked. User has approved the plan.

---

### Phase 3: Preparation

Set up safety nets before executing any migration step.

**Step 1 — Create backups:**

| System | Backup Method | Verification |
|--------|--------------|-------------|
| PostgreSQL | `pg_dump` or point-in-time recovery setup | Restore to test environment, verify row counts |
| MySQL | `mysqldump` or binary log position recorded | Restore to test environment, verify checksums |
| MongoDB | `mongodump` or snapshot | Restore to test environment, verify document counts |
| Files/config | Git commit or archive | Verify archive contents match source |
| Redis/cache | `BGSAVE` or snapshot | Verify key counts after restore |
| Application state | Git tag at current stable commit | `git checkout <tag>` restores working state |

```bash
# Tag the current stable state
git tag pre-migration-$(date +%Y%m%d-%H%M%S)

# Record the current commit as restore point
git rev-parse HEAD > .migration-restore-point
```

**Step 2 — Set up feature flags (if applicable):**

```
Feature flags for migration:
  migration_use_new_schema:   false  (toggle reads between old/new)
  migration_dual_write:       false  (enable writing to both old/new)
  migration_new_api_version:  false  (route to v2 endpoints)
```

**Step 3 — Create compatibility layers:**

| Migration Type | Compatibility Layer | Purpose |
|----------------|-------------------|---------|
| Database schema | Dual-write middleware | Write to both old and new schema simultaneously |
| API version | Versioned router | Serve both v1 and v2 from the same deployment |
| Data format | Format adapter | Read/write both old and new formats transparently |
| Framework upgrade | Polyfill/shim | Bridge removed APIs during transition |
| Architecture | API gateway / facade | Route requests to old or new service transparently |

**Step 4 — Verify compatibility tooling:**

| Language/Framework | Compatibility Check Tool | Command |
|--------------------|------------------------|---------|
| Node.js | `nvm` + `engines` field | `node --check <file>`, `npx tsc --noEmit` |
| Python | `pyupgrade`, `ruff` | `pyupgrade --py3X-plus *.py`, `ruff check .` |
| Go | `go vet`, `staticcheck` | `go vet ./...`, `staticcheck ./...` |
| Rust | `cargo clippy`, edition migration | `cargo clippy`, `cargo fix --edition` |
| React/Next.js | Codemods | `npx @next/codemod@latest <transform>` |
| Django | `django-upgrade`, system checks | `django-upgrade --target <ver>`, `python manage.py check` |
| Rails | `rails app:update` | `rails app:update`, `rubocop -A` |
| TypeScript | `tsc --noEmit` | `npx tsc --noEmit` |

**Step 5 — Run pre-migration verification:**

```bash
# Full test suite must be green
<test-runner>

# Type checker clean
<type-checker>

# Linter clean
<linter>

# Build succeeds
<build-command>
```

**Output:** Backups verified, feature flags configured, compatibility layers in place, baseline green.

**Validation:** Can restore from backup in a test environment. Feature flags toggle correctly. All pre-migration checks pass.

---

### Phase 4: Execution

Execute the approved migration plan incrementally with verification at each step.

**For each step in the approved plan:**

1. **Announce** — State which step is being executed, its risk level, and its rollback strategy
2. **Execute** — Apply the single migration step
3. **Verify** — Run the step-specific verification (tests, data checks, health checks)
4. **Checkpoint** — Record the state for potential rollback:
   ```bash
   git add <affected-files>
   git commit -m "migration: step N — <description>"
   ```
5. **Evaluate** — Check results:
   - If verification passes: mark step complete, proceed to next
   - If verification fails: **immediately execute rollback** for this step and halt

**Track progress with TodoWrite** — One todo item per migration step.

**Execution rules by migration type:**

| Migration Type | Execution Pattern | Verification Between Steps |
|----------------|------------------|---------------------------|
| Database schema | Run migration scripts sequentially | Query affected tables, verify row counts |
| Framework upgrade | Update dependency → apply codemods → fix manual changes | Type check + test suite + build |
| Language version | Switch runtime → fix syntax → update stdlib usage | Compile/interpret + test suite |
| Architecture | Extract service → deploy → route traffic → verify | Health checks + integration tests + latency metrics |
| Data format | Deploy dual-write → backfill → verify → switch reads | Data integrity checks, diff old vs new |
| API version | Deploy v2 alongside v1 → migrate consumers → deprecate v1 | Contract tests + consumer verification |

**Rollback procedure (on any verification failure):**

```bash
# If the step only changed code:
git revert HEAD

# If the step changed database schema:
<run-reverse-migration-script>

# If the step changed infrastructure:
<restore-previous-configuration>

# If the step changed data format:
<toggle-feature-flag-to-old-format>

# Verify rollback was successful
<test-runner>
```

**Output:** Series of verified, individually-committed migration steps.

**Validation:** Each step has a passing verification. No step was skipped. Rollback was not needed, or was executed cleanly.

---

### Phase 5: Verification

Run comprehensive post-migration verification to confirm full success.

**Step 1 — Full test suite:**
```bash
<test-runner> --coverage
```

**Step 2 — Type checker:**
```bash
<type-checker>
```

**Step 3 — Integration and E2E tests:**
```bash
# Run integration tests covering cross-system boundaries
<integration-test-runner>

# Run E2E tests if available
<e2e-test-runner>
```

**Step 4 — Data integrity checks (for data migrations):**

| Check | Method | Pass Criteria |
|-------|--------|--------------|
| Row count parity | `SELECT COUNT(*)` on old vs new | Counts match exactly |
| Null check on required fields | `SELECT COUNT(*) WHERE new_col IS NULL` | Zero nulls in required fields |
| Referential integrity | Foreign key constraint validation | Zero orphaned references |
| Value range validation | `SELECT MIN/MAX/AVG` on numeric columns | Values within expected bounds |
| Sample spot check | Random sample of 100 rows, compare old vs new | 100% match on transformed fields |
| Checksum verification | Hash comparison on critical data sets | Checksums match |

**Step 5 — Performance comparison:**

| Metric | Before | After | Threshold |
|--------|--------|-------|-----------|
| Average response time (p50) | — | — | < 10% regression |
| Tail latency (p99) | — | — | < 20% regression |
| Query execution time | — | — | No slower than baseline |
| Memory usage | — | — | < 15% increase |
| CPU usage | — | — | < 15% increase |
| Error rate | — | — | No increase |
| Build time | — | — | < 25% increase |

**Step 6 — Produce migration report:**

```markdown
# Migration Report

## Summary
- Migration type: [type]
- Strategy: [strategy]
- Steps executed: N / N
- Duration: [time]
- Rollbacks triggered: 0

## Changes Applied
1. [step] — [description] — [status]
2. ...

## Verification Results
- Test suite: PASS (N tests, N% coverage)
- Type checker: PASS
- Data integrity: PASS (N checks)
- Performance: PASS (within thresholds)

## Post-Migration Notes
- [Cleanup tasks remaining]
- [Deprecation timeline for old components]
- [Monitoring recommendations]
```

**Step 7 — Clean up (after verification window):**

Remove compatibility layers, old code paths, and feature flags only after the migration has been stable for the agreed monitoring period.

**Output:** Migration report with verified results across all dimensions.

**Validation:** All tests pass. Data integrity confirmed. Performance within thresholds. No regressions detected.

---

## Error Handling

| Issue | Resolution |
|-------|------------|
| Test suite fails before migration starts | Stop immediately — do not migrate against a broken baseline. Fix tests first. |
| Database migration script fails mid-execution | Execute reverse migration script. If reverse fails, restore from backup. Analyze the failure point and fix the script. |
| Migration introduces type errors | Run type checker, group errors by root cause. Fix the upstream type change first, then cascading errors resolve. |
| Data integrity check fails after migration | Do NOT drop old data. Investigate discrepancies. Fix the migration transform and re-run the backfill on affected rows only. |
| Performance regression exceeds threshold | Profile the regression (query plan, memory allocation, network calls). Optimize or rollback if not fixable within the rollback window. |
| Feature flag fails to toggle | Verify flag configuration and deployment. If flags are stuck, use direct code deployment to rollback. |
| Compatibility layer introduces bugs | Isolate and fix the adapter. Run both old and new paths through the test suite independently. |
| Migration step partially completes | Determine the exact point of failure. Rollback the partial step before re-attempting. Never re-run a partially completed step without rollback first. |
| External service dependency blocks migration | Decouple the migration step from the external service. Use mocks or stubs for verification, defer the integration step. |
| Rollback itself fails | Escalate immediately. Restore from backup as last resort. Document the failure chain for post-mortem. |

---

## Outputs

| Output | Location | Purpose |
|--------|----------|---------|
| Migration assessment | Presented in chat | Risk classification and scope analysis |
| Migration plan | Presented in chat | Step-by-step plan with rollback points for user approval |
| Backup verification | Backup location per system | Safety net for catastrophic rollback |
| Migration commits | Git history | Atomic, traceable, reversible migration steps |
| Migration scripts | Project convention (e.g., `migrations/`, `db/migrate/`) | Repeatable schema or data migration |
| Migration report | Presented in chat | Comprehensive verification results and summary |
| Cleanup tasks | Presented in chat | Post-migration tasks to remove compatibility layers |

---

## Quality Checklist

Before marking the migration workflow complete:

- [ ] Migration type and risk level correctly classified
- [ ] All dependencies and blast radius mapped before starting
- [ ] Backup created and verified restorable before execution
- [ ] Migration plan approved by user before execution began
- [ ] Every step has an explicit rollback strategy documented
- [ ] Points of no return are clearly marked and acknowledged
- [ ] Each migration step committed individually with descriptive message
- [ ] Verification passed at every step — no step was skipped
- [ ] Full test suite passes after migration completes
- [ ] Data integrity checks pass (for data-carrying migrations)
- [ ] Performance is within acceptable thresholds compared to baseline
- [ ] Cleanup tasks documented for removing compatibility layers and feature flags

---

## Related

- **Command:** [`ai/commands/development/migrate-deps.md`](ai/commands/development/migrate-deps.md)
- **Skill:** [`ai/skills/testing/clean-code/SKILL.md`](ai/skills/testing/clean-code/SKILL.md)
- **Skill:** [`ai/skills/backend/architecture-patterns/SKILL.md`](ai/skills/backend/architecture-patterns/SKILL.md)
- **Skill:** [`ai/skills/api/database-migrations/SKILL.md`](ai/skills/api/database-migrations/SKILL.md)
- **Agent:** [`ai/agents/debugging/AGENT.md`](ai/agents/debugging/AGENT.md)
- **Agent:** [`ai/agents/testing/AGENT.md`](ai/agents/testing/AGENT.md)
- **Agent:** [`ai/agents/refactoring/AGENT.md`](ai/agents/refactoring/AGENT.md)

---

## NEVER Do

- **Never migrate without a green test baseline** — If tests are already failing, you cannot distinguish pre-existing failures from migration regressions. Fix the baseline first.
- **Never skip the backup step for data-carrying migrations** — Database schema changes, data format migrations, and any operation touching persistent data must have a verified backup before execution begins.
- **Never execute a migration without user approval of the plan** — The user must review and confirm the migration strategy, steps, and rollback points before any changes are made.
- **Never combine multiple migration types in a single step** — Upgrade the framework and migrate the database in separate, independently-verifiable steps. Mixing makes rollback impossible.
- **Never pass a point of no return without explicit confirmation** — Steps that cannot be rolled back (dropping columns, deleting old data, decommissioning services) require a separate, explicit user acknowledgment.
- **Never skip verification between migration steps** — Each step must be verified before proceeding to the next. A chain of unverified steps creates a rollback nightmare.
- **Never delete old data, schemas, or code paths during migration** — Keep them until the verification window closes. Cleanup is a separate, post-migration activity.
- **Never assume backward compatibility** — Verify it. Test old clients against new APIs, old queries against new schemas, old data against new parsers. Assumptions cause production incidents.
- **Never force a migration through failing checks** — If verification fails, stop and rollback. Proceeding past a failure compounds the problem and may cross a point of no return.
- **Never migrate without monitoring in place** — Error rates, latency, and data integrity must be observable during and after migration. Flying blind means you cannot detect regressions.
