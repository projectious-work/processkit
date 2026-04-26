---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1738-NobleBrook-skill-dag-validator-cycle
  created: '2026-04-09T17:38:28+00:00'
  updated: '2026-04-26T15:44:54+00:00'
spec:
  title: Skill DAG validator — cycle detection and layer constraint checks
  state: done
  type: task
  priority: medium
  description: 'Add scripts/validate-skill-dag.py: walks src/skills/*/SKILL.md, builds
    the uses: dependency graph, and checks:

    - No missing references (every uses: entry names an existing skill)

    - No cycles in the DAG

    - Process-primitive skills (layer 0-4) only reference skills at equal or lower
    layer numbers

    Output mirrors smoke-test-servers.py style. Add to the release checklist in AGENTS.md
    and CONTRIBUTING.md.'
  started_at: '2026-04-26T15:29:34+00:00'
  completed_at: '2026-04-26T15:44:54+00:00'
---

## Transition note (2026-04-26T15:29:34+00:00)

v0.23.0-bound (DEC-20260426_1529-TidyLynx). Implementation delegated to a sonnet-tier subagent.


## Transition note (2026-04-26T15:44:50+00:00)

skill_dag check landed at context/skills/processkit/pk-doctor/scripts/checks/skill_dag.py (mirrored). Walks every SKILL.md, builds the uses[] dependency graph, validates: no missing refs, no cycles (iterative DFS with 3-colour marking), and layer constraints (skill at layer N only references skills at layer ≤ N). Registered in checks/__init__.py. 14/14 tests pass in test_doctor.py (5 new tests cover: clean roster, missing-ref, 3-node cycle, layer violation, --category=skill_dag integration). Surfaces 5 pre-existing layer violations in the live tree on first run; those have been resolved as part of the v0.23.0 prep by promoting the affected SKILL.md layer values (changelog 2→3, status-briefing/status-update-writer/onboarding-guide 2→4).


## Transition note (2026-04-26T15:44:54+00:00)

Closed. Will ship in v0.23.0.
