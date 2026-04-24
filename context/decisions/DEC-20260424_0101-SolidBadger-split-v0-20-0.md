---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260424_0101-SolidBadger-split-v0-20-0
  created: '2026-04-24T01:01:09+00:00'
  updated: '2026-04-24T01:01:45+00:00'
spec:
  title: 'Split v0.20.0: ship WildLake + ToughAnt + SwiftLynx; defer SharpBrook +
    SnappyBird to v0.21.0 after design discussion'
  state: accepted
  decision: v0.20.0 ships only the three small retro WIs (WildLake — already in review;
    ToughAnt; SwiftLynx). SharpBrook and SnappyBird are deferred to v0.21.0 pending
    dedicated design discussions, because both alter cross-cutting invariants (schema-reload
    semantics and the append-only log invariant) where a rushed MVP has outsized downside
    risk.
  context: Supersedes DEC-20260424_0053-GentleDove-ship-all-5-retro, which had committed
    all five retro WIs to v0.20.0 in a single session. After sizing each WI honestly
    (6–8h total), SharpBrook (new MCP reload_schemas tool) and SnappyBird (data-repair
    path for append-only LogEntries) were identified as medium-sized stories that
    each alter an architectural invariant. Owner agreed to split.
  rationale: Cost of a botched MVP on SharpBrook (reload-schemas race with in-flight
    requests) or SnappyBird (accidental append-only breakage) is much higher than
    the benefit of a slightly bigger single release. Splitting keeps v0.20.0 tight
    and buys design space for the two riskier WIs.
  consequences: 'v0.20.0 becomes a smaller, safer release. SharpBrook and SnappyBird
    move back to backlog pending discussion outcomes (DISC-* entities to be opened
    in same turn). v0.21.0 target date: after both discussions resolve.'
  deciders:
  - TEAMMEMBER-cora
  related_workitems:
  - BACK-20260424_0038-WildLake-pk-retro-auto-workitems
  - BACK-20260424_0038-ToughAnt-ephemeral-sub-agent-defaults
  - BACK-20260424_0038-SwiftLynx-compliance-contract-acknowledgement-ttl
  - BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas
  - BACK-20260424_0038-SnappyBird-data-repair-path-for
  decided_at: '2026-04-24T01:01:09+00:00'
  supersedes: DEC-20260424_0053-GentleDove-ship-all-5-retro
---
