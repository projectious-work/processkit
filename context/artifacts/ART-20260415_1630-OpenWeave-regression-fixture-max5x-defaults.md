---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260415_1630-OpenWeave-regression-fixture-max5x-defaults
  created: '2026-04-15T16:30:00+00:00'
spec:
  name: team-creator regression fixture — Max-5× kit defaults (OpenWeave)
  kind: test-fixture
  location: context/artifacts/ART-20260415_1630-OpenWeave-regression-fixture-max5x-defaults.md
  format: markdown
  version: 1.0.0
  tags:
  - team-creator
  - regression-fixture
  - openweave
  - kit-defaults
  - acceptance-gate
  produced_by: BACK-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
  owner: ACTOR-developer
  links:
    workitem: BACK-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
    inputs:
    - ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff
    - ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
---

# team-creator Regression Fixture — Max-5× Kit Defaults

**Purpose:** Locked expected output for `team-create --dry-run` with
kit-default weights and no OpenWeave overrides. Any deviation from these
values fails the regression gate. Values sourced from Phase 3 dogfood diff
(ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff) §7 P1 post-formula
adjustment, which is the accepted Phase 3.5 arithmetic.

**This fixture is immutable.** Update only intentionally, with a new WorkItem.

---

## Invocation parameters (locked)

```
team-create \
  --subscription anthropic:max-5x \
  --providers anthropic \
  --governance-floor 4 \
  --parallelism-cap 5
  # No --weight-overrides
  # No --threshold-overrides
  # No --landscape-artifact
  # No context/team/role-archetypes.yaml
```

## Override surface state (all absent)

| Layer | Source | Value |
|---|---|---|
| Layer 1 — landscape | kit-default | ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured |
| Layer 2 — weights | skill-default | `{C:0.60, K:0.20, L:0.10, G:0.10}` |
| Layer 3 — thresholds | skill-default | `{heavy_min:0.70, medium_min:0.40}` |
| Layer 4 — role pins | absent | Kit defaults from references/role-archetypes.md |

## Candidate set (anthropic + G-floor=4)

All three Anthropic Max-5× subscription models pass the G-floor gate (G=5 ≥ 4).

Raw metrics (from ART-20260415_1525-LandscapeSummary; see dogfood diff §2 for derivation):

| Model | SWE-V | SWE-P | CR | C raw | $/M out | Burn | K raw | L tok/s | G raw |
|---|---|---|---|---|---|---|---|---|---|
| Opus 4.6 | 0.808 | 0.460 | 0.95 | 0.739 | 25 | 1.0× | 0.0400 | 25 | 1.00 |
| Sonnet 4.6 | 0.796 | 0.440 | 0.85 | 0.695 | 15 | 0.5× | 0.1333 | 50 | 1.00 |
| Haiku 4.5 | ~0.60 | ~0.30 | 0.75 | 0.550 | 5 | 0.15× | 1.3333 | 90 | 1.00 |

## Normalised values (post-Phase-3.5 weights)

Min-max bounds across accessible set:

| Dim | min | max | range |
|---|---|---|---|
| C | 0.550 | 0.739 | 0.189 |
| K | 0.0400 | 1.3333 | 1.2933 |
| L | 25 | 90 | 65 |
| G | 1.00 | 1.00 | 0.000 (zero-range → all clamp to 0.01) |

Normalised values:

| Model | norm(C) | norm(K) | norm(L) | norm(G) |
|---|---|---|---|---|
| Opus 4.6 | 1.000 | 0.010 | 0.010 | 0.010 |
| Sonnet 4.6 | 0.767 | 0.0722 | 0.385 | 0.010 |
| Haiku 4.5 | 0.010 | 1.000 | 1.000 | 0.010 |

## Locked TierScores

Formula: `TierScore = 0.60·C + 0.20·K + 0.10·L + 0.10·G`

| Model | 0.60·C | 0.20·K | 0.10·L | 0.10·G | **TierScore** |
|---|---|---|---|---|---|
| Opus 4.6 | 0.6000 | 0.0020 | 0.0010 | 0.0010 | **0.606** |
| Sonnet 4.6 | 0.4602 | 0.01444 | 0.0385 | 0.0010 | **0.514** |
| Haiku 4.5 | 0.0060 | 0.2000 | 0.1000 | 0.0010 | **0.307** |

**Classification (thresholds: heavy ≥ 0.70, medium 0.40–0.69, light < 0.40):**

| Model | TierScore | Raw tier | Post-fallback tier |
|---|---|---|---|
| Opus 4.6 | 0.606 | medium | **heavy** (fallback: highest-scoring; no candidate clears 0.70) |
| Sonnet 4.6 | 0.514 | medium | **medium** |
| Haiku 4.5 | 0.307 | light | **light** |

Fallback rule fires: no candidate clears 0.70. Opus 4.6 (0.606, highest) promoted
to heavy. Three distinct tiers present post-fallback; tier-collapse rule does NOT fire.

## Locked role assignments (8 rows)

| Role | Tier pin | Assigned model | TierScore | Tier |
|---|---|---|---|---|
| project-manager | heavy | Opus 4.6 | 0.606 | heavy (fallback) |
| senior-architect | heavy | Opus 4.6 | 0.606 | heavy (fallback) |
| senior-researcher | heavy | Opus 4.6 | 0.606 | heavy (fallback) |
| junior-architect | medium | Sonnet 4.6 | 0.514 | medium |
| developer | medium | Sonnet 4.6 | 0.514 | medium |
| junior-researcher | medium | Sonnet 4.6 | 0.514 | medium |
| junior-developer | light | Haiku 4.5 | 0.307 | light |
| assistant | light | Haiku 4.5 | 0.307 | light |

Override-when checks:
- junior-architect medium→heavy: heavy tier's SWE-V (Opus, 0.808) > medium tier's
  SWE-V (Sonnet, 0.796) by only 1.2pp — far below 15pp threshold. No upgrade.
- developer: `--security-critical` not set. No upgrade.
- senior-architect/researcher: three tiers accessible. No downgrade.
- assistant: light tier accessible (Haiku). No shared-model arrangement needed.

## inputs_snapshot (expected in chartering DecisionRecord)

```yaml
inputs_snapshot:
  subscription: anthropic:max-5x
  governance_floor: 4
  parallelism_cap: 5
  weights: {C: 0.60, K: 0.20, L: 0.10, G: 0.10}
  weights_source: skill-default
  tier_thresholds: {heavy_min: 0.70, medium_min: 0.40}
  tier_thresholds_source: skill-default
  landscape_artifact: ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
  landscape_artifact_source: kit-default
  weight_overrides_applied: false
  archetype_override_file: absent
  tier_scores:
    opus-4.6: 0.606
    sonnet-4.6: 0.514
    haiku-4.5: 0.307
```

## CI gate rule

`team-create --dry-run` output must match the role assignments table above
exactly (8 rows, model per role, tier per role, TierScore rounded to 3 dp).
Any deviation — including fallback tier reclassification changing — is a
regression failure. Do not update this fixture without a dedicated WorkItem
and owner sign-off.
