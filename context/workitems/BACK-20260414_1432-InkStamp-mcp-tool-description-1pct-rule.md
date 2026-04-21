---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260414_1432-InkStamp-mcp-tool-description-1pct-rule
  legacy_id: BACK-20260414_1432-InkStamp-mcp-tool-description-1pct-rule
  created: '2026-04-14T14:32:00+00:00'
  labels:
    component: mcp-servers
    area: enforcement
spec:
  title: Embed the 1% rule in the eight locked MCP tool descriptions (+ CI guard)
  state: done
  type: story
  priority: high
  size: S
  description: >
    Append a one-sentence 1%-rule reminder to the docstrings of exactly
    eight MCP tools locked in DEC-20260414_1430-SteelLatch. Add a
    smoke-test assertion so the string "1% rule" cannot silently be
    dropped. No new tools, no docstring rewrites — extend only.
  inputs:
    - /workspace/context/decisions/DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list.md
    - /workspace/context/skills/processkit/task-router/mcp/server.py
    - /workspace/context/skills/processkit/skill-finder/mcp/server.py
    - /workspace/context/skills/processkit/workitem-management/mcp/server.py
    - /workspace/context/skills/processkit/decision-record/mcp/server.py
    - /workspace/context/skills/processkit/event-log/mcp/server.py
    - /workspace/context/skills/processkit/discussion-management/mcp/server.py
    - /workspace/context/skills/processkit/artifact-management/mcp/server.py
    - /workspace/scripts/smoke-test-servers.py
  locked_tool_set:
    - route_task (task-router)
    - find_skill (skill-finder)
    - create_workitem (workitem-management)
    - transition_workitem (workitem-management)
    - record_decision (decision-record)
    - log_event (event-log)
    - open_discussion (discussion-management)
    - create_artifact (artifact-management)
  canonical_suffix_reading: >
    Entry tools (route_task, find_skill): " 1% rule: if there is a 1%
    chance a processkit skill covers this task, call route_task before
    acting."
    Write tools (create_*, record_*, log_*, open_*, transition_*):
    " 1% rule: call route_task first; commit in the same turn — deferred
    writes are dropped."
  deliverables:
    - 8 edited tool docstrings across the server.py files listed above.
    - scripts/smoke-test-servers.py updated with an assertion looping over the 8 qualified tool names and failing if "1% rule" is absent from the description.
  success_criteria:
    - Each of the eight tools' docstrings, when read via `tool.description` in FastMCP, contains the literal string "1% rule".
    - Each appended suffix is ≤120 characters.
    - No existing docstring text is removed or reordered.
    - "`uv run scripts/smoke-test-servers.py` passes; deleting the suffix from any one tool causes the new assertion to fail."
    - No MCP tool outside the locked set is edited in this WorkItem.
  out_of_scope:
    - Adding the rule to any ninth tool. That requires a superseding DecisionRecord.
    - Touching the read-side query_* / get_* / list_* tools.
  related_decisions:
    - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  assigned_to: ACTOR-developer
  parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
  progress_notes:
    - timestamp: '2026-04-14T14:35:00+00:00'
      actor: ACTOR-developer
      note: >
        open→in-progress: Starting implementation. Located all 8 server.py
        files and smoke-test-servers.py.
    - timestamp: '2026-04-14T14:40:00+00:00'
      actor: ACTOR-developer
      note: >
        in-progress→done: Appended 1%-rule sentences to all 8 locked tool
        docstrings (read-side suffix on route_task + find_skill; write-side
        suffix on create_workitem, transition_workitem, record_decision,
        log_event, open_discussion, create_artifact). Added CI guard block
        to scripts/smoke-test-servers.py asserting "1% rule" is present in
        all 8 tool descriptions. No tools outside the locked set were touched.
---
