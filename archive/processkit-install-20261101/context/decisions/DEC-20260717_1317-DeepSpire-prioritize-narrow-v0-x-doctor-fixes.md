---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260717_1317-DeepSpire-prioritize-narrow-v0-x-doctor-fixes
  created: '2026-07-17T13:17:52+00:00'
spec:
  title: Prioritize narrow v0.x doctor fixes before resuming v1.0
  state: accepted
  decision: Ship a v0.x patch release containing narrow pk-doctor remediation, archive-routing,
    Binding filename-policy, and project-local pk-commands fixes, then return development
    focus to the v1.0 branch.
  context: A derived project on processkit v0.27.1 reported actionable doctor findings
    that could not be completed through the advertised surface.
  rationale: Correct false positives and close small remediation-surface gaps for
    current adopters without building a broad v0 history-rewrite engine; carry the
    stronger remediation contract into v1 planning.
  consequences: The maintenance patch remains narrowly scoped. Declarative data-fix
    execution, ID aliasing, and comprehensive remediation contracts remain v1.0 work.
  decided_at: '2026-07-17T13:17:52+00:00'
---
