---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260411_1755-SmartPanda-architectural-model-class-assignment
  created: '2026-04-11T17:55:16+00:00'
  labels:
    component: architecture
    scope: cross-skill
    track: routing
  updated: '2026-04-30T11:04:21+00:00'
spec:
  title: 'Architectural: model-class assignment for processkit skills (fast/standard/powerful
    routing)'
  state: done
  type: epic
  priority: low
  description: |
    Define a `routing_model_class` convention that any processkit skill or MCP
    server can declare to indicate the minimum model capability tier required.

    ## Motivation

    The cheap-model escalation pattern (task-router v0.2) requires knowing which
    model to use per routing stage. Currently there is no processkit-level concept
    of model tiers — each derived project hard-codes model names. This creates
    tight coupling between skill logic and provider-specific model IDs.

    ## Proposed convention

    1. Skill frontmatter gains an optional field:
       ```yaml
       metadata:
         processkit:
           routing_model_class: fast | standard | powerful
       ```
       Default: `standard`.

    2. `settings.toml` in derived projects maps classes to provider model IDs:
       ```toml
       [model_classes]
       fast     = "claude-haiku-4-5-20251001"
       standard = "claude-sonnet-4-6"
       powerful = "claude-opus-4-6"
       ```

    3. `task-router` (and any skill that invokes a sub-agent) reads
       `model_classes.{class}` to select the model for its operation.

    ## Scope

    - Applies to all skills that invoke models directly
    - Needs a companion aibox issue to propagate settings.toml model_classes
      to derived project configurations at install time
    - Needs `model-recommender` to expose `get_model_for_class(class)` tool

    ## Dependencies

    Blocks: task-router v0.2 cheap-model escalation
  started_at: '2026-04-30T11:03:42+00:00'
  completed_at: '2026-04-30T11:04:21+00:00'
---

## Transition note (2026-04-30T11:03:42+00:00)

Implemented provider-neutral model class coverage: Model schema fields, model-characteristics reference, user config model_classes, get_model_for_class(), tests, and docs.


## Transition note (2026-04-30T11:04:06+00:00)

Model-class architecture implemented and validated; moving through review state for completion.


## Transition note (2026-04-30T11:04:21+00:00)

Completed: provider-neutral model classes are represented in schema/config/docs and exposed via get_model_for_class(), with focused tests passing.
