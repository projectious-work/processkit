---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260426_1214-SolidWolf-model-recommender-query-models
  created: '2026-04-26T12:14:38+00:00'
spec:
  title: model-recommender query_models() filter implementation for RoyalFern fields
    (jurisdiction, data_privacy, etc.)
  state: backlog
  type: story
  priority: medium
  description: 'RoyalFern (DEC-20260425_2256, shipped to main 4a0e1d6 + 8e914d7) added
    5 optional Model schema fields and backfilled them across all 34 model entities:

    - vendor_model_id (string)

    - jurisdiction (object: vendor_hq_country, applicable_legal_regimes, data_residency_regions)

    - data_privacy (object: dpa_available, data_retention_days, training_on_customer_data,
    pii_eligible, phi_hipaa_eligible, gdpr_eligible, sub_processors_url)

    - knowledge_cutoff (date)

    - latency_p50_ms (integer)


    The model-recommender SKILL.md was updated with structured-fields docs under the
    Governance dimension and 4 query_models() filter examples (e.g. phi_hipaa_eligible=true,
    jurisdiction.vendor_hq_country in ["US","EU"], data_privacy.training_on_customer_data="never",
    data_privacy.data_retention_days=0). HOWEVER the model-recommender MCP server''s
    query_models() tool does not yet implement filtering on any of these new fields
    — the docs describe behavior the server cannot deliver.


    SCOPE:

    - Extend query_models() (in the model-recommender MCP server) to accept filter
    kwargs covering each new field.

    - For object-typed fields (jurisdiction, data_privacy), accept dotted-path filters
    (e.g. jurisdiction__vendor_hq_country, data_privacy__phi_hipaa_eligible) following
    the existing sub_R/sub_E/sub_B convention.

    - For array-typed sub-fields (applicable_legal_regimes, data_residency_regions),
    accept list-membership filters (any-match semantics by default).

    - Update query_models() return shape to include the new fields where present.

    - Add unit tests covering each of the 4 SKILL.md examples end-to-end.

    - Do NOT change the SKILL.md docs — the docs are the spec, the implementation
    must match them.


    ACCEPTANCE:

    - All 4 query_models() filter examples in model-recommender SKILL.md execute successfully
    and return non-empty result sets where supporting models exist in context/models/.

    - Existing query_models() callers (no filter / score-only filters) continue to
    work unchanged.

    - pk-doctor passes.


    TARGETED FOR: v0.23.0 (per DEC-20260426_1214-SoundLark).'
---
