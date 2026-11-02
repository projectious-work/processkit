---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_1416-SnowyDew-adopt-stronger-router-signals-and-fallback
  created: '2026-05-04T14:16:46+00:00'
spec:
  title: Adopt stronger router signals and fallback routing
  state: accepted
  decision: Implement router improvements that add first-class routing candidates
    for skills and pk-* commands, explicit high-signal phrases in routing metadata,
    lower-confidence fallback to skill-finder, multi-route output for compound requests,
    and optional caller-provided intent signals as additive hints.
  context: Release-oriented requests have repeatedly produced low-confidence or misleading
    route_task results even when a directly relevant processkit skill such as pk-release-audit
    exists. The user accepted the recommended router improvements on 2026-05-04.
  rationale: The router currently overweights weak domain keyword matches and can
    skip skill-finder fallback once a weak group clears the group threshold. Explicit
    command/skill signals and fallback on low final confidence should make intent
    routing deterministic for high-signal processkit workflows without relying on
    vector search.
  alternatives:
  - option: Only add caller-provided keywords
    reason_rejected: Useful as an additive hint, but it keeps correctness dependent
      on each calling agent guessing the right phrases.
  - option: Rely on sqlite-vec semantic routing
    reason_rejected: Vector search may help recall, but routing needs deterministic
      command and skill metadata for high-value workflows such as releases.
  consequences: Future implementation should update task-router scoring, route_task
    output shape, tests, and command/skill metadata. Caller intent signals may improve
    routing, but must remain optional and should not override stronger canonical metadata.
  decided_at: '2026-05-04T14:16:46+00:00'
---
