---
sidebar_position: 2
title: "Process Skills"
---

# Process Skills

Skills for managing project workflows, team coordination, and operational
processes. Most process-primitive skills have an accompanying MCP server
that enforces schema validation and state-machine rules.

---

### workitem-management

> Creates, transitions, and queries WorkItems — the task-tracking
> primitive in processkit. Use when managing backlog items, updating
> work item state, or querying items by status, owner, or priority.

**Triggers:** When the user asks to create a ticket, update a work item,
query the backlog, or track progress on a task.
**Tools:** `create_workitem`, `transition_workitem`, `query_workitems`,
`get_workitem`, `link_workitems`
**Layers:** Layer 2 (depends on `event-log`, `actor-profile`)

Key capabilities:

- Create WorkItems with type (`task`, `story`, `bug`, `epic`, `spike`, `chore`)
  and priority (`critical`, `high`, `medium`, `low`)
- Transition through the default state machine:
  `backlog → in-progress → review → done` (with `blocked` as a side state)
- Link parent/child WorkItems for epics and subtasks
- Query by state, type, priority, owner, or label
- All state transitions auto-append a LogEntry via `event-log`

<details><summary>Example usage</summary>

User asks to create a ticket for a new feature. Agent calls
`generate_id` to get a `BACK-` ID, then `create_workitem` with title,
type `story`, and priority `high`. Later the user starts work — agent
calls `transition_workitem` to move it to `in-progress`.

</details>

---

### decision-record

> Captures architectural and product decisions as DecisionRecord entities
> (ADR pattern). Use when the team makes a significant choice with
> rationale, alternatives, and implications.

**Triggers:** When the user says "write a decision", "document this ADR",
"record why we chose X", or "capture this architectural decision".
**Tools:** `record_decision`, `transition_decision`, `query_decisions`,
`get_decision`, `supersede_decision`, `link_decision_to_workitem`
**Layers:** Layer 2 (depends on `event-log`)

Key capabilities:

- Record decisions with status (`proposed`, `accepted`, `rejected`),
  rationale, alternatives considered, and implications
- Link decisions to WorkItems for traceability
- Supersede old decisions when context changes
- Query by status, tag, or date

<details><summary>Example usage</summary>

