---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0038-SnappyBird-data-repair-path-for
  created: '2026-04-24T00:38:38+00:00'
  updated: '2026-04-24T01:29:25+00:00'
spec:
  title: Data-repair path for malformed append-only LogEntries — migration or log_event
    override
  state: cancelled
  type: task
  priority: low
  assignee: TEAMMEMBER-cora
  description: '**Observed pattern (v0.19.2 retro):** `LOG-20260422_1643-CalmAnt-workitem-created.md`
    was written by a pre-TeamMember MCP server without populating the required `actor`
    field, so `pk-doctor --category=schema_filename` reported a schema ERROR. LogEntries
    are `append_only: true` and `log_event` only creates new entries — there is no
    MCP path to repair an existing malformed LogEntry. The fix had to be a direct
    hand-edit (allowed because the file was already schema-invalid, but still friction).


    **Proposed approaches:**

    - Data-fix migration kind in `migration-management` that declares a repair, routes
    through a review gate, and applies as a proper channel.

    - `log_event --repair=<existing_id>` flag that overwrites a single malformed entry
    with an auto-appended `repaired_from` field pointing at the original.

    - OR a pk-doctor `--fix=schema_filename` path that offers to patch known-safe
    missing fields (like `actor: system` for pre-TeamMember logs).


    **Done criteria:**

    - Any future malformed LogEntry can be repaired via an MCP-sanctioned path. No
    more hand-edits to `context/logs/`.

    - Audit trail preserved: the repair itself emits a log entry.


    **Target:** v0.20.0. **Owner:** cora.'
  completed_at: '2026-04-24T01:29:25+00:00'
---

## Transition note (2026-04-24T01:29:25+00:00)

Superseded by DEC-20260424_0128-BrightHawk. Replaced with narrow WI BACK-MightyFjord (pk-doctor --fix=schema_filename + AGENTS.md note). The general data-fix migration kind is NOT being built.
