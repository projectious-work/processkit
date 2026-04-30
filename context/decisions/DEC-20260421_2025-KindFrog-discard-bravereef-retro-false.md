---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260421_2025-KindFrog-discard-bravereef-retro-false
  created: '2026-04-21T20:25:01+00:00'
spec:
  title: Discard BraveReef — retro false positive; file pk-retro signal bug
  state: accepted
  decision: 'Cancel BraveReef (BACK-20260421_1748) — the concern it restated was already
    resolved on 2026-04-11 when SunnyDawn was cancelled with an explicit transition
    note: "processkit config lives in the preferences table in AGENTS.md, managed
    in-place by agents editing context/skills/*/config/settings.toml. aibox writes
    these at install time. Provider-neutral config story is already solved." The only
    remaining `[processkit]` key in aibox.toml is the consumer-side `source`/`version`/`src_path`
    triple, which is aibox CLI''s legitimate concern (it needs to know which processkit
    repo to install). Nothing to move. Also file a bug against the retrospective skill:
    `signals/workitems.py` treats any `cancelled` WorkItem as "slipped", conflating
    cancelled-because-resolved with cancelled-because-abandoned.'
  context: Owner reviewed aibox.toml after KindMeadow shipped and observed no processkit
    config that needs moving. /pk-retro's v0.18.2 dogfood run had flagged SunnyDawn
    as "slipped" because its final state was `cancelled` — but cancelled means "resolved
    differently", not "abandoned". The retrospective's signals/workitems.py does not
    read the cancellation transition note, so it materialised a false action item
    which then got promoted to a WorkItem via --auto-workitems.
  rationale: 'Two-line root cause: (1) SunnyDawn was already resolved via per-skill
    settings.toml files — we have the resolution note. (2) pk-retro''s classifier
    treats `cancelled` as slipped; it needs to either read the transition note or
    accept only `superseded`/`deferred` states as slippage evidence.'
  consequences: BraveReef cancelled. ART-20260421_1747-BrightCrow retro artifact stays
    untouched (frozen point-in-time record of what /pk-retro actually produced — historically
    honest). A new bug WorkItem will be filed for the retrospective signals regression.
  deciders:
  - ACTOR-owner
  related_workitems:
  - BACK-20260421_1748-BraveReef-move-processkit-config-out
  - BACK-20260409_1452-SunnyDawn-move-processkit-config-out
  - BACK-20260420_1340-LoyalFrog-add-pk-retro-skill
  decided_at: '2026-04-21T20:25:01+00:00'
---
