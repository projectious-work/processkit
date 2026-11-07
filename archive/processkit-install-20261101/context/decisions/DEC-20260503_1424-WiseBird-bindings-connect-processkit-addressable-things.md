---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260503_1424-WiseBird-bindings-connect-processkit-addressable-things
  created: '2026-05-03T14:24:43+00:00'
spec:
  title: Bindings connect processkit-addressable things
  state: accepted
  decision: A processkit Binding should connect processkit-addressable entities. JSON
    files, generated indexes, runtime projections, and external resources must not
    be canonical binding targets unless represented by a processkit entity, usually
    an Artifact pointer/spec.
  context: 'The model-assignment design exposed a general ambiguity: bindings were
    described as relationships between entities, but some targets were hidden inside
    MCP JSON. The user accepted the greenfield principle that bindings should stay
    simple and only connect addressable processkit things.'
  rationale: Keeping Binding endpoints entity-addressable preserves validation, migration,
    archiving, auditability, and a uniform mental model. When a relationship has its
    own scope, conditions, rank, validity window, policy, or rationale, use a Binding;
    when the relationship is a plain pointer, use frontmatter references.
  alternatives:
  - option: Allow binding targets to arbitrary registry IDs
    tradeoff: Flexible, but opaque and hard to migrate or validate consistently.
  - option: Create a primitive for every bindable concept
    tradeoff: Strong typing, but primitive sprawl.
  - option: Bind only processkit-addressable entities and use Artifact for specs/pointers
    tradeoff: Simple and uniform; some artifact subtype validation is needed in pk-doctor/schema
      tooling.
  consequences: Binding schemas should validate endpoints as processkit entities where
    possible. Non-processkit or generated targets should first be represented as Artifacts.
    model-assignment bindings should target Artifact(kind=model-spec), while model-recommender
    JSON should be treated as a projection/cache generated from or validated against
    those artifacts.
  decided_at: '2026-05-03T14:24:43+00:00'
---
