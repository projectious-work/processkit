---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260415_1600-OpenWeave-openweave-skill-design
  created: '2026-04-15T16:00:00+00:00'
spec:
  name: team-creator openness — Phase 1 design (OpenWeave)
  kind: design
  location: context/artifacts/ART-20260415_1600-OpenWeave-openweave-skill-design.md
  format: markdown
  version: 1.0.0
  tags:
  - team-creator
  - skill-design
  - openweave
  - configurable-defaults
  - landscape-override
  - weight-override
  - tier-thresholds
  - role-archetypes
  produced_by: BACK-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
  owner: ACTOR-jr-architect
  links:
    workitem: BACK-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
    inputs:
    - ART-20260415_1505-TeamWeaver-team-creator-skill-design
    - ART-20260415_1525-LandscapeSummary-ai-provider-comparison-april-2026-structured
    - ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff
---

# team-creator openness — Phase 1 Design (OpenWeave)

**Author:** ACTOR-jr-architect (Sonnet 4.6)
**Date:** 2026-04-15
**Phase:** 1 of 2 — Design only. No skill modifications here.
**WorkItem:** BACK-20260415_1600-OpenWeave-team-creator-user-configurable-defaults

---

## 1. Layer 1 — Default Model Override (Landscape Artifact)

### Naming convention

The kit's canonical landscape summary carries the tag
`landscape-summary`. A derived project's override artifact uses an
additional tag `landscape-summary-project` and must include a
`project_id` field in its frontmatter:

```yaml
tags: [landscape, landscape-summary, landscape-summary-project]
project_id: <project-slug>          # e.g. "edge-lab-q2-2026"
```

**Precedence rule.** When `team-create` resolves the landscape artifact:

1. If `--landscape-artifact <ART-id>` is supplied, use it exactly.
2. Else query index for artifacts tagged `landscape-summary-project`
   whose `project_id` matches the current project context; use the
   most-recently-created match.
3. Else fall back to the kit default: most-recently-created artifact
   tagged `landscape-summary`.

Project artifact wins over kit default without any CLI flag, because
the project tag signals deliberate override. Explicit CLI flag wins
over both (escape hatch).

### CLI surface

```
team-create
  --landscape-artifact <ART-id>   # explicit override; skips discovery
```

Alias `--landscape` (existing) is kept for compatibility; both flags
resolve to the same Step-1 lookup path.

### landscape-curator compatibility

The future `landscape-curator` skill will emit artifacts with the same
`landscape-summary` tag (and optionally `landscape-summary-project`
when scoped). The three-level precedence rule already accommodates
curator-generated artifacts without schema changes — curator output is
just another tagged artifact in the index.

---

## 2. Layer 2 — Weight Overrides (DEC-*-TeamWeights)

### DecisionRecord schema

```yaml
kind: DecisionRecord
spec:
  title: "Team weight override — <project-slug> — <date>"
  state: accepted
  context: "<why this project needs non-default weights>"
  decision: "Override team-creator formula weights"
  rationale: |
    <required; at minimum one sentence per dimension changed>
  alternatives:
    - option: "Keep kit defaults (C=0.60, K=0.20, L=0.10, G=0.10)"
      rejected_because: "<reason>"
  consequences: |
    <expected effects on tier classification>
  deciders: [<ACTOR-id>, ...]
  decided_at: <ISO-8601>
  # OpenWeave extension fields:
  weight_overrides:
    C: <float>   # Capability
    K: <float>   # Cost efficiency
    L: <float>   # Latency fit
    G: <float>   # Governance
    # must sum to 1.00 ± 0.001
  applies_to: team-creator          # discriminator
```

### Discovery rule

`team-create` queries the decision index for DecisionRecords where
`spec.applies_to == "team-creator"` and `spec.state == "accepted"`,
ordered by `metadata.created` descending. The most-recently-accepted
record wins. Tag: `team-weights-override` on the DecisionRecord for
fast index lookup.

### Precedence chain

```
CLI --weight-overrides <json>
  > DEC-*-TeamWeights (most recent accepted)
    > skill defaults in references/tiering-formula.md
```

All three levels are recorded in the chartering DecisionRecord's
`inputs_snapshot.weights_source` field (values: `"cli"`,
`"dec-team-weights"`, `"skill-default"`).

### team-rebalance interaction

`team-rebalance` currently reads weights from the governing team
DecisionRecord's `inputs_snapshot.weights`. With Layer 2:

1. On startup, `team-rebalance` runs the same DEC-*-TeamWeights
   discovery query.
