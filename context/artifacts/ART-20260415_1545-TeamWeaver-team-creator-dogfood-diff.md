---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff
  created: '2026-04-15T15:45:00+00:00'
spec:
  name: "team-creator skill — Phase 3 dogfood diff (TeamWeaver)"
  kind: diagnostic
  location: context/artifacts/ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff.md
  format: markdown
  version: "1.0.0"
  tags: [team-creator, dogfood, tiering-formula, acceptance-gate, diagnostic]
  produced_by: BACK-20260415_1505-TeamWeaver-team-creator-skill
  owner: ACTOR-sr-researcher
  links:
    workitem: BACK-20260415_1505-TeamWeaver-team-creator-skill
    inputs:
      - ART-20260415_1505-TeamWeaver-team-creator-skill-design
      - ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
      - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---

# team-creator skill — Phase 3 Dogfood Diff

**Author:** ACTOR-sr-researcher (Opus)
**Date:** 2026-04-15
**Phase:** 3 of 4 — Diagnostic simulation. No skill modification.
**WorkItem:** `BACK-20260415_1505-TeamWeaver-team-creator-skill`
**Verdict (preview):** FAIL — the current formula inverts the tiers
relative to the existing team. Recommended adjustments in §7.

---

## 1. Inputs used (simulated invocation)

Simulated command:

```
team-create \
  --subscription anthropic:max-5x \
  --providers anthropic \
  --governance-floor 4 \
  --parallelism-cap 5 \
  --landscape ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
```

Default weights (no `--weight-overrides`):
`{C: 0.40, K: 0.35, L: 0.15, G: 0.10}`

---

## 2. Accessible candidate set

Anthropic-only filter + G-floor=4. Anthropic is the "flagship case"
from the worked example in `references/tiering-formula.md` (G=5).
All three subscription-included Anthropic models clear the gate.

