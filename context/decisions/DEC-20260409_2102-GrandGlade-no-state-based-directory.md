---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260409_2102-GrandGlade-no-state-based-directory
  created: '2026-04-09T21:02:07+00:00'
spec:
  title: No state-based directory sharding for entity kinds
  state: accepted
  decision: Entity directories are NOT sharded by state (e.g., active/, archived/).
    All entities of a kind live in the same directory tree regardless of state. Terminal
    states are expressed in the entity's spec.state field; the SQLite index is the
    archiving and query mechanism.
  context: During the date-based sharding implementation (v0.7.0+), the question arose
    whether to also shard by entity state (e.g., context/workitems/active/, context/workitems/done/).
    This was explicitly considered and rejected.
  rationale: State changes frequently; file moves on every transition are expensive,
    error-prone, and break references. The SQLite index handles filtering by state
    cheaply without any file movement. State-based directories would also break the
    flat rglob scan that rebuilds the index. Date-based sharding is the only approved
    sharding axis because dates are immutable after creation.
  alternatives:
  - option: State-based sharding
    rejected_because: State changes break file paths referenced elsewhere; creates
      churn on every transition; no benefit over index query
  consequences: Queries that filter by state must go through the index (query_entities).
    Direct filesystem inspection of a state subset is not supported. Large flat directories
    accumulate over time — mitigated by date-based sharding for high-volume kinds
    like LogEntry.
  decided_at: '2026-04-09T21:02:07+00:00'
---
