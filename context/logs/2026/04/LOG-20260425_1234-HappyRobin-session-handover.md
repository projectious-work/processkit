---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260425_1234-HappyRobin-session-handover
  created: '2026-04-25T12:34:57+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-25T12:34:14Z'
  summary: Session handover — v0.21.0 shipped with 8 fixes incl. critical pk-doctor
    derived-project bugs; aibox should bump pin
  actor: claude-opus-4-7
  details:
    session_date: '2026-04-25'
    current_state: 'v0.21.0 released and verified (commit aa3b441, GitHub Release
      published 2026-04-25T11:12:23Z). All 5 retro WorkItems from v0.19.2 retro are
      resolved: 3 shipped in v0.20.0, 2 superseded via split decisions (SharpBrook
      → DEC-QuickPine; SnappyBird → DEC-NobleSky). v0.21.0 bundles 8 fixes — most
      notably HappyReef (pk-doctor schema_filename layout-fallback) and DeepMoss (migrations
      layout-fallback), discovered when user reported pk-doctor returning 0/0 in the
      aibox derived project despite obvious entity-hygiene issues. After fix, aibox
      doctor surfaces 96 ERROR / 129 WARN across 186 walked entity files. KeenFern
      expanded default-bindings MANIFEST 30→50 to close the 5-level seniority ladder
      gap (specialist/expert tiers). Tree is clean on main; no stashes; no in-progress
      or blocked WorkItems.'
    open_threads:
    - 'aibox derived project: bump processkit pin from v0.20.0 → v0.21.0 to pick up
      HappyReef + DeepMoss doctor fixes; re-run /pk-doctor and triage the surfaced
      96 ERROR / 129 WARN.'
    - 'BACK-20260424_0128-RapidSwan (backlog, low): pk-doctor server_header_drift
      WARN — supersedes SharpBrook scope, deferred from v0.21.0 by DEC-QuickPine.'
    - 'BACK-20260423_0829-TrueQuail (review, high): aibox installer reconcile .mcp.json
      on per-skill-config drift, not just version delta — sitting in review.'
    - Skill-gate auto-renew (SwiftLynx) did not fire on create_binding calls earlier
      in this session — current PreToolUse matcher list is incomplete; workaround
      was manual re-ack. Not yet filed as a WorkItem.
    - 'Pre-existing v0.22.0+ backlog: SmartPanda model-class assignment epic, SprySage
      task-router v0.2, SpryLark context-archiving skill, SunnyLily library-expert
      spike, plus assorted skill-creation stories — none touched this session.'
    next_recommended_action: Bump aibox to processkit v0.21.0 (edit aibox.lock processkit.version
      + release_asset_sha256), run /pk-doctor in the aibox container, and triage the
      96 ERROR / 129 WARN — most likely candidates are CalmAnt-class missing-actor
      and x-aibox-* unknown-field entries that originally motivated this session.
    branch: main
    commit: aa3b441
    behavioral_retrospective:
    - pk-doctor checks were silently dogfood-path-only (hardcoded src/context/schemas
      + pending/ subdir). Encoded as test_doctor.py[8] HappyReef and [9] DeepMoss
      layout-fallback regression tests. Future check authors should default to a fallback
      chain (src/context/<x> → context/<x>) — consider adding an explicit note in
      pk-doctor's SKILL.md or in checks/common.py.
    - Issue surfaced only when the user manually ran the tool in the derived project;
      smoke-test-servers.py and dogfood pk-doctor both passed. Filing follow-up WorkItem
      to add a derived-project simulation harness to CI is worth considering for v0.22.0
      — not filed yet.
    - Skill-gate SwiftLynx auto-renew limitation (PreToolUse matcher list does not
      include create_binding) caused a stale-ack at the 2026-04-24 → 2026-04-25 boundary.
      Not yet filed; recommend a small WorkItem to expand the matcher to all write-side
      tools.
    - 'WorkItem state-machine forbids backlog → done; SharpBrook + SnappyBird were
      transitioned to cancelled with ''superseded by DEC-…'' rationale. This is the
      documented protocol — no gap, but worth restating: superseded ≠ done.'
---
