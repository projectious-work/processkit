---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1505-TeamWeaver-team-creator-skill-design
  created: '2026-04-15T16:00:00+00:00'
spec:
  name: "team-creator skill — Phase 1 design (TeamWeaver)"
  kind: design
  location: context/artifacts/ART-20260415_1505-TeamWeaver-team-creator-skill-design.md
  format: markdown
  version: "1.0.0"
  tags: [team-creator, skill-design, tiering-formula, role-archetypes, team-composition]
  produced_by: BACK-20260415_1505-TeamWeaver-team-creator-skill
  owner: ACTOR-jr-architect
  links:
    workitem: BACK-20260415_1505-TeamWeaver-team-creator-skill
    inputs:
      - ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026
      - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---

# team-creator skill — Phase 1 Design

**Author:** ACTOR-jr-architect (Sonnet 4.6)
**Date:** 2026-04-15
**Phase:** 1 of 4 — Design only. No code, no skill directory, no MCP server created here.
**WorkItem:** `BACK-20260415_1505-TeamWeaver-team-creator-skill`

---

## 1. Skill surface — SKILL.md outline

Target: ≤200 lines in the final SKILL.md.

| Section | Purpose |
|---|---|
| Frontmatter | Skill ID, version, `uses` (5 skills composed), `provides` (commands + 0 new MCP tools) |
| Intro | What the skill does in two sentences: tiered team composition from owner constraints |
| Overview / When to use | Trigger conditions: new project, provider change, quarterly rebalance |
| Inputs schema | Owner-supplied parameters (subscription, providers, parallelism cap, weight overrides) |
| Tiering formula | Concrete formula; references `references/tiering-formula.md` for detail |
| Role archetypes | 8-role table with tier pin and override-when rules; references `references/role-archetypes.md` |
| Commands | `team-create`, `team-review`, `team-rebalance` — one paragraph each |
| Outputs | Exact files/entities per command |
| Composed skills | Explicit call-graph: which primitive skill is called for each step |
| Gotchas | 5–7 failure modes specific to team composition |
| No-skill-inflation rationale | Why Option C was chosen over extending `agent-management` or `model-recommender` |

---

## 2. Commands

### `team-create`

**Purpose:** Full team derivation from scratch. Supersedes any prior team DecisionRecord.

**Arguments:**

```
team-create
  --subscription <provider>:<tier>          # e.g. anthropic:max-5x, openai:pro-5x
  --providers <list>                        # comma-separated; "any" = use model-recommender default
  --parallelism-cap <int>                   # max clones per role, default 5
  --governance-floor <0-5>                  # G-score floor passed to model-recommender gates
  --weight-overrides <json>                 # optional: override default dimension weights
  --dry-run                                 # print plan without writing entities
```

**Process (sequential, no fan-out):**
1. Call `model-recommender` (`query_models`, `get_pricing`, `check_availability`) to build a scored candidate list filtered by `--providers` and `--governance-floor`.
2. Apply the tiering formula to classify candidates into heavy / medium / light.
3. Map each of the 8 role archetypes to its pinned tier; select best-scoring candidate per tier.
4. Write entities via composed skills:
   - 8 × `role-management.create_role`
   - 8 × `actor-profile.create_actor` (type: ai-agent)
   - 8 × `binding-management.create_binding` (role-assignment, permanent scope)
5. Write `context/team/roster.md` (narrative + routing table).
6. Write a new `DecisionRecord` via `decision-record-write` that explicitly supersedes `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`.

**State side effects:** Creates 24 new entities (8 Role + 8 Actor + 8 Binding) plus 2 files (roster.md, DecisionRecord). Deactivates any prior team entities that are being replaced.

**`team-create` vs `team-review` distinction:** `team-create` **writes** entities and files. `team-review` only **reads** the current team and the current landscape snapshot, produces a diff report, and surfaces a recommendation — no entities are written.

### `team-review`

**Purpose:** Periodic health-check. Compares current team assignments against the latest landscape snapshot without writing anything.

**Arguments:**

```
team-review
  --landscape <artifact-id>     # which snapshot to compare against (default: latest)
  --threshold <float>           # flag if tier score drifted by more than N points (default: 0.15)
```

**Process:**
1. Read current team from `context/team/roster.md` and resolve all active Bindings.
2. Call `model-recommender.get_pricing` and `get_profile` for each currently-assigned model.
3. Recompute tier scores using the stored formula weights.
4. Diff tier scores against the scores recorded when the team was last created/rebalanced.
5. Output: a markdown diff report with: (a) models that would tier-shift, (b) models that have gone unavailable, (c) new models from landscape that would outperform current assignments. No files written.

**State side effects:** None. Read-only.

### `team-rebalance`

**Purpose:** Apply a `team-review` recommendation. Targeted re-tiering of one or more roles without full team recreation.

**Arguments:**

```
team-rebalance
  --roles <list>           # which roles to rebalance; "all" re-runs full create logic
  --confirm                # required flag to prevent accidental writes
  --reason <string>        # recorded in the DecisionRecord amendment note
```

