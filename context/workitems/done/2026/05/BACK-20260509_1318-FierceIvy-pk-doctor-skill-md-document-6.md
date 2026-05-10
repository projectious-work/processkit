---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1318-FierceIvy-pk-doctor-skill-md-document-6
  created: '2026-05-09T13:18:28+00:00'
  labels:
    github_issue: 23
    area: pk-doctor
    cluster: v1-drift
  updated: '2026-05-10T03:46:02+00:00'
spec:
  title: 'pk-doctor SKILL.md: document 6 missing check modules (gh#23)'
  state: done
  type: task
  priority: medium
  description: 'Triaged from GH #23. SKILL.md documents Phase 1 (4) + post-Phase 1
    (6) checks but `scripts/checks/` actually contains 6 undocumented modules: `v2_contracts.py`,
    `context_hygiene.py`, `schema_vocabulary.py`, `migration_integrity.py`, `mcp_gateway.py`,
    `skill_dag.py`. Agent reading SKILL.md cannot lean on undocumented checks; in
    aibox v0.25.6 release re-plan an agent answered "no, pk-doctor would not catch
    v1-stale state" when partial coverage may exist.\n\nFix options:\n- (a) Document
    each module in SKILL.md: one paragraph each — what it catches, severity, --fix
    path. Mirror existing format.\n- (b) Mark unfinished/unwired modules as such or
    remove them.\n\nBonus: pk-release-audit enforces every checks/ module is registered+documented
    OR has `_unregistered.py` suffix.\n\nUnblocks gh#22 (need to know what existing
    checks already cover before adding `v1_entity_drift`).'
  started_at: '2026-05-09T13:46:35+00:00'
  completed_at: '2026-05-10T03:46:02+00:00'
---

## Transition note (2026-05-09T13:46:35+00:00)

Wave 1 dispatch approved by owner; ephemeral ROLE-technical-writer/specialist on Haiku 4.5 picking it up.


## Transition note (2026-05-09T13:49:38+00:00)

Docs landed in context/ and src/context/ mirror. Cora reviewed the diff and confirmed all 6 entries match the existing format and reference only IDs found in module docstrings. Holding in review for owner sign-off if desired.


## Transition note (2026-05-10T03:46:02+00:00)

Shipped to main on 2026-05-09 via PR #24; closing per v0.26.0 release prep.
