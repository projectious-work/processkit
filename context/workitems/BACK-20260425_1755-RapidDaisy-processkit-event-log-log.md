---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_1755-RapidDaisy-processkit-event-log-log
  created: '2026-04-25T17:55:34+00:00'
  updated: '2026-04-26T14:57:51+00:00'
spec:
  title: processkit-event-log log_event MCP skips actor required-field validation
  state: done
  type: bug
  priority: medium
  description: '## What


    `log_event` writes LogEntry files that violate the schema by omitting the required
    `actor` field.


    ## Repro


    Two log entries created today by `log_event` have no `actor` in spec, despite
    `src/context/schemas/logentry.yaml:23` declaring `required: [event_type, actor,
    timestamp]`:


    - `context/logs/2026/04/LOG-20260425_1734-TallSage-workitem-note.md`

    - `context/logs/2026/04/LOG-20260425_1724-MightySage-workitem-note.md`


    Both were hand-fixed today (added `actor: ACTOR-claude`) so pk-doctor schema_filename
    goes 3 ERROR → 0 ERROR. The MCP is the producer to fix.


    ## Surfaced by


    pk-doctor `schema_filename` check during the v0.22.0 pre-release sweep (after
    RapidSwan landed).


    ## Suggested fix


    Either:

    1. Reject `log_event` calls that don''t pass `actor` (matches schema strictly),
    or

    2. Auto-inject `actor` from the calling agent''s session identity (matches the
    `ACTOR-claude` convention used by the other ~600 in-repo log entries).


    Option 2 is the friendlier default; the contract still requires the agent to be
    identifiable, so a registered actor is always available.


    ## Done when


    - `log_event` rejects (or auto-fills) calls without `actor`.

    - Test added that asserts a malformed call fails with a clear error.

    - pk-doctor schema_filename stays at 0 ERROR for log entries on a fresh dogfood
    run.'
  started_at: '2026-04-26T14:56:03+00:00'
  completed_at: '2026-04-26T14:57:51+00:00'
---

## Transition note (2026-04-26T14:56:03+00:00)

Starting work — going with strict validation (Option 1 from the WI). Will add schema.validate_spec("LogEntry", spec) before write so missing actor produces a clear error response. Auto-default to ACTOR-claude is too presumptuous in derived projects (their default actor varies); the contract requires a registered actor anyway, so the caller should always have one.


## Transition note (2026-04-26T14:57:46+00:00)

Fix landed in context/skills/processkit/event-log/mcp/server.py (mirrored to src/). Strict validation via schema.validate_spec("LogEntry", spec) before write; missing/empty actor returns {"error": "..."} with no file written. Docstring + module preamble updated to mark actor as required. 3 tests in event-log/scripts/test_log_event.py: missing-actor → error, valid-actor → success, empty-actor → error. pk-doctor green (0 ERROR / 2 WARN — both unchanged drift WARNs).


## Transition note (2026-04-26T14:57:51+00:00)

Closed. Implementation in main, tested, schema-clean. Will ship in v0.23.0.
