---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260422_0231-WarmHare-v0-19-0-phase
  created: '2026-04-22T02:31:45+00:00'
  updated: '2026-04-22T06:07:14+00:00'
spec:
  title: v0.19.0 Phase 3 — Extract models from model_scores.json into context/models/
    artifacts
  state: done
  type: task
  priority: high
  assignee: ACTOR-developer
  description: |
    Models become first-class entities, one file per (provider, family), versions nested.

    **Migration**
    - Source: `context/skills/processkit/model-recommender/mcp/model_scores.json` (~45 entries)
    - Destination: `context/models/<provider>-<family>.yaml` (~18-20 family files after grouping)
    - Each file: spec per new model.yaml schema (Phase 1) with all historical versions nested under versions[]
    - Write an idempotent migration script so it can be rerun

    **Update model-recommender**
    - Read source of truth from `context/models/` entity files (not the monolithic JSON)
    - The old JSON becomes a compiled cache emitted by a build step (or deleted outright if not needed)
    - Tools that reference models (list_models, get_profile, compare_models, etc.) keep their interfaces; internal loader swaps

    **Done when**
    - `context/models/` populated with family+versions files.
    - model-recommender reads from artifacts, not JSON.
    - pk-doctor schema check clean on all model files.
    - Dual-tree mirror clean.
  started_at: '2026-04-22T05:35:29+00:00'
  completed_at: '2026-04-22T06:07:14+00:00'
---

## Transition note (2026-04-22T05:35:29+00:00)

Delegated to background agent for migration script + ~20 model family artifacts under context/models/.


## Transition note (2026-04-22T06:07:08+00:00)

Model extraction complete: 34 family artifacts under context/models/, migrate_models.py + 20 pytest tests passing, model-recommender loader prefers artifacts, dual-tree clean.
