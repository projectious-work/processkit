---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260421_2028-SharpGrove-wiseash-adopt-option-2
  created: '2026-04-21T20:28:22+00:00'
spec:
  title: WiseAsh — adopt option 2 (cancelled = success-neutral)
  state: accepted
  decision: 'Fix BACK-20260421_2025-WiseAsh via option 2 from the WorkItem description:
    signals/workitems.py counts only `deferred` and `superseded` as slippage evidence.
    `cancelled` is dropped from the slipped bucket entirely. Semantics align with
    PM norm: cancelled = "we''re not doing this; no longer a concern". No schema changes.
    Option 3 (explicit `cancellation_reason` enum) is explicitly deferred until we
    see a real case where cancelled-resolved vs cancelled-abandoned needs separation.'
  context: Owner reviewed the 3 fix options in BACK-20260421_2025-WiseAsh following
    the BraveReef false-positive incident, and approved option 2. The existing "slipped
    includes cancelled" assertion in test_retro.py encodes the bug and must be updated.
  rationale: Cheapest correct fix. Zero schema migration. Aligns cancel semantics
    with how the rest of the project management universe uses it.
  deciders:
  - ACTOR-owner
  related_workitems:
  - BACK-20260421_2025-WiseAsh-pk-retro-signals-workitems
  - BACK-20260421_1748-BraveReef-move-processkit-config-out
  - BACK-20260420_1340-LoyalFrog-add-pk-retro-skill
  decided_at: '2026-04-21T20:28:22+00:00'
---
