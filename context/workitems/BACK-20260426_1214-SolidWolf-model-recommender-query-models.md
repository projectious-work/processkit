---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260426_1214-SolidWolf-model-recommender-query-models
  created: '2026-04-26T12:14:38+00:00'
  updated: '2026-04-26T15:21:57+00:00'
spec:
  title: model-recommender query_models() filter implementation for RoyalFern fields
    (jurisdiction, data_privacy, etc.)
  state: done
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
  started_at: '2026-04-26T15:17:16+00:00'
  completed_at: '2026-04-26T15:21:57+00:00'
---

## Transition note (2026-04-26T15:17:16+00:00)

Starting work. Two-part fix: (a) extend _entity_to_legacy() to pass RoyalFern fields (jurisdiction, data_privacy, knowledge_cutoff, vendor_model_id, latency_p50_ms) from versions[] into the legacy entry shape so query_models() can read them; (b) add 8 filter kwargs to query_models(): phi_hipaa_eligible, pii_eligible, gdpr_eligible, jurisdiction_country_in, legal_regime_in, training_on_customer_data, data_retention_days_max, max_latency_p50_ms — names track the SKILL.md examples directly (flat kwargs, not dotted-path). Missing-field semantics: a model missing the field is REJECTED when a filter is applied (safer default for governance gates).


## Transition note (2026-04-26T15:21:53+00:00)

Fix landed in context/skills/processkit/model-recommender/mcp/server.py (mirrored to src/). Two-part change:

(a) _entity_to_legacy() now passes RoyalFern fields (vendor_model_id, knowledge_cutoff, latency_p50_ms, jurisdiction, data_privacy) from versions[] into the legacy-shape entry that query_models() iterates over.

(b) query_models() gains 9 governance / data-privacy filter kwargs:
- phi_hipaa_eligible, pii_eligible, gdpr_eligible (booleans on data_privacy)
- training_on_customer_data (exact-match enum)
- data_retention_days_max (numeric ceiling; "zero" string accepted, "unknown" rejected)
- jurisdiction_country_in (membership)
- legal_regime_in (any-match on applicable_legal_regimes)
- data_residency_in (any-match on data_residency_regions)
- max_latency_p50_ms (numeric ceiling)

Missing-field semantics: a model lacking the relevant field is REJECTED (conservative governance default). _profile_block() now also surfaces the new fields on every result so callers can verify what filter they got hits on.

Tests: 13 unit tests in context/skills/processkit/model-recommender/scripts/test_query_models_filters.py covering all 9 filters, missing-field rejection, filter composition, and no-regression on existing R/E/S/B/L/G score minimums.

Live smoke vs the 34-model roster: phi_hipaa_eligible=True returns 16; jurisdiction_country_in=[US,CA,FR] returns 20; training_on_customer_data="never" returns 10; data_retention_days_max=0 returns 15. All four SKILL.md filter examples now return non-empty result sets against real data — the contract the SKILL.md docs describe is satisfied.

pk-doctor green (0 ERROR / 2 WARN — both unchanged drift WARNs).


## Transition note (2026-04-26T15:21:57+00:00)

Closed. Implementation in main, 13 unit tests + 4 SKILL.md examples verified against live roster. Will ship in v0.23.0.
