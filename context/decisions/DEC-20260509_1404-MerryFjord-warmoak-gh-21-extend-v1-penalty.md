---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260509_1404-MerryFjord-warmoak-gh-21-extend-v1-penalty
  created: '2026-05-09T14:04:00+00:00'
spec:
  title: 'WarmOak (gh#21): extend v1 penalty into index-management entity-level paths'
  state: accepted
  decision: Re-open BACK-WarmOak from review and extend the v1-entity penalty mechanism
    into index-management's entity-level read paths (`query_entities`, `get_entity`,
    `search_entities`). The current implementation covers skill-level routing only
    (find_skill / route_task SKILL.md apiVersion + the v1 `actor` DOMAIN_GROUP); the
    original aibox v0.25.6 harm case may have also involved index-returned entities
    by ID (e.g. `PROC-release` from a query/get hit), which is a separate code path.
  context: 'WarmOak''s first dispatch (TEAMMEMBER-finn on Sonnet 4.5) flagged this
    gap in its review note: "If the harm-case in aibox v0.25.6 was about the index
    returning v1 entities by ID, this PR does not cover that — flag back to me to
    extend." Owner answered "extend now."'
  rationale: 'Owner judgment at Wave 2 review: ship one coherent v1-drift fix rather
    than fragment across multiple WorkItems. Penalty knob (`v1_entity_penalty` in
    task-router/mcp/user_config.json) already exists from the first WarmOak pass;
    extension is an addition to index-management''s scoring/sort path, not a redesign.'
  consequences: WarmOak transitions review → in-progress. Wave 2 doesn't fully close
    until the extension lands. Wave 3b (WildPanda) can still proceed in parallel since
    it touches compliance-contract / pk-doctor / AGENTS.md / task-router response
    shape — no overlap with index-management.
  deciders:
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260509_1318-WarmOak-down-weight-v1-entities-in-find
  decided_at: '2026-05-09T14:04:00+00:00'
---
