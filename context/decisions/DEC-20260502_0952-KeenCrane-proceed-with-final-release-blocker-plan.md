---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260502_0952-KeenCrane-proceed-with-final-release-blocker-plan
  created: '2026-05-02T09:52:46+00:00'
spec:
  title: Proceed with final release blocker plan and optional aibox reset handoff
  state: accepted
  decision: Implement the final processkit release blocker plan, including deliverable-scoped
    release gates, v2 deliverable audit updates, Model/Process/Metric demotion contract
    cleanup, final verification, and an aibox handover. The harder aibox reset is
    optional and should be recommended as an opt-in mode of aibox apply or aibox reset;
    the normal migration flow remains the default.
  context: 'The user approved the remaining blocker plan and requested Lane 4 adaptations:
    make the reset optional and user-decided, keep current migrations as the normal
    path, and add a final aibox handover document covering Lane 4 and other release-facing
    changes.'
  rationale: This keeps processkit/aibox decoupled, avoids forcing destructive reset
    semantics onto normal upgrades, and gives aibox a concrete integration contract
    for MCP daemon deployment and migration/reset orchestration.
  alternatives:
  - option: Make hard reset the default upgrade path
    reason_not_chosen: Too disruptive and unnecessary for normal migrations.
  - option: Leave reset entirely out of processkit planning
    reason_not_chosen: aibox needs a clear handoff contract and processkit-owned schema/export
      expectations.
  consequences: processkit will provide release gates, deliverable audit checks, reset
    handoff specs, and documentation. aibox remains responsible for optional reset
    command UX and devcontainer wiring. Generated harness config remains managed by
    aibox sync rather than hand-edited in processkit.
  related_workitems:
  - BACK-20260502_0952-SunnyButter-final-release-blockers-aibox-handoff
  decided_at: '2026-05-02T09:52:46+00:00'
---
