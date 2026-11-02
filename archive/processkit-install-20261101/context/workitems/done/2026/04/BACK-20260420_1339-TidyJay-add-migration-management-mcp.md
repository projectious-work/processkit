---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260420_1339-TidyJay-add-migration-management-mcp
  created: '2026-04-20T13:39:49+00:00'
  updated: '2026-04-20T16:08:41+00:00'
spec:
  title: 'Add migration-management MCP server — expose Migration state machine to
    in-session agents (closes #9)'
  state: done
  type: epic
  priority: high
  description: |
    Reported upstream in issue #9 (2026-04-19, filed from aibox consumer). processkit exposes MCP tools for every state machine except Migration: WorkItem (transition_workitem), DecisionRecord (transition_decision, supersede_decision), Discussion (transition_discussion, add_outcome, open_discussion), Scope (transition_scope) — but Migration has none. The lifecycle `context/migrations/{pending,in-progress,applied}/` is fully implemented on the CLI side (aibox migrate apply) but unreachable from an in-container agent, forcing it to either shell out (bypasses MCP audit trail) or leave pending migrations across sessions.

    Proposed shape from #9:
    - list_migrations(state=None) — read-side
    - get_migration(id) — read-side
    - start_migration(id) — pending → in-progress
    - apply_migration(id, notes=None) — in-progress (or pending via implicit start) → applied
    - reject_migration(id, reason) — → rejected (terminal)

    Transitions must validate the edge, update YAML frontmatter (spec.state, started_at, applied_at/rejection_reason), move files between directory buckets, refresh context/migrations/INDEX.md, and auto-log a `migration.transitioned` / `migration.applied` / `migration.rejected` LogEntry via event-log — matching the pattern of workitem-management / decision-record / discussion-management.

    Open scoping question (blocks kick-off): new `migration-management` skill + MCP server vs. extending an existing skill. Recommended shape: new skill + MCP server (mirrors how the other 3 state machines each own their own skill), but memory cautions against skill inflation, so this needs an explicit DecisionRecord before implementation begins.

    Real-world driver: aibox has 5 pending migrations right now (2 v0.18.1 no-ops + 3 from the 2026-04-19 sync) that the in-container agent cannot transition without host intervention.
  started_at: '2026-04-20T14:05:41+00:00'
  completed_at: '2026-04-20T16:08:41+00:00'
---

## Transition note (2026-04-20T14:05:41+00:00)

Implementation complete and smoke-tested; moving to review after owner sign-off. Dual-tree mirroring verified (context/ and src/context/ both carry identical server.py + SERVER.md + mcp-config.json). Drift guard passes. Awaiting owner review before transitioning to review → done.


## Transition note (2026-04-20T16:08:37+00:00)

Implementation, smoke tests, and drift guard all green. Owner approved in-session.


## Transition note (2026-04-20T16:08:41+00:00)

Landed via feat commit (below). Smoke tests + drift guard both green; owner approved.
