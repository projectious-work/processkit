---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260504_0929-HonestSea-active-interlocutor-runtime-binding
  created: '2026-05-04T09:29:11+00:00'
  updated: '2026-05-04T09:39:38+00:00'
spec:
  title: Capability-negotiated active interlocutor runtime binding
  state: done
  type: story
  priority: high
  assignee: TEAMMEMBER-cora
  description: 'Implement capability-negotiated session binding for active TeamMembers:
    keep identity-only fallback, resolve desired runtime model/effort through model-recommender
    provider gates, surface identity/runtime mismatch at session start, improve Claude
    adapter export where safe, and document subagent/MCP lifecycle guardrails. Implementation
    is main-session only because harness subagents currently crash or leave MCP servers
    running.'
  started_at: '2026-05-04T09:29:24+00:00'
  completed_at: '2026-05-04T09:39:38+00:00'
---

## Transition note (2026-05-04T09:29:24+00:00)

Approved by user; implementation starting in main session only, no subagents.


## Transition note (2026-05-04T09:39:31+00:00)

Implemented active interlocutor runtime binding, conservative Claude adapter resolved model policy, subagent MCP guard documentation, src mirrors, and verification. Focused tests and smoke tests passed.


## Transition note (2026-05-04T09:39:38+00:00)

Verification passed: context and src team-manager suites 56 passed each, server smoke tests passed, py_compile passed, git diff --check clean, pk-doctor 0 errors with only archive.applied-migrations warning.
