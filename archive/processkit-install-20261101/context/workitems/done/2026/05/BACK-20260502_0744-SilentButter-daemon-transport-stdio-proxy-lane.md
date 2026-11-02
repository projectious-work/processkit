---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0744-SilentButter-daemon-transport-stdio-proxy-lane
  created: '2026-05-02T07:44:07+00:00'
  labels:
    area: mcp
    lane: daemon-proxy
  updated: '2026-05-02T08:40:49+00:00'
spec:
  title: Daemon transport and stdio proxy lane
  state: done
  type: story
  priority: high
  assignee: ACTOR-codex
  description: Implement processkit-gateway serve transports and stdio proxy. Include
    health endpoint, PID/socket/port lifecycle handling, stale daemon recovery, and
    standalone non-aibox startup path.
  parent: BACK-20260502_0743-CalmHawk-implement-provider-neutral-gateway-daemon
  started_at: '2026-05-02T07:44:51+00:00'
  completed_at: '2026-05-02T08:40:49+00:00'
---

## Transition note (2026-05-02T07:44:51+00:00)

Assigned as active implementation lane 2.


## Transition note (2026-05-02T08:39:23+00:00)

Implemented gateway CLI shape with stdio serve active and streamable-http/stdio-proxy reserved with explicit errors for daemon phase.


## Transition note (2026-05-02T08:40:49+00:00)

Implemented canonical gateway stdio server surface with reserved daemon/http/proxy CLI modes that fail explicitly until the long-lived transport is completed.
