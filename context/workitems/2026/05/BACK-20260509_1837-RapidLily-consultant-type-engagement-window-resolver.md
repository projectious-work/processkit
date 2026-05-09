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
spec:
  title: 'team-creator v2 SUB-3: consultant type + engagement window'
  state: backlog
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
---
