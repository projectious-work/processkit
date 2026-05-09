---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1837-LuckyWren-catalog-driven-pk-team-create
  created: '2026-05-09T18:37:05+00:00'
  labels:
    github_issue_parent: 20
    area: team-creator
    cluster: team-model-v2
    epic_sub: SUB-2
    design_artifact_ref: ART-20260509_1836-SmartPanda-team-creator-v2-design
    effort: medium
    model_class: balanced
    owner_role: ROLE-software-engineer/senior
    depends_on: SUB-1
spec:
  title: 'team-creator v2 SUB-2: catalog-driven pk-team-create'
  state: backlog
  type: task
  priority: medium
  description: 'Sub-item of VastVale (gh#20). Delete the 8-archetype Role write step
    from pk-team-create. Ship assets/archetype-catalog-mapping.yaml (kit defaults)
    + project override loader (context/team/archetype-catalog-mapping.yaml). Add archetype_catalog_mapping_file
    audit fields to chartering DecisionRecord inputs_snapshot. Update pk-team-rebalance
    and pk-team-review to resolve archetypes through the mapping. Effort: medium.
    Owner role: ROLE-software-engineer/senior. Model class: balanced. Depends on:
    SUB-1 (writes RoleSlots, not Roles). Architectural reference: ART-20260509_1836-SmartPanda-team-creator-v2-design.
    Open question 6 (assistant archetype catalog target) needs owner answer before
    final mapping.yaml ships.'
  parent: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
---
