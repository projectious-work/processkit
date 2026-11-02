---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260509_1836-SmartPanda-team-creator-v2-design
  created: '2026-05-09T18:36:00+00:00'
spec:
  name: Design — team-creator v2 (5-gap consolidation)
  kind: design
  owner: TEAMMEMBER-cora
  produced_by: TEAMMEMBER-cora
  tags:
  - design
  - team-creator
  - team-model-v2
  - github-issue-20
  - vastvale
  produced_at: '2026-05-09T18:36:00+00:00'
---

# Design — team-creator v2 (5-gap consolidation)

> Produced by ephemeral ROLE-solutions-architect/senior on Opus 4.7 in the
> 2026-05-09 GH-issue-cluster work-down session. Companion to plan
> ART-20260509_1323-DeepSpruce. Splits VastVale (BACK-20260509_1318) into
> 5 sub-WorkItems (BACK-20260509_1836-TidyAsh, -1837-LuckyWren,
> -1837-RapidLily, -1837-SwiftReef, -1837-MerryPlum). Six owner open
> questions block SUB-1 implementation.

## Executive summary

`pk-team-create` becomes a **catalog-aware charter**, not an entity factory. It selects existing `context/roles/ROLE-*` records (51 available) by archetype mapping, opens **RoleSlot** entities (one per parallelism unit) inside a chartering Scope, assigns **TeamMembers (`type=consultant` or `type=ai-agent`)** to those slots through `role-assignment` Bindings carrying a closed `engagement_window`, and persists a `budget_projection` block in the chartering DecisionRecord. Codename surfaces ("OpenWeave", "TeamWeaver Phase 3 dogfood") collapse to plain phrasing.

Why now: v1 confuses **identity (who)** with **capacity (how many)** via `clone_cap`, duplicates the role catalog with 8 archetype Roles, and treats time-bounded engagements as permanent staff. Each gap propagates downstream — fixing them piecemeal would require two migrations.

Biggest risk: the RoleSlot primitive is new and read by `team-manager`'s resolver, `pk-team-review`, and `task-router`. A botched migration leaves orphan Bindings whose `subject` no longer resolves; the migration must be **additive then cutover**, not destructive.

## Gap-by-gap shape

### Gap 4 — Identity model (foundational, do first)

**Recommendation: Hybrid — `RoleSlot` (capacity) + `TeamMember` (identity), joined by an assignment Binding.** Aligns with the owner's lean.

**Rationale.** `clone_cap=5` on TeamMember conflates two orthogonal axes: *who am I* (persistent persona, memory, relationships) vs *how many parallel workers does this role need this sprint* (capacity planning). A `TeamMember` with personality/memory cannot be meaningfully cloned — clone-2 either shares the seed's memory (race-conditioned, breaks the A-MemGuard consensus model) or starts blank (then it's not the same persona). Splitting these axes lets:

- Pure-person TeamMembers (Cora, Finn, Bernhard) keep memory + personality intact, `clone_cap` removed.
- Capacity scaling lives on a **RoleSlot** — a charter-level reservation with no memory.
- Ephemeral worker invocations (`(role, seniority)` dispatches) map onto a RoleSlot without ever materialising a TeamMember; `task-router` resolves through the slot.

**What changes.**

*TeamMember frontmatter (`SCHEMA-team-member` v1.2.0):*

| Action | Field | Notes |
|---|---|---|
| Remove | `clone_cap`, `cap_escalation`, `is_template`, `templated_from` (currently on Role per skill body §"Canonical schema fields") | Capacity moves to RoleSlot. The fields stay readable during the deprecation window. |
| Add | `type=consultant` (enum value) | See Gap 3. |
| Add | `engaged_for` (string, nullable; ScopeID) | See Gap 3. |
| Add | `engagement_window` (object: `{starts_at, ends_at}`, nullable) | See Gap 3. |
| Keep | `default_role`, `default_seniority`, `personality`, `memory`, `relationships` | These are person-axis fields. Untouched. |

*New entity: **RoleSlot** (`SCHEMA-roleslot`, primitive layer 1, owned by `team-manager`).*

