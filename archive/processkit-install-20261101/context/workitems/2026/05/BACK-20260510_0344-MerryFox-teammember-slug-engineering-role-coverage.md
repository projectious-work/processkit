---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260510_0344-MerryFox-teammember-slug-engineering-role-coverage
  created: '2026-05-10T03:44:18+00:00'
  labels:
    github_issue: 17
    cluster: agent-dispatch
    follow-up-of: WildPanda
  updated: '2026-05-10T03:47:03+00:00'
spec:
  title: 'WildPanda P2 follow-up: extend recommended_team_member_slug to engineering-role
    groups'
  state: in-progress
  type: task
  priority: medium
  description: P2 deferral from BACK-WildPanda (gh#17). Currently route_task returns
    recommended_team_member_slug only for 5/14 PM-owned domain groups. Extend coverage
    to engineering-role groups (workitem, decision, scope, binding, etc.) so the field
    is populated for the most common write-side dispatches.
  started_at: '2026-05-10T03:47:03+00:00'
---

## Transition note (2026-05-10T03:47:03+00:00)

Picked up by MerryFox. Reading server.py and team roster. Plan: extend GROUP_PREFERRED_ROLE from 5 PM groups to cover all 14 domain groups with appropriate ROLE-* slugs; finn (ROLE-software-engineer/senior) will cover engineering groups.
