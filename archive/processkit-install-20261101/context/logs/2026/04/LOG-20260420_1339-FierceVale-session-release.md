---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260420_1339-FierceVale-session-release
  created: '2026-04-20T13:39:28+00:00'
spec:
  event_type: session.release
  timestamp: '2026-04-20T13:39:28+00:00'
  summary: 'processkit v0.18.2 released: issue #8 fixed (mcp-config.json path regression),
    skip_decision_record + contract v2 + drift guard + SnappyTrout shipped. Release
    URL: https://github.com/projectious-work/processkit/releases/tag/v0.18.2'
  actor: ACTOR-pm-claude
  details:
    version: v0.18.2
    released_at: '2026-04-18T20:50:00Z'
    commits:
    - e9768b7
    - c54af68
    - 451a930
    tarball_size: 726K
    issue_closed: 8
    deviation_note: MCP write tools were unreachable during release session; release
      pipeline is file-only (git + scripts + gh) so proceeded without MCP writes.
      This log_event + the re-recorded DEC-20260417_1800 close the 4-handover deviation
      window.
---
