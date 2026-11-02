---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260411_0559-RapidFjord-three-tier-hot-warm
  created: '2026-04-11T05:59:28+00:00'
spec:
  title: Three-tier hot/warm/cold storage architecture for entity scaling
  state: accepted
  decision: 'Entity storage uses a three-tier architecture: Hot (individual .md files,
    git-tracked, filesystem-resident) for active items; Warm (SQLite index, gitignored)
    as the derived query layer, always current; Cold (tar.gz archives, git-LFS) for
    completed items older than a configurable threshold. The index retains entity
    and event metadata permanently regardless of tier; full content of cold items
    requires archive extraction.'
  context: 'MightyDaisy discussion (DISC-20260410_1038) identified that file-per-entity
    storage becomes shaky at 50K+ files and breaks beyond that. kaits (a consumer
    of processkit/aibox) can plausibly generate 50K+ artifacts for a single simulated
    company. Three mitigations were researched: directory sharding (year/month subdirs),
    git fsmonitor + feature.manyFiles, and sparse checkout. These push the comfortable
    limit to ~100K active files. Beyond that, hot/cold archiving is required. The
    decision was reached tentatively in MightyDaisy and never formalized.'
  rationale: 'Directory sharding alone is insufficient for very large projects. Hot/cold
    archiving reduces active file count without losing queryability: the SQLite index
    retains metadata for cold items, and full payloads are retrievable via archive
    extraction (slow, acceptable for historical queries). git-LFS is accepted for
    cold archives because very old items rarely change, making binary storage overhead
    acceptable. This scales to 100K+ items per project; kaits scales further via repo-per-project.'
  alternatives:
  - option: All-hot file-per-entity (no cold tier)
    rejected_because: Breaks at 50K+ files; unacceptable for kaits-scale projects.
  - option: Full database (SQLite or Postgres)
    rejected_because: Loses git-native collaboration, human-readable files, and the
      markdown-as-interchange-format property.
  - option: State-based directory sharding as proxy for hot/cold
    rejected_because: Rejected separately in DEC-20260409_2102-GrandGlade. State changes
      are too frequent; file moves create churn and break references.
  consequences: 'A context-archiving skill and MCP server are needed to implement
    the cold tier: detecting items past the age threshold, packaging them into tar.gz,
    updating the index storage_location, and optionally pushing to git-LFS. Until
    that skill exists, only the hot and warm tiers are operational. Projects that
    do not hit scale limits are unaffected.'
  deciders:
  - ACTOR-owner
  decided_at: '2026-04-11T05:59:28+00:00'
---
