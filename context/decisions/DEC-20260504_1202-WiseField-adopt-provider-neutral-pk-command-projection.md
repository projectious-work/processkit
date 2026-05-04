---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_1202-WiseField-adopt-provider-neutral-pk-command-projection
  created: '2026-05-04T12:02:35+00:00'
spec:
  title: Adopt provider-neutral pk command projection model
  state: accepted
  decision: Processkit commands use canonical pk-* command adapters as the source
    of truth, project them into slash-command surfaces for harnesses that support
    registration, and project them into natural-language skill shims for harnesses
    that do not.
  context: The user approved the plan on 2026-05-04 after observing that unprefixed
    team commands and a Claude-only pk-explain-routing command caused command-surface
    drift. The desired behavior is that /pk-* works in slash-capable harnesses and
    prompts such as 'please pk-wrapup' trigger equivalent behavior in non-slash harnesses.
  rationale: A single canonical pk-* command namespace keeps processkit provider-neutral
    while preserving ergonomic harness-specific registration. Projection parity checks
    prevent Claude-only or Codex-only drift from reappearing.
  consequences: Implementation will update command docs, doctor checks, and projections.
    pk-explain-routing will be canonicalized if confirmed valuable; otherwise its
    Claude-only projection will be removed. Future processkit commands must ship canonical
    command adapters and matching harness projections.
  related_workitems:
  - BACK-20260504_1202-HappyThorn-provider-neutral-pk-command-projections
  decided_at: '2026-05-04T12:02:35+00:00'
---
