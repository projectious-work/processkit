---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0857-JollyDove-gateway-stdio-proxy-lane
  created: '2026-05-02T08:57:13+00:00'
  updated: '2026-05-02T09:34:02+00:00'
spec:
  title: Gateway stdio proxy lane
  state: review
  type: story
  priority: critical
  assignee: ACTOR-codex
  description: Implement processkit-gateway stdio-proxy --url as a lightweight MCP
    stdio-to-daemon bridge that does not import processkit backing servers. Cover
    initialization, tool listing, tool calls, errors, and shutdown.
  parent: BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
  started_at: '2026-05-02T08:57:33+00:00'
---

## Transition note (2026-05-02T08:57:33+00:00)

Starting stdio proxy implementation.


## Transition note (2026-05-02T09:34:02+00:00)

Stdio proxy helper implemented and end-to-end smoke-tested against local streamable-http daemon.
