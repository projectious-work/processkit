---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_1643-BraveDove-schema-drift-workitem-assignee
  created: '2026-04-22T16:43:52+00:00'
spec:
  title: 'Schema drift: workitem.assignee + decisionrecord.deciders[] still require
    ACTOR-*, reject TEAMMEMBER-*'
  state: backlog
  type: task
  priority: medium
  description: '**Missed during v0.19.0 Phase 1 schema work.** Two schemas still carry
    the old ACTOR-only pattern and reject the new TEAMMEMBER-* IDs:


    - `context/schemas/workitem.yaml` — `spec.assignee` pattern `^ACTOR-[a-zA-Z0-9_-]+$`

    - `context/schemas/decisionrecord.yaml` — `spec.deciders[]` items pattern (same
    shape)


    **Observed symptoms this session**:

    - `create_workitem(..., assignee="TEAMMEMBER-cora")` → schema validation failure
    (Phase 6 WI creation, worked around by omitting assignee).

    - `record_decision(..., deciders=["TEAMMEMBER-thrifty-otter"])` → schema validation
    failure (DEC-SnowyWolf recording, worked around by omitting deciders).


    **Fix (both trees)**:

    Extend both pattern fields to an alternation accepting either ACTOR-* (legacy)
    or TEAMMEMBER-*. Suggested pattern:

    `^(ACTOR|TEAMMEMBER)-[a-zA-Z0-9_-]+$`


    Even cleaner (if legacy Actor entities are fully removed by now): drop ACTOR-*
    entirely and require `^TEAMMEMBER-[a-zA-Z0-9_-]+$`. Verify there are no remaining
    ACTOR-* references in WorkItems or Decisions before flipping.


    **Also consider**: any other schemas that reference entity IDs of the identity
    class. Full audit with `grep -l ''^ACTOR-'' context/schemas/*.yaml` before shipping
    the fix.


    **Done when**

    - Both schemas accept TEAMMEMBER-*.

    - pk-doctor passes.

    - A quick smoke test: `create_workitem(..., assignee="TEAMMEMBER-cora")` and `record_decision(...,
    deciders=["TEAMMEMBER-thrifty-otter"])` both succeed.

    - Dual-tree drift clean.

    - Candidate for v0.19.2 patch release.'
---
