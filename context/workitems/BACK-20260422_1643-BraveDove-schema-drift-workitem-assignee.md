---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_1643-BraveDove-schema-drift-workitem-assignee
  created: '2026-04-22T16:43:52+00:00'
  updated: '2026-04-23T11:01:53+00:00'
spec:
  title: 'Schema drift: workitem.assignee + decisionrecord.deciders[] still require
    ACTOR-*, reject TEAMMEMBER-*'
  state: done
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
  started_at: '2026-04-23T09:01:59+00:00'
  completed_at: '2026-04-23T11:01:53+00:00'
---

## Transition note (2026-04-23T09:01:59+00:00)

Starting: will audit all schemas for ACTOR-* patterns, count residual ACTOR-* references in WorkItems/Decisions to decide alternation vs. clean flip, then apply fix to both trees and smoke-test.


## Transition note (2026-04-23T09:04:51+00:00)

Fix applied to 5 schemas (broader than the 2 originally called out — audit surfaced artifact.owner, metric.owner, and discussion.participants[] as additional affected fields):

- context/schemas/workitem.yaml:46 spec.assignee
- context/schemas/decisionrecord.yaml:62 spec.deciders[] items
- context/schemas/discussion.yaml:36 spec.participants[] items
- context/schemas/artifact.yaml:64 spec.owner
- context/schemas/metric.yaml:56 spec.owner

Pattern updated from `^ACTOR-[a-zA-Z0-9_-]+$` to `^(ACTOR|TEAMMEMBER)-[a-zA-Z0-9_-]+$` (alternation chosen over clean flip — 90 residual ACTOR-* references across 44 existing entity files would otherwise retroactively fail validation). Descriptions updated to read "Actor or TeamMember".

Both trees in sync: context/schemas/ ↔ src/context/schemas/ (diff -q clean). No residual `^ACTOR-only` patterns remain in schemas.

Offline verification passed: jsonschema/regex test of all 5 patterns accepts TEAMMEMBER-cora, TEAMMEMBER-thrifty-otter, ACTOR-pm-claude, ACTOR-legacy; rejects FOO-bar, teammember-cora (lowercase), ACTOR- (empty suffix), -cora.

Live MCP smoke test result: create_workitem(..., assignee="TEAMMEMBER-cora") FAILED with the OLD schema error ("'TEAMMEMBER-cora' does not match '^ACTOR-[a-zA-Z0-9_-]+$'"). Confirmed: workitem-management MCP server caches schemas at startup; harness restart required to pick up the fix. This is the same wait-for-restart pattern as SteadyCedar was.

Pending: harness restart → re-run create_workitem smoke test with TEAMMEMBER-cora assignee → if it succeeds, transition to done. If it fails after restart, there is a further bug beneath the schema.


## Transition note (2026-04-23T11:01:53+00:00)

Post-restart live smoke tests green: (1) create_workitem accepted assignee=TEAMMEMBER-cora → BACK-20260423_1101-TrueGrove; (2) record_decision accepted deciders=[TEAMMEMBER-cora] → DEC-20260423_1101-SunnyComet. Alternation pattern `^(ACTOR|TEAMMEMBER)-[a-zA-Z0-9_-]+$` is live across all 5 audited schemas.
