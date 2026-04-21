---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260420_1340-LoyalFrog-add-pk-retro-skill
  created: '2026-04-20T13:40:28+00:00'
  updated: '2026-04-21T16:58:10+00:00'
spec:
  title: Add /pk-retro skill — post-release retrospective
  state: done
  type: story
  priority: medium
  description: 'Motivation: the v0.15.0–v0.18.0 content drift + v0.18.1 hotfix + v0.18.2
    release-under-MCP-outage sequence is enough of a pattern that a structured post-release
    retrospective pays for itself. Target: a `retrospective` skill that, given a release
    tag, generates a retro artifact covering (a) what went well, (b) what broke /
    was deferred, (c) drift / divergence between plan and execution, (d) action items
    to prevent recurrence. Candidate input: LogEntries tagged `session.release`, commits
    between the previous tag and this tag, any `skip_decision_record` markers from
    the release window.


    Acceptance: a `/pk-retro <tag>` slash command produces a retro LogEntry or Artifact
    and lists candidate backlog items. First dog-food target: v0.18.2. Feeds backlog
    candidates like "runtime-MCP-handshake guard" (handover open_thread runtime-vs-release-drift-class).'
  started_at: '2026-04-21T11:26:01+00:00'
  completed_at: '2026-04-21T16:58:10+00:00'
---

## Transition note (2026-04-21T11:26:01+00:00)

Owner approved all-phases scope + Phase 0 rename (morning-briefing → status-briefing). Dispatching two sequential Sonnet workers (A=rename, B=retrospective skill Phase 1-3).


## Transition note (2026-04-21T16:58:04+00:00)

All phases shipped in 87e185e: Phase 0 rename, Phase 1 base skill + 4 signals, Phase 2 --auto-workitems, Phase 3 --verbose. Tests 27/27 pass; pk-doctor 0 ERROR / 0 WARN; dogfood dry-run on v0.18.2 produced valid retro with [uncertain] guard firing correctly.


## Transition note (2026-04-21T16:58:10+00:00)

Shipped in 87e185e (pushed to main e164fdb..87e185e).
