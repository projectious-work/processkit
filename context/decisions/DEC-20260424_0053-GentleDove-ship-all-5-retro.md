---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260424_0053-GentleDove-ship-all-5-retro
  created: '2026-04-24T00:53:16+00:00'
  updated: '2026-04-24T01:01:45+00:00'
spec:
  title: Ship all 5 retro-derived WorkItems as v0.20.0
  state: superseded
  decision: Implement WildLake, ToughAnt, SwiftLynx, SharpBrook, and SnappyBird in
    this session and cut v0.20.0 immediately after.
  context: v0.19.2 retrospective produced 5 action-item WIs all tagged at v0.19.3/v0.20.0
    targets. Owner elected to fold all five into one v0.20.0 release rather than spread
    them across multiple point releases.
  rationale: Four of the five already target v0.20.0, and batching WildLake (originally
    v0.19.3) avoids a trivial point release. Lower release overhead, single drift/provenance
    stamp, one retro log entry. The WIs are largely independent so there is no sequencing
    blocker.
  consequences: v0.20.0 becomes a larger release than v0.19.x baseline; scope must
    stay bounded to these 5 WIs (no scope creep). Session will be long.
  deciders:
  - TEAMMEMBER-cora
  related_workitems:
  - BACK-20260424_0038-WildLake-pk-retro-auto-workitems
  - BACK-20260424_0038-ToughAnt-ephemeral-sub-agent-defaults
  - BACK-20260424_0038-SwiftLynx-compliance-contract-acknowledgement-ttl
  - BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas
  - BACK-20260424_0038-SnappyBird-data-repair-path-for
  decided_at: '2026-04-24T00:53:16+00:00'
  superseded_by: DEC-20260424_0101-SolidBadger-split-v0-20-0
---
