---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1317-WildPanda-force-teammember-based-sub-agent-dispatch
  created: '2026-05-09T13:17:35+00:00'
  labels:
    github_issue: 17
    area: compliance
    cluster: agent-dispatch
  updated: '2026-05-10T03:46:05+00:00'
spec:
  title: Force TeamMember-based sub-agent dispatch (gh#17)
  state: done
  type: task
  priority: high
  description: 'Triaged from GH #17. Bare `Agent()` / `Task()` dispatch bypasses route_task
    → TeamMember → resolved model, so sub-agents inherit parent model regardless of
    task class. Five proposals:\n- P1: Add a sub-agent-dispatch clause to `skill-gate/assets/compliance-contract.md`
    (highest leverage)\n- P2: Add `recommended_team_member_slug` + `recommended_model_class`
    to `route_task` response\n- P3: New pk-doctor check `team_member_exports` (warn
    when TeamMembers exist but `.claude/agents/` empty/stale)\n- P4: aibox-side PreToolUse
    hook to block bare Agent() (separate aibox issue, deferred)\n- P5: AGENTS.md template
    "Before sub-agent dispatch" section\n\nOwners: P1/P2/P3/P5 = processkit, P4 =
    aibox. Related to gh#18 (contract sentiment) and gh#19 (Claude Code knobs). Discovered
    in DISC-20260507_0610-MerryCedar.'
  started_at: '2026-05-09T14:04:10+00:00'
  completed_at: '2026-05-10T03:46:05+00:00'
---

## Transition note (2026-05-09T14:04:10+00:00)

Wave 3b dispatch — TEAMMEMBER-finn on Sonnet 4.5. Scope: P1 (sub-agent-dispatch clause at WildPanda placeholder line 12 of compliance-contract.md), P2 (route_task response gets recommended_team_member_slug + recommended_model_class), P3 (new pk-doctor check team_member_exports), P5 (AGENTS.md template "Before sub-agent dispatch" section). P4 deferred to aibox repo per WorkItem.


## Transition note (2026-05-09T14:12:03+00:00)

All 4 proposals shipped (P1/P2/P3/P5). P1: sub-agent-dispatch clause in compliance-contract.md (+10 lines, replaced TODO marker). P2: route_task response now includes recommended_team_member_slug + recommended_model_class; coverage 5/14 domain groups (PM-owned only — Cora). Engineering groups deferred (would need ROLE-software-engineer mapping; flagged for follow-up). P3: new team_member_exports pk-doctor check, 3 WARNs against current repo (cora, finn, thrifty-otter all missing .claude/agents exports). P5: AGENTS.md "Before sub-agent dispatch" section (22 lines vs 15 soft budget — Cora to confirm or trim). 2 new tests, all 9 task-router tests pass. Trees in sync. Open: src/AGENTS.md mirror left alone (pre-existing divergence). P4 deferred to aibox repo per WorkItem.


## Transition note (2026-05-10T03:46:05+00:00)

Shipped to main on 2026-05-09 via PR #24; closing per v0.26.0 release prep.
