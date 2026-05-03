---
sidebar_position: 3
title: "Your First Entity"
---

# Your First Entity

Create your first WorkItem and see how processkit's entity format works.

## Prerequisites

- A project with processkit installed (see [Installing](./installing)).
- A package tier that includes `workitem-management`; `minimal` and
  higher tiers include it.

## Creating a WorkItem by hand

Write a file at `context/workitems/BACK-first-task.md`:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-first-task
  created: 2026-04-06T10:00:00Z
  labels:
    area: onboarding
spec:
  title: "Try out processkit"
  state: backlog
  type: task
  priority: medium
  description: "Walk through the processkit docs and create a few entities."
---

## Acceptance criteria

- [ ] Read the primitives overview
- [ ] Read the skills overview
- [ ] Create this first WorkItem
- [ ] Transition it to in-progress, then done
```

If your installer has a validation command, run it now. The file has the
core `apiVersion`, `kind`, `metadata.id`, and `spec` fields expected by
the WorkItem schema.

## Transitioning

When you start the task, update `spec.state`:

```yaml
spec:
  state: in-progress
  started_at: 2026-04-06T10:15:00Z
```

and ideally write a LogEntry to `context/logs/`:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-started-first-task
  created: 2026-04-06T10:15:00Z
spec:
  event_type: workitem.transitioned
  timestamp: 2026-04-06T10:15:00Z
  actor: ACTOR-you
  subject: BACK-first-task
  subject_kind: WorkItem
  summary: "Started work on BACK-first-task"
  details:
    from_state: backlog
    to_state: in-progress
---
```

When you finish the task, transition to `done` and write another LogEntry.

## Doing this via an agent

If you use an MCP-capable agent, ask:

> "Create a WorkItem for the task 'Walk through the processkit onboarding'
> and log its creation."

The `workitem-management` skill tells the agent what shape to produce.
The agent can call the `workitem-management` MCP server directly:

```
create_workitem(title="Walk through the processkit onboarding", type="task")
→ BACK-calm-fox
```

and the server validates the schema, writes the file, and logs the event
automatically.

## Next

- Explore the [primitives](../primitives/overview) to see the durable
  entity model.
- Browse the [skill catalog](../skills/overview) to see what else the
  agent can do.
