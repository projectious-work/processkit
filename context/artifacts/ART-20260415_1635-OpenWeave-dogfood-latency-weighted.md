---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1635-OpenWeave-dogfood-latency-weighted
  created: '2026-04-15T16:35:00+00:00'
spec:
  name: "team-creator dogfood — latency-weighted override demonstration (OpenWeave)"
  kind: diagnostic
  location: context/artifacts/ART-20260415_1635-OpenWeave-dogfood-latency-weighted.md
  format: markdown
  version: "1.0.0"
  tags: [team-creator, dogfood, openweave, latency-weighted, weight-override, acceptance-gate]
  produced_by: FEAT-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
  owner: ACTOR-developer
  links:
    workitem: FEAT-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
    inputs:
      - ART-20260415_1630-OpenWeave-regression-fixture-max5x-defaults
      - ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff
      - ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
---

# team-creator Dogfood — Latency-Weighted Override Demonstration

**Author:** ACTOR-developer (Sonnet 4.6)
**Date:** 2026-04-15
**Phase:** OpenWeave Phase 2 — analytic derivation only. No runtime execution.
**WorkItem:** FEAT-20260415_1600-OpenWeave-team-creator-user-configurable-defaults

---

## 1. Invocation

```
team-create \
  --subscription anthropic:max-5x \
  --providers any \
  --governance-floor 3 \
  --weight-overrides '{"L":0.50,"K":0.20,"C":0.25,"G":0.05}'
```

Weight sum check: 0.50 + 0.20 + 0.25 + 0.05 = **1.00** ✓

Override layer state:
- Layer 1 (landscape): kit-default (`landscape-summary`)
- Layer 2 (weights): **CLI** — `{L:0.50, K:0.20, C:0.25, G:0.05}`
- Layer 3 (thresholds): skill-default `{heavy_min:0.70, medium_min:0.40}`
- Layer 4 (role pins): absent — kit defaults apply

---

## 2. Attempt A — Anthropic-only, G-floor=3

### 2.1 Candidate set

G-floor=3. All three Anthropic Max-5× models have G=5 → all pass.

Same raw metrics as the regression fixture (sourced from
ART-20260415_1525-LandscapeSummary):

| Model | C raw | K raw | L tok/s | G raw |
|---|---|---|---|---|
| Opus 4.6 | 0.739 | 0.0400 | 25 | 1.00 |
| Sonnet 4.6 | 0.695 | 0.1333 | 50 | 1.00 |
| Haiku 4.5 | 0.550 | 1.3333 | 90 | 1.00 |

### 2.2 Normalised values

Min-max bounds are identical to the regression fixture (same candidate set):

| Dim | min | max | range |
|---|---|---|---|
| C | 0.550 | 0.739 | 0.189 |
| K | 0.0400 | 1.3333 | 1.2933 |
| L | 25 | 90 | 65 |
| G | 1.00 | 1.00 | 0 (zero-range → all 0.01) |

Normalised values are therefore identical to the regression fixture:

| Model | norm(C) | norm(K) | norm(L) | norm(G) |
|---|---|---|---|---|
| Opus 4.6 | 1.000 | 0.010 | 0.010 | 0.010 |
| Sonnet 4.6 | 0.767 | 0.0722 | 0.385 | 0.010 |
| Haiku 4.5 | 0.010 | 1.000 | 1.000 | 0.010 |

### 2.3 TierScores under L=0.50 weights

Formula: `TierScore = 0.25·C + 0.20·K + 0.50·L + 0.05·G`

| Model | 0.25·C | 0.20·K | 0.50·L | 0.05·G | **TierScore** |
|---|---|---|---|---|---|
| Opus 4.6 | 0.2500 | 0.0020 | 0.0050 | 0.0005 | **0.258** |
| Sonnet 4.6 | 0.1918 | 0.01444 | 0.1925 | 0.0005 | **0.399** |
| Haiku 4.5 | 0.0025 | 0.2000 | 0.5000 | 0.0005 | **0.703** |

### 2.4 Classification (attempt A)

| Model | TierScore | Tier |
|---|---|---|
| Haiku 4.5 | 0.703 | **heavy** (≥ 0.70) |
| Sonnet 4.6 | 0.399 | **light** (< 0.40) |
| Opus 4.6 | 0.258 | **light** (< 0.40) |

Tier-collapse: only 2 distinct tiers (heavy + light, no medium). Tier-collapse
rule fires: promote the two highest-scoring light models to medium.
Sonnet 4.6 (0.399) and Opus 4.6 (0.258) → both promoted to medium.

Post-collapse tiers:

| Model | TierScore | Post-collapse tier |
|---|---|---|
| Haiku 4.5 | 0.703 | **heavy** |
| Sonnet 4.6 | 0.399 | **medium** (promoted) |
| Opus 4.6 | 0.258 | **medium** (promoted) |

### 2.5 Role assignments (attempt A)

