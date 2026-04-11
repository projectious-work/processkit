---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_1755-SmartPanda-architectural-model-class-assignment
  created: '2026-04-11T17:55:16+00:00'
  labels:
    component: architecture
    scope: cross-skill
    track: routing
spec:
  title: 'Architectural: model-class assignment for processkit skills (fast/standard/powerful
    routing)'
  state: backlog
  type: epic
  priority: low
  description: "Define a `routing_model_class` convention that any processkit skill\
    \ or MCP\nserver can declare to indicate the minimum model capability tier required.\n\
    \n## Motivation\n\nThe cheap-model escalation pattern (task-router v0.2) requires\
    \ knowing which\nmodel to use per routing stage. Currently there is no processkit-level\
    \ concept\nof model tiers — each derived project hard-codes model names. This\
    \ creates\ntight coupling between skill logic and provider-specific model IDs.\n\
    \n## Proposed convention\n\n1. Skill frontmatter gains an optional field:\n  \
    \ ```yaml\n   metadata:\n     processkit:\n       routing_model_class: fast |\
    \ standard | powerful\n   ```\n   Default: `standard`.\n\n2. `settings.toml` in\
    \ derived projects maps classes to provider model IDs:\n   ```toml\n   [model_classes]\n\
    \   fast     = \"claude-haiku-4-5-20251001\"\n   standard = \"claude-sonnet-4-6\"\
    \n   powerful = \"claude-opus-4-6\"\n   ```\n\n3. `task-router` (and any skill\
    \ that invokes a sub-agent) reads\n   `model_classes.{class}` to select the model\
    \ for its operation.\n\n## Scope\n\n- Applies to all skills that invoke models\
    \ directly\n- Needs a companion aibox issue to propagate settings.toml model_classes\n\
    \  to derived project configurations at install time\n- Needs `model-recommender`\
    \ to expose `get_model_for_class(class)` tool\n\n## Dependencies\n\nBlocks: task-router\
    \ v0.2 cheap-model escalation"
---
