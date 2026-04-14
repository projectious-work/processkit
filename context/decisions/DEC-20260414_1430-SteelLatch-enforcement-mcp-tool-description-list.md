---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  created: '2026-04-14T14:30:00+00:00'
spec:
  title: 'Lock the list of MCP tools that embed the 1% rule in their description'
  state: accepted
  decision: >
    Embed a one-sentence 1%-rule reminder into the MCP tool description
    of exactly eight tools, locked by this record: route_task,
    find_skill, create_workitem, transition_workitem, record_decision,
    log_event, open_discussion, create_artifact. Each tool's existing
    docstring is extended (not replaced) with a ≤120-character suffix
    of the form "Call route_task first — if there is a 1% chance a
    processkit skill applies, route before acting." The three write-
    side tools (create_workitem, record_decision, create_artifact)
    also carry "Commit in the same turn; deferred writes are dropped."
    A smoke-test assertion verifies the string "1% rule" is present in
    every listed description so future edits cannot silently drop it.
  context: >
    The enforcement research (ART-20260414_1230-ReachReady) shows tool
    descriptions are the most durable prose surface — they ship inside
    the synthesised system prompt every turn on any MCP-speaking
    harness. Anthropic's own guidance says tool descriptions are good
    for short discovery-shaped rules; long rules belong in the system
    prompt. processkit has ~70+ MCP tools across 15 skills; putting
    the reminder on all of them would bloat the tool list. Owner
    explicitly asked for a locked, auditable list.
  rationale: >
    Four criteria drove the eight-tool selection. (1) Entry points —
    route_task and find_skill are the two tools an agent should reach
    for first on any domain task; the 1% rule is most actionable on
    them. (2) High-leverage writes — create_workitem, record_decision,
    create_artifact, open_discussion, log_event are the create-side
    tools most often called from general knowledge instead of via
    route_task. (3) State changes — transition_workitem is the main
    state-changing call and is the one where a skipped route_task most
    often produces an invalid transition. (4) Stable descriptions —
    every listed tool has a stable, well-tested docstring; adding a
    sentence does not risk a long-form regression. Read-side tools
    (query_*, get_*, list_*) are excluded — they are low-risk and
    adding boilerplate to every one of them would dominate the tool
    list. Layer-0 primitives beyond log_event (generate_id, reindex,
    search_entities) are excluded as they are too foundational to
    carry enforcement text without noise.
  alternatives:
  - option: "Embed on every MCP tool (71+ tools)"
    rejected_because: "Bloats the tool list, hurts attention, and
      buries the signal in boilerplate; fails Anthropic's own guidance
      on keeping tool descriptions focused."
  - option: "Embed on only route_task and find_skill (two-tool minimum)"
    rejected_because: "Leaves the create_* surface unguarded — the
      exact tools agents reach for from general knowledge without
      routing. Research §3 lists these as the highest-leverage write-
      side gaps."
  - option: "Put the 1% rule only in AGENTS.md and hook output, not in
      tool descriptions at all"
    rejected_because: "Tool descriptions are the only surface that
      survives compaction on Claude Code without a hook, and the only
      rail that works on harnesses without hooks or AGENTS.md
      re-injection. Skipping this rail drops a zero-cost transport."
  - option: "Embed a multi-sentence rule, not a single sentence"
    rejected_because: "Anthropic guidance: long tool-description rules
      are worse than short ones; long rules belong in the system
      prompt. Multi-sentence descriptions also hurt the tool list's
      scannability."
  - option: "Rotate the set annually based on telemetry"
    rejected_because: "No telemetry pipeline exists today; locking the
      list is a precondition for measuring. Revisit in the A/B
      evaluation recommended by the research report."
  consequences: >
    (1) The smoke-test suite (scripts/smoke-test-servers.py) gains an
    assertion that each of the eight tool descriptions contains the
    literal string "1% rule"; PRs that drop it fail CI. (2) skill-
    builder's new-skill template documents the criterion so additions
    to this list have a clear bar. (3) The WorkItem
    FEAT-20260414_1432-InkStamp-mcp-tool-description-1pct-rule
    implements the eight edits and the CI guard. (4) Any future
    proposal to add a ninth tool or remove one must supersede this
    record, not amend it silently.
  decided_at: '2026-04-14T14:30:00+00:00'
  related:
    - SKILL-skill-gate
    - SKILL-task-router
    - SKILL-skill-finder
    - SKILL-workitem-management
    - SKILL-decision-record
    - SKILL-event-log
    - SKILL-discussion-management
    - SKILL-artifact-management
  supersedes: []
  superseded_by: null
---

# Locked list: MCP tools that carry the 1% rule

The eight tools are:

| # | Tool | Server / skill | Role |
|---|---|---|---|
| 1 | `route_task` | `task-router` | Primary entry point — "call first". |
| 2 | `find_skill` | `skill-finder` | Fallback entry point when route confidence is low. |
| 3 | `create_workitem` | `workitem-management` | Highest-volume write. |
| 4 | `transition_workitem` | `workitem-management` | State-changing write; most vulnerable to invalid transitions. |
| 5 | `record_decision` | `decision-record` | Cross-cutting record; routinely skipped from general knowledge. |
| 6 | `log_event` | `event-log` | Audit-trail entry point; skipped after hand-edits. |
| 7 | `open_discussion` | `discussion-management` | Multi-turn conversation entry; used for upstream-proposal workflow. |
| 8 | `create_artifact` | `artifact-management` | Deliverable registration; often done as a hand-edit. |

Each description keeps its existing docstring and gains ≤120 extra
characters. The canonical reminder text is owned by
`FEAT-20260414_1432-InkStamp-mcp-tool-description-1pct-rule`.
