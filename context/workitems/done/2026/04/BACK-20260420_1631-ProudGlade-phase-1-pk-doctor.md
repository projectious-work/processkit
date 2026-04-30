---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260420_1631-ProudGlade-phase-1-pk-doctor
  created: '2026-04-20T16:31:22+00:00'
  updated: '2026-04-20T17:29:23+00:00'
spec:
  title: 'Phase 1: /pk-doctor skill + slash command — detect-only aggregator with
    4 categories (schema+filename, sharding, migrations, drift)'
  state: done
  type: epic
  priority: high
  description: |
    Ship Phase 1 of the `/pk-doctor` health-check aggregator per the shape approved in DEC-20260420_XXXX (pk-doctor). Four categories: schema+filename validation, sharding audit, pending-migration detection, src/↔context/ drift check.

    **Shape:** new skill at `context/skills/processkit/pk-doctor/` + `src/context/` mirror + slash command `/pk-doctor`. No MCP server in Phase 1. Detect-only default; opt-in `--fix=<cat[,cat...]>` or `--fix-all` for direct fixes (go through MCP write tools where applicable; prompt interactively on data-loss cases).

    **Layout:**
    ```
    context/skills/processkit/pk-doctor/                  (+ src/context/ mirror)
    ├── SKILL.md                       # 8 categories doc, severity model, --fix policy
    ├── commands/
    │   └── pk-doctor.md               # slash command entry (pattern: /pk-resume)
    ├── scripts/
    │   ├── check_schemas.py           # A. schema + filename check
    │   ├── check_sharding.py          # B. sharding audit (logs YYYY/MM, migrations buckets)
    │   ├── check_migrations.py        # C. pending migrations (wraps migration-mgmt MCP)
    │   └── check_drift.py             # D. wraps scripts/check-src-context-drift.sh
    └── doctor.py                      # aggregator: runs 4 checks, emits report + LogEntry
    ```

    **Invocation:**
    - `/pk-doctor` — default: all 4 detect
    - `/pk-doctor --category=schemas,migrations`
    - `/pk-doctor --fix=schemas` — scoped fix (prompts on data-loss)
    - `/pk-doctor --fix-all` — every fix path (still prompts on data-loss)
    - `/pk-doctor --since=v0.18.2`

    **Report:** `doctor.report` LogEntry with per-category {errors, warns, infos, top_findings}; summary to stdout.

    **Acceptance:**
    1. `/pk-doctor` completes in ≤10s over the current 323-entity index.
    2. Running against the current working tree surfaces: (a) 5 pending migrations, (b) any schema validation failures the per-write validator hasn't caught yet, (c) clean drift report.
    3. `--fix-all` handled interactively for any destructive path.
    4. LogEntry visible via `query_events(event_type="doctor.report")`.
    5. Dual-tree drift guard passes (`scripts/check-src-context-drift.sh`).

    **Out of scope (Phase 2 / separate WorkItems):** cross-ref integrity, PROVENANCE drift, MCP config integrity, smoke-import, version skew.</parameter>
    </invoke>
  started_at: '2026-04-20T16:34:04+00:00'
  completed_at: '2026-04-20T17:29:23+00:00'
---

## Transition note (2026-04-20T16:34:04+00:00)

Dispatching Plan agent to produce a detailed implementation plan (Phase 1: 4 categories), then worker for implementation per DEC-20260420_1631-WiseGarnet.


## Transition note (2026-04-20T17:29:22+00:00)

Implementation complete, smoke/drift/test all green, slash command registered in harness skill catalog, doctor.report LogEntry queryable. Owner accepted both architectural deviations. Grooming follow-up tracked in BACK-20260420_1729-SureTiger.


## Transition note (2026-04-20T17:29:23+00:00)

Shipping in the commit below.