**Process:**
1. For each target role, re-run steps 1–3 of `team-create` scoped to that role.
2. If a new model would be assigned: end the existing Binding (`binding-management.end_binding`), create a new Actor entity (or reuse if model unchanged), create a new Binding.
3. Update `context/team/roster.md` in-place.
4. Append a `progress_notes` entry to the governing DecisionRecord (does NOT write a new DecisionRecord unless `--roles all`).

**State side effects:** Ends N old Bindings, creates N new Actors + Bindings. Amends roster.md and DecisionRecord notes.

---

## 3. Tiering formula

### Dimensions and weights (defaults; owner-overridable)

| Dimension | Symbol | Source field(s) from model-recommender | Default weight |
|---|---|---|---|
| Capability | C | `(swe_bench_verified + swe_bench_pro + community_rating) / 3`, normalised 0–1 | **0.40** |
| Cost efficiency | K | `1 / (output_price_per_1M × quota_burn_vs_flagship)`, normalised 0–1 | **0.35** |
| Latency fit | L | `output_tokens_per_sec`, normalised 0–1 | **0.15** |
| Governance | G | G-score from model-recommender, normalised 0–1 | **0.10** |

Weights sum to 1.00. Owner may supply `--weight-overrides '{"C":0.5,"K":0.3,"L":0.1,"G":0.1}'`.

### Normalisation

Each raw metric is min-max normalised across the **accessible candidate set** (not the global roster). Normalisation is per-run, so results are relative to what the owner can actually use.

```
norm(x) = (x - min_in_set) / (max_in_set - min_in_set)
          clamp to [0.01, 1.00] to avoid zero-division on single-model sets
```

### Composite tier score

```
TierScore(m) = 0.40 × norm(C(m))
             + 0.35 × norm(K(m))
             + 0.15 × norm(L(m))
             + 0.10 × norm(G(m))
```

### Classification thresholds

| TierScore range | Tier |
|---|---|
| ≥ 0.70 | **heavy** |
| 0.40 – 0.69 | **medium** |
| < 0.40 | **light** |

Thresholds are fixed; not owner-overridable (keeps the formula auditable). If no candidate clears 0.70 (e.g. only one accessible model), the highest-scoring candidate is promoted to heavy regardless.

### Worked example: Claude Opus 4.6 vs GPT-5.4 Thinking

Source data from the April 2026 landscape snapshot (Anthropic Max 5× subscription, G-floor = 4):

| Metric | Opus 4.6 | GPT-5.4 Thinking |
|---|---|---|
| SWE-bench Verified | 80.8% | ~80% |
| SWE-bench Pro | ~46% | 57.7% |
| Community rating | 9.5/10 | 9.0/10 |
| C (raw avg) | 0.739 | 0.759 |
| Output price /1M | $25 | $15 |
| Quota burn vs flagship | 1.0× | ~0.5× |
| K raw = 1/(price × burn) | 0.040 | 0.133 |
| Output tok/s | ~25 | ~82.5 |
| G score | 5 | 2 |

**Normalised (two-model set):** norm(Opus C)=0.01, norm(GPT C)=1.00; norm(Opus K)=0.01, norm(GPT K)=1.00; norm(Opus L)=0.01, norm(GPT L)=1.00; norm(Opus G)=1.00, norm(GPT G)=0.01.

**TierScore:**
- Opus 4.6: 0.40×0.01 + 0.35×0.01 + 0.15×0.01 + 0.10×1.00 = **0.110**
- GPT-5.4 Thinking: 0.40×1.00 + 0.35×1.00 + 0.15×1.00 + 0.10×0.01 = **0.901**

**Interpretation:** Against a G-floor of 4, GPT-5.4 Thinking (G=2) would be excluded at the gate check before formula scoring. Opus passes the gate (G=5 ≥ 4) and is the sole survivor; the fallback rule promotes it to heavy. This reproduces the current team's Opus assignments for heavy roles when constrained to Anthropic + G-floor=4. In a G-floor=2 scenario, GPT-5.4 scores 0.901 (heavy) vs Opus 0.110 (light in this two-model set) — demonstrating provider-neutrality.

**Note:** A real run with 10–15 accessible models spreads scores evenly; the two-model example is illustrative only.

---

## 4. Role archetypes → tier mapping

| Role archetype | Tier pin | Rationale | Override-when |
|---|---|---|---|
| project-manager | **heavy** | Routing quality compounds; every routing error propagates | Never override |
| senior-architect | **heavy** | Cross-subsystem design; blast radius is high | Medium only if no heavy model clears G-floor and owner explicitly approves |
| senior-researcher | **heavy** | Multi-source synthesis; wrong synthesis poisons downstream decisions | Same as senior-architect |
| junior-architect | **medium** | Single-module scope; bounded blast radius | Heavy if median capability gap between medium and heavy exceeds 15pp on SWE-bench |
| developer | **medium** | Implementation against a written plan | Heavy for security-critical or regulated subsystems (owner flag) |
| junior-researcher | **medium** | Bounded single-topic research | No override |
| junior-developer | **light** | Well-specified single-file edits | Medium if no light-tier model accessible (escalation fallback) |
| assistant | **light** | Admin, formatting, summarisation | No override. If no light model: share junior-developer model |

