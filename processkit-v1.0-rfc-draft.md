# RFC — processkit v1.0: greenfield ontology rebuild on parallel v1 branches

**Status:** DRAFT — awaiting derived-project owner sign-off before upstream submission
**Audience:** maintainers of `projectious-work/processkit`
**Authored from:** derived project `projectious-work-internal` (the dogfooding project)
**Source decisions:**
[DEC-DeepTide](/workspace/context/decisions/DEC-20260520_1755-DeepTide-settle-disc-briskwillow-q-i-accept.md) (rebuild authorisation),
[DEC-BraveAtlas](/workspace/context/decisions/DEC-20260608_1625-BraveAtlas-adopt-round-20-cutover-acceptance-criteria.md) (81-criterion cutover gate)
**Related upstream issues filed today:** [#74](https://github.com/projectious-work/processkit/issues/74) (pk-doctor frontmatter parser bug), [#75](https://github.com/projectious-work/processkit/issues/75) (pk-doctor credit-card false-positive)

---

## TL;DR

After a 20-round ontology discussion in our derived project, we have concluded that **processkit's current 13-primitive ontology cannot bend far enough** to cover AI-first SAFe execution at 100×5000 scale without leaking grammar concepts (Predicate, Type, Action, Attribute, Tag, Category) into the entity layer. We have authorised — internally — a **full greenfield rebuild** of the ontology to 89 concepts organised in a four-class system (T/P/D/C), composed via Jinja+YAML with a build-time `_generated/` tree.

We want to do this **upstream, on `projectious-work/processkit`**, not as a fork. The proposed shape:

1. A **`v1.x-dev` development branch** on this repository. `main` continues
   receiving only finalized v0.x.y releases throughout the rebuild.
2. A **`v1.x-pre-release` integration branch** for the pre-release tag
   stream (`v1.0.0-alpha.* → -beta.* → -rc.*`).
3. **Backport policy**: security fixes and dependency bumps flow between
   version lines as needed; no feature backports either direction.
4. **Cutover** = create `v1.x-release` from the selected prerelease state,
   validate and tag `v1.0.0` there, then merge it into `main`. Derived
   projects flip a pin in `aibox.toml`.
5. An **81-criterion acceptance gate** (75 strict + 6 soft, 8 phases) governs when v1.0.0 ships. The gate is durably recorded in our derived project as DEC-BraveAtlas; we propose adopting it upstream as the formal v1.0 release criteria.

The ontology work is fully scoped. Implementation needs upstream agreement on the branch model and a maintainer commitment to host it. **This RFC is asking for that agreement, not for upstream to take over the engineering.**

---

## 1. Why a rebuild, not an extension

### 1.1 What the current ontology cannot express cleanly

The Round-16 SAFe fit-test of our derived project's current corpus showed a **92→94 % coverage** of full-SAFe semantics with the existing 13 primitives, *but* the missing 6–8 % required pushing concepts into the wrong abstraction layer:

- **Risk, Belief, WorldFact** want to be siblings of a primitive that doesn't exist (a Proposition F/P).
- **Capability, Command, Event** are repeatedly encoded as ad-hoc fields on WorkItem or Note, even though they are first-class in any non-trivial agent system.
- **Location** (geographic, site, coordinate, logical-region, timezone) has no home; we kept synthesising it as tags.
- **Channel, Resource, Queue, Policy, Outcome, Recurrence, Skill** are similar — present in the domain, absent from the ontology.

Adding these as new D variants of existing primitives causes a separate problem: the existing primitive set already leaks grammar concepts (Predicate, Type, Action, Attribute, Tag, Category) into the entity layer, where they pretend to be first-class but are really host-language artefacts. Round 14 in our discussion dropped six of these on the floor.

So a brownfield expansion (adding new primitives atop the current 13) **doesn't fix the leak**, and a thin remodel **doesn't add the missing first-class primitives**. We need both at once.

### 1.2 Scale evidence (Round 17)

We ran a scaling analysis from 10×500 to 100×5000 (100 humans + agents operating at 5000-person enterprise scale). The new ontology survived 10× scale-up **without adding new concepts** — all enterprise SAFe needs map onto compositions of existing primitives. The scale-up cost shifts entirely to engineering (composition tooling, indexing, federation) and governance (canonical interpretation, agent training), not vocabulary.

Conclusion: **the right time to rebuild is now**, before the corpus grows past easy migration size, and before the grammar leak metastasises into more agent prompts.

---

## 2. The new ontology in one screen

### 2.1 Class system: T / P / D / C

Four classes, distinguished by what kind of thing the concept *is*:

| Class | Reading | Lifecycle | Composability |
|---|---|---|---|
| **T** | Foundational — a *kind of slot* or *meta-mechanic* (State, Transition, StateMachine, Constraint, Guard, Identity, Versioning, Ownership, Immutability, Schema, Composition, Inheritance, Uniqueness, …) | No state of their own | Reusable across kinds, often as fragments |
| **P** | Primitive — an *atomic entity kind* with its own schema, lifecycle, and persistence (WorkItem, DecisionRecord, Artifact, Capability, Command, Event, Proposition, Location, Channel, Resource, Queue, Policy, Skill, Outcome, Recurrence, …) | Yes — own state machine | Composable as parts of C |
| **D** | Discriminated variant of a P — same schema, different `kind:` enum value (`Proposition{kind=risk}`, `Container{kind=portfolio}`, `Capability{kind=disposition}`, …) | Inherits parent's lifecycle | Not separately composable; a refinement |
| **C** | Composition — a kind built by combining other primitives + T fragments (TeamMember as `C(Actor + calendar + capabilities + persona + skill-list + journal)`, ProcessSpecification, GoalSpecification, Service as `S(Capability)/C`, …) | Compound — typically named lifecycle | Composable; the building blocks of the system |

### 2.2 Final counts

| Class | Count | Notes |
|---|---:|---|
| T | 19 | Adds Inheritance + Uniqueness as F/T meta-operators |
| P | 22 | +1 Location vs Round-14 baseline |
| D | 24 | +5 Location D variants, +1 Capability{kind=disposition} (Q6 settlement), −1 TeamMember (moved to C) |
| C | 24 | +1 TeamMember (promoted from D) |
| **Total** | **89** | |

A complete row-by-row mapping is in our derived project's working file (currently untracked, will be promoted to an upstream `docs/concept-mapping/` artifact as part of Phase 1).

### 2.3 Key settlements worth flagging to upstream now

- **Service is `S(Capability)/C`** — a composition, not a new primitive. (Was tentatively flagged as F/P during early rounds; Q3 demoted it.)
- **Skill is a P primitive** — not a composition. First-class entity with its own schema and lifecycle, distinct from Capability.
- **TeamMember moves from D to C** — `C(Actor + calendar + capabilities + persona + skill-list + journal)`. Was `Actor{kind=team-member}` in v0.x; that mapping survives as a migration mapping for legacy corpora but not as the canonical shape.
- **Proposition F/P is new** and is the parent of Belief, Risk, WorldFact, WSJF-estimate, and other epistemic content. This is what closes the "Risk is just a WorkItem with a tag" anti-pattern.
- **Hierarchy stays as a named concept** even though it is `Binding{kind=parent-child}` — for mental anchor. (Q4.)
- **Position is `Binding{kind=role-slot}`** with nullable subject. (Q1.)
- **Location is new F/P** with 5 D variants (geographic-region, site, coordinate, logical-region, timezone). (Q6.)

---

## 3. Implementation mechanics

### 3.1 Composition: Jinja + YAML

Schemas live as YAML fragments under `schemas/src/`. A build-time step renders Jinja templates into a flat `_generated/*.yaml` tree that runtime tooling consumes. Composition annotations:

- `extends: parent.yaml` for C compositions
- `{% include %}` for T fragments
- `__merge: replace|concat|name-merge` for per-field merge strategy (kustomize-style, settled in I2)

**The `_generated/` tree is committed to git.** This is non-standard but deliberate: agents diff schemas frequently, and the build step would otherwise be opaque on GitHub. (Settled in I1.)

### 3.2 The build endpoint

A new MCP tool:

```python
regenerate_schemas(kinds: list | None) -> {rebuilt, unchanged, errors}
```

Both full and partial rebuilds in one signature. `aibox apply` triggers a full rebuild by default with an opt-out flag for fast iteration. (Settled in I4 + I5.)

### 3.3 Validation policy

Phase-gated:

- For a kind whose migration is complete: strict validation.
- For a kind still being migrated: tolerant validation (warn but pass).
- Per-kind validation mode is observable via MCP. (Settled in I3.)

### 3.4 Polymorphic queries

Schemas declare interfaces:

```yaml
interfaces: [Record, Versioned]
```

The indexer extends the existing FTS5 surface with interface-level grouping (no full indexer replacement). Agents query `query_by_interface(Record, …)` to get mixed-kind results — the central capability that closes the "WorkItem-vs-DecisionRecord-vs-Artifact" routing problem agents repeatedly fail at today. (Settled in I6 + I7.)

---

## 4. The git / release model

### 4.1 Branches

```
v0.x-dev ──merge──> v0.x-release ──tag v0.x.y──> main

v1.x-dev ──merge──> v1.x-pre-release ──tag v1 prereleases
                                      └─promote──> v1.x-release
                                                       └─tag v1.x.y──> main
```

`main` is the published-history branch: it receives each stable release
after its tag is created on the relevant integration branch. `v0.x-dev` is
the v0 maintenance development line and `v0.x-release` is its release and
tag authority. `v1.x-dev` is where rebuild work lands: composition tooling,
schemas, skills, MCP gateway redesign, pk-doctor rewrite, and indexer
extension. Its prereleases are integrated and tagged on
`v1.x-pre-release`.

At v1 general availability, create `v1.x-release` from the selected
prerelease state, perform final validation, tag `v1.0.0`, and merge that
release branch into `main`. Subsequent stable v1 releases follow the same
development-to-release-to-main pattern. The v0.x line remains available as
an LTS branch for slow adopters.

### 4.2 Pre-release stream

| Pre-release tag | Required acceptance-gate progress |
|---|---|
| `v1.0.0-alpha.*` | Phase 1 (ontology completeness) green; Phase 2 (tooling parity) ≥75 % |
| `v1.0.0-beta.*` | Phases 1–3 all green (incl. corpus migration); Phase 4 ≥75 % |
| `v1.0.0-rc.*` | Phases 1–5 strict green; G6 cutover-gate outstanding |
| `v1.0.0` (final) | All strict criteria pass; G6 approved; tagged on `v1.x-release`, then merged to `main` |

All pre-release tags cut with `gh release create --prerelease`, so the GitHub "Latest" badge stays on the v0.x.y line until cutover. No surprises for casual visitors.

### 4.3 Adopter opt-in

Derived projects already pin `processkit_source` in `aibox.toml`. Three lanes coexist naturally:

```toml
# Production (default)
processkit_source = { ..., ref = "v0.27.0" }

# Early adopter, alpha
processkit_source = { ..., ref = "v1.0.0-alpha.3" }

# Pre-cutover rehearsal
processkit_source = { ..., ref = "v1.0.0-rc.1" }
```

Per semver, every pre-release tag sorts strictly before `v1.0.0`, and `v1.0.0-alpha.*` is unambiguous against v0.x.y, so version resolvers and dependency tools handle this correctly with no special configuration.

### 4.4 Backport policy

- **Security fixes** flow between the relevant v0 and v1 development lines
  as soon as they land on either side.
- **Dependency bumps** flow either direction at maintainer discretion.
- **Feature work** does NOT backport in either direction. Features intended for both ontologies are implemented twice (once in v0.x idioms, once in v1.0 idioms) or deferred to v1.x.

This is intentionally tight to keep the diverging codebases legible. The 9–12 month window is long but bounded.

---

## 5. The 81-criterion cutover gate

A formal acceptance gate governs when `v1.0.0` final ships. Full text is in our DEC-BraveAtlas (rationale block); a one-screen summary:

| Phase | Criteria | Strict | Soft |
|---|---:|---:|---:|
| P0 — Pre-conditions (must hold before any code) | 5 | 5 | 0 |
| O1 — Ontology completeness | 11 | 9 | 2 |
| T2 — Tooling parity | 12 | 9 | 3 |
| C3 — Corpus migration | 10 | 10 | 0 |
| S4 — Skills & agents | 8 | 8 | 0 |
| A5 — First-ART validation (the proof) | 18 | 18 | 0 |
| G6 — Cutover decision point | 8 | 8 | 0 |
| R7 — Post-cutover stabilisation | 9 | 8 | 1 |
| **Total** | **81** | **75** | **6** |

The phase that proves the rebuild actually works is **A5 (first-ART validation)**: model a real ART end-to-end in the new ontology, run one full PI cycle (planning → execution → demo → I&A), exercise every settlement in production-shaped use. Our derived project commits B7 (test-project SAFe-for-AI track) as the pilot ART.

A few criteria worth surfacing because they affect upstream design:

- **T2.4** — `regenerate_schemas(kinds: list | None)` MCP endpoint required.
- **T2.10** — search backend must include FTS5 + interface grouping; canned-query set is a signed-off Artifact before rc.
- **T2.11** — all MCP tools must have valid Python type signatures *and* draft-2020-12 JSON Schemas that match.
- **R7.9** — new pk-doctor checks must pass a golden adversarial fixture (deliberately-invalid entities; doctor must flag every one). This criterion exists because today's upstream issues [#74](https://github.com/projectious-work/processkit/issues/74) and [#75](https://github.com/projectious-work/processkit/issues/75) demonstrated real pk-doctor false-positive and false-negative risks; we are not willing to trust the rebuilt doctor without an adversarial smoke test.

---

## 6. Concrete asks of upstream maintainers

We are asking for **five specific things**:

1. **Agreement to host the `v1.0` feature branch on `projectious-work/processkit`** (not on a fork). This is the single most important ask — everything else can be negotiated.
2. **Endorsement of the merge-to-main + v1.0.0 release model** described in §4. If you'd prefer a different release shape (separate repo, LTS branch from day one, etc.), say so before we start cutting alpha tags.
3. **Backport policy acceptance** as described in §4.4. We can iterate this if you want a different shape.
4. **A named upstream owner / contact** for the rebuild track. We are happy to do the engineering; we need someone on the maintainer side who can review the v1.0 PRs and merge them with appropriate cadence.
5. **Adoption of DEC-BraveAtlas as the formal v1.0 release-gate criteria** (or a counter-proposed gate). We do not want v1.0.0 to ship on calendar pressure; we want it to ship on the gate.

What we are **not** asking for:

- Engineering capacity from upstream (we will staff this from the derived-project side).
- Schema review during alphas (we'll iterate publicly on `v1.0`; review at beta is plenty).
- Backport of v1.0 features into v0.x.

---

## 7. Timeline (indicative)

- **Months 1–2** — Phase 1: composition tooling (Jinja + YAML build + `regenerate_schemas` MCP endpoint). First `v1.0.0-alpha.1`.
- **Months 3–4** — Phase 2: parent-promotion implementation + entity migration scripts.
- **Months 5–6** — Phase 3: C(Specification) family + Channel/Queue/Resource/Container. Beta stream begins.
- **Months 7–9** — Phase 4: skill / MCP-tool rebuild, doctor rewrite, indexer redesign. Beta → rc transition.
- **Months 10–12** — Phase 5: cutover. First ART runs on v1.0.
- **Post-cutover** — Phase 7 stabilisation (14 days minimum per R7.1). On clean exit, old processkit `context/skills/processkit/` archived; v0.x line moves to LTS posture.

These are budgets, not commitments. The gate decides when each pre-release tag ships, not the calendar.

---

## 8. Open risks and how they're mitigated

| Risk | Mitigation |
|---|---|
| Upstream rejects the v1.0 branch model | This RFC. If declined, fallback is a fork — we'd prefer not to. |
| Single decider on the derived-project side (TEAMMEMBER-bnaard) blocks gate sign-off | Acknowledged in DEC-BraveAtlas; widening the decider set is deferred but tracked. |
| pk-doctor self-referential bugs hide gate failures | R7.9 adversarial-fixture criterion + the two upstream issues filed today (#74, #75) as evidence the doctor needs hardening. |
| Corpus-migration data loss | C3.4 +5 % field-loss ceiling + C3.7 hard-reject on orphans + C3.6 LogEntry hash-immutability check. |
| Agents drift to non-canonical interpretations during transition | S4.4 multi-persona prompt update + S4.6 ≥20 canned scenarios + S4.7 <0.1 % malformed rate. |
| 9–12 month divergence between `main` and `v1.0` produces merge hell at cutover | Tight backport policy (§4.4) keeps the diverging surface bounded; final merge is a fast-forward or squash, not a long-history merge. |

---

## 9. Reference

- **DEC-DeepTide** (rebuild authorisation, 2026-05-20) — settles 6 ontology questions + 8 implementation questions; commits to parallel-implementation full-greenfield rebuild.
- **DEC-BraveAtlas** (cutover gate, 2026-06-08) — 81-criterion acceptance gate across 8 phases.
- **DISC-BriskWillow** (closed 2026-06-08) — 20-round ontology discussion that produced the new concept set.
- **Upstream issues filed 2026-06-06**: [#74](https://github.com/projectious-work/processkit/issues/74), [#75](https://github.com/projectious-work/processkit/issues/75).

---

## 10. How to respond

Open a comment thread on the GitHub Discussion that accompanies this RFC. We'll iterate on §6 specifically; the ontology and gate are settled on our side but the upstream / release model is genuinely up for negotiation.

— derived project `projectious-work-internal`
