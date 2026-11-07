---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260722_1637-ProudHorizon-target-60-70-percent-ontology-coverage
  created: '2026-07-22T16:37:44+00:00'
spec:
  title: Target 60-70 percent ontology coverage for v1 beta
  state: accepted
  decision: Plan the v1.0 beta stream toward implementing approximately 60-70% of
    the settled 89-concept ontology, corresponding to roughly 54-62 concepts. Treat
    this as a directional planning target alongside the capability-based beta acceptance
    gate, not as a substitute for migration, validation, tooling, and documentation
    evidence.
  context: The existing beta gate requires ontology expansion beyond the 14-concept
    alpha subset but does not set a numeric implementation target. The project owner
    wants beta to demonstrate substantially broader ontology coverage.
  rationale: A 60-70% target makes beta representative enough for meaningful migration
    and integration feedback while preserving room to complete and stabilize the remaining
    ontology before release candidate and general availability.
  alternatives:
  - option: Keep beta capability-only
    reason: Rejected because it permits an undersized beta ontology slice.
  - option: Require all 89 concepts by beta
    reason: Rejected because it removes useful staged delivery and validation room
      before release candidate.
  consequences: The beta concept inventory must select roughly 54-62 concepts and
    document exclusions. Beta readiness still requires Phases 1-3 green and Phase
    4 at least 75% complete; hitting the count alone is insufficient. The exact inventory
    can be refined based on dependency and composition evidence.
  decided_at: '2026-07-22T16:37:44+00:00'
---
