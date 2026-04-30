---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260423_1101-SunnyComet-extend-v0-19-2
  created: '2026-04-23T11:01:43+00:00'
spec:
  title: Extend v0.19.2 scope to include pk-doctor commands/ directory gap
  state: accepted
  decision: 'Add a fourth v0.19.2 workstream after TrueQuail: ship the missing `context/skills/processkit/pk-doctor/commands/pk-doctor.md`
    file and re-mirror into the template tree so derived projects that install v0.19.2
    get the `/pk-doctor` slash command registered.'
  context: 'A derived project reported that pk-doctor is not available as a slash
    command despite v0.19.1 installing the skill. Root cause: v0.19.1 shipped SKILL.md
    and scripts/doctor.py, but the `commands/` directory was never created for the
    pk-doctor skill, so the slash-command registration step in the installer has nothing
    to pick up. Confirmed by diff against the template mirror at `context/templates/processkit/v0.19.1/`:
    peer skills like status-briefing and model-recommender have their `commands/pk-*.md`
    files, pk-doctor does not.'
  rationale: The gap is purely a missing file — minutes of work — and blocks every
    derived project from using /pk-doctor. Folding it into v0.19.2 avoids shipping
    a v0.19.3 patch release just for this. Fits naturally after BraveDove/TrueQuail
    as a low-risk tail item.
  consequences: v0.19.2 grows from 3 → 4 items. Template mirror must be re-generated
    as part of the release to propagate the new commands/ file. A brief audit should
    check whether any other shipped skill with a `commands:` metadata block also lacks
    its commands/ directory, to avoid a recurrence.
  deciders:
  - TEAMMEMBER-cora
  decided_at: '2026-04-23T11:01:43+00:00'
---
