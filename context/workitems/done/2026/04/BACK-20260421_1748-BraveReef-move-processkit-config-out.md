---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260421_1748-BraveReef-move-processkit-config-out
  created: '2026-04-21T17:48:30+00:00'
  updated: '2026-04-21T20:25:17+00:00'
spec:
  title: Move processkit config out of aibox.toml (revisit SunnyDawn for v0.19.0)
  state: cancelled
  type: chore
  priority: medium
  description: |
    Materialized by /pk-retro v0.18.2 retrospective as the sole proposed action item. The original SunnyDawn WorkItem (BACK-20260409_1452) was cancelled last cycle without being reassessed; owner directive 2026-04-21 is "no deferral" for v0.19.0.

    Source retro artifact: ART-20260421_1747-BrightCrow-retrospective-v0-18-2.
    Source retro decision: DEC-20260421_1125-SpryCedar-loyalfrog-ship-all-phases (retro skill delivery that surfaced this item).

    Scope to re-evaluate in v0.19.0 grooming:
    - What provider-neutral location replaces aibox.toml for the processkit section?
    - Is this still driven by the original motivation, or has it shifted (e.g. new harness added since)?
    - Does the migration need a content migration doc for downstream projects pinned to aibox.toml?
  completed_at: '2026-04-21T20:25:17+00:00'
---

## Transition note (2026-04-21T20:25:17+00:00)

Cancelled per owner review 2026-04-21: retro false positive. SunnyDawn (the source item /pk-retro referenced) was itself cancelled 2026-04-11 because the concern was already resolved via per-skill settings.toml files + AGENTS.md preferences section. The only [processkit] key remaining in aibox.toml is the consumer-side source/version/src_path triple, which is aibox CLI's legitimate concern. Root cause of the false positive: pk-retro's signals/workitems.py treats all cancelled WorkItems as slipped — filed separately as a retrospective-skill bug.
