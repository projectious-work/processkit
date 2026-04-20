---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260420_1342-WarmClover-close-issue-9-via
  created: '2026-04-20T13:42:50+00:00'
spec:
  title: 'Close issue #9 via a new migration-management skill + MCP server (not an
    extension of an existing skill)'
  state: accepted
  decision: 'Add a new `migration-management` skill under `context/skills/processkit/migration-management/`
    with its own MCP server exposing 5 tools: `list_migrations(state=None)`, `get_migration(id)`,
    `start_migration(id)` (pending → in-progress), `apply_migration(id, notes=None)`
    (in-progress or pending via implicit start → applied), `reject_migration(id, reason)`
    (→ rejected, terminal). Transitions validate the state-machine edge, update YAML
    frontmatter (spec.state, started_at, applied_at/rejection_reason), move the file
    between directory buckets, refresh context/migrations/INDEX.md, and auto-log `migration.transitioned`
    / `migration.applied` / `migration.rejected` LogEntries via event-log. Reference
    implementation: mirror the layout of `workitem-management` (skill + MCP server
    + schema + scripts). Registration follows the existing per-skill mcp-config.json
    + installer merge pattern (do not hand-edit the generated harness config).'
  context: 'GitHub issue #9 reports that processkit exposes MCP tools for every state-machine-backed
    entity (WorkItem, DecisionRecord, Discussion, Scope) except Migration. The lifecycle
    context/migrations/{pending,in-progress,applied}/ is fully implemented on the
    CLI side (aibox migrate apply) but unreachable from an in-container agent, forcing
    it to shell out (bypassing MCP audit trail) or leave migrations pending across
    sessions. Real-world driver: aibox currently has 5 pending migrations the in-container
    agent cannot transition without host intervention. Owner approved the "new skill
    + MCP server" shape on 2026-04-20.'
  rationale: '(1) Pattern match — the 4 other state machines each own their own skill
    + server; giving Migration a parallel home preserves the mental model. (2) Directory
    shape — pending/in-progress/applied is unique to Migration; no existing skill
    owns that layout. (3) Downstream consumers expect the same addressability for
    every state machine; aibox and any future consumer will look under `migration-management`.
    Alternative considered and rejected: extending `workitem-management` to handle
    migrations as a WorkItem subtype — rejected because Migration has a different
    state set, directory layout, and auto-log event types; conflation would contort
    the WorkItem schema. The "no skill inflation" memory rule is satisfied because
    this is a new entity kind''s state machine, not a new workflow on an existing
    entity — the justification lives in WorkItem BACK-20260420_1339-TidyJay.'
  consequences: 'processkit gains a 5th state-machine-backed MCP surface. Downstream
    consumers (aibox + future) can drive migrations from any MCP-capable harness without
    shelling out. Migration index + event log auto-maintenance close the "hand-edit
    under context/" class of compliance-contract violation for this entity. Landing
    target: next minor release (v0.19.0 candidate), shipped through the standard release-semver
    pipeline. Requires coordinated update to consumer CLIs that duplicate the logic
    (aibox migrate apply) — they should delegate to the MCP surface where possible.'
  deciders:
  - ACTOR-owner
  - ACTOR-pm-claude
  related_workitems:
  - BACK-20260420_1339-TidyJay-add-migration-management-mcp
  decided_at: '2026-04-20T13:42:50+00:00'
---
