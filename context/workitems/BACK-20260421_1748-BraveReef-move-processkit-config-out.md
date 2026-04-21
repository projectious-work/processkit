---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260421_1748-BraveReef-move-processkit-config-out
  created: '2026-04-21T17:48:30+00:00'
spec:
  title: Move processkit config out of aibox.toml (revisit SunnyDawn for v0.19.0)
  state: backlog
  type: chore
  priority: medium
  description: 'Materialized by /pk-retro v0.18.2 retrospective as the sole proposed
    action item. The original SunnyDawn WorkItem (BACK-20260409_1452) was cancelled
    last cycle without being reassessed; owner directive 2026-04-21 is "no deferral"
    for v0.19.0.


    Source retro artifact: ART-20260421_1747-BrightCrow-retrospective-v0-18-2.

    Source retro decision: DEC-20260421_1125-SpryCedar-loyalfrog-ship-all-phases (retro
    skill delivery that surfaced this item).


    Scope to re-evaluate in v0.19.0 grooming:

    - What provider-neutral location replaces aibox.toml for the processkit section?

    - Is this still driven by the original motivation, or has it shifted (e.g. new
    harness added since)?

    - Does the migration need a content migration doc for downstream projects pinned
    to aibox.toml?'
---
