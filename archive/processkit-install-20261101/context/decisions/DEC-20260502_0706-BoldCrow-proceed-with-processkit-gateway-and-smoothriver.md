---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260502_0706-BoldCrow-proceed-with-processkit-gateway-and-smoothriver
  created: '2026-05-02T07:06:29+00:00'
spec:
  title: Proceed with processkit gateway and SmoothRiver v2 recovery using parallel
    lanes
  state: accepted
  decision: 'Proceed with the approved implementation plan: persist the plan as a
    processkit Artifact, split work into parallel developer lanes, implement a staged
    processkit MCP gateway to reduce devcontainer memory pressure, and complete remaining
    SmoothRiver/SmoothTiger v2 deliverables in src/ while preserving the split-track
    no-shim rule.'
  context: The owner approved the reconstructed plan after a crash lost the previous
    implementation plan. Current source state shows an aggregate-mcp prototype, partial
    v2 foundations, incomplete Model/Process/Schedule/StateMachine demotions, and
    stale docs. aibox is waiting on processkit deliverables and owns deployment/wiring,
    while processkit owns gateway semantics and entity/tool runtime behavior.
  rationale: Persisting the plan first prevents another interruption from losing the
    execution structure. Parallel lanes are appropriate because gateway runtime, schema
    demotions, MCP semantics, doctor/tests, and docs have mostly disjoint write scopes.
    The staged gateway path gives a quick aggregate-mode memory improvement before
    building the fuller daemon/lazy-loading runtime.
  alternatives:
  - option: Continue without recording the plan
    rejected_because: The previous crash already demonstrated that unrecorded plans
      are lost and hard to reconstruct.
  - option: Implement only aibox-side process reduction
    rejected_because: That would force aibox to own processkit semantics and violate
      the accepted processkit/aibox split.
  - option: Jump directly to a daemon without aggregate-mode staging
    rejected_because: Higher risk; aggregate mode already exists and can validate
      the one-process tool surface first.
  - option: Keep v1/v2 compatibility shims indefinitely
    rejected_because: Conflicts with the accepted SmoothTiger breaking-v2 no-shim
      direction.
  consequences: The implementation will create multiple lane WorkItems, run worker
    agents on disjoint write scopes, keep live context changes MCP-managed, and use
    the main session for integration and verification. aibox follow-up work can consume
    the gateway/deployment boundary once processkit delivers the runtime shape.
  deciders:
  - TEAMMEMBER-thrifty-otter
  - ACTOR-codex
  related_workitems:
  - BACK-20260409_1652-WildButter-create-polish-and-deploy
  decided_at: '2026-05-02T07:06:29+00:00'
---
