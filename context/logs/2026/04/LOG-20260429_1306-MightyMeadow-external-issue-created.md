---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260429_1306-MightyMeadow-external-issue-created
  created: '2026-04-29T13:06:53+00:00'
spec:
  event_type: external_issue.created
  timestamp: '2026-04-29T13:06:53+00:00'
  summary: Filed aibox issues for derived-project preauth persistence and stale generated
    skill pruning
  actor: codex
  subject: projectious-work/aibox#58,#59
  subject_kind: GitHubIssue
  details:
    issues:
    - https://github.com/projectious-work/aibox/issues/58
    - https://github.com/projectious-work/aibox/issues/59
    classification:
      '58': aibox-owned harness preauth merge/persistence after rebuilds; processkit
        owns spec/diagnostic
      '59': aibox-owned pruning of stale generated processkit skill/command artifacts
        after upstream renames
    processkit_changes: Updated processkit preauth spec/diagnostic for Codex and status-briefing/pk-resume
      migration surfacing.
---
