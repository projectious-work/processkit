---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_1422-ThriftyAsh-enable-sqlite-vec-as-an-observable
  created: '2026-05-04T14:22:56+00:00'
spec:
  title: Enable sqlite-vec as an observable index capability
  state: accepted
  decision: Make sqlite-vec enablement deterministic and observable by preserving
    vector-capable index state, exposing load diagnostics, checking vector health
    in pk-doctor, and rebuilding vectors after runtime dependency coverage is fixed.
  context: The live processkit semantic index has semantic chunks but reports sqlite_vec_available=false,
    so hybrid search falls back to FTS and the project does not benefit from vector
    KNN retrieval.
  rationale: The current implementation silently disables sqlite-vec and may drop
    the vector table when a non-vector-capable process opens the shared index. Diagnostics
    and health checks are needed before relying on semantic retrieval for routing
    or context search.
  consequences: Index-management and gateway code should expose sqlite-vec load status/failure
    reason, avoid destructive vector-table cleanup except during explicit repair,
    and add release/doctor coverage for semantic vector availability.
  related_workitems:
  - BACK-20260504_1422-SmoothWolf-router-sqlite-vec-capacity-spark-release
  decided_at: '2026-05-04T14:22:56+00:00'
---
