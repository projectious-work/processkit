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
  updated: '2026-05-10T03:46:09+00:00'
spec:
  title: 'team-creator v2 SUB-4: budget projection + drift detection'
  state: done
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
  started_at: '2026-05-10T02:25:39+00:00'
  completed_at: '2026-05-10T03:46:09+00:00'
---

## Transition note (2026-05-10T02:25:39+00:00)

Wave 4 SUB-4 dispatch — TEAMMEMBER-finn (ROLE-software-engineer/senior) on Sonnet 4.6 (explicit model param). Branch: feat/sub-4-budget (off main with SUB-1+SUB-2+SUB-3 already merged via PR #24/27/28/29). Final sub-WorkItem of VastVale.


## Transition note (2026-05-10T02:34:37+00:00)

SUB-4 shipped on Sonnet 4.6 (explicit model). Final VastVale sub-WorkItem complete. inputs_snapshot.budget_projection block per design (+ effective_window per slot for consultant traceability, only deviation). pk-team-create gains Step 7.5 projection compute + --budget-drift-threshold/--projection-method flags. team_creator_lib helpers: intersect_windows, compute_slot_projection, build_budget_projection, compute_budget_drift. team-manager gets query_budget_drift MCP tool + event-log scan helpers. pk-team-review Step 5c + BUDGET DRIFT report section (warning on over-spend, info on under-spend, skip when no projection). Consultant slots use engagement_window ∩ Scope window for per-slot cost windows. 9 new tests; 97/97 team-manager tests pass on both trees. Open: actual cost recompute uses snapshotted unit_cost_usd (volume drift only) — live get_pricing is achievable via the actual_slot_costs injection parameter when the calling workflow pre-computes; cross-server team-manager->model-recommender call avoided as scope discipline.


## Transition note (2026-05-10T03:46:09+00:00)

Shipped to main on 2026-05-09 via PR #30; closing per v0.26.0 release prep.
