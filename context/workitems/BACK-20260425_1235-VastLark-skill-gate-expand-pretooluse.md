---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_1235-VastLark-skill-gate-expand-pretooluse
  created: '2026-04-25T12:35:30+00:00'
spec:
  title: 'skill-gate: expand PreToolUse matcher to all write-side MCP tools (auto-renew
    gap)'
  state: backlog
  type: task
  priority: low
  description: '**Problem.** SwiftLynx''s auto-renew (introduced in v0.21.0 via `check_route_task_called.py`)
    only fires when one of the matched tools is invoked. The current PreToolUse matcher
    list is narrower than the full set of write-side MCP tools — observed gap: `create_binding`
    is not matched, so during a session that only calls binding tools, the contract
    ack expires at the 12 h boundary and the next write fails until the agent manually
    re-acknowledges.


    **Repro from 2026-04-25 session.** Date crossed 2026-04-24 → 2026-04-25 mid-session;
    the only write traffic in the window was a sequence of `create_binding` calls.
    SwiftLynx never renewed, ack expired, next unrelated write hit the gate.


    **Fix sketch.**

    - Audit the matcher patterns in skill-gate hooks (`scripts/check_route_task_called.py`,
    plus the generated harness hook config).

    - Add the full write-side surface: `create_*`, `transition_*`, `link_*`, `record_*`,
    `open_*`, `update_*`, `apply_*`, `reject_*`, `add_*`, `end_*`, `import_*`, `reactivate_*`,
    `deactivate_*`, `release_*`, `reserve_*`, `supersede_*`.

    - Or invert the matcher: match on tool *server* (any `mcp__processkit-*`) and
    exclude read-only tools by name pattern. Inversion is more robust as new servers
    are added.


    **Acceptance.** During a session that only exercises `create_binding` (or any
    single previously-unmatched tool), auto-renew fires and ack does not expire.


    **Origin.** Filed from session-handover behavioral retrospective in `LOG-20260425_1234-HappyRobin-session-handover`.'
---
