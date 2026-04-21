---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260421_2025-WiseAsh-pk-retro-signals-workitems
  created: '2026-04-21T20:25:14+00:00'
spec:
  title: pk-retro signals/workitems.py conflates cancelled-resolved with slipped
  state: backlog
  type: bug
  priority: medium
  description: 'context/skills/processkit/retrospective/scripts/signals/workitems.py
    classifies any WorkItem ending in state `cancelled` as "slipped" in the "What
    Slipped" section. But WorkItems get cancelled for different reasons:


    - **cancelled-resolved**: the underlying concern was addressed a different way
    (e.g. SunnyDawn 2026-04-09 → cancelled 2026-04-11 with transition note explaining
    that processkit config lives in per-skill settings.toml, not a new processkit.toml).

    - **cancelled-deferred**: still a real concern, pushed out (should maybe be `deferred`
    state in the first place).

    - **cancelled-abandoned**: decided we never want to do this.


    Only the second and third categories are retro-worthy "slippage". The first is
    project success, not failure.


    **Concrete incident:** /pk-retro --release v0.18.2 flagged SunnyDawn as slipped
    → --auto-workitems materialised BraveReef (BACK-20260421_1748) → owner caught
    the false positive on 2026-04-21.


    **Fix options:**

    1. Read the final transition note when classifying a cancelled WorkItem. Heuristic:
    if note contains "already solved", "already resolved", "superseded by", "decided
    against" → exclude from slipped list.

    2. Require the owner to pick `deferred` or `superseded` state explicitly for slippage;
    treat `cancelled` as success-neutral (exclude by default).

    3. Add an optional `cancellation_reason` field to the WorkItem schema with values
    `resolved | deferred | abandoned`, and gate slippage on the field. Needs schema
    migration.


    Recommend option 2 first (zero schema changes, aligns cancel semantics with project
    management norms — "cancelled" means "we''re not doing this; no longer a concern"),
    then option 3 as follow-up if the extra fidelity is needed.


    Also update `context/skills/processkit/retrospective/scripts/test_retro.py` —
    the "What Slipped" test currently asserts cancelled WorkItems flow into slipped;
    that assertion encoded the bug.


    Source retro artifact: ART-20260421_1747-BrightCrow-retrospective-v0-18-2

    Source DR: DEC-20260421_2033-*'
---
