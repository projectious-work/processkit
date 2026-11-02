---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260722_1753-GentleValley-separate-v1-product-entity-api-and
  created: '2026-07-22T17:53:13+00:00'
spec:
  title: Separate v1 product, entity API, and schema versions
  state: accepted
  decision: For the v1.x product line, report the processkit product and internal
    library release as 1.x (beginning with 1.0.0-alpha.1), retain processkit.projectious.work/v2
    as the entity API throughout v1.x, retain schema source format version 1, and
    version each generated entity schema independently. Migrated breaking schemas
    may retain 2.x lineage; newly introduced v1 ontology schemas begin at 1.0.0-alpha.1.
  context: The v1 architecture already declares product and entity API versions independent,
    but the shared library reports 2.0.0-alpha.1 as PK_VERSION. Migration management
    persists that value as target_processkit_version, causing v1 prereleases to identify
    themselves as processkit 2.0. Schema metadata is already intentionally mixed by
    kind.
  rationale: Separating the version axes preserves the deliberate breaking entity
    API v2 migration while keeping product release tags and migration provenance truthful.
    Independent per-kind schema semver avoids unnecessary synchronized schema bumps.
  alternatives:
  - option: Treat processkit v1 as product 2.0
    reason: Rejected because the accepted branch and release stream is v1.0.0-alpha/beta/rc.
  - option: Change entity API back to v1
    reason: Rejected because accepted v2 schema/index contracts require explicit migration
      and are already the v1 rebuild foundation.
  - option: Force every schema to product version 1.x
    reason: Rejected because schema contracts have independent compatibility histories.
  consequences: Migration tools must report product 1.x while producing entity API
    v2. Tests and documentation must assert the axes separately. Product releases
    must update one authoritative product-version source. Per-kind schema versions
    change only for their own compatibility changes.
  deciders:
  - TEAMMEMBER-cora
  decided_at: '2026-07-22T17:53:13+00:00'
---
