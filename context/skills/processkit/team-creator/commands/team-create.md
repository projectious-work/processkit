# Command: team-create

Full team derivation from scratch. Writes 8 Role + 8 Actor + 8 Binding
entities, rewrites `context/team/roster.md`, and emits a chartering
DecisionRecord that supersedes the prior team DecisionRecord.

## Syntax

```
team-create
  --subscription <provider>:<tier>   # e.g. anthropic:max-5x
  --providers <list|"any">           # comma-separated; "any" = all accessible
  --parallelism-cap <int>            # max clones per role, default 5
  --governance-floor <0-5>           # G-score floor, default 3
  [--weight-overrides <json>]        # {"C":0.60,"K":0.20,"L":0.10,"G":0.10}
  [--landscape <artifact-id>]        # default: latest landscape-summary artifact
  [--dry-run]                        # print plan; write nothing
```

## Process (sequential)

### Step 1 — Resolve landscape snapshot

Locate the landscape artifact:
1. If `--landscape <artifact-id>` is supplied, load that artifact.
2. Otherwise query artifact index for the latest artifact tagged
   `landscape-summary`. If none found, **abort** with:
   > "No landscape-summary artifact found. Run the Haiku landscape-
   > ingest task to produce an ART-*-LandscapeSnapshot artifact before
   > running team-create."
3. If the artifact is older than 90 days, emit a warning but continue.
   Record the artifact ID and its `created` date in the DecisionRecord
   `inputs_snapshot`.

### Step 2 — Query accessible models

```
model-recommender.check_availability()
model-recommender.query_models(
  providers=<--providers>,
  G_floor=<--governance-floor>,
  apply_user_filter=true
)
model-recommender.get_pricing(sort_by="value_score")
```

Filter out any model with availability != "operational" unless the
owner explicitly passes `--allow-degraded`.

### Step 3 — Apply tiering formula

For each accessible candidate model `m`:

1. Compute raw dimension values:
   - `C_raw(m)` = (swe_bench_verified + swe_bench_pro +
                   community_rating) / 3
   - `K_raw(m)` = 1 / (output_price_per_1M × quota_burn_vs_flagship)
   - `L_raw(m)` = output_tokens_per_sec
   - `G_raw(m)` = G-score from model-recommender (0–5 scale,
                  normalise to 0–1 by dividing by 5)

2. Min-max normalise each dimension across the full candidate set:
   `norm(x) = clamp((x - min) / (max - min), 0.01, 1.00)`

3. Compute TierScore using weights `{C, K, L, G}` (defaults or
   `--weight-overrides`):
   `TierScore(m) = C×norm(C) + K×norm(K) + L×norm(L) + G×norm(G)`

4. Classify:
   - TierScore ≥ 0.70 → **heavy**
   - TierScore 0.40–0.69 → **medium**
   - TierScore < 0.40 → **light**

5. Tier-collapse rule: if fewer than 3 distinct tiers result, promote
   the two highest-scoring light models to medium.

See `references/tiering-formula.md` for the full formula and worked
example.

### Step 4 — Map archetypes to candidates

For each of the 8 role archetypes (see `references/role-archetypes.md`):

1. Select the archetype's pinned tier.
2. From the models classified into that tier, pick the highest TierScore.
3. If preferred_providers are supplied and two models score within 0.05
   of each other, prefer the model from the preferred provider.
4. If the pinned tier has no candidates: apply the override-when rule
   from `references/role-archetypes.md`; if no override applies, fail
   with a clear message.

### Step 5 — Deactivate prior team (if re-running)

If `context/team/roster.md` already exists:

1. Parse the prior team's Actor and Binding IDs from roster.md.
2. For each prior Binding:
   `binding-management.end_binding(id, reason=
     "superseded by team-create run <ISO-timestamp>")`
3. For each prior Actor whose model ID does NOT appear in the new
   team assignments:
   `actor-profile.deactivate_actor(id)`
4. For each prior Actor whose model IS being re-assigned to the SAME
   role in the new team: REUSE the existing Actor ID — do not create
   a new Actor entity.

### Step 6 — Write entities

Skip if `--dry-run`.

For each of the 8 archetypes:
```
role-management.create_role(
  id=ROLE-<archetype-name>,
  name=<archetype-name>,
  description=<one-line responsibility>,
  responsibilities=[...],
  default_scope="permanent"
)
actor-profile.create_actor(
  id=ACTOR-<archetype-alias>,     # reuse existing if same model
  type="ai-agent",
  name=<model-display-name>,      # from model-recommender, not hardcoded
  active=true
)
binding-management.create_binding(
  type="role-assignment",
  subject=<ACTOR-id>,
  target=<ROLE-id>,
  valid_from=<today>,
  description="<model-id> fills <archetype-name>"
)
```

### Step 7 — Write roster.md

Write `context/team/roster.md` with:
- Narrative preamble (team charter, subscription, governance floor)
- Routing table: role → actor → model-id → tier → tier-score
- Parallelism cap and PM clone-cap note
- Weights used (from inputs or defaults)
- Landscape artifact ID and date
- DecisionRecord ID (written in step 8)

### Step 8 — Write chartering DecisionRecord

```
decision-record-write(
  title="Team composition — <subscription> — <date>",
  state="accepted",
  supersedes=[<prior-team-decisionrecord-id>],  # if re-running
  inputs_snapshot={
    subscription: ...,
    governance_floor: ...,
    parallelism_cap: ...,
    weights: {C, K, L, G},
    landscape_artifact: <ART-id>,
    landscape_artifact_date: <date>,
    tier_scores: {<model-id>: <score>, ...},
    weight_overrides_applied: <bool>
  }
)
```

The `inputs_snapshot.weights` block is the canonical weight store
that `team-rebalance` will read on future runs.

## Dry-run output format

```
=== team-create DRY RUN ===
Subscription: <value>   Governance floor: <value>
Landscape: <artifact-id> (<date>)
Weights: C=0.60 K=0.20 L=0.10 G=0.10

Candidate models scored:
  <model-id>  TierScore=0.92  → heavy
  <model-id>  TierScore=0.61  → medium
  ...

Role assignments:
  project-manager   → <model-id>  (heavy, score=0.92)
  senior-architect  → <model-id>  (heavy, score=0.87)
  ...

Entities to write (skipped in dry-run):
  8 Role entities, 8 Actor entities, 8 Binding entities
  context/team/roster.md
  DecisionRecord superseding <DEC-id>
===========================
```

## State side-effects (non-dry-run)

Creates: 8 Role + 8 Actor + 8 Binding entities, roster.md,
1 DecisionRecord. Deactivates: prior Bindings (end_binding) and
prior Actors not re-used.
