---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260502_0707-CleverHare-mcp-semantics-gateway-lane
  created: '2026-05-02T07:07:26+00:00'
  updated: '2026-05-02T07:27:24+00:00'
spec:
  title: MCP semantics lane - align servers with v2 gateway surface
  state: done
  type: task
  priority: high
  assignee: ACTOR-codex
  description: 'Developer lane. Write scope: affected processkit MCP servers and shared
    semantics, especially model-recommender, artifact-management, binding-management,
    note-management, migration-management, index-management, and related mcp/SERVER.md
    files. Align APIs with v2 demoted contracts, preserve schema/state-machine enforcement,
    and ensure aggregate/gateway tool surface does not expose unintended tools.'
  parent: BACK-20260502_0706-NobleSwan-gateway-v2-recovery-epic
  started_at: '2026-05-02T07:08:07+00:00'
  completed_at: '2026-05-02T07:27:24+00:00'
---

## Transition note (2026-05-02T07:08:07+00:00)

Developer lane starting.


## Transition note (2026-05-02T07:27:02+00:00)

Implementation complete: model recommender now prefers roster JSON, docs/tool descriptions aligned with v2 and gateway surface; focused and full smoke verification passed.


## Transition note (2026-05-02T07:27:24+00:00)

Accepted after focused model-recommender tests and full smoke.
