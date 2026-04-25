---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_2256-RoyalFern-model-schema-add-jurisdiction
  created: '2026-04-25T22:56:57+00:00'
  updated: '2026-04-25T22:57:07+00:00'
spec:
  title: 'Model schema: add jurisdiction, data_privacy, latency_p50_ms, knowledge_cutoff,
    vendor_model_id'
  state: in-progress
  type: story
  priority: high
  description: '## What


    Add five structured fields to `Model.spec_schema.versions[]` and backfill the
    18 live model entities under `context/models/`:


    - `jurisdiction` — object: `vendor_hq_country` (ISO-3166), `applicable_legal_regimes`
    (array of slugs like `EU-GDPR`, `US-CLOUD-Act`, `CN-DSL`), `data_residency_regions`
    (array of region codes the vendor offers).

    - `data_privacy` — object: `dpa_available` (boolean or url), `data_retention_days`
    (integer or `"zero"`), `training_on_customer_data` (enum: `never|opt-in|opt-out|always|unknown`),
    `pii_eligible` (bool), `phi_hipaa_eligible` (bool), `gdpr_eligible` (bool), `sub_processors_url`
    (uri).

    - `latency_p50_ms` — integer, ballpark median first-token / completion latency
    to complement the qualitative `dimensions.speed` 1–5.

    - `knowledge_cutoff` — date, currently only inferable from `rationale` prose.

    - `vendor_model_id` — string, the actual SDK model string (e.g. `claude-opus-4-7-20251031`)
    — today only implied by `family + version_id`.


    ## Why


    Today jurisdiction and data-privacy posture are encoded as a single `dimensions.governance`
    1–5 score plus optional free-text `governance_warning` (only DeepSeek has it).
    That is lossy — a project that needs HIPAA-eligible models cannot filter, and
    the model-recommender SKILL.md docs already describe these concepts under the
    G dimension but with no schema fields to back them. Surfacing them structurally
    lets `query_models()` filter explicitly instead of via the score.


    Latency, knowledge-cutoff and the vendor model id were also flagged as gaps in
    the same audit.


    ## Scope


    1. Update `src/context/schemas/model.yaml` spec_schema with the five new fields
    (all optional, additive — backwards compatible).

    2. Backfill all 18 files under `context/models/` with best-effort values from
    public vendor docs and the existing `governance_warning` prose. Use `unknown`
    / omit for fields where the vendor does not publish a clear value.

    3. Mirror src→context, regenerate `.processkit-mcp-manifest.json` if needed (no
    MCP config change expected here, but check), run drift guard, run pk-doctor.

    4. Update `model-recommender` SKILL.md to document the new filter dimensions and
    how `query_models()` can filter on them. (MCP server tool extension is out of
    scope for this WI — separate follow-up if needed.)

    5. Note: this is an additive, optional schema change — no Migration entity required
    (no breaking change to existing data).


    ## Done when


    - Schema parses; `pk-doctor schema_filename` clean across all 18 model files.

    - All 18 model files have at least `jurisdiction.vendor_hq_country` populated
    (the easy one) and `data_privacy.training_on_customer_data` populated (even if
    `unknown`).

    - Drift guard clean, manifest regenerated if needed.

    - SKILL.md mentions the new fields in the Governance dimension section.


    ## Origin


    Filed from owner audit on 2026-04-26. Owner explicitly requested jurisdiction
    + data_privacy be added to the characteristics list. Other three fields (latency_p50_ms,
    knowledge_cutoff, vendor_model_id) bundled because they were flagged in the same
    audit and are cheap to add in one schema migration cycle.'
  started_at: '2026-04-25T22:57:07+00:00'
---
