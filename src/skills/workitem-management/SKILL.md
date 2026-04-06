---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-workitem-management
  name: workitem-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Create, transition, query, and link WorkItems — tasks, stories, bugs, epics."
  category: process
  layer: 2
  uses: [event-log, actor-profile, index-management, id-management]
  provides:
    primitives: [WorkItem]
    mcp_tools: [create_workitem, transition_workitem, query_workitems, link_workitems]
    templates: [workitem, workitem-bug, workitem-story]
  when_to_use: "Use when the user asks to add, update, query, or link work items — backlog items, tasks, bugs, user stories, or epics."
---

# WorkItem Management

## Level 1 — Intro

WorkItems are the fundamental tracked unit of work in processkit — tasks,
stories, bugs, spikes, epics, tickets. This skill creates them, transitions
them through their state machine, links them to other entities, and queries
them.

## Level 2 — Overview

### When to create a WorkItem

Whenever the user (or you) identifies a distinct unit of work that should be
tracked. Don't create work items for every tiny thing — a WorkItem is worth
creating when it has:

- A clear title ("Add aibox lint command")
- A distinct state lifecycle (it starts somewhere, ends somewhere)
- Someone who should own it (even if not yet assigned)

If it's just a one-liner you're about to do in the next 30 seconds, don't
bother.

### WorkItem types

`spec.type` distinguishes subtypes:

| type    | When to use                                   |
|---------|-----------------------------------------------|
| `task`  | Default — generic unit of work                |
| `story` | User-facing feature framed as a user story    |
| `bug`   | Something that isn't working as intended      |
| `epic`  | Large body of work, parent of other WorkItems |
| `spike` | Time-boxed investigation with no committed deliverable |
| `chore` | Maintenance, cleanup, refactoring             |

### Creating

1. Pick the `type`.
2. Write a short, imperative `title`.
3. Set `state` to the initial state (`backlog` by default).
4. Set `priority` if known (`critical`/`high`/`medium`/`low`).
5. Assign to an Actor (optional at creation).
6. Write the file to `context/workitems/BACK-<id>.md`.
7. Log `workitem.created`.

### Transitioning

The default state machine is:

```
backlog → in-progress → review → done
            ↓      ↑
          blocked ↑
            ↓      ↑
          backlog ←
(any state) → cancelled (terminal)
```

To transition:
1. Check the current state allows the transition (see `primitives/state-machines/workitem.yaml`).
2. Update `spec.state`.
3. Update `metadata.updated`.
4. Set `spec.started_at` on first entry to `in-progress` (if unset).
5. Set `spec.completed_at` when entering a terminal state.
6. Log `workitem.transitioned` with `from_state` and `to_state` in `details`.

### Linking

Four types of links, all expressed in frontmatter:

| Field                | Meaning                                                |
|----------------------|--------------------------------------------------------|
| `parent`             | This WorkItem is a child of a larger one (epic)        |
| `children`           | This WorkItem has sub-items                            |
| `blocks`             | This WorkItem blocks others until done                 |
| `blocked_by`         | This WorkItem cannot proceed until others are done     |
| `related_decisions`  | DecisionRecord IDs that motivated or constrain this    |

For scoped/temporal relationships (e.g. "Alice is assigned to this for sprint 42
only"), use a Binding instead of `spec.assignee`.

### Querying

Common queries the index MCP server will expose in Phase 3:

- All WorkItems in a given state
- All WorkItems assigned to an actor
- All WorkItems blocked (or blocking something)
- All WorkItems in a scope
- Full-text search across title + body

Before Phase 3, query via filesystem glob + grep of `context/workitems/`.

## Level 3 — Full reference

### Full field list

See `src/primitives/schemas/workitem.yaml` for the authoritative schema.
Every field there is valid in a WorkItem `spec`.

### State machine override

To customize the state machine, put a project-specific file at
`context/state-machines/workitem.yaml`. The index MCP server will prefer the
project file over the processkit default. Transitions not listed in the
custom machine are rejected.

### Estimates

`spec.estimate` is intentionally freeform:

```yaml
estimate:
  unit: points
  value: 5
```

or

```yaml
estimate:
  unit: hours
  value: 4
  confidence: rough
```

processkit does not mandate a unit. Projects pick one and stick with it.

### Epics and hierarchy

An epic is just a WorkItem with `spec.type: epic` and many `children`.
Children link back via `parent`. There is no hard limit on nesting, but
flat → one level of epic → tasks is the common shape.

### Relationship to Discussions

When a WorkItem emerges from a discussion, link the discussion via
`spec.related_decisions` (if a decision was recorded) or mention it in the
body. The Discussion primitive (shipped later) captures multi-turn
conversations — a WorkItem is the action that comes out of one.

### Creating via MCP

In Phase 3, the `workitem-management` MCP server provides:

```
create_workitem(title, type, priority=None, assignee=None, parent=None, scope=None)
  -> {id, path, state}

transition_workitem(id, to_state, note=None)
  -> {ok, from_state, to_state}

query_workitems(state=None, assignee=None, type=None, scope=None, limit=50)
  -> [{id, title, state, assignee, priority}, ...]

link_workitems(from_id, to_id, relation)  # relation ∈ blocks|parent|related
  -> {ok}
```

Until then, agents perform the same operations by editing files directly
following this SKILL.md.

### File naming

Default: `context/workitems/BACK-<id>.md`. With shards:

```toml
[context.sharding.WorkItem]
scheme = "state"
pattern = "context/workitems/{state}/"
```

This moves files as they transition. Turned off by default — most projects
prefer flat.