Team decides to use SQLite for local dev instead of PostgreSQL. Agent
records a DecisionRecord with the rationale ("zero-config, no Docker
dependency for contributors"), alternatives considered, and implications.
Status starts as `proposed`; on approval it transitions to `accepted`.

</details>

---

### artifact-management

> Registers and retrieves completed deliverables — documents, datasets,
> builds, diagrams, URLs, runbooks. Use when cataloguing a produced
> output so future agents and humans can find it.

**Triggers:** When the user says "register an artifact", "catalog this
document", "store this deliverable", or "link this design file".
**Tools:** `create_artifact`, `get_artifact`, `query_artifacts`,
`update_artifact`
**Layers:** Layer 2 (no state machine — Artifact is a catalogue record)

Key capabilities:

- Two usage patterns: **self-hosted** (Markdown body in the entity file)
  and **pointer** (external URL or file path via `location`)
- Tag artifacts for filtering (`kind`, labels)
- Query by kind, tag, or title substring
- Update metadata on existing artifacts

<details><summary>Example usage</summary>

After generating a runbook, agent calls `create_artifact` with
`kind: document`, `title: "Deploy Runbook — v0.12.0"`, and stores the
Markdown body directly in the artifact file. A design file lives in
Figma — agent creates a pointer artifact with
`location: "https://figma.com/..."`.

</details>

---

### event-log

> Writes auditable LogEntry records for any project event. Use when you
> want an immutable record of something that happened.

**Triggers:** When the user says "log this event", "audit trail",
"record that we did X", or when any entity-mutating MCP server fires a
side-effect log.
**Tools:** `log_event`, `query_events`, `recent_events`
**Layers:** Layer 0 (foundation — no dependencies)

Key capabilities:

- Append-only — LogEntries are never updated or deleted
- Entity-mutating MCP servers (create, transition, link) auto-append
  a LogEntry without the caller doing anything extra
- Query by actor, entity, event type, or date range
- `recent_events` returns the last N entries across all entities

<details><summary>Example usage</summary>

Agent explicitly logs a manual step: "Deployed v0.12.0 tarball to GitHub
Releases". Separately, every `transition_workitem` call automatically
appends a log entry recording the before/after state.

</details>

---

### note-management

> Captures, reviews, and promotes fleeting ideas and insights using the
> Zettelkasten method. Use when the user wants to record an observation,
> link related ideas, or build a personal knowledge base.

**Triggers:** When the user says "remember this", "note this idea",
"capture this", or "link this to another note".
**Tools:** None (file-based via SKILL.md instructions)
**Layers:** Layer 4

Key capabilities:

- Three note types: `fleeting` (raw capture), `insight` (permanent note,
  never discarded), `reference` (literature note)
- `links` field for typed Zettelkasten edges:
  `elaborates`, `contradicts`, `supports`, `is-example-of`, `see-also`,
  `refines`, `sourced-from`
- Each link requires a `context` sentence explaining *why* the connection
  matters — tags group, links argue
- Notes stored under `context/notes/`

<details><summary>Example usage</summary>

During research the user observes: "FTS5 trigram tokeniser can match
partial words without prior tokenisation." Agent creates a `fleeting`
note. Later the user promotes it to an `insight` and links it to a
related note about search UX with relation `supports`.

</details>

---

### session-handover

> Writes an end-of-session handover document before the agent shuts down
> or the container restarts. Use to preserve state across context resets.

**Triggers:** When the user says "write a handover", "shutting down",
"container restart", "end of session", or when context is approaching
its limit.
**Tools:** None (file-based via SKILL.md instructions)
**Layers:** Layer 4

Key capabilities:

- Captures: current task state, open decisions, blockers, what was
  completed, and suggested next actions
- Stores as a LogEntry with a generated `LOG-` ID under `context/logs/`
- Includes a `generate_id` call and date-sharded path derivation
- Designed to be the first thing the next agent reads at session start

<details><summary>Example usage</summary>

Before shutdown, agent writes a handover capturing the in-progress
WorkItem IDs, the open Discussion about the schema change, and the
three concrete next steps for the incoming session.

</details>

---

### standup-context

> Writes a standup update in Done / Doing / Next / Blockers format. Use
> at the start of a work session, for daily standups, or for async team
> updates.

**Triggers:** When the user says "write a standup", "daily update",
"what did we do yesterday", or "status update for the team".
**Tools:** None (file-based via SKILL.md instructions)
**Layers:** Layer 4

Key capabilities:

- Reads open and recently-completed WorkItems to populate Done / Doing
- Reads Discussion entities for blockers
- Outputs a clean, copy-pasteable standup
- Optionally stores as a LogEntry for the audit trail

---

### morning-briefing

> Generates a session-start orientation from the current project state.
> Use at the beginning of a session to get a fast, structured catch-up.

**Triggers:** When the user says "morning briefing", "catch me up",
"state of things", or "what's on the board".
**Tools:** Reads `query_entities`, `recent_events` via index-management
**Layers:** Layer 4

Key capabilities:

- Summarises open WorkItems by state and priority
- Surfaces recent LogEntries (what changed since last session)
- Highlights open Discussions and pending Decisions
- Reports any pending Migrations

---

### context-grooming

> Periodically prunes and compacts the project context to keep it
> navigable. Use when `context/` has grown stale or cluttered.

**Triggers:** When the user says "groom the context", "clean up context",
or when the entity count in any directory is getting unwieldy.
**Tools:** index-management for enumeration; per-kind MCP servers for
transitions
**Layers:** Layer 4

Key capabilities:

- Identifies `done` WorkItems older than N days as candidates for
  archiving
- Surfaces Discussions in `open` state that have had no activity
- Detects Notes in `fleeting` state that have not been promoted
- Proposes a grooming plan — does not auto-archive without confirmation

---

### release-semver

> Plans and executes a semantic versioning release. Use when preparing a
> new version of a project or library.

**Triggers:** When the user says "plan the release", "version bump",
"cut a release", or "prepare vX.Y.Z".
**Tools:** None (checklist-driven via SKILL.md instructions)
**Layers:** Layer 4

Key capabilities:

- Determine bump type (patch/minor/major) from change audit
- Update CHANGELOG and PROVENANCE
- Run smoke tests before tagging
- Commit, tag, push, build release tarball, create GitHub release
- processkit-specific: `stamp-provenance.sh` and
  `build-release-tarball.sh` are the canonical scripts

---

### retrospective

> Facilitates team or project retrospectives — what worked, what didn't,
> action items. Use at the end of a sprint, milestone, or project phase.

**Triggers:** When the user says "let's do a retro", "what went well?",
"lessons learned", or "end of sprint review".
**Tools:** None
**Layers:** Layer 4

Key capabilities:

- Scope the retrospective (time period or milestone)
- Gather input in three categories: What Worked, What Didn't, What to
  Try Next
- Action items must be specific, assignable, and time-bound
- Store as a LogEntry or Artifact in `context/`

---

### incident-response

> Guides production incident handling — triage, communicate, fix,
> postmortem. Use when something is broken in production.

**Triggers:** When the user reports a production issue or says "production
is down", "users are affected", "we have an incident".
**Tools:** None
**Layers:** Layer 4

Key capabilities:

- Triage within first 5 minutes: assess user impact, identify recent
  changes, evaluate rollback options
- Communicate to stakeholders with status, impact, and ETA
- Mitigate first, fix later: rollback or temporary workaround
- Postmortem within 48 hours: timeline, root cause, action items,
  blameless approach

---

### estimation-planning

> Software estimation and planning — story points, velocity tracking,
> scope negotiation, technical debt budgeting. Use when estimating work
> or planning sprints.

**Triggers:** When the user asks to estimate work, plan a sprint,
negotiate scope, or asks "how should I estimate this?".
**Tools:** None
**Layers:** Layer 4

Key capabilities:

- Story points vs time estimates: Fibonacci sizing, relative complexity
- Planning poker with anchoring-bias prevention
- Cone of uncertainty: communicate estimates as ranges with confidence
- Velocity tracking and MoSCoW prioritisation
- Three-point estimation with PERT formula

---

### postmortem-writing

> Blameless postmortem writing with timeline, root cause analysis, and
> corrective actions. Use when writing incident postmortems.

**Triggers:** When writing an incident postmortem, conducting a
post-incident review, or asking "how do I write a blameless postmortem?".
**Tools:** None
**Layers:** Layer 4

Key capabilities:

- Structured template: summary, impact, timeline, root cause, corrective
  actions, lessons learned
- 5 Whys root cause analysis down to systemic/process issues
- Corrective actions in prevent/detect/mitigate categories, each with
  owner and due date
- Blameless culture: systems-focused language, passive voice for human
  errors
