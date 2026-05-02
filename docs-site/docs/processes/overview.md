---
sidebar_position: 1
title: "Overview"
---

# Processes — Overview

A v1 **Process** was a declarative workflow definition: a sequence of
steps, roles, gates, and definition of done. In the
SmoothTiger/SmoothRiver v2 direction, processkit does not ship Process
as a first-class entity surface. A concrete run is a process-instance
WorkItem; a reusable definition is an Artifact; gates and bindings hold
the enforceable policy around the run.

processkit still does not execute workflows. Agents, humans, schedulers,
or CI systems perform the work and record progress through MCP tools.

## Shape

Legacy v1 shape:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Process
metadata:
  id: PROC-code-review
spec:
  name: code-review
  description: "Review a pull request before merge."
  triggers: [pr.opened, pr.review-requested]
  roles: [developer, reviewer]
  steps:
    - name: author-self-check
      role: developer
      uses_skill: code-review
    - name: peer-review
      role: reviewer
      uses_skill: code-review
      gates: [GATE-no-blocking-comments]
    - name: approval
      role: reviewer
      gates: [GATE-code-review-passed]
    - name: merge
      role: developer
      gates: [GATE-ci-passed, GATE-code-review-passed]
  definition_of_done: "PR merged with approval and CI green."
---
```

## v2 shape

For v2 documentation and checks, use:

- `WorkItem` with `spec.type: process-instance` for the run.
- `Artifact` for a process definition, referenced from the WorkItem.
- `Gate` for pass/fail checkpoints.
- `Binding` for policy, budget, scope, and time-window relationships.

`pk-doctor`'s `v2_contracts` check verifies that process-instance
WorkItems point at a definition.

## See also

- [`workitem-management` MCP server](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/workitem-management/mcp/)
- [`artifact-management` MCP server](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/artifact-management/mcp/)
- [Skills → Hierarchy](../skills/hierarchy)
