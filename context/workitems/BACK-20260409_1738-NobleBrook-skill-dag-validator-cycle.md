---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1738-NobleBrook-skill-dag-validator-cycle
  created: '2026-04-09T17:38:28+00:00'
spec:
  title: Skill DAG validator — cycle detection and layer constraint checks
  state: backlog
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
---
