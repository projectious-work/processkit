---
sidebar_position: 1
title: "Overview"
---

# Processes — Overview

A **Process** is a declarative definition of a workflow: a sequence of
steps, the roles involved, the gates that must pass, and the definition
of done. processkit does NOT execute processes — agents and humans do.
processkit just defines them.

## Shape

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

## Formal process definitions

processkit ships the `process-management` skill that describes how to write
and read Process entities. Formal definitions for the common workflows
(`bug-fix`, `code-review`, `feature-development`, `release`) are planned
for a future release — they will appear as YAML files under
`context/processes/` once shipped.

## See also

- [`process-management` skill](https://github.com/projectious-work/processkit/blob/main/src/skills/process-management/SKILL.md)
- [Skills → Hierarchy](../skills/hierarchy)
