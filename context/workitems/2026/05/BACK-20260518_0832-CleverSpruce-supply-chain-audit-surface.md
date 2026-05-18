---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260518_0832-CleverSpruce-supply-chain-audit-surface
  created: '2026-05-18T08:32:32+00:00'
  labels:
    area: processkit
    feature: supply-chain-audit
    phases:
    - license-inventory
    - security-outdated
    - supplier-quality
  updated: '2026-05-18T08:46:54+00:00'
spec:
  title: Implement supply-chain audit skill, MCP, command, and doctor integration
  state: review
  type: story
  priority: high
  description: 'Implement all supply-chain audit phases: Phase 1 offline dependency
    inventory/license classification/SBOM/reporting; Phase 2 optional vulnerability
    and outdated scanner orchestration; Phase 3 advisory supplier quality signals.
    Add skill UX, command adapter, MCP server, pk-doctor supply_chain summary, policy
    file contract, tests, and src/context mirroring.'
  started_at: '2026-05-18T08:32:58+00:00'
---

## Transition note (2026-05-18T08:32:58+00:00)

Implementation started after accepted supply-chain audit surface decision DEC-20260518_0832-WorthyOrchard.


## Transition note (2026-05-18T08:46:54+00:00)

Implementation and validation completed. Ready for review; direct in-progress -> done transition is not allowed by the WorkItem state machine.
