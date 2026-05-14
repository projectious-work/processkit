---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260514_0841-FairOasis-use-rag-assisted-allocation-for-semantic
  created: '2026-05-14T08:41:12+00:00'
spec:
  title: Use RAG-assisted allocation for semantic ID palettes
  state: accepted
  decision: processkit ID allocation will use RAG-style semantic retrieval to select
    and rank vocabulary palettes, while keeping the allocator constraint-based and
    deterministic. The implementation should reuse the existing index-management SQLite/sqlite-vec
    infrastructure with a separate ID vocabulary namespace or table set instead of
    adding a disconnected vector database.
  context: The accepted vocabulary design introduces tagged word pools and high-volume
    three-token modes. The follow-up architecture question asked whether embeddings/RAG
    should group related items by category or content, inspired by what3words separation
    and Plus Code locality. The repository already has sqlite-vec-backed semantic_chunks/entity_vec
    tables and hybrid search for processkit entities, so the architectural fit is
    to extend the existing semantic index rather than create a parallel database.
  rationale: Embeddings are useful for selecting nearby categories and related prior
    entities, but they must not be the source of uniqueness. The allocator must enforce
    global lexical-token reservation, capacity limits, process-word blocks, and confusability
    rules. Keeping ID vectors in the existing index-management database preserves
    one operational indexing surface and lets pk-doctor validate semantic health in
    one place.
  alternatives:
  - option: Create a separate sqlite-vec database for ID allocation
    rationale: Not chosen because it duplicates operational health checks and splits
      semantic indexing across stores without clear benefit at processkit's current
      scale.
  - option: Let embeddings directly generate or encode IDs
    rationale: Not chosen because embeddings are approximate and cannot guarantee
      uniqueness, stable allocation, or shorthand disambiguation.
  - option: Use only static per-kind category palettes
    rationale: Not chosen because it ignores content-level grouping and cannot adapt
      to project-specific semantics.
  - option: Adopt hierarchical locality in the visible ID token
    rationale: Not chosen because human mnemonic IDs should remain distinct; locality
      belongs in retrieval metadata, not in visually similar identifiers.
  consequences: Implementation should add ID vocabulary metadata and vector rows in
    a separate namespace/table, build an ID intent document from entity kind/title/labels/stable
    subtype/slug summary, retrieve category and related-entity hints, score candidate
    IDs with hard constraints, and atomically reserve the selected lexical token.
    Similar content may draw from similar palettes, but similar-looking or similar-sounding
    ID tokens should be separated to avoid conversational ambiguity.
  decided_at: '2026-05-14T08:41:12+00:00'
---
