---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1837-RapidLily-consultant-type-engagement-window-resolver
  created: '2026-05-09T18:37:13+00:00'
  labels:
    github_issue_parent: 20
    area: team-creator
    cluster: team-model-v2
    epic_sub: SUB-3
    design_artifact_ref: ART-20260509_1836-SmartPanda-team-creator-v2-design
    effort: medium
    model_class: balanced
    owner_role: ROLE-software-engineer/senior
    depends_on: SUB-1
  updated: '2026-05-10T03:46:09+00:00'
spec:
  title: 'team-creator v2 SUB-3: consultant type + engagement window'
  state: done
  type: task
  priority: medium
  description: 'Sub-item of VastVale (gh#20). Bump SCHEMA-team-member to v1.2.0; add
    consultant enum value, engaged_for (SCOPE-id), engagement_window ({starts_at,
    ends_at}). Update team-manager resolver to filter consultants by window in get_interlocutor_runtime_binding
    and list_team_members(active=true). Add pk-team-review finding code team.consultant.expired_but_active
    (severity: warning). Add Scope-close hook → consultant auto-deactivate (emit team_member.auto_deactivated
    event; respect auto_deactivate_on_scope_close=false override). Effort: medium.
    Owner role: ROLE-software-engineer/senior. Model class: balanced. Depends on:
    SUB-1 (resolver path is shared). Architectural reference: ART-20260509_1836-SmartPanda-team-creator-v2-design.
    Open question 4 (auto-deactivate on Scope close) needs owner confirmation.'
  parent: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
  started_at: '2026-05-09T22:11:48+00:00'
  completed_at: '2026-05-10T03:46:09+00:00'
---

## Transition note (2026-05-09T22:11:48+00:00)

Wave 4 SUB-3 dispatch — TEAMMEMBER-finn (ROLE-software-engineer/senior) on Sonnet 4.6 (explicit model param this time per the billing finding). Branch: feat/sub-3-consultant (off main; SUB-1 + SUB-2 already merged via PR #27 + #28).


## Transition note (2026-05-09T22:21:15+00:00)

SUB-3 shipped on Sonnet 4.6 (explicit model param). team-member schema bump v1.1.0->v1.2.0 with consultant type + engaged_for + engagement_window + auto_deactivate_on_scope_close. Conditional validation in server layer (_validate_consultant_fields) since JSON Schema if/then isn't supported by validate_spec engine. team-manager resolver filters consultants by window; out-of-window consultants are skipped (not deactivated). scope-management transition_scope hook auto-deactivates consultants engaged_for the closing Scope when auto_deactivate_on_scope_close=true; emits team_member.auto_deactivated event (added to known_event_types). pk-team-review gets new query_consultant_findings MCP tool + Step 5b + CONSULTANT WARNINGS output section. 11 new tests, 88 total all passing on both trees. Trees sync clean. SUB-4 hooks: engagement_window provides natural per-slot cost windows; team_member.auto_deactivated events can bound budget actuals.


## Transition note (2026-05-10T03:46:09+00:00)

Shipped to main on 2026-05-09 via PR #29; closing per v0.26.0 release prep.
