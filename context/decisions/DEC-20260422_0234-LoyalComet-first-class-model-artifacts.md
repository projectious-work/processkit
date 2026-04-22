---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260422_0234-LoyalComet-first-class-model-artifacts
  created: '2026-04-22T02:34:43+00:00'
spec:
  title: First-class Model artifacts, T-shirt capacity tiers, named efforts, and binding-based
    role↔model routing
  state: accepted
  decision: 'Promote models to first-class processkit entities under `context/models/`,
    one file per `(provider, family)` with all historical versions nested under a
    `versions[]` array. Adopt the new `model.yaml` schema with dimensions (R/E/S/B/L/G),
    efforts_supported, modalities, access_tier, pricing per version, and an `equivalent_tier`
    field that maps each model to a provider-neutral capacity tier. Adopt T-shirt-size
    naming for capacity tiers: `xs / s / m / l / xl / xxl`, extensible in both directions
    by convention (xxxs, xxxl, …) as generations change. Adopt named efforts `[none,
    low, medium, high, extra-high, max]` with `extra-high → xhigh` aliasing at the
    Anthropic provider adapter boundary. Replace `role.spec.model_profiles[]` with
    a new binding type `model-assignment` whose subject may be Role, TeamMember, or
    ProjectScope and whose conditions encode seniority, rank, effort_floor/ceiling,
    version_pin, blocked, cost_bias, and provider_preference. Resolution uses the
    8-layer precedence ladder (task-pin → team-member pref → project veto → capability
    filter → role+seniority ranking → role default ranking → project bias → shim fallback).
    Ship a default binding pack for starter projects; keep a thin `role.default_model`
    shim as explicit last-resort fallback.'
  context: Currently ~45 models live inside a monolithic `model_scores.json` at `context/skills/processkit/model-recommender/mcp/`.
    Edits bypass schema validation, event-log auto-entry, and the entity-per-file
    pattern every other primitive follows. Role→Model linkage is embedded as `model_profiles[]`
    arrays inside role YAML, which couples model-catalog changes to role-file edits.
    The binding-management skill is already live and already handles role-assignment
    bindings — the mechanism for model-role relationships exists, it's just not used.
    Provider-neutral naming is required to avoid locking into any one vendor's model
    family naming and to allow capability bands to grow both stronger and weaker as
    the market evolves.
  rationale: (1) Model entities get the same auditability, schema validation, and
    event-log provenance as every other processkit primitive. (2) One file per (provider,
    family) with nested versions matches how humans reason about "Claude Opus 4.6
    vs 4.7" as the same product evolving, and collapses ~45 JSON entries into ~18-20
    files. (3) T-shirt sizes (xs/s/m/l/xl/xxl) are abstract enough to age well, ordinal-obvious,
    universally understood, and extend trivially in both directions. Each model declares
    its own `equivalent_tier`, so re-tiering a generation shift is a model-file edit,
    not a naming refactor. (4) Efforts list `[none, low, medium, high, extra-high,
    max]` spans the actual usage range with headroom for future providers beyond current
    maxima. (5) Replacing embedded model_profiles with bindings unifies three previously-separate
    layers (catalog / project prefs / role defaults / team-member overrides) under
    one mechanism — bindings with different subject types. (6) The 8-layer resolution
    precedence provides clear, testable, cache-able routing with an explain-mode trace
    for debugging. (7) Shim fallback + default binding pack give ergonomic zero-config
    defaults while keeping the mechanism strict.
  alternatives:
  - option: Keep model_scores.json as source of truth
    rejected_because: Inconsistent with processkit's entity-per-file pattern; no schema
      validation; no event-log provenance.
  - option: One file per (provider, family, version) — ~45+ files
    rejected_because: Full provenance per entity but duplicates family-level metadata
      across versions; harder to reason about family evolution.
  - option: Capability bands (compact/balanced/advanced/flagship/frontier) instead
      of T-shirt sizes
    rejected_because: Labels age poorly (today's `flagship` is tomorrow's mid-tier);
      T-shirt sizes stay semantically stable.
  - option: Numeric tier names (m1..m5)
    rejected_because: Lower readability; T-shirt sizes have the same ordinal property
      with better mnemonic.
  - option: Keep model_profiles[] embedded in roles
    rejected_because: Couples model-catalog updates to role-file edits; bindings give
      temporal, scoped, auditable linkage.
  - option: No shim fallback — strict bindings only
    rejected_because: Adds ceremony to trivial cases without meaningful safety gain;
      shim + bindings-override is the pragmatic middle.
  - option: Fewer precedence layers (e.g., skip project-bias step 7)
    rejected_because: Cost and provider preference are legitimate project concerns;
      collapsing them into role+seniority bindings would bloat those bindings with
      project-specific logic.
  consequences: 'Breaking change: `role.spec.model_profiles[]` removed; `model_scores.json`
    becomes a compiled cache or is removed outright. `context/models/` directory added
    as first-class entity root. model-recommender''s internal loader swaps; external
    tool interfaces (list_models, get_profile, compare_models, query_models, get_pricing,
    check_availability) remain stable. binding-management extended with `model-assignment`
    type. New CLI: `pk explain-routing ROLE@SENIORITY` using resolve_bindings_for''s
    explain mode. Ship a default binding pack under `model-recommender/default-bindings/`.
    pk-doctor adds drift checks for model artifacts. Provider-adapter layer gains
    effort-aliasing (extra-high → xhigh for Anthropic).'
  deciders:
  - ACTOR-20260421_0144-ThriftyOtter-owner
  related_workitems:
  - BACK-20260422_0231-WildSeal-v0-19-0-phase
  - BACK-20260422_0231-WarmHare-v0-19-0-phase
  - BACK-20260422_0231-HonestFjord-v0-19-0-phase
  - BACK-20260422_0232-ShinyIvy-v0-19-0-phase
  - BACK-20260422_0232-CuriousOwl-v0-19-0-phase
  decided_at: '2026-04-22T02:34:43+00:00'
---
