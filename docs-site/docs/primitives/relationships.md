---
sidebar_position: 4
title: "Relationships"
---

# Relationships — Cross-References and Bindings

processkit expresses relationships between entities two ways:

1. **Cross-references** — lightweight fields in frontmatter
2. **Bindings** — first-class entities with their own files

Pick the right one based on what the relationship needs.

## The rule

> If a relationship has **scope**, **time**, or **its own attributes** → Binding.
> Otherwise → cross-reference.

## Cross-reference examples

```yaml
# In a WorkItem
spec:
  blocks: [BACK-swift-oak]
  blocked_by: [BACK-calm-fox]
  related_decisions: [DEC-023]
  parent: BACK-epic-lint
```

Conventional field names:

| Field               | Meaning                                  |
|---------------------|------------------------------------------|
| `parent`            | This entity is a child of another        |
| `children`          | This entity has sub-items                |
| `blocks`            | This entity blocks others until resolved |
| `blocked_by`        | This entity is blocked by others         |
| `related_workitems` | Typed relationship to WorkItems          |
| `related_decisions` | Typed relationship to DecisionRecords    |
| `supersedes`        | This entity replaces an older one        |
| `superseded_by`     | This entity has been replaced            |
| `implements`        | This entity implements a decision        |

See the [`cross-reference-management` skill](https://github.com/projectious-work/processkit/blob/main/src/context/skills/processkit/cross-reference-management/SKILL.md)
for the full list and conventions.

## Binding examples

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-bright-falcon
  created: 2026-04-06T00:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-tech-lead
  scope: SCOPE-project-x
  valid_from: 2026-01-01
  valid_until: 2026-12-31
---
```

Conventional binding types:

| type                  | subject kind | target kind |
|-----------------------|--------------|-------------|
| `role-assignment`     | Actor        | Role        |
| `work-assignment`     | WorkItem     | Actor       |
| `workitem-gate`       | WorkItem     | Gate        |
| `scope-gate`          | Scope        | Gate        |
| `time-window`         | any          | any         |
| `budget-application`  | Artifact     | WorkItem/Scope |

Legacy `process-gate`, `process-scope`, and `schedule-scope` Bindings
are v1 migration inputs only. New v2 relationships should target the
concrete WorkItem, Scope, Artifact, or Gate being governed.

See the [`binding-management` skill](https://github.com/projectious-work/processkit/blob/main/src/context/skills/processkit/binding-management/SKILL.md)
for the full spec.

## Why Binding was generalized from RoleBinding

DISC-002 §11 analyzes the decision to generalize the 18th primitive from
RoleBinding to Binding. The short version: the indirection pattern applies
to at least 7 relationship types across processkit, and one generalized
primitive is cleaner than multiplying specific bindings. See
[DEC-023](https://github.com/projectious-work/aibox/blob/main/context/DECISIONS.md)
in the aibox repo.
