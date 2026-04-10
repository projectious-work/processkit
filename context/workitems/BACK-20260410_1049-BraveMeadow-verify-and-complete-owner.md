---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1049-BraveMeadow-verify-and-complete-owner
  created: '2026-04-10T10:49:40+00:00'
spec:
  title: Verify and complete owner-profiling reference files
  state: backlog
  type: task
  priority: medium
  description: 'The owner-profiling skill references two files that must exist and
    be complete:

    - context/skills/owner-profiling/references/observable-signals.md

    - context/skills/owner-profiling/references/interview-protocol.md


    Full spec for observable-signals.md is in NOTE-20260410_1046-StoutSwan (sourced
    from aibox/move-to-processkit/research/owner-profiling-skill-2026-03.md). It defines
    24 signals across 4 categories (communication, technical preferences, decision
    patterns, workflow patterns).


    Action:

    1. Check whether these files exist and are populated

    2. If missing or stub: write them using the spec in the Note

    3. Also check: src/context/skills/owner-profiling/ mirrors context/skills/owner-profiling/


    Note: multi-actor extension (context/actors/<actor-id>/ four-file structure) is
    a future item, not in scope here.'
---
