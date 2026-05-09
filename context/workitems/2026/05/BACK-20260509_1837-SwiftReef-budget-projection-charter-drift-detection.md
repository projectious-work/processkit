---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1837-SwiftReef-budget-projection-charter-drift-detection
  created: '2026-05-09T18:37:17+00:00'
  labels:
    github_issue_parent: 20
    area: team-creator
    cluster: team-model-v2
    epic_sub: SUB-4
    design_artifact_ref: ART-20260509_1836-SmartPanda-team-creator-v2-design
    effort: medium
    model_class: balanced
    owner_role: ROLE-software-engineer/senior
    depends_on: SUB-1,SUB-2
spec:
  title: 'team-creator v2 SUB-4: budget projection + drift detection'
  state: backlog
  type: task
  priority: medium
  description: 'Sub-item of VastVale (gh#20). Extend inputs_snapshot schema with budget_projection
    block: currency, window, projected_total, projection_method, slot_projections[]
    (per RoleSlot: role, seniority, model_profile, expected_invocations_per_week,
    avg_tokens_per_invocation, unit_cost_usd, projected_total_usd), drift_threshold_pct
    (default 20), notes. Add charter-time projection step to pk-team-create that calls
    model-recommender.get_pricing per slot. Add pk-team-review drift computation:
    query event-log for invocations bound to chartering Scope''s RoleSlots, sum actual
    cost, emit team.budget.drift finding when |drift_pct| exceeds threshold. Add --budget-drift-threshold
    CLI flag. Effort: medium. Owner role: ROLE-software-engineer/senior. Model class:
    balanced. Depends on: SUB-1 (slots), SUB-2 (catalog mapping informs which roles
    get projected). Open question 5 (live get_pricing vs frozen pricing snapshot)
    needs owner answer before charter step ships.'
  parent: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
---
