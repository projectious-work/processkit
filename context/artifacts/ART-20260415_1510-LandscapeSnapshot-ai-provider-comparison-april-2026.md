---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026
  created: '2026-04-15T15:10:00+00:00'
spec:
  name: "AI provider comparison — April 2026 (landscape snapshot)"
  kind: reference-dataset
  location: context/artifacts/ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026.html
  format: html
  version: "1.0.0"
  tags: [landscape, providers, models, cost, benchmarks, swe-bench, livecodebench, team-creator]
  owner: ACTOR-assistant
  ingested_by: ACTOR-pm-claude
  ingested_at: '2026-04-15T15:10:00+00:00'
  original_filename: ai-provider-comparison-april-2026.html
  summary: >
    Static HTML comparison of six major AI providers (Anthropic,
    OpenAI, Google Gemini, Mistral, xAI Grok, DeepSeek) across
    subscription tiers, flagship model capability benchmarks
    (SWE-bench Verified, SWE-bench Pro, LiveCodeBench, community
    coding rating), context windows, API pricing (input/output, cache
    hit, batch discount), speed, and quota-burn ratios. Captured
    2026-04-14 by the owner as input for the `team-creator` skill
    (FEAT-20260415_1505-TeamWeaver).
  criteria_index:
    cost: [subscription_price, input_per_million, output_per_million, cache_hit, batch_discount, quota_burn_vs_flagship]
    capability: [swe_bench_verified, swe_bench_pro, livecodebench, community_coding_rating, context_window]
    fit: [agentic_best_for, when_not_to_use]
  consumes: []
  consumed_by:
    - FEAT-20260415_1505-TeamWeaver-team-creator-skill
  freshness: |
    Snapshots of the provider landscape go stale within a quarter.
    Re-capture before every `team-rebalance` run. This snapshot is
    valid as of 2026-04-14; treat anything older than 2026-07-14 as
    suspect.
---

# AI provider comparison — April 2026

This artifact wraps a standalone HTML comparison document captured by
the owner on 2026-04-14 as the criteria input for the `team-creator`
skill (see WorkItem FEAT-20260415_1505-TeamWeaver).

## Why it exists

The `team-creator` skill tiers available models into heavy / medium /
light buckets using a weighted formula over cost, capability, latency,
and fit dimensions. That formula needs a concrete per-provider /
per-model dataset to operate against — this HTML is the first such
snapshot.

## Contents (sections)

1. Subscription tiers — what €90/mo buys across providers.
2. Daily-usage transparency per provider.
3. Flagship model benchmark table (SWE-bench Verified / Pro,
   LiveCodeBench, community coding rating).
4. Strengths and "if you need X, pick Y" recommendations.
5. Quality-vs-flagship / speed / quota-burn comparison.
6. API pricing table — input, output, cache hit, batch discount,
   context window, agentic best-for.

## Usage

- Read by `team-creator` at `team-create` time.
- Re-captured by the owner or `senior-researcher` quarterly.
- Superseded (not versioned in place) when a new snapshot is ingested.
