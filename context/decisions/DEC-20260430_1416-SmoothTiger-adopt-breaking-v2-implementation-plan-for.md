---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for
  created: '2026-04-30T14:16:14+00:00'
spec:
  title: Adopt breaking v2 implementation plan for SteadyTiger v0.3 processkit support
  state: accepted
  decision: Implement the SmoothRiver/SteadyTiger v0.3 processkit work as a breaking
    v2 program, with no backward-compatibility shims. The v2 schema and index contracts
    become authoritative; v1 contexts are handled only through an explicit migration
    path.
  context: 'The approved implementation plan covers large processkit changes: closed
    schema vocabulary, new artifact kinds and binding types, index-managed sharding/archive
    paths, migration source-version semantics, Hook inbox, AgentCard projection, process/schedule
    demotions, eval gates, cost enforcement, and security projections.'
  rationale: Several action items are API-breaking. Treating them as a v2 foundation
    avoids hidden compatibility layers and lets schemas, MCP APIs, doctor checks,
    and derived-project migration behavior converge on one contract.
  alternatives:
  - option: Keep changes backward compatible in the v0.x line
    reason_rejected: Would require dual-read and permissive validation paths that
      obscure the new schema/index contract.
  - option: Implement projections first
    reason_rejected: AgentCard, Hook inbox, eval, and cost features depend on stable
      v2 schema and path authority.
  consequences: Downstream consumers must migrate deliberately. Unknown kinds/types
    and ad hoc event types should fail once v2 validation is active. Implementation
    should start with schema/index/migration/diagnostic foundations before projections
    or workflow surfaces.
  deciders:
  - TEAMMEMBER-thrifty-otter
  - TEAMMEMBER-cora
  decided_at: '2026-04-30T14:16:14+00:00'
---
