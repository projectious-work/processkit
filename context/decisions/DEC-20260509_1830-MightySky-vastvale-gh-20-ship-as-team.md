---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260509_1830-MightySky-vastvale-gh-20-ship-as-team
  created: '2026-05-09T18:30:47+00:00'
spec:
  title: 'VastVale (gh#20): ship as team-creator v2 in-place; dispatch Opus architect
    for design synthesis'
  state: accepted
  decision: Ship the team-creator v2 redesign IN-PLACE inside the existing team-creator
    skill (do NOT fork as a new team-planner skill). The 5 gaps land as breaking changes
    accompanied by a v1→v2 Migration. Dispatch a ROLE-solutions-architect/senior ephemeral
    consultant on Opus 4.7 NOW to produce the cross-gap design synthesis (per-gap
    shape, dependency graph, suggested sequencing, breaking-change analysis); downstream
    Sonnet implementation agents will work from that artifact.
  context: 'Plan ART-20260509_1323-DeepSpruce flagged this question for Wave-4 kickoff.
    Five gaps: (1) catalog integration, (2) codename rename, (3) consultant/ephemeral
    TeamMember type, (4) identity model RoleSlot+TeamMember-assignment vs person-with-clones,
    (5) explicit budget_projection in chartering DecisionRecord.'
  rationale: 'Owner judgment: one skill, one mental model is cleaner long-term than
    maintaining team-creator + team-planner side-by-side. Migration churn is a one-time
    cost; coexisting skills is permanent install-base drag. Architect dispatch now
    (rather than splitting first then synthesizing later) means downstream sub-WorkItems
    get a coherent design baseline rather than each impl agent re-deriving the architecture
    independently.'
  consequences: VastVale enters in-progress. Cora dispatches Opus architect (~50-80k
    token bounded burst). Architect output → captured as a design Artifact via Cora's
    MCP write. Then Cora splits into ≤5 sub-WorkItems with the design as their architectural
    reference. Sonnet impl agents pick up gap-by-gap from there.
  deciders:
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
  decided_at: '2026-05-09T18:30:47+00:00'
---
