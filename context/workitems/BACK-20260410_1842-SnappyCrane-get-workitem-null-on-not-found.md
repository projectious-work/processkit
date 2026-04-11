---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1842-SnappyCrane-get-workitem-null-on-not-found
  created: '2026-04-10T18:42:00+00:00'
  updated: '2026-04-11T06:26:33+00:00'
spec:
  title: 'Bug: get_workitem returns null for not-found IDs instead of a clear error'
  state: done
  type: bug
  priority: medium
  description: 'Observed: calling get_workitem with a non-existent ID (e.g. "BACK-20260410_1050-StoutCrow",
    which is a truncated form of the real ID) returns {"result":null}. This is indistinguishable
    from a found-but-empty entity and gives the agent no signal that the lookup failed.


    Expected: the MCP server should return a clear error — e.g. {"error": "WorkItem
    not found: BACK-20260410_1050-StoutCrow"} — so the agent can detect the failure
    and take corrective action (fall back to search, report to the user, etc.).


    Impact: agents silently proceed as if the entity is empty rather than realising
    the ID was wrong. Discovered when looking up StoutCrow by word-pair only (see
    BACK-20260410_1842-SteadyPeak-entity-lookup-by-word for the related lookup capability
    gap).


    Fix location: processkit workitem-management MCP server — get_workitem handler
    should raise / return an error when the entity file does not exist or the ID is
    not found in the index.'
  started_at: '2026-04-11T06:26:25+00:00'
  completed_at: '2026-04-11T06:26:33+00:00'
---

## Transition note (2026-04-11T06:26:33+00:00)

Already fixed. get_workitem uses resolve_entity and explicitly returns {"error": "WorkItem not found: ..."} when row is None. Verified by test: get_workitem("BACK-99991234-FakeCrow-does-not-exist") → {"error": "WorkItem not found: ..."}. Not null.