```yaml
apiVersion: processkit.projectious.work/v2
kind: RoleSlot
metadata:
  id: SLOT-<scope-slug>-<role-slug>-<rank>     # SLOT-q2-2026-software-engineer-2
spec:
  scope: SCOPE-<id>                            # the chartering Scope; mandatory
  role: ROLE-<id>                              # FK into context/roles/ catalog
  seniority: junior|specialist|expert|senior|principal
  rank: <int, 1..N>                            # 1 = primary, 2..N = parallel
  state: open | filled | closed
  filled_by: TEAMMEMBER-<slug> | null          # set when assigned
  default_model_profile: ART-*-ModelProfile-*  # optional pin (Layer 8 fallback)
  effort_floor: low|medium|high|extra-high|max # optional
  effort_ceiling: ...                          # optional
  rationale: <one-line>
  created: <ISO>
```

State machine: `open → filled → closed`. `closed` is terminal; reopening means a new SLOT-id at the next charter. Slots are **scoped to a Scope** — when the Scope closes, all open slots auto-close.

*Assignment Binding.* New binding type `role-slot-fill`:
- `subject = TEAMMEMBER-<slug>`
- `target = SLOT-<id>`
- `valid_from / valid_until = engagement_window`
- `conditions.rationale = <why this person for this slot>`

Adds `role-slot-fill` to `binding.yaml` `known_types` (additive — no breakage).

**Migration shape (v1 → v2).**

1. For each existing `Role` in `context/roles/` carrying `clone_cap=N` (the 8 archetypes): emit `N` RoleSlots under the team's chartering Scope (parent: the active project Scope). Slot `rank` 1..N.
2. For each existing `Binding(type=role-assignment)` from the v1 team: write a parallel `role-slot-fill` Binding pointing TeamMember → SLOT-rank-1.
3. v1 `role-assignment` Bindings remain readable for one minor version (deprecation window). `pk-team-review` learns to resolve through either path.
4. v0.16.0 fields (`clone_cap`, `cap_escalation`, `primary_contact`, `is_template`, `templated_from`) deleted from Role schema after the deprecation window. `primary_contact=true` for project-manager moves to `RoleSlot.rank=1` semantics.

**Resolver impact (team-manager).**

`get_interlocutor_runtime_binding` and `task-router` lookup chain becomes:

```
1. (role, seniority, scope) → query RoleSlot(scope active, role match, seniority match, state=filled)
2. RoleSlot.filled_by → TeamMember
3. TeamMember.default_seniority overrides RoleSlot.seniority for model resolution if set
4. fall through to existing 8-layer model-assignment binding precedence
```

For ephemeral dispatches (no persistent TeamMember): step 2 returns null, the slot itself carries `default_model_profile` for Layer 8 fallback.

**Breaking changes.**
- Role schema loses `clone_cap`, `cap_escalation`, `primary_contact`, `is_template`, `templated_from`. Released as `SCHEMA-role@2.2.0`; old Role files validate-warn until cutover.
- New required field on `role-assignment`-class flows: `scope` (was optional). Charters without a Scope hard-error.
- `pk-team-create` no longer writes Role entities — see Gap 1.

**Open question for owner.** Should RoleSlots be a primitive of `team-manager` (alongside TeamMember) or a new layer-1 skill `slot-management`? Recommendation: extend `team-manager` (already owns the runtime resolver; lowest skill-inflation cost). Owner confirms or splits.

### Gap 1 — Catalog integration

**Recommendation: Direct catalog consumption + Layer-4 archetype-to-catalog mapping file.** No archetype Roles are written.

**Rationale.** v1 writes 8 archetype Roles parallel to a 51-role catalog. The v2 schema (DEC-20260422_0234-BraveFalcon) already strips seniority from Role slugs — the catalog is the source of truth. A layer-5 override mechanism (the alternative) would still leave the 8 archetype Roles around; the right move is to delete the archetype Role write-step entirely.

**What changes.**

`pk-team-create` step 6 changes from "create 8 Role entities" to "select 8 catalog Roles":

| Archetype | Default catalog Role |
|---|---|
| project-manager | `ROLE-product-manager` (immutable, primary_contact=1) |
| senior-architect | `ROLE-solutions-architect` |
| senior-researcher | `ROLE-research-scientist` |
| junior-architect | `ROLE-solutions-architect` (seniority=specialist) |
| developer | `ROLE-software-engineer` |
| junior-researcher | `ROLE-research-scientist` (seniority=specialist) |
| junior-developer | `ROLE-software-engineer` (seniority=junior) |
| assistant | `ROLE-assistant` |