2. If a TeamWeights DEC exists and is newer than the governing team
   DecisionRecord, use the TeamWeights DEC weights (weight policy has
   been updated since last run).
3. Otherwise fall back to `inputs_snapshot.weights` from the governing
   team DecisionRecord.
4. CLI `--weight-overrides` always wins regardless.

The TeamWeights record is a **separate** record from the governing
team DecisionRecord — it governs policy, not a specific run.

---

## 3. Layer 3 — Tier Threshold Overrides

### Co-location decision: same DEC-*-TeamWeights record

Thresholds are co-located with weights in the single
`DEC-*-TeamWeights` record. Rationale: thresholds and weights are
coupled — changing weights without adjusting thresholds can silently
shift all roles. Keeping them in one record forces the decider to
reason about both simultaneously and produces a single audit event.
A separate `DEC-*-TeamThresholds` would allow configurations where
the two records drift out of sync, creating silent mismatches.

### Extended schema (threshold fields added to Layer 2 schema)

```yaml
  tier_thresholds:
    heavy_min: <float>    # default 0.70; TierScore >= this → heavy
    medium_min: <float>   # default 0.40; TierScore >= this → medium
                          # light is implicit: TierScore < medium_min
    rationale: |
      <REQUIRED — minimum two sentences: (1) why these thresholds
      fit this project's model set; (2) what analysis was done>
```

### Validation rules (Phase 2 must enforce)

Rejected combinations:
- `heavy_min <= medium_min` — violates tier ordering
- `heavy_min > 0.95` — leaves no practical heavy band
- `medium_min < 0.10` — effectively eliminates light tier
- `heavy_min - medium_min < 0.10` — band too narrow; rounding
  instability in real candidate sets
- Missing or empty `rationale` field — hard error, not a warning

Valid range: `0.10 ≤ medium_min < heavy_min ≤ 0.95`.

### Audit trail

The chartering team DecisionRecord records
`inputs_snapshot.tier_thresholds_source` as `"dec-team-weights"` or
`"skill-default"`, plus the actual values used.

---

## 4. Layer 4 — Role→Class Pins (role-archetypes.yaml)

### File location and format

```
context/team/role-archetypes.yaml   # project-level override
```

YAML is chosen over TOML: the kit already uses YAML for all schema
files; TOML would introduce a second config language with no benefit.

### Schema

```yaml
version: "1"
override_semantics: delta   # "delta" | "replace"
roles:
  <archetype-name>:          # must match one of the 8 kit archetypes
    tier_pin: heavy|medium|light
    rationale: |
      <REQUIRED — why this project overrides the kit default>
    clone_cap_override: <int|null>   # null = inherit project default
    override_when: []        # optional; inherits kit rules if omitted
```

### Override semantics

**`delta` (default):** Only roles listed are overridden; all other
roles inherit kit archetypes. This is the safe default — a project
that only needs to change `senior-architect` from heavy to medium
touches exactly one entry.

**`replace`:** The file is the complete archetype table. All 8 roles
must be listed; missing roles cause a validation error. Required only
if a project needs to rename or restructure the full set.

### Validation invariants (Phase 2 must enforce)

- `project-manager.tier_pin` must remain `heavy` — PM is never
  overridable (see DEC-20260414_0900).
- `project-manager.clone_cap_override` must be `null` or `1` — PM
  clone cap is immutable.
