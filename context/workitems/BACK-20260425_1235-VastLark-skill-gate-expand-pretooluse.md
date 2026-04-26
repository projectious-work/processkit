---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_1235-VastLark-skill-gate-expand-pretooluse
  created: '2026-04-25T12:35:30+00:00'
  updated: '2026-04-26T15:16:09+00:00'
spec:
  title: 'skill-gate: expand PreToolUse matcher to all write-side MCP tools (auto-renew
    gap)'
  state: done
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
  started_at: '2026-04-26T14:58:45+00:00'
  completed_at: '2026-04-26T15:16:09+00:00'
---

## Transition note (2026-04-26T14:58:45+00:00)

Starting work — going with the inverted approach from the WI (match on write-side prefixes, not an explicit allowlist). The unqualified tool_name shape (e.g. "create_workitem", "create_binding") makes prefix matching trivial. Will keep the explicit set as documentation but extend match logic to cover all write-side prefixes the contract enumerates.


## Transition note (2026-04-26T15:16:06+00:00)

Fix landed in context/skills/processkit/skill-gate/scripts/check_route_task_called.py (mirrored to src/). Switched from explicit allowlist to prefix-based matcher: any tool whose name starts with create_/transition_/link_/record_/open_/update_/apply_/reject_/add_/end_/import_/reactivate_/deactivate_/release_/reserve_/supersede_/start_/evaluate_/skip_ is now gate-locked. log_event remains explicit (verb+noun shape). Read-side (get_*/query_*/list_*/search_*/recent_*/find_*/resolve_*/compare_*/explain_*/route_task/acknowledge_contract/check_*) all pass through. test_hooks.py extended with 40 new cases covering 25 locked-prefix tools (incl. the original create_binding repro from the WI) and 15 read-side passthrough tools — all pass. pk-doctor green.


## Transition note (2026-04-26T15:16:09+00:00)

Closed. Implementation in main, all 40 prefix-matcher tests pass. Will ship in v0.23.0.
