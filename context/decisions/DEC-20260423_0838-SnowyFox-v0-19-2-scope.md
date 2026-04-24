---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260423_0838-SnowyFox-v0-19-2-scope
  created: '2026-04-23T08:38:21+00:00'
spec:
  title: 'v0.19.2 scope and fix order: SteadyCedar → BraveDove → TrueQuail'
  state: accepted
  decision: 'v0.19.2 will contain three WorkItems: BACK-20260423_0829-SteadyCedar
    (model-recommender pyyaml dependency), BACK-20260422_1643-BraveDove (schema drift
    on workitem.assignee + decisionrecord.deciders[]), and BACK-20260423_0829-TrueQuail
    (aibox installer .mcp.json drift reconciliation). They will be fixed in the stated
    order.'
  context: After the v0.19.0/v0.19.1 ship and the ProudStone diagnostic session on
    2026-04-23, three concrete defects blocking full v0.19.0 dogfood were identified
    and filed as backlog items. The user authorized proceeding with the work in response
    to the session-start briefing.
  rationale: Fix order is picked on unblock-value:\n1. SteadyCedar first — it is the
    shortest fix (one-line PEP 723 edit) and it unblocks the Cora routing dogfood
    that was already the explicit next-recommended-action.\n2. BraveDove second —
    it unblocks correct TeamMember-* assignee fields across every create_workitem
    / record_decision call, which is a constant ergonomic tax until fixed.\n3. TrueQuail
    third — it is the structural fix that prevents the whole class of "hand-merged
    .mcp.json" sessions from recurring, but is harder and does not block anything
    while the hand-merge stays in place.
  alternatives:
  - option: Ship only SteadyCedar as a v0.19.1.1 hotfix
    rejected_because: Three known defects of similar scope — bundling them into v0.19.2
      is cheaper than cutting two releases.
  - option: Defer all three to v0.20.0 alongside new features
    rejected_because: SteadyCedar blocks the v0.19.0 dogfood right now; v0.20.0 timing
      is not set.
  - option: Fix BraveDove first
    rejected_because: BraveDove's test surface is wider; SteadyCedar is a strict subset
      and lets the dogfood proceed in parallel.
  consequences: v0.19.2 ships as a defect-only bugfix release, no new features. Once
    merged, the compliance-contract rule "do not hand-edit .mcp.json" is restored
    to real enforceability because the installer will re-merge on per-skill-config
    drift. BraveDove's fix retires the ACTOR-* workaround used in several recent WIs.
  related_workitems:
  - BACK-20260423_0829-SteadyCedar-model-recommender-mcp-server
  - BACK-20260422_1643-BraveDove-schema-drift-workitem-assignee
  - BACK-20260423_0829-TrueQuail-aibox-installer-reconcile-mcp
  decided_at: '2026-04-23T08:38:21+00:00'
---