Raw metrics sourced verbatim from the landscape-summary artifact
(§"Model Ladder — Anthropic Claude" and §"Coding Capability —
Benchmarks & Models"). `C raw` is the arithmetic mean of
`swe_bench_verified` (0–1 scale), `swe_bench_pro` (0–1 scale), and
`community_rating` (0–1 scale). `K raw = 1 / (output_price × burn)`.
`L raw` uses midpoints of published ranges. Haiku SWE-bench values
are absent from the landscape; the "~75% quality vs Opus" figure is
used as a proxy (see §8 open issue #1).

| Model      | Prov. | SWE-V | SWE-P | CR   | C raw | $/M out | Burn | K raw  | L tok/s | G raw | G-gate |
|------------|-------|-------|-------|------|-------|---------|------|--------|---------|-------|--------|
| Opus 4.6   | Anth. | 0.808 | 0.460 | 0.95 | 0.739 | 25      | 1.0  | 0.0400 | 25      | 1.00  | PASS   |
| Sonnet 4.6 | Anth. | 0.796 | 0.440 | 0.85 | 0.695 | 15      | 0.5  | 0.1333 | 50      | 1.00  | PASS   |
| Haiku 4.5  | Anth. | ~0.60 | ~0.30 | 0.75 | 0.550 | 5       | 0.15 | 1.3333 | 90      | 1.00  | PASS   |

Notes:
- `L tok/s` uses published midpoints: Opus 20–30 → 25; Sonnet 40–60
  → 50; Haiku 80–100 → 90.
- `G raw = G_score/5`. All three Anthropic subscription-tier models
  are treated equally (G=5) — the provider-level governance rating
  does not distinguish among same-provider models in the source data.
- Haiku SWE-bench proxy: landscape says "~75% quality vs Opus"; that
  maps to `0.75 × 0.808 = 0.606` (SWE-V) and `0.75 × 0.46 = 0.345`
  (SWE-P) — I use 0.60 and 0.30 rounded.

---

## 3. Tiering arithmetic

### 3.1 Min-max bounds across the accessible set

| Dim | min   | max    | range  |
|-----|-------|--------|--------|
| C   | 0.550 | 0.739  | 0.189  |
| K   | 0.040 | 1.333  | 1.293  |
| L   | 25    | 90     | 65     |
| G   | 1.00  | 1.00   | 0.000  |

G has zero range across the set (all providers equal). Per the
skill's `norm(x)` rule with the `[0.01, 1.00]` clamp, the degenerate
case collapses to the floor. I apply `norm(G)=0.01` uniformly to all
three models — this is what the formula text prescribes when
`max==min` (division by zero would otherwise occur). See §8 open
issue #2 — the reference file is ambiguous here and this is the
defensible reading.

### 3.2 Normalised values

| Model      | norm(C)                | norm(K)                | norm(L)          | norm(G) |
|------------|------------------------|------------------------|------------------|---------|
| Opus 4.6   | (0.739-0.550)/0.189 = 1.000 | (0.040-0.040)/1.293 = 0.010 (floor) | (25-25)/65 = 0.010 (floor) | 0.010 |
| Sonnet 4.6 | (0.695-0.550)/0.189 = 0.767 | (0.1333-0.040)/1.293 = 0.0722 | (50-25)/65 = 0.385 | 0.010 |
| Haiku 4.5  | (0.550-0.550)/0.189 = 0.010 (floor) | (1.333-0.040)/1.293 = 1.000 | (90-25)/65 = 1.000 | 0.010 |

### 3.3 TierScore

```
TierScore = 0.40·norm(C) + 0.35·norm(K) + 0.15·norm(L) + 0.10·norm(G)
```

| Model      | 0.40·C  | 0.35·K  | 0.15·L  | 0.10·G  | TierScore |
|------------|---------|---------|---------|---------|-----------|
| Opus 4.6   | 0.4000  | 0.0035  | 0.0015  | 0.0010  | **0.406** |
| Sonnet 4.6 | 0.3068  | 0.0253  | 0.0578  | 0.0010  | **0.391** |
| Haiku 4.5  | 0.0040  | 0.3500  | 0.1500  | 0.0010  | **0.505** |

### 3.4 Raw classification (thresholds ≥0.70 heavy, 0.40–0.69 med,
<0.40 light)

| Model      | TierScore | Raw tier |
|------------|-----------|----------|
| Opus 4.6   | 0.406     | medium   |
| Sonnet 4.6 | 0.391     | light    |
| Haiku 4.5  | 0.505     | medium   |

No candidate clears 0.70 → **fallback rule fires**: highest-scoring
candidate (Haiku, 0.505) promoted to heavy.

Post-fallback tiers: Haiku=heavy, Opus=medium, Sonnet=light.
Three distinct tiers present → tier-collapse rule does NOT fire.

---

## 4. Role → model mapping (skill's output)

Per `references/role-archetypes.md`, tier pins mapped onto the
post-fallback tier assignments:

| Role              | Tier pin | Best candidate in tier | Assigned model |
|-------------------|----------|------------------------|----------------|
| project-manager   | heavy    | Haiku 4.5              | Haiku 4.5      |
| senior-architect  | heavy    | Haiku 4.5              | Haiku 4.5      |
| senior-researcher | heavy    | Haiku 4.5              | Haiku 4.5      |
| junior-architect  | medium   | Opus 4.6               | Opus 4.6       |
| developer         | medium   | Opus 4.6               | Opus 4.6       |
| junior-researcher | medium   | Opus 4.6               | Opus 4.6       |
| junior-developer  | light    | Sonnet 4.6             | Sonnet 4.6     |
| assistant         | light    | Sonnet 4.6             | Sonnet 4.6     |

Override-when rules checked:
- junior-architect medium→heavy override: requires `>15pp` gap on
  SWE-V between best medium and best heavy. Best medium = Opus
  (80.8); best heavy = Haiku (~60). Gap is `80.8 - 60 = 20.8pp`,
  but it runs in the *wrong direction* (heavy tier is weaker on
  capability). The override text says "median capability gap between
  medium and heavy tiers exceeds 15pp on SWE-bench Verified" without
  a sign check — this is a **latent defect** (see §7) but does not
  actually fire because the skill's intent is gap-in-favour-of-heavy.
- `--security-critical` not set → no developer override.
- No senior downgrade needed (three tiers exist).

---

## 5. Diff vs current team

Current team source: `context/team/roster.md` + DEC-20260414_0900.

| Role              | Current model | Skill's output | Status          |
|-------------------|---------------|----------------|-----------------|
| project-manager   | Opus 4.6      | Haiku 4.5      | **DRIFT**       |
| senior-architect  | Opus 4.6      | Haiku 4.5      | **DRIFT**       |
| senior-researcher | Opus 4.6      | Haiku 4.5      | **DRIFT**       |
| junior-architect  | Sonnet 4.6    | Opus 4.6       | **DRIFT**       |
| developer         | Sonnet 4.6    | Opus 4.6       | **DRIFT**       |
| junior-researcher | Sonnet 4.6    | Opus 4.6       | **DRIFT**       |
| junior-developer  | Haiku 4.5     | Sonnet 4.6     | **DRIFT**       |
| assistant         | Haiku 4.5     | Sonnet 4.6     | **DRIFT**       |

**8 / 8 roles drift.** The skill's output is a complete **tier
inversion** of the current team. Fallback-rule fired for PM/sr-arch/
sr-researcher (heavy tier assignment). No explicit override-when
rules fired beyond the generic fallback.

### 5.1 Orientation-target share comparison

Current DEC-20260414_0900 targets: Opus ≈5%, Sonnet ≈85%, Haiku
≈10% (as session-effort shares across the 8-role team).

Skill's emitted targets would reflect the *new* mapping — heavy
roles (PM + sr-arch + sr-researcher, now Haiku) at ≈5%, medium
(jr-arch + dev + jr-res, now Opus) at ≈85%, light (jr-dev + asst,
now Sonnet) at ≈10%. If we read the targets as the current team's
**per-model** shares:

| Model   | Current target | Skill's implied share | Δ (pp)  |
|---------|----------------|-----------------------|---------|
| Opus    | 5 %            | 85 %                  | +80 pp  |
| Sonnet  | 85 %           | 10 %                  | −75 pp  |
| Haiku   | 10 %           | 5 %                   | −5 pp   |

Δ on Opus/Sonnet shares is ~75–80 pp — **catastrophically outside
the ±5pp window** set by the WorkItem success criterion.

---

## 6. Verdict

**FAIL.** The skill does NOT reproduce the current team. All 8
roles drift; per-model share delta exceeds the ±5pp window by a
factor of ~15×. The first acceptance gate is not met.

**Root cause.** On a single-provider (same-G) candidate set:

1. `G` adds zero signal (all values equal, all clamped to the 0.01
   floor). The 10% weight becomes noise.
2. Min-max normalisation of `K` (cost) spreads Haiku/Opus to the
   [0.01, 1.00] extremes — Haiku collects the full 35% K weight,
   Opus collects only 0.35 × 0.01 = 0.35% of its weight slot.
3. `L` (latency) amplifies this: Haiku again wins and gets
   0.15 × 1.00 = 15%, Opus gets 0.15 × 0.01 = 0.15%.
4. Only `C` (40%) rewards capability, but even there Haiku's floor
   (0.01) denies it most of the loss and the Sonnet–Opus delta in C
   (0.767 vs 1.000) is a mere 23pp inside a 40% slot — not enough
   to offset the combined 50% that cost+latency pour onto Haiku.

Net: **the formula buys "cheap + fast" at 50% weight while
penalising the cost/latency laggard to near-zero across that 50%**.
In a same-provider set where cost and capability are inversely
correlated by design (Anthropic prices scale with capability), the
formula systematically elevates the cheapest model.

---

## 7. Recommended formula / threshold adjustments (priority order)

Do NOT modify the skill in Phase 3. These are diagnostic proposals
for owner triage before Phase 4.

### P1 — Rebalance default weights toward capability

The 0.40 C weight underweights the dimension that actually separates
roles. A team composed for a high-stakes owner needs capability to
dominate. Proposal:

```
{C: 0.60, K: 0.20, L: 0.10, G: 0.10}
```

Re-running with these weights on the same candidate set:
- Opus: 0.60·1.000 + 0.20·0.010 + 0.10·0.010 + 0.10·0.010 = **0.606**
- Sonnet: 0.60·0.767 + 0.20·0.0722 + 0.10·0.385 + 0.10·0.010 = **0.514**
- Haiku: 0.60·0.010 + 0.20·1.000 + 0.10·1.000 + 0.10·0.010 = **0.307**

Result: Opus=medium (fallback→heavy), Sonnet=medium, Haiku=light.
Post-fallback: Opus=heavy, Sonnet=medium, Haiku=light.
Mapping reproduces current team exactly. **8/8 MATCH.**

### P2 — Introduce a capability floor before cost optimisation

Even with P1, a future landscape shift (e.g. a new ultra-cheap
model with mid-tier capability) could re-invert tiers. A capability
floor — "models with `C_raw < 0.60` cannot be classified heavy
regardless of TierScore" — would harden the formula. Implement as a
post-classification filter, not a gate (so lights/mediums still
compete on K/L).

### P3 — Drop the 0.01 floor or make it soft

The current `[0.01, 1.00]` clamp converts the min-of-set model into
effective zero on that dimension. On a 3-model set this creates
exactly the pathological collapse seen above. Options:
  (a) soften the floor to 0.25 — preserves ranking without
      annihilating the minimum,
  (b) replace min-max with z-score normalisation for sets of ≤5
      models,
  (c) widen the candidate set to include at least one model per
      provider to prevent same-provider cost/capability anti-
      correlation from dominating.

### P4 — Fix the junior-architect override sign

`references/role-archetypes.md` text: "Heavy if median capability
gap between medium and heavy tiers exceeds 15pp on SWE-bench
Verified". Needs an explicit sign requirement — "where heavy-tier
SWE-V exceeds medium-tier SWE-V by >15pp". Otherwise the override
could fire in a tier-inverted run (as here) and promote the wrong
role.

### P5 — G-dimension degenerate handling

When G has zero variance, its weight (0.10) should either (a)
redistribute to the other dimensions or (b) remain clamped to 0.01
as done here. Document the chosen semantics in
`references/tiering-formula.md`.

Recommended order for Phase 3.5 (formula adjustment cycle): **P1 +
P4** first (smallest diff, fixes the acceptance gate), then P2/P3
as hardening before Phase 4 register. P5 is cosmetic.

---

## 8. Open issues surfaced

1. **Haiku benchmark gap in landscape.** SWE-V and SWE-P for Haiku
   are absent in the source artifact. Proxy via "75% vs Opus" is
   defensible but not auditable. Phase 4 should re-ingest with
   explicit Haiku numbers OR the skill should require them from
   `model-recommender` with a clear error when missing.

2. **G-dimension ambiguity on zero-variance sets.**
   `references/tiering-formula.md` norm() definition doesn't specify
   behaviour when `max == min`. I chose uniform 0.01 (the floor).
   Alternatives: uniform 1.00 (equally favourable), or
   redistribute the 10% weight to remaining dimensions. Owner
   should decide; Phase 4 register should lock the semantic.

3. **Tier-score thresholds vs candidate-set size.** The fixed
   thresholds (≥0.70 heavy) assume dense candidate sets. On
   small single-provider sets, min-max normalisation guarantees
   the top score clusters around the weighted average of ~0.5 —
   no candidate ever clears 0.70, and the fallback always fires.
   This makes the threshold effectively unused on the most common
   case (single-provider subscriptions). Either (a) adopt
   rank-based tiering for |candidates| ≤ 5, or (b) publish
   expected TierScore distributions so the thresholds are
   calibrated.

4. **Single-Actor-per-tier pathology.** With 3 accessible models and
   8 role slots, multiple roles must share a model. The skill's
   current output assigns 3 roles to the same Actor (Haiku for
   heavy, Opus for medium). This is correct — but the skill
   writes 8 Actor entities per the design doc. Phase 4 must
   clarify whether same-model/different-role creates 1 Actor with
   8 Bindings or 8 Actors all pointing at the same model.

5. **Provider-neutrality regression risk.** P2 (capability floor)
   introduces an absolute capability threshold. Phase 4 must
   verify this floor is provider-neutral — i.e. calibrated
   against the global landscape, not anchored to any specific
   model family.

---

**End of dogfood diff.** Phase 3 verdict: **FAIL**. Phase 4
(register) should block pending P1+P4 formula adjustments in a
Phase 3.5 cycle; re-run dogfood before proceeding.
