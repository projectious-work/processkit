---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260409_1757-SolidSky-auto-log-in-entity
  created: '2026-04-09T17:57:53+00:00'
  updated: '2026-04-09T21:33:57+00:00'
spec:
  title: Index freshness strategy — auto-reindex and auto-log
  state: done
  type: task
  priority: medium
  description: |
    Two related gaps in index freshness:

    1. Auto-reindex on session start (or after out-of-band writes). Any write that bypasses the MCP
       path — migration scripts, hand edits, git checkout, aibox sync — leaves the index
       stale with no automatic recovery. Options: (a) index-management exposes a lightweight
       freshness check (file mtime vs index updated_at) that agents run on session start;
       (b) a post-write hook in the lib that triggers upsert after any entity.write();
       (c) document that reindex() should be the last step of any out-of-band bulk operation
       (currently done by convention only).

    2. Auto-log in entity-creating and state-transitioning MCP servers. Mechanical
       operations (create_workitem, transition_workitem, record_decision, create_scope,
       evaluate_gate, etc.) should write a LogEntry as a side effect — the same way
       they already call index.upsert_entity. Explicit judgment-call logging (session
       handovers, behavioral notes) stays agent-driven via the event-log MCP server.

    Implementation for (1): add entity.write() to call index.upsert_entity as a side
    effect via an optional callback, OR add a session-start freshness hint to
    agent-management skill. Implementation for (2): add a log_side_effect() helper
    in src/lib/processkit/ called by each server after the entity write succeeds.
    Extend smoke-test-servers.py to assert log entries are created as side effects.
  started_at: '2026-04-09T21:33:48+00:00'
  completed_at: '2026-04-09T21:33:57+00:00'
---
