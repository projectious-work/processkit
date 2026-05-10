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
  updated: '2026-05-10T03:46:08+00:00'
spec:
  title: 'team-creator v2 SUB-2: catalog-driven pk-team-create'
  state: done
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
  started_at: '2026-05-09T21:46:11+00:00'
  completed_at: '2026-05-10T03:46:08+00:00'
---

## Transition note (2026-05-09T21:46:11+00:00)

Wave 4 SUB-2 dispatch — TEAMMEMBER-finn (ROLE-software-engineer/senior) on Sonnet 4.5. Branch: feat/sub-2-catalog-driven (off feat/sub-1-roleslot-primitive / PR #25). Brief includes SUB-1's findings: (1) v0.16.0 capacity-field doc scrub in team-creator/ skill body+commands+references (the schemas don't have these fields anymore); (2) Phase A backfill apply script (SUB-1 deferred); (3) gateway tool-catalog regeneration for SUB-1's 5 new RoleSlot tools.


## Transition note (2026-05-09T22:04:55+00:00)

SUB-2 shipped on Sonnet (likely Opus inheritance, see prior billing finding). pk-team-create cuts over to RoleSlots via SUB-1's create_role_slot/fill_role_slot MCP tools — no more archetype Roles. New archetype-catalog-mapping.yaml + team_creator_lib helper. 3 commands updated (pk-team-create, pk-team-rebalance, pk-team-review) + 2 references (role-archetypes, role-archetypes-override). v0.16.0 doc scrub clean (14 remaining hits are deliberate v1-history annotations). apply_migration_2139.py shipped (idempotent backfill; v2-native no-op verified). Gateway tool-catalog regenerated via the regen script: now 152 tools (+339/-5 from SUB-1's 5 new tools). 13 new tests, all 77 in test file pass. Trees mirrored clean. Open follow-ups: a doctor check could flag archetype Roles as superseded after full cutover; apply_migration_2139.py needs chartering_scope on CLI (deferrable to SUB-3/4 if migration entity gains that field).


## Transition note (2026-05-10T03:46:08+00:00)

Shipped to main on 2026-05-09 via PR #28; closing per v0.26.0 release prep.
