---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260502_0744-BoldCrane-harness-compatibility-documentation-lane
  created: '2026-05-02T07:44:16+00:00'
  labels:
    area: docs
    lane: harness-compat
  updated: '2026-05-02T08:41:00+00:00'
spec:
  title: Harness compatibility documentation lane
  state: done
  type: story
  priority: medium
  assignee: ACTOR-codex
  description: Document per-skill, aggregate, daemon, and daemon-proxy modes for Claude/Codex,
    OpenCode, Hermes, and Aider. Include non-aibox usage and aibox boundary without
    making processkit depend on aibox.
  parent: BACK-20260502_0743-CalmHawk-implement-provider-neutral-gateway-daemon
  started_at: '2026-05-02T08:40:56+00:00'
  completed_at: '2026-05-02T08:41:00+00:00'
---

## Transition note (2026-05-02T08:40:56+00:00)

Documented provider-neutral gateway modes and harness compatibility for Claude Code, Codex, OpenCode, Hermes, and Aider.


## Transition note (2026-05-02T08:40:58+00:00)

Docs include processkit/aibox boundary and explain that processkit remains usable without aibox.


## Transition note (2026-05-02T08:41:00+00:00)

Documentation build passed; only existing site-wide /processkit/ broken-link warning remains.
