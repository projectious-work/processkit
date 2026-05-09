---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
  created: '2026-05-09T13:18:02+00:00'
  labels:
    github_issue: 20
    area: team-creator
    cluster: team-model-v2
  updated: '2026-05-09T18:30:49+00:00'
spec:
  title: 'team-creator v2: 5 design gaps (catalog/codenames/consultants/clones/budget)
    (gh#20)'
  state: in-progress
  type: epic
  priority: medium
  description: 'Triaged from GH #20. Five surfaced gaps from a real ~3-hour session:\n\nGap
    1: pk-team-create writes 8 new archetype Roles parallel to the rich `context/roles/`
    catalog instead of selecting from it. Fix: consume catalog or add layer-5 archetype→catalog-role
    override.\n\nGap 2: Skill body uses internal codenames (`OpenWeave`, `TeamWeaver
    Phase 3 dogfood`) without inline definition. Fix: rename to self-explanatory phrasing
    in user-facing surfaces.\n\nGap 3: No first-class `consultant` / ephemeral TeamMember
    concept. Fix: add `type=consultant` with `engaged_for` + `engagement_window`;
    resolver picks bindings only within window; pk-team-review flags expired-but-active.\n\nGap
    4: TeamMember is modeled as a person (personality, memory, joined_at) but `clone_cap=5`
    lets it be cloned for parallelism — confused identity model. Pick one: pure person,
    pure role-instance, or hybrid (RoleSlot + TeamMember assignment, recommended).\n\nGap
    5: Resource/budget model is implicit. Fix: add `budget_projection` block to chartering
    DecisionRecord inputs_snapshot; pk-team-review surfaces drift.\n\nUnifying issue:
    pk-team-create was built as a model-tier-allocator, not a team-resource-planner.
    Treat as v2 design epic; consider splitting into 5 sub-WorkItems if scheduled.
    Companion to gh#18, gh#19.'
  started_at: '2026-05-09T18:30:49+00:00'
---

## Transition note (2026-05-09T18:30:49+00:00)

Wave 4 kickoff. Decision: v2 in-place (not fork). Cora dispatching ephemeral ROLE-solutions-architect/senior on Opus 4.7 for cross-gap design synthesis; downstream sub-WorkItems will use the resulting design artifact as their architectural reference.
