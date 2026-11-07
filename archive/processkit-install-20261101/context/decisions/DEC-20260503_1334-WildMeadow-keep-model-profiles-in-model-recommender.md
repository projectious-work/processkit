---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260503_1334-WildMeadow-keep-model-profiles-in-model-recommender
  created: '2026-05-03T13:34:21+00:00'
  updated: '2026-05-03T13:40:10+00:00'
spec:
  title: Keep model profiles in model-recommender JSON
  state: superseded
  decision: Use the model-recommender JSON roster/profile data as the authoritative
    representation of model status, capabilities, and suitability instead of restoring
    first-class Model entities as the runtime source of truth.
  context: The v0.25.x deliverable no longer ships src/context/models/ or model.yaml,
    while prior decisions expected first-class Model artifacts. The user confirmed
    it is acceptable to keep model status in JSON, provided migrations and pk-doctor
    detect the change for derived projects that still have old model artifacts.
  rationale: The recommender JSON is the operational source consumed by model routing.
    Keeping it authoritative avoids duplicating model metadata across entities and
    JSON, but requires explicit migration/drift checks so derived projects remove
    obsolete model artifacts and bindings stay consistent.
  alternatives:
  - option: Restore first-class Model entities as authoritative artifacts
    tradeoff: More natural for processkit Binding targets, but duplicates recommender
      data and risks runtime drift.
  - option: Keep JSON only with opaque string bindings
    tradeoff: Simple implementation, but weak domain modeling and harder for pk-doctor
      to validate meaningfully.
  - option: Keep JSON authoritative and expose stable model-profile target IDs or
      generated artifacts
    tradeoff: Preserves one operational source while giving bindings a durable processkit-visible
      target contract.
  consequences: aibox migrations should be the first line of defense for model representation
    changes between releases. pk-doctor must add fallback checks that detect stale
    model artifacts/schemas and binding targets inconsistent with the JSON roster.
    Binding semantics need a published-language target for JSON-backed model profiles
    rather than opaque hidden references.
  decided_at: '2026-05-03T13:34:21+00:00'
---
