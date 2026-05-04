---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260504_1202-HappyThorn-provider-neutral-pk-command-projections
  created: '2026-05-04T12:02:22+00:00'
  labels:
    component: commands
    harnesses:
    - claude
    - codex
    approved_on: '2026-05-04'
  updated: '2026-05-04T12:13:33+00:00'
spec:
  title: Implement provider-neutral pk command projections
  state: done
  type: task
  priority: medium
  description: 'Approved plan: codify processkit pk-* command model with canonical
    commands under context/skills/**/commands, slash-capable harness projections under
    .claude/commands, non-slash Codex trigger projections under .agents/skills, doctor
    parity checks, pk-explain-routing canonicalization or removal after analysis,
    stale command documentation cleanup, and verification via pk-doctor/release-audit.'
  started_at: '2026-05-04T12:13:18+00:00'
  completed_at: '2026-05-04T12:13:33+00:00'
---

## Transition note (2026-05-04T12:13:18+00:00)

Implementation started after approved plan recording.


## Transition note (2026-05-04T12:13:28+00:00)

Implementation complete; verification passed.


## Transition note (2026-05-04T12:13:33+00:00)

Verified with test_doctor, full pk-doctor, and release-audit --tree=src-context.