**Tier-collapse rule:** If the accessible candidate set yields fewer than 3 distinct tiers, the skill promotes the two highest-scoring light models to medium. It does not fail.

**Clone cap:** `--parallelism-cap` applies uniformly to all roles except PM (PM is never cloned, per DEC-20260414_0900).

---

## 5. Inputs schema

```yaml
subscription:
  type: string
  format: "<provider>:<tier-id>"    # e.g. "anthropic:max-5x", "openai:pro-5x"
  required: true

api_keys:
  type: list[string]
  required: false
  description: Additional providers accessible via pay-per-token API (not subscription-gated).

governance_floor:
  type: integer
  range: [0, 5]
  default: 3
  description: Minimum G-score. Models below are excluded before formula scoring.

parallelism_cap:
  type: integer
  range: [1, 10]
  default: 5
  description: Maximum clones per role. PM always 1. Values >5 require explicit owner approval.

preferred_providers:
  type: list[string]
  required: false
  description: Tiebreak only — not a hard filter. Applied when scores within 0.05 of each other.

weight_overrides:
  type: object
  schema: {C: float, K: float, L: float, G: float}  # must sum to 1.0 ± 0.001
  required: false

landscape_artifact:
  type: string
  format: ART-<id>
  default: "latest ingested LandscapeSnapshot artifact"
  required: false
```

---

## 6. Outputs

### What `team-create` writes (that `team-review` does not)

| Output | Path | Written by | `team-create` | `team-review` |
|---|---|---|---|---|
| Role entities (×8) | `context/roles/ROLE-<name>.md` | role-management | YES | NO |
| Actor entities (×8) | `context/actors/ACTOR-<alias>.md` | actor-profile | YES | NO |
| Binding entities (×8) | `context/bindings/BIND-<id>.md` | binding-management | YES | NO |
| `roster.md` | `context/team/roster.md` | team-creator | YES | NO |
| DecisionRecord | `context/decisions/DEC-<ts>-TeamRoster-<alias>.md` | decision-record-write | YES | NO |
| Diff/review report | (stdout / ephemeral artifact) | team-creator | NO | YES |

### DecisionRecord charter content

- `supersedes: [DEC-20260414_0900-TeamRoster-permanent-ai-team-composition]`
- Exact inputs used (subscription, providers, weights, landscape artifact ID)
- Tier scores for each assigned model (for audit / Phase 3 dogfood diff)
- Parallelism cap and any override-when rules applied
- Owner-approved exception flags (e.g. parallelism > 5, governance-floor < 3)

### `team-rebalance` output delta

Same entity types as `team-create`, scoped to rebalanced roles. Does NOT write a new DecisionRecord — appends a `progress_notes` entry to the existing one.

---

## 7. No-skill-inflation compliance

Chosen as Option C — a new narrow skill — after explicitly rejecting two extensions. Option A (extending `agent-management`) was rejected because `agent-management` is already the heaviest skill in the kit and team composition is an orchestration concern, not a session-management concern; blurring the boundary would make both harder to evolve independently. Option B (extending `model-recommender`) was rejected because `model-recommender` profiles individual models and routes individual tasks; composing 8 roles into a team with a tiering formula and emitting Role/Actor/Binding triples is a qualitatively different abstraction layer. This skill is a **pure orchestration consumer**: it calls `model-recommender`, `role-management`, `actor-profile`, `binding-management`, and `decision-record-write` without duplicating any surface. It adds exactly three commands, one tiering formula document, and one role-archetypes reference — all new territory.

---

## 8. Open questions for Phase 2

1. **Formula weight persistence.** Where are weights stored between runs? Options: (a) embed in emitted DecisionRecord and re-read on `team-rebalance`; (b) a `team-creator/config.json` within the skill directory; (c) require `--weight-overrides` explicitly on rebalance. Option (a) is preferred for auditability but Phase 2 must confirm viable via the `decision-record` skill's query interface.

2. **Landscape snapshot ingestion protocol.** Must define: (a) how "latest" is resolved (index-management query by tag + created timestamp?); (b) whether HTML is parsed programmatically or the skill relies on a pre-structured markdown summary artifact; (c) what happens when snapshot is >90 days old (warn and proceed, or block?).

3. **Entity deactivation on re-create.** When `team-create` is re-run, old Role/Actor/Binding entities must be deactivated (not deleted). Phase 2 must define the deactivation sequence — particularly whether `actor-profile.deactivate_actor` is called before or after writing new entities, and how to handle same-model-same-role re-assignments (avoid duplicate Actors).
