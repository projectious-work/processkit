---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260420_1631-WiseGarnet-add-pk-doctor-skill
  created: '2026-04-20T16:31:13+00:00'
  updated: '2026-04-20T16:34:04+00:00'
spec:
  title: 'Add pk-doctor skill — detect-only aggregator health check with opt-in direct
    fixes (Phase 1 scope: 4 categories)'
  state: accepted
  decision: |
    Add a new `pk-doctor` skill under `context/skills/processkit/pk-doctor/` (+ `src/context/` mirror) exposed via the `/pk-doctor` slash command. No MCP server in the initial landing — this is a user-triggered diagnostic aggregator, not a machine-invocable tool. Skill is justified against the "no skill inflation" rule as a distinct aggregator workflow (peer precedent: `morning-briefing`), not an extension of any existing entity skill.

    **Invocation:**
    - `/pk-doctor` — detect-only, all categories, full report (default)
    - `/pk-doctor --category=<name[,name...]>` — scoped detect
    - `/pk-doctor --fix=<name[,name...]>` — opt-in autofix, one or more categories
    - `/pk-doctor --fix-all` — autofix across every category that supports fix (explicit owner request; matches the "rescue a freshly-upgraded repo" use case)
    - `/pk-doctor --since=<git-ref>` — only check entities modified since ref

    **Fix policy:** doctor fixes directly (not via emitted Migration entities — owner override of the PM's proposal to route through the migration state machine). Direct fixes still go through the appropriate MCP write tool for the entity kind (transition_*, update metadata.id via file rename + index reindex, etc.) — they do NOT hand-edit under `context/`. For any fix where data might be lost (e.g., schema field removal), doctor prompts interactively before writing. Audit trail is preserved via the doctor.report LogEntry plus the auto-logged MCP write events.

    **Report storage:** each run writes a `doctor.report` LogEntry with per-category counts, severity breakdown (ERROR/WARN/INFO), and top findings. Reports are queryable via `query_events(event_type="doctor.report")` for trend analysis. Human-readable summary goes to stdout on invocation.

    **Phase 1 scope (this WorkItem):** 4 checks that reuse existing MCP reads + scripts:
    1. **schema + filename** — each entity validates against `src/context/schemas/<kind>.yaml` (NOT the template mirror, which is a diff baseline); filename stem matches `metadata.id`; if filename encodes a date, it matches `metadata.created`.
    2. **sharding** — logs split by `YYYY/MM`; migrations in state-bucket subdirs; entities in wrong buckets flagged.
    3. **migrations** — pending migrations listed via `migration-management.list_migrations`; stale pending entries surfaced; `--fix` offers to apply (interactive).
    4. **drift** — wraps `scripts/check-src-context-drift.sh`; surfaces `context/` ↔ `src/context/` divergence.

    **Phase 2 (separate WorkItem, out of scope here):** cross-refs (orphan + dangling), `PROVENANCE.toml` drift, `mcp-config.json` integrity, smoke-import of each MCP server, version skew (aibox.lock vs installed SKILL.md pins).

    **Phase 3 (future, only if demand shows up):** lift checks into an MCP server for machine invocation; harden `--fix` paths.</parameter>
    <parameter name="rationale">(1) Aggregator over existing infra — 7 of 8 proposed checks reuse existing MCP reads + scripts; net-new code is mostly the aggregator + report formatter + severity tiers. (2) Detect-only default matches the npm/brew/rustup doctor pattern and keeps blast radius low; `--fix` and `--fix-all` are explicit opt-in, scoped to categories, and prompt on data-loss cases. (3) Doctor fixes directly rather than emitting Migrations — owner's call; rationale is "one-step rescue" for a just-upgraded repo, rather than a second-stage approval loop. Tradeoff accepted: less reversibility, but the `doctor.report` LogEntry + auto-logged MCP write events provide adequate audit trail for this use case. (4) LogEntry for report storage (not Artifact) — lighter, queryable by event_type, fits the aggregate-history use case. (5) Slash command + skill (no MCP server) — user-triggered; MCP server earns its place later if machine invocation emerges.</parameter>
    <parameter name="consequences">processkit gains a single user-visible health-check surface. Phase 1 lands ~600 LOC of net-new code + ~600 LOC of dual-tree mirror. CHANGELOG entry under v0.19.0-candidate adds /pk-doctor alongside migration-management. No schema changes in Phase 1. Downstream consumers (aibox) will gain `/pk-doctor` as a user-invokable slash command after they pull v0.19.0; no aibox-side integration required. Phase 2 + Phase 3 each get their own WorkItem + DecisionRecord when scheduled.</parameter>
    <parameter name="deciders">["ACTOR-owner", "ACTOR-pm-claude"]
  context: Owner has been repeatedly burned by incomplete upgrades between processkit
    releases (v0.15.0–v0.18.0 silent drift, v0.18.1 path regression, 5 pending migrations
    across 2 sync cycles). The existing diagnostic surface is fragmented across `scripts/smoke-test-servers.py`,
    `scripts/check-src-context-drift.sh`, `index-management.list_errors`, `id-management.validate_id`,
    and the new `migration-management` MCP — none of these is a single aggregator
    the operator can invoke on demand ("is this repo healthy?"). Owner sketched the
    shape in `pk-doctor skill.txt` with 3 sections (schema+filename, sharding, migration
    cleanup); this decision broadens scope to 8 categories, formalizes the detect/fix
    split, and picks an implementation shape.
  decided_at: '2026-04-20T16:31:13+00:00'
  related_workitems:
  - BACK-20260420_1631-ProudGlade-phase-1-pk-doctor
---
