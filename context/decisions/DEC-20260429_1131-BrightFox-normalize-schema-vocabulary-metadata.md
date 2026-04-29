---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260429_1131-BrightFox-normalize-schema-vocabulary-metadata
  created: '2026-04-29T11:31:38+00:00'
spec:
  title: Normalize schema vocabulary metadata
  state: accepted
  decision: Represent processkit schema vocabulary lists as ordinary Schema spec fields
    rather than top-level x-* extension keys.
  context: A review of the delivery standard found top-level x-* schema metadata in
    actor, binding, role, model, and team-member schemas. These lists describe processkit-owned
    vocabularies such as binding types, seniority levels, function groups, model capacity
    tiers, model effort levels, team-member memory tiers, sensitivity levels, and
    role actor IDs.
  rationale: The x-* convention is useful for foreign extension points, but these
    values are not foreign extensions; they are part of the processkit standard. Keeping
    them under spec makes the standard cleaner, easier to document, and less surprising
    for derived projects while preserving the same validation semantics.
  alternatives:
  - option: Keep top-level x-* keys
    reason: No migration cost, but preserves a local extension style for first-class
      processkit concepts.
  - option: Inline every vocabulary only inside JSON Schema enum fields
    reason: Reduces metadata fields, but loses a central readable vocabulary section
      and duplicates values across schemas.
  consequences: New processkit releases should ship spec.role_actor_ids, spec.known_types,
    spec.seniority_levels, spec.function_groups, spec.capacity_tiers, spec.effort_levels,
    spec.memory_tiers, and spec.sensitivity_levels. Runtime readers may keep compatibility
    fallbacks for older derived-project schemas.
  decided_at: '2026-04-29T11:31:38+00:00'
---
