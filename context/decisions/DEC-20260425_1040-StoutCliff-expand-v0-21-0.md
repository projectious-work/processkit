---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260425_1040-StoutCliff-expand-v0-21-0
  created: '2026-04-25T10:40:50+00:00'
spec:
  title: 'Expand v0.21.0 scope: add two pk-doctor portability fixes for derived projects
    (silent-zero schema_filename + migrations layout fallback)'
  state: accepted
  decision: 'Add two new fixes to the v0.21.0 release before cutting: (1) `pk-doctor
    schema_filename` resolves the schemas dir with a fallback chain (`src/context/schemas/`
    → `context/schemas/`) so it actually validates entities in derived projects instead
    of silently walking 0 files; (2) `pk-doctor migrations` accepts both layouts (processkit
    `context/migrations/pending/` AND top-level + `applied/`) so it actually counts
    pending migrations in derived projects. File two WIs against v0.21.0 to track
    each.'
  context: 'Owner ran `/pk-doctor` inside the aibox derived-project container and
    got 0 ERROR / 0 WARN despite obvious schema and migration issues. Investigation
    revealed both checks silently no-op on derived projects: schema_filename hard-codes
    `src/context/schemas/` (which only exists in the processkit dogfood repo), and
    migrations hard-codes `context/migrations/pending/` (which does not match aibox''s
    top-level + `applied/` convention). Together these two bugs make pk-doctor falsely
    reassuring on every derived install — the exact failure mode the user just hit.'
  rationale: These are silent-correctness bugs, not feature gaps. Shipping v0.21.0
    without them means every derived-project pk-doctor run is misleading. The fixes
    are small (path fallback chains in two places) and self-contained, so adding them
    to the release in flight is a much better trade than waiting for v0.21.1.
  consequences: v0.21.0 scope grows by two small tasks. Cut is delayed by maybe an
    hour. After release, derived projects on processkit ≥ v0.21.0 will get faithful
    pk-doctor results out of the box. Existing derived projects on v0.18.1–v0.20.0
    keep getting silent zeros until they bump.
  deciders:
  - TEAMMEMBER-thrifty-otter
  - TEAMMEMBER-cora
  decided_at: '2026-04-25T10:40:50+00:00'
---
