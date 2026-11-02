---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260719_1406-AmpleHare-ship-v1-schema-sources-with-generated
  created: '2026-07-19T14:06:35+00:00'
  updated: '2026-07-19T14:08:43+00:00'
spec:
  title: Ship v1 schema sources with generated schemas
  state: accepted
  decision: Place schema composition inputs under src/context/schemas/src and committed
    outputs under src/context/schemas/_generated. Retain existing flat schemas as
    the compatibility fallback during alpha.
  context: Release tarballs copy only src. Root-level schemas/src inputs would not
    reach derived projects, preventing the planned processkit-native regeneration
    surface from working after installation.
  rationale: Co-locating shipped inputs and outputs keeps regeneration a package capability,
    preserves the literal consumer-tree invariant, and permits a generated-first,
    flat-second runtime cutover without duplicating canonical source files.
  alternatives:
  - option: Keep root schemas/src and copy it during release
    rejected_because: It creates two source trees and makes ordinary staged-package
      tests depend on a release-only copy step.
  - option: Ship generated schemas only
    rejected_because: Derived projects could not use regenerate_schemas without fetching
      repository-only inputs.
  consequences: The earlier root-level source-layout decision is superseded. Planning
    documentation and tests must use the shipped path.
  decided_at: '2026-07-19T14:06:35+00:00'
  supersedes: DEC-20260719_1405-GracefulMaple-freeze-the-v1-alpha-schema-foundation
---
