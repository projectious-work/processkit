---
sidebar_position: 3
title: "State Machines"
---

# State Machines

Primitives with lifecycle (WorkItem, DecisionRecord, Scope, Discussion)
are governed by state machines. processkit ships default machines that
projects can override.

## WorkItem default

```
backlog → in-progress → review → done
            ↓      ↑
          blocked ↑
            ↓      ↑
          backlog ←
(any state) → cancelled (terminal)
```

Source: [`src/primitives/state-machines/workitem.yaml`](https://github.com/projectious-work/processkit/blob/main/src/primitives/state-machines/workitem.yaml).

## DecisionRecord default

```
proposed → accepted → superseded (terminal)
    ↓
  rejected (terminal)
```

Source: [`src/primitives/state-machines/decisionrecord.yaml`](https://github.com/projectious-work/processkit/blob/main/src/primitives/state-machines/decisionrecord.yaml).

## Overriding a default

Projects override a default by placing a same-named file in their own
`context/state-machines/` directory. The index MCP server (v0.3.0) and any
validator prefer the project file over the processkit default.

Overrides must:
- Keep the same `initial` state (or migrate existing data).
- Not remove states that existing entities are currently in.
- Add new transitions only from states that already exist.

See the [`state-machine-management` skill](https://github.com/projectious-work/processkit/blob/main/src/skills/state-machine-management/SKILL.md)
for details.

## Multiple machines for one kind

You can ship multiple state machines for the same primitive kind by using
distinct `name`s. Entities opt into a specific machine via
`spec.state_machine: <name>`. Useful when the same kind has fundamentally
different lifecycles (e.g. a WorkItem with `bug-lifecycle` vs
`story-lifecycle`).
