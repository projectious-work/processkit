---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0857-JollyDove-gateway-stdio-proxy-lane
  created: '2026-05-02T08:57:13+00:00'
  updated: '2026-05-10T03:51:23+00:00'
spec:
  title: Gateway stdio proxy lane
  state: done
  type: story
  priority: critical
  assignee: ACTOR-codex
  description: Implement processkit-gateway stdio-proxy --url as a lightweight MCP
    stdio-to-daemon bridge that does not import processkit backing servers. Cover
    initialization, tool listing, tool calls, errors, and shutdown.
  parent: BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
  started_at: '2026-05-02T08:57:33+00:00'
  completed_at: '2026-05-10T03:51:23+00:00'
---

## Transition note (2026-05-02T08:57:33+00:00)

Starting stdio proxy implementation.


## Transition note (2026-05-02T09:34:02+00:00)

Stdio proxy helper implemented and end-to-end smoke-tested against local streamable-http daemon.


## Transition note (2026-05-10T03:51:23+00:00)

Triage audit 2026-05-10: Shipped. stdio-proxy helper implemented and end-to-end smoke-tested per WI note at 2026-05-02T09:34:02. v0.25.0 CHANGELOG confirms stdio-proxy transport added (commit 8b219b3). Auto-start of local daemon further fixed in commit ee231d2 (v0.25.4). Active .mcp.json confirms gateway stdio-proxy is the live harness config.