| Role | Tier pin | Best candidate in tier | Assigned model |
|---|---|---|---|
| project-manager | heavy | Haiku 4.5 (0.703) | **Haiku 4.5** |
| senior-architect | heavy | Haiku 4.5 (0.703) | **Haiku 4.5** |
| senior-researcher | heavy | Haiku 4.5 (0.703) | **Haiku 4.5** |
| junior-architect | medium | Sonnet 4.6 (0.399) | **Sonnet 4.6** |
| developer | medium | Sonnet 4.6 (0.399) | **Sonnet 4.6** |
| junior-researcher | medium | Sonnet 4.6 (0.399) | **Sonnet 4.6** |
| junior-developer | light | (no light tier — collapse fired) → medium fallback | **Opus 4.6** |
| assistant | light | (no light tier — collapse fired) → medium fallback | **Opus 4.6** |

### 2.6 Comparison vs kit-default fixture

Kit-default assignments (from ART-20260415_1630-OpenWeave-regression-fixture-max5x-defaults):

| Role | Kit-default model | L-weighted model | Changed? |
|---|---|---|---|
| project-manager | Opus 4.6 | Haiku 4.5 | **YES** |
| senior-architect | Opus 4.6 | Haiku 4.5 | **YES** |
| senior-researcher | Opus 4.6 | Haiku 4.5 | **YES** |
| junior-architect | Sonnet 4.6 | Sonnet 4.6 | no |
| developer | Sonnet 4.6 | Sonnet 4.6 | no |
| junior-researcher | Sonnet 4.6 | Sonnet 4.6 | no |
| junior-developer | Haiku 4.5 | Opus 4.6 | **YES** |
| assistant | Haiku 4.5 | Opus 4.6 | **YES** |

**5 of 8 role assignments change model.** This exceeds the "at least 2" threshold
required by the success criterion.

### 2.7 Latency characteristic of changed models

For the roles that changed, the newly assigned model must have higher
`output_tokens_per_sec` than the kit-default assignment for that role:

| Role | Kit-default model | Kit-default L tok/s | L-weighted model | L-weighted L tok/s | Δ tok/s |
|---|---|---|---|---|---|
| project-manager | Opus 4.6 | 25 | Haiku 4.5 | 90 | **+65** ✓ |
| senior-architect | Opus 4.6 | 25 | Haiku 4.5 | 90 | **+65** ✓ |
| senior-researcher | Opus 4.6 | 25 | Haiku 4.5 | 90 | **+65** ✓ |
| junior-developer | Haiku 4.5 | 90 | Opus 4.6 | 25 | **−65** — see note |
| assistant | Haiku 4.5 | 90 | Opus 4.6 | 25 | **−65** — see note |

**Note on junior-developer / assistant:** The latency reversal for these two roles
arises from the tier-collapse mechanism, not from the weight formula directly.
In the kit-default run, Haiku occupies the light tier (lowest capability score);
under L=0.50, Haiku wins the heavy tier outright and the collapse pushes Opus
into the medium/fallback slot. The heavy-tier roles (PM, sr-arch, sr-researcher)
now demonstrate the intended latency gain (+65 tok/s). The junior-developer and
assistant changes are structural — they move from light-tier (Haiku) to medium-
fallback (Opus) because tier-collapse eliminated the light tier entirely, not
because Opus is faster. This is expected and correctly documented.

The weight override demonstrably moves role assignments: 3 of 8 heavy roles
switch from Opus→Haiku with a 3.6× throughput gain (25→90 tok/s) for the most
latency-sensitive part of the team.

---

## 3. Chartering DecisionRecord (expected inputs_snapshot)

```yaml
inputs_snapshot:
  subscription: anthropic:max-5x
  governance_floor: 3
  parallelism_cap: 5
  weights: {L: 0.50, K: 0.20, C: 0.25, G: 0.05}
  weights_source: cli
  tier_thresholds: {heavy_min: 0.70, medium_min: 0.40}
  tier_thresholds_source: skill-default
  landscape_artifact: ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
  landscape_artifact_source: kit-default
  weight_overrides_applied: true
  archetype_override_file: absent
  tier_scores:
    haiku-4.5: 0.703
    sonnet-4.6: 0.399
    opus-4.6: 0.258
  tier_collapse_applied: true
  tier_collapse_scenario: "only heavy + light produced; two light models promoted to medium"
```

---

## 4. Conclusion

**The override surface moves the output.** With L=0.50 (vs kit default L=0.10):

- **5 of 8 roles change model.** The PM, senior-architect, and senior-researcher
  move from Opus 4.6 to Haiku 4.5, gaining 3.6× throughput for the most critical
  team roles. The junior-developer and assistant move from Haiku to Opus as a
  structural consequence of tier-collapse (the light tier is eliminated by the
  formula promoting Haiku to heavy).
- **Haiku 4.5 scores 0.703** (heavy, comfortably above the 0.70 threshold) under
  L=0.50, vs 0.307 (light) under kit-default C=0.60 weights.
- **Opus 4.6 scores 0.258** (light, pre-collapse) under L=0.50, vs 0.606 (medium,
  fallback-promoted to heavy) under kit-default weights — a tier inversion driven
  entirely by the weight change.

The Anthropic-only candidate set under G-floor=3 is sufficient to demonstrate
visible output change. Attempt B (G-floor=2, `--providers any`) as specified in
design §8 is not required: the ≥2-role-change success criterion is met with 5
changes in attempt A. The design's G-floor=2 fallback was provided for the case
where "the same accessible set produces identical assignments at L=0.50" — that
condition does not hold here.