The archetype-to-catalog mapping is a YAML file in the kit: `assets/archetype-catalog-mapping.yaml`. Project override: `context/team/archetype-catalog-mapping.yaml` (delta or replace, same semantics as today's `role-archetypes.yaml` layer-4 override).

Two archetypes (`junior-architect`, `junior-researcher`) collapse onto the same catalog Role with a different seniority — that's correct and aligns with v2 schema (seniority is an ordinal attribute, not encoded in slug).

**inputs_snapshot extension.** `archetype_catalog_mapping_file` (kit-default | project | cli) and `archetype_catalog_overrides[]` audit fields added to the chartering DecisionRecord.

**Breaking changes.**
- v1 Roles named `ROLE-team-creator-*` (or whatever current archetype slugs are) are orphaned. Migration: end their Bindings, mark them `superseded_by` the catalog Role, leave files in place (read-only history).
- The `8-archetype assumption is hard-coded` extension-point in current SKILL.md §"New role archetype" relaxes — archetypes are now keys in the mapping file, not Role entities.

**Open question for owner.** Two archetypes (`assistant`, `junior-developer`) currently share a model in the kit defaults (§"Role archetype pin table"). Under direct catalog consumption, do they share a RoleSlot too? Recommendation: separate slots — same catalog Role, distinct RoleSlots, independent model-assignment bindings allowed.

### Gap 3 — Consultant / ephemeral TeamMember

**Recommendation: Add `type=consultant` enum value to TeamMember, with mandatory `engaged_for` (Scope) + `engagement_window`. Resolver excludes consultants outside the window. `pk-team-review` flags expired-but-active.**

**What changes.**

*Schema (SCHEMA-team-member v1.2.0):*
- `type` enum: `human | ai-agent | service | consultant`.
- New required-when-consultant fields: `engaged_for: SCOPE-<id>`, `engagement_window: {starts_at: <ISO>, ends_at: <ISO>}`. Both rejected (lint warning) for non-consultant types.
- `default_seniority` and `default_role` remain mandatory — a consultant is still a participant with role context.
- Consultants do **not** require a name-pool reservation (parallel to humans and services).
- Consultants are exportable but `export_policy.include` defaults to `[persona, card]` only — no memory leakage between engagements.

*Resolver behavior.* `get_interlocutor_runtime_binding` and `list_team_members(active=true)`:

```
filter: active=true AND (type != consultant OR
        (engagement_window.starts_at <= now <= engagement_window.ends_at))
```

Consultants outside the window are non-resolvable but not deactivated. Re-engagement: extend `engagement_window.ends_at` (write through `update_team_member`) — no new TeamMember.

*pk-team-review extension.* Adds finding code `team.consultant.expired_but_active`, severity warning. Surfaces consultants whose `engagement_window.ends_at < now` AND `active=true`. Action prompt: "deactivate or extend engagement_window".

*Existing TeamMembers.* No change. Cora, Finn, Bernhard remain `type=ai-agent` / `type=human`. Migration: none required for current TeamMembers; the field additions are additive and only required when `type=consultant`.

**Breaking changes.** None for existing data. The TeamMember schema bumps to v1.2.0; old records validate.

**Open question for owner.** When a Scope closes (e.g. `SCOPE-q2-2026 → completed`), should consultants `engaged_for` that scope auto-deactivate? Recommendation: yes — emit `team_member.auto_deactivated` event, log the closing scope as the cause. Owner can override per-consultant via `auto_deactivate_on_scope_close: false`.

### Gap 5 — Budget projection

**Recommendation: Add a `budget_projection` block to chartering DecisionRecord `inputs_snapshot`. `pk-team-review` re-computes actual spend against projection and surfaces drift.**

**Block shape.**

```yaml
spec:
  inputs_snapshot:
    # ... existing fields ...
    budget_projection:
      currency: USD
      window:
        starts_at: <ISO date>            # = chartering Scope.starts_at
        ends_at: <ISO date>              # = chartering Scope.ends_at
      projected_total: <float>           # sum of slot projections
      projection_method: heuristic | model-recommender-quote | manual
      slot_projections:                  # one row per RoleSlot
        - slot: SLOT-<id>
          role: ROLE-<id>
          seniority: <enum>
          model_profile: ART-*-ModelProfile-*
          expected_invocations_per_week: <int>
          avg_tokens_per_invocation: {input: <int>, output: <int>}
          unit_cost_usd: <float>          # from get_pricing at charter time
          projected_total_usd: <float>
      drift_threshold_pct: 20             # default; configurable via --budget-drift-threshold
      notes: <free-text>
```

**Where it sits.** Inside `inputs_snapshot`, alongside `tier_scores`. Same write path (`record_decision`), same read path (`get_decision`).

**Drift detection in pk-team-review.**

1. Query event-log entries within `window` for invocations bound to the chartering Scope's RoleSlots.
2. Sum actual cost (token counts × actual unit_cost from the time of invocation).
3. Compute `drift_pct = (actual - projected) / projected`.
4. If `|drift_pct| > drift_threshold_pct`: emit finding `team.budget.drift`, severity warning. Include per-slot drift table in the diff report.

Surfaces both over- and under-spend. Under-spend is informational (capacity planning signal); over-spend is the actionable case.

**Breaking changes.** None. Additive to `inputs_snapshot`. Old DecisionRecords without the block: `pk-team-review` skips the drift check and notes "no budget projection on file".

**Open question for owner.** Where do unit costs come from at projection time — `model-recommender.get_pricing` (live) or a stored snapshot artifact (frozen)? Recommendation: live `get_pricing` at charter time, snapshot the value into `slot_projections[].unit_cost_usd`, recompute live for actuals. Drift thus captures both volume changes and price changes; if owner wants volume-only, store `pricing_snapshot_artifact` and recompute pre-priced.

### Gap 2 — Codename rename (cheapest)

Mechanical search-and-replace in `context/skills/processkit/team-creator/SKILL.md` and likely also in `commands/`, `references/`, and the chartering DecisionRecord template. Targets:

| Codename | Replacement |
|---|---|
| `OpenWeave` (used in §"Override audit trails (OpenWeave layers 1–4)" and §"OpenWeave 4-layer override model") | `team-creator override layers` |
| `OpenWeave layers 1–4` | `override layers 1–4` |
| `TeamWeaver Phase 3 dogfood` (used in §"Tiering formula (summary)") | `the 2026-04-15 internal review` (and link to ART-20260415_1545 by ID, not code-name) |
| `ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff` (referenced by ID) | Keep the ID stable (it's already created). Rename the artifact's display title only. |
| `BraveFalcon`, `LoyalComet`, `ShinyBear`, `WiseBird`, `SpryTulip` (DEC suffixes — codenames embedded in DEC IDs) | **Do not rename.** DEC IDs are immutable references. Add a one-line gloss on first use: `"DEC-20260422_0234-BraveFalcon (the 2026-04-22 seniority-decoupling decision)"`. |

Files to scan: `context/skills/processkit/team-creator/SKILL.md` (verified), plus its `commands/*.md` and `references/*.md` (use `query_entities` / search for `OpenWeave|TeamWeaver`). Mechanical work.

**No architectural decision.** No schema change. Pure documentation pass.

## Dependency graph

```
Gap 4 (Identity / RoleSlot) ─────┬──► Gap 1 (Catalog integration)
                                 │       (catalog selection writes
                                 │        RoleSlots, not Roles)
                                 │
                                 ├──► Gap 3 (Consultant type)
                                 │       (engagement_window resolver
                                 │        sits on top of slot resolver)
                                 │
                                 └──► Gap 5 (Budget projection)
                                         (slot_projections need
                                          RoleSlot IDs to key on)

Gap 2 (Codename rename) ────────────► independent; can land any time
```

**Suggested order: Gap 4 → Gap 1 → Gap 3 → Gap 5 → Gap 2.**

- Gap 4 must land first; everything else references RoleSlot.
- Gap 1 next: smallest engineering surface once RoleSlot exists (delete archetype-Role write step, add catalog selection).
- Gap 3 then Gap 5 are independent of each other; Gap 3 chosen first because it's a schema bump (smaller blast radius than Gap 5's review-tool extension).
- Gap 2 can land in parallel with any of the above; assigned last so the rename pass sees the final SKILL.md state.

Acyclic. ✓

## Sub-WorkItem split (5)

| ID | Title | Effort | Owner role | Model class | Depends on |
|---|---|---|---|---|---|
| BACK-20260509_1836-TidyAsh | RoleSlot primitive + identity-axis decoupling | large | software-engineer/senior | deep | — |
| BACK-20260509_1837-LuckyWren | Catalog-driven pk-team-create | medium | software-engineer/senior | balanced | TidyAsh |
| BACK-20260509_1837-RapidLily | Consultant type + engagement window | medium | software-engineer/senior | balanced | TidyAsh |
| BACK-20260509_1837-SwiftReef | Budget projection + drift detection | medium | software-engineer/senior | balanced | TidyAsh, LuckyWren |
| BACK-20260509_1837-MerryPlum | Codename rename pass (mechanical) | small | technical-writer/specialist | fast | — |

Per-WorkItem scope, fields, and owner-role rationale are in each WorkItem's `description`.

## Migration sketch

**v1 → v2 migration outline (single MIG entity, multi-phase apply).**

*Affected groups.*
1. Live charters (chartering DecisionRecords with `state=accepted`).
2. Existing 8-archetype `Role` entities written by prior `pk-team-create` runs.
3. `Binding(type=role-assignment)` records pointing at those Roles.
4. TeamMember records carrying v0.16.0 fields (`is_template`, `templated_from`) — these were on Actor; double-check they didn't migrate to TeamMember in v0.19.0.

*Affected files.*
- `context/roles/ROLE-<archetype>-*.md` (the 8-or-so archetype-spawned Roles, NOT the 51-role catalog).
- `context/bindings/BIND-*-role-assignment-*.md`.
- `context/decisions/DEC-*-team-charter-*.md` (read-only; new charter writes superseding).
- `src/context/schemas/role.yaml`, `team-member.yaml`, `binding.yaml`.

*Payload approach.* Additive-then-cutover, two phases:
- **Phase A (additive, reversible):** Land RoleSlot schema + `role-slot-fill` binding type. Back-fill RoleSlots and fill-Bindings from current state. Both old and new resolution paths work.
- **Phase B (cutover, one-way):** New `pk-team-create` runs stop writing archetype Roles + role-assignment Bindings. Phase A back-fills are now canonical. Old archetype Roles get `superseded_by` set; files retained.
- **Phase C (deprecation, after 1 minor version):** Remove old code paths from resolver. Old archetype Role files can be archived to `context/archived/`.

*Rollback feasibility.* Phase A fully rollback-able (delete the new RoleSlots + fill-Bindings; old path still works). Phase B reversible by un-setting `superseded_by` and re-enabling archetype-Role writes (one minor version of risk window). Phase C non-reversible — by design.

*Out of scope for this Migration.* The 51-role `context/roles/` catalog is **untouched**. v2 selects from it; it does not modify it.

## Open questions for owner

1. **RoleSlot primitive ownership.** Extend `team-manager` (recommended) or split into a new `slot-management` skill?
2. **TeamMember v0.16.0 fields cleanup.** Confirm `is_template`/`templated_from`/`clone_cap`/`cap_escalation`/`primary_contact` should be **removed** from Role schema (not just deprecated). They were added in v0.16.0 specifically for the v1 clone model — Gap 4 obviates them.
3. **Personality/memory on consultants.** Keep on the same TeamMember schema (recommended; `engagement_window` is the only differentiator) or split consultants into a separate Profile entity? Recommend the former; the latter doubles the schema surface.
4. **Auto-deactivate consultants on Scope close** (recommended yes, with per-consultant opt-out flag).
5. **Budget unit-cost source: live `get_pricing` at charter (recommended) vs frozen pricing snapshot artifact.** Affects what "drift" means (volume vs volume+price).
6. **Mapping ambiguity for `assistant` archetype.** `ROLE-assistant` exists in the catalog — confirm it's the right target (not, e.g., a function-group-specific catalog Role).

## Out of scope (explicit)

- **Modifying the 51-role catalog under `context/roles/`.** Read-only inputs to v2.
- **Changing the tiering formula (`{C, K, L, G}` weights, normalisation, thresholds).** Untouched; layers 1–4 audit fields keep their existing semantics, only the codename ("OpenWeave") is renamed.
- **Replacing or extending `model-recommender`'s candidate landscape format.** v2 still ingests `landscape-summary` artifacts unchanged.
- **A2A Agent Card schema changes.** Consultants reuse the existing card schema verbatim.
- **Cross-project consultant sharing.** Export/import works as today (`exportable: true` per record); no new bundle format. Defer multi-project consultant directories to a future skill.
- **Refactoring `task-router`'s 8-layer model-assignment binding precedence.** RoleSlot inserts a new pre-step but does not reshape the 8 layers.
- **Adjacent issue (flagged, no sub-WorkItem):** `pk-team-rebalance --roles all` currently writes a *new* chartering DecisionRecord and supersedes the prior one; with `budget_projection` in the snapshot, sub-rebalances (`--roles <list>`) should arguably also write a new DEC instead of amending `progress_notes`. Not in scope here — record the issue, defer.
