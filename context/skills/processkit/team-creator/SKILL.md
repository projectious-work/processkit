---
name: team-creator
description: |
  Compose a provider-neutral AI team by tiering accessible models on
  cost-efficiency, capability, latency, and governance, then mapping
  the 8 processkit role archetypes onto those tiers. Use when
  bootstrapping a new project team, rotating after a provider change,
  or quarterly rebalancing. Triggers: "create my AI team",
  "compose a team", "rebalance the team", "review the team".
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-team-creator
    version: "1.0.0"
    created: 2026-04-15T00:00:00Z
    category: processkit
    layer: null
    uses:
      - skill: model-recommender
        purpose: >
          Query, score, and filter accessible models via
          query_models, get_pricing, check_availability.
      - skill: role-management
        purpose: Create Role entities via create_role.
      - skill: actor-profile
        purpose: >
          Create Actor entities (type: ai-agent) via create_actor;
          deactivate replaced actors via deactivate_actor.
      - skill: binding-management
        purpose: >
          Create role-assignment Bindings via create_binding;
          end superseded Bindings via end_binding.
      - skill: decision-record
        purpose: >
          Write the chartering DecisionRecord; read stored
          formula weights on rebalance via get_decision.
    provides:
      primitives: []
      mcp_tools: []
      commands:
        - name: team-create
          args: "--subscription --providers --parallelism-cap \
--governance-floor [--weight-overrides] [--dry-run]"
          description: >
            Full team derivation. Writes 8 Role + 8 Actor + 8
            Binding entities, roster.md, and a chartering
            DecisionRecord.
        - name: team-review
          args: "[--landscape <artifact-id>] [--threshold <float>]"
          description: >
            Read-only health-check. Diffs current assignments
            against the latest landscape snapshot. No writes.
        - name: team-rebalance
          args: "--roles <list> --confirm --reason <string>"
          description: >
            Apply a team-review recommendation. Ends old Bindings,
            creates new ones, amends roster.md and DecisionRecord.
---

# Team Creator

## Intro

`team-creator` derives a provider-neutral AI team by scoring all
accessible models on four weighted dimensions (Capability, Cost,
Latency, Governance) and mapping the 8 processkit role archetypes
onto the resulting heavy / medium / light tiers. It composes 5
existing skills — no new primitives or MCP tools are introduced.

## Overview

### When to use

| Trigger | Command |
|---|---|
| New project or provider subscription | `team-create` |
| Quarterly landscape shift | `team-review` → `team-rebalance` |
| Provider outage, rapid rotation | `team-rebalance --roles all` |
| Spot-check current assignments | `team-review` |

### Inputs (key parameters)

| Parameter | Required | Default | Notes |
|---|---|---|---|
| `--subscription <provider>:<tier>` | yes | — | e.g. `anthropic:max-5x` |
| `--governance-floor <0-5>` | no | 3 | Models below excluded before scoring |
| `--parallelism-cap <1-10>` | no | 5 | PM always capped at 1 |
| `--weight-overrides <json>` | no | see formula | Must sum to 1.0 ± 0.001 |
| `--landscape <ART-id>` | no | latest `landscape-summary` artifact | |

### Tiering formula (summary)

**Defaults rebalanced 2026-04-15 after Phase 3 dogfood (see ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff §7).** Capability weight raised from 0.40 to 0.60 to prevent tier inversion on same-provider candidate sets where cost and capability are anti-correlated.

| Dim | Weight | Source |
|---|---|---|
| Capability (C) | 0.60 | swe_bench + community rating, normalised |
| Cost efficiency (K) | 0.20 | 1 / (output_price × quota_burn), normalised |
| Latency fit (L) | 0.10 | output_tokens_per_sec, normalised |
| Governance (G) | 0.10 | G-score from model-recommender, normalised |

`TierScore ≥ 0.70 → heavy | 0.40–0.69 → medium | < 0.40 → light`

See `references/tiering-formula.md` for normalisation, thresholds,
and a full worked example.

### Role archetypes → tier mapping

| Role | Tier pin | Override? |
|---|---|---|
| project-manager | heavy | Never |
| senior-architect | heavy | Medium only if no heavy clears G-floor + owner approval |
| senior-researcher | heavy | Same as senior-architect |
| junior-architect | medium | Heavy if capability gap > 15pp on SWE-bench |
| developer | medium | Heavy if `--security-critical` flag set |
| junior-researcher | medium | No override |
| junior-developer | light | Medium if no light model accessible |
| assistant | light | No override; shares junior-developer model if no light available |

See `references/role-archetypes.md` for full override-when rules.

### Commands

**`team-create`** runs the full derivation: queries models, applies
the tiering formula, maps archetypes, writes 8 Role + 8 Actor + 8
Binding entities, rewrites `context/team/roster.md`, and emits a
chartering DecisionRecord that explicitly supersedes the prior team
DecisionRecord. Use `--dry-run` to print the plan without writing.

**`team-review`** is read-only. Re-scores current assignments against
the latest landscape snapshot, diffs tier scores against those stored
in the governing DecisionRecord, and surfaces tier-shifts, unavailable
models, and new outperformers. No entities are written.

**`team-rebalance`** applies a review recommendation. Requires
`--confirm`. For `--roles all`, the full create logic re-runs and a
new DecisionRecord is written. For named roles, the governing
DecisionRecord's `progress_notes` are amended instead.

### Outputs

| Output | `team-create` | `team-review` | `team-rebalance` |
|---|---|---|---|
| Role / Actor / Binding entities | YES ×8 | NO | scoped roles |
| `context/team/roster.md` | YES | NO | YES (in-place) |
| DecisionRecord | YES (new) | NO | amend notes |
| Diff report | NO | YES (stdout) | NO |

## Gotchas

- **Missing landscape-summary artifact.** This skill ingests a
  pre-structured markdown artifact tagged `landscape-summary`, NOT
  raw HTML. If none exists, error: "No landscape-summary artifact
  found. Run the Haiku landscape-ingest task to produce
  ART-*-LandscapeSnapshot before team-create." Do not parse HTML.

- **Entity deactivation sequence on re-create.** When `team-create`
  is re-run: (a) resolve prior team from roster.md; (b) for each
  prior Binding call `binding-management.end_binding` with
  `reason="superseded by team-create run <timestamp>"`; (c) for each
  prior Actor whose model is NOT in the new team call
  `actor-profile.deactivate_actor`; (d) for prior Actors whose model
  IS re-assigned to the same role REUSE the existing Actor — do not
  create a duplicate; (e) then create new Bindings.

- **Formula weight persistence.** Weights live in the chartering
  DecisionRecord's `spec.inputs_snapshot` block. `team-rebalance`
  reads them via `decision-record.get_decision`. No skill-local
  config file for weights.

- **Tier-collapse (< 3 tiers accessible).** Promote the two highest-
  scoring light models to medium. Never fail; degrade gracefully.

- **PM clone cap.** Parallelism cap never applies to project-manager;
  PM is always exactly 1 (per DEC-20260414_0900).

- **Snapshot staleness.** Artifact older than 90 days → warn and
  proceed. Surface the artifact date in the DecisionRecord.

- **Provider-neutrality.** Never hardcode any model name, provider
  name, or tier label anywhere in this skill. All identifiers flow
  in from `model-recommender`.

## No-skill-inflation rationale

Option C chosen over extending `agent-management` (heaviest skill;
scope bleed) or `model-recommender` (individual model profiling vs.
team orchestration). Pure orchestration consumer: 5 existing skills
composed, 3 commands added, 0 new primitives or MCP tools.
