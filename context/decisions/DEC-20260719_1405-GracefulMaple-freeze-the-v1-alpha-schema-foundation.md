---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260719_1405-GracefulMaple-freeze-the-v1-alpha-schema-foundation
  created: '2026-07-19T14:05:11+00:00'
  updated: '2026-07-19T14:08:43+00:00'
spec:
  title: Freeze the v1 alpha schema foundation
  state: superseded
  decision: Use repository build inputs under schemas/src, commit generated runtime
    schemas under src/context/schemas/_generated, freeze the first implementation
    slice to WorkItem, DecisionRecord, Binding, and LogEntry, and verify generation
    and fixtures without requiring aibox.
  context: The user approved the recommended v1.0 implementation plan. The v1 branch
    already has architecture and test strategy documents plus native CI, but no deterministic
    schema generator or fixture projects.
  rationale: This isolates human-authored schema composition from shipped runtime
    output, proves the highest-value entity, record, relation, and event semantics
    first, and preserves an aibox-independent correctness path.
  alternatives:
  - option: Generate every alpha kind immediately
    rejected_because: It expands the blast radius before composition and determinism
      are proven.
  - option: Overwrite existing flat runtime schemas now
    rejected_because: It would mix generator validation with a runtime compatibility
      cutover.
  consequences: The existing flat runtime schemas remain the compatibility path during
    the alpha foundation. Generated schemas are introduced alongside them until a
    later cutover gate switches runtime loading.
  decided_at: '2026-07-19T14:05:11+00:00'
  superseded_by: DEC-20260719_1406-AmpleHare-ship-v1-schema-sources-with-generated
---