- Each role `rationale` must be non-empty.
- In `replace` mode: all 8 archetypes must appear.
- `clone_cap_override` must not exceed `--parallelism-cap` for the
  run (error: "Role X clone_cap_override N exceeds project
  parallelism-cap M").
- No two roles may share the same `tier_pin: heavy` pin unless the
  accessible heavy-tier set has at least as many models as roles so
  pinned (warn, not error; log to DecisionRecord).

### Audit trail

When `context/team/role-archetypes.yaml` is present, `team-create`
records `inputs_snapshot.archetype_override_file: "present"` and
lists each overridden role with its new pin in the chartering
DecisionRecord.

---

## 5. Agent-Driven Discovery — Trigger Phrase Table

| Layer | Trigger phrases | Routed action |
|---|---|---|
| Layer 1 — landscape | "use our own model list", "we have a custom provider set", "this project uses different models", "update the landscape for this project" | Create project-tagged landscape artifact; use `--landscape-artifact` |
| Layer 2 — weights | "we value latency more", "cost matters more here", "prioritise governance", "adjust the scoring weights", "latency is critical for this project" | `decision-record-write` a DEC-*-TeamWeights; re-run `team-create` |
| Layer 3 — thresholds | "the tier cutoffs don't fit our model set", "too many models landing in medium", "adjust the heavy threshold", "nothing is reaching heavy tier" | Amend or create DEC-*-TeamWeights with `tier_thresholds` block |
| Layer 4 — pins | "pin senior-architect to medium for this project", "we want all researchers on heavy", "remap role classes", "change the role tier assignments" | Create `context/team/role-archetypes.yaml`; re-run `team-create` |

Agents resolve these phrases via skill-finder before routing to any
layer. The trigger phrases are additive to the existing team-creator
triggers in SKILL.md (they are `skill-finder` entries, not
replacements).

---

## 6. Audit Trail Consolidation

| Override | Artifact / Record written | When |
|---|---|---|
| Layer 1 landscape | Project landscape artifact (ART-*) | Before or separate from team-create run; referenced in team DecisionRecord |
| Layer 2 weights | DEC-*-TeamWeights (tag: team-weights-override) | Before team-create; discovered at run start |
| Layer 3 thresholds | Same DEC-*-TeamWeights record | Co-located with weights |
| Layer 4 role pins | `context/team/role-archetypes.yaml` + note in chartering team DecisionRecord | File present at run time; noted in `inputs_snapshot` |
| Any run with overrides | Chartering team DecisionRecord records all sources | Every team-create / team-rebalance run |

Every run's chartering DecisionRecord is the single join point: it
records which overrides were active, their source IDs, and the
actual values applied. Querying one DecisionRecord fully reconstructs
the run's configuration.

---

## 7. Regression Gate — Kit-Default Test Fixture

Phase 2 must create:

```
context/artifacts/ART-*-OpenWeave-regression-fixture-max5x-defaults.md
```

Contents:
- Subscription: `anthropic:max-5x`
- Governance floor: 4
- Weights: `{C:0.60, K:0.20, L:0.10, G:0.10}` (kit defaults)
- Landscape artifact: ART-20260415_1525-LandscapeSummary-...
- No DEC-*-TeamWeights, no role-archetypes.yaml
- Expected tier scores per model (from Phase 3 dogfood diff)
- Expected role assignments (8 rows)

CI diff check: `team-create --dry-run` output must match this fixture
exactly. Any deviation fails the gate. This fixture is locked at
Phase 3 dogfood results and updated only intentionally.

---

## 8. Latency-Weighted Demo Artifact

Phase 2 must create:

```
context/artifacts/ART-*-OpenWeave-dogfood-latency-weighted.md
```

Invocation:
```
team-create \
  --subscription anthropic:max-5x \
  --providers any \
  --governance-floor 3 \
  --weight-overrides '{"L":0.50,"K":0.20,"C":0.25,"G":0.05}'
```

The artifact must demonstrate:
1. At least one role changes model vs the kit-default run on the
   same landscape (proves overrides move output).
2. The newly assigned model has a higher `output_tokens_per_sec` than
   the kit-default assignment for that role.
3. Tier scores are re-listed showing L-weighted rerank.
4. The chartering DecisionRecord for this run references
   `weights_source: "cli"` and records the override values.

"Visibly different" means at least 2 of the 8 role assignments change
model. If the same landscape produces identical assignments at L=0.50,
this is a finding, not a success — the fixture must call it out and
explain why (e.g. only one accessible model per tier after G-floor).
In that case, lower G-floor to 2 and re-run with broader provider set
(`--providers any`) to force tier separation.

---

## 9. Open Questions for Phase 2

1. **Index query for DEC-*-TeamWeights discovery.** Does
   `index-management` support querying on arbitrary `spec.*` fields
   (e.g. `spec.applies_to == "team-creator"`)? Or must the tag
   `team-weights-override` be the sole lookup key? If the latter,
   tag-only discovery is sufficient but fragile if tags drift.

2. **role-archetypes.yaml validation timing.** Should the override
   file be validated eagerly at `team-create` startup (before model
   scoring) or lazily at archetype-mapping time (Step 4)? Eager
   validation fails fast; lazy validation allows dry-run to show
   partial results before the constraint error. Recommendation: eager,
   because a PM pin violation should never reach the scoring stage.

3. **DEC-*-TeamWeights and team-rebalance conflict resolution.**
   If the TeamWeights DEC was created between two rebalance runs,
   the rebalance must apply the new weights. But this could silently
   change tier classifications for roles not being rebalanced.
   Should `team-rebalance` warn when TeamWeights DEC is newer than
   the governing team DecisionRecord and suggest `--roles all`?
