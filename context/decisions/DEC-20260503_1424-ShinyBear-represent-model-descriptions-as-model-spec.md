---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260503_1424-ShinyBear-represent-model-descriptions-as-model-spec
  created: '2026-05-03T14:24:35+00:00'
spec:
  title: Represent model descriptions as model-spec artifacts
  state: accepted
  decision: Represent model descriptions as processkit Artifacts with spec.kind=model-spec,
    not as a separate Model primitive and not as hidden canonical rows inside model-recommender
    JSON.
  context: The previous Model primitive was removed from the v0.25.x deliverable,
    but making model-assignment bindings point directly at entries inside model-recommender
    JSON made binding semantics opaque. The user accepted the greenfield recommendation
    to keep bindings simple by making model descriptions addressable processkit artifacts.
  rationale: Artifact(kind=model-spec) keeps model descriptions processkit-addressable,
    migratable, archivable, auditable, and bindable without adding a new primitive.
    The model-recommender JSON can still exist as a generated runtime projection/cache
    for fast routing, but not as the canonical binding target.
  alternatives:
  - option: Restore Model as a primitive
    tradeoff: Strong typing, but adds a primitive whose lifecycle does not justify
      the extra schema and tooling surface.
  - option: Keep JSON as canonical source
    tradeoff: Fast for routing, but makes bindings point at non-entity implementation
      details and complicates migration/doctor validation.
  - option: Use Artifact(kind=model-spec) as canonical source
    tradeoff: Uses existing primitive and keeps bindings simple; requires projection
      tooling for model-recommender JSON.
  consequences: processkit should ship model-spec artifacts, change model-assignment
    bindings to target ART-* model-spec artifacts, and validate or generate the recommender
    JSON from those artifacts. Derived-project migrations should convert old context/models/MODEL-*.md
    files into model-spec artifacts and rewrite bindings away from MODEL-* targets.
  decided_at: '2026-05-03T14:24:35+00:00'
---
