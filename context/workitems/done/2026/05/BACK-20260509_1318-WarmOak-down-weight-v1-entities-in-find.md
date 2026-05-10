---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1318-WarmOak-down-weight-v1-entities-in-find
  created: '2026-05-09T13:18:10+00:00'
  labels:
    github_issue: 21
    area: task-router
    cluster: v1-drift
  updated: '2026-05-10T03:46:04+00:00'
spec:
  title: Down-weight v1 entities in find_skill / task-router (gh#21)
  state: done
  type: task
  priority: high
  description: 'Triaged from GH #21. find_skill/task-router returns v1 `PROC-release`
    (etc.) as authoritative even when v2 successor primitives exist (Process→Scope+Gate,
    Actor→TeamMember, StateMachine→lifecycle metadata). Caused real harm in aibox
    v0.25.6 release re-planning (cost ~2 re-plan loops).\n\nFix:\n- When candidate
    carries `apiVersion: ...v1` AND v2 successor primitive exists for that kind, multiply
    score by configurable penalty (start 0.3)\n- Surface penalty in routing trace
    ("matched X; v1-entity penalty applied; consider v2 successors: ...")\n- Make
    penalty configurable per-project (some projects intentionally on v1)\n\nLocalized
    change in router scoring. Pairs with gh#22 (pk-doctor v1_entity_drift).'
  started_at: '2026-05-09T13:48:38+00:00'
  completed_at: '2026-05-10T03:46:04+00:00'
---

## Transition note (2026-05-09T13:48:38+00:00)

Wave 2 dispatch — TEAMMEMBER-finn (SE/senior) on Sonnet 4.5.


## Transition note (2026-05-09T13:55:21+00:00)

Router penalty (default 0.3) + configurable knob (`v1_entity_penalty` in task-router/mcp/user_config.json) shipped to both task-router and skill-finder MCP servers; trace surfacing implemented; v1 actor DOMAIN_GROUP and v1 SKILL.md-level apiVersion both covered. Two new tests (test_phase1_groups_applies_v1_penalty_to_actor_group, test_skill_finder_fallback_applies_v1_penalty_for_v1_skill) — all 7 tests pass. Trees mirrored. CAVEAT for Cora's review: implementation penalizes at the skill/group level only; if the v0.25.6 harm case was about index-returned entities (PROC-release ID lookup via query_entities/get_entity), that path is NOT covered. May warrant a follow-up WorkItem under index-management. Also: model DOMAIN_GROUP intentionally excluded (it points at v2 model-recommender, not v1 Model entity).


## Transition note (2026-05-09T14:04:07+00:00)

Re-opened per owner decision (DEC: WarmOak entity-level extension). TEAMMEMBER-finn on Sonnet 4.5 dispatched to extend penalty into index-management entity-level read paths (query_entities, get_entity, search_entities).


## Transition note (2026-05-09T14:09:28+00:00)

Extension landed. index-management/mcp/server.py: query_entities + get_entity annotation-only (no native score in those surfaces); search_entities gets multiplicative penalty + re-rank via synthesized base_score=1/(1+rank_index). Same `v1_entity_penalty` knob in task-router/mcp/user_config.json (no second config primitive). Both trees byte-identical. No tests (no test pattern exists in index-management). Open follow-up question: semantic_search_entities and hybrid_search_entities follow the same ranked-result shape and would benefit from the same penalty — flag for a separate WorkItem rather than scope-creep here. Now Wave 2 closes.


## Transition note (2026-05-10T03:46:04+00:00)

Shipped to main on 2026-05-09 via PR #24; closing per v0.26.0 release prep.
