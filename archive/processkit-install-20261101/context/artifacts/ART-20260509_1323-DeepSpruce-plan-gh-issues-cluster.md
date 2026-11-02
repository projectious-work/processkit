---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260509_1323-DeepSpruce-plan-gh-issues-cluster
  created: '2026-05-09T13:23:40+00:00'
spec:
  name: 'Plan: resolve 7 GitHub-issue WorkItems with hybrid role-based dispatch'
  kind: design
  owner: TEAMMEMBER-cora
  produced_by: TEAMMEMBER-cora
  tags:
  - plan
  - github-issues
  - agent-dispatch
  - v1-drift
  - team-model-v2
  produced_at: '2026-05-09T13:23:40+00:00'
---

# Plan — resolve 7 GitHub-issue WorkItems

Implementation plan for the seven backlog WorkItems triaged from GitHub
issues #17–#23 (processkit repo). Drafted in session of 2026-05-09
following `/pk-resume` and migration cleanup.

## 1. Roster for this initiative

Per the v0.19.0 team model (`DEC-20260422_0234-LoyalComet`), persistent
TeamMembers are kept minimal; everything else dispatches via
`(role, seniority)` and `model-recommender.resolve_model()`. Hybrid
chosen for this initiative:

| Member / Role                                  | Identity                  | Seniority  | Model profile      | Resolved primary model | Used for                                                            |
|------------------------------------------------|---------------------------|------------|--------------------|------------------------|---------------------------------------------------------------------|
| Cora (PM)                                      | `TEAMMEMBER-cora`         | senior     | (PM coordination)  | Sonnet 4.5 (xl)        | Wave kickoff, triage, status updates, decision sweeps               |
| Finn (engineer)                                | `TEAMMEMBER-finn`         | senior     | code-balanced      | Sonnet 4.5 (xl)        | All recurring engineering across the 7 WorkItems                    |
| Tech-writer (ephemeral)                        | dispatch                  | specialist | general-fast       | Haiku 4.5 (m)          | SKILL.md docs, AGENTS.md template edits                             |
| Solutions architect (ephemeral)                | dispatch                  | senior     | general-deep       | Opus 4.7 (xxl)         | Design synthesis for #20 (team-creator v2) only — bounded budget    |
| AI-research-scientist (ephemeral, optional)    | dispatch                  | senior     | research-deep      | Opus 4.7 (xxl)         | Compliance-contract sentiment rewrite for #18 — short bounded burst |

Owner (`TEAMMEMBER-thrifty-otter`) makes go/no-go calls at wave
boundaries.

## 2. Three thematic clusters

The seven issues partition into three clusters with strong intra-cluster
coupling:

### Cluster A — agent-dispatch (`#17`, `#18`, `#19`)
Symptoms of one root cause: the compliance contract leans on negative
imperatives, contains no positive sub-agent-dispatch clause, and is
amplified per-turn by Claude-Code-shaped hooks. The three WorkItems
should land together so the contract rewrite, the new positive clause,
and the harness changes ship as one coherent shift.

### Cluster B — v1-drift (`#21`, `#22`, `#23`)
Surfaced together during the aibox v0.25.6 release re-plan loop. `#23`
(documenting the 6 missing pk-doctor check modules) unblocks `#22`
(adding `v1_entity_drift` — the existing `v2_contracts.py` /
`context_hygiene.py` may already cover parts). `#21` (router
down-weight) is independent code work but pairs with the doctor check
in user-visible behavior.

### Cluster C — team-model-v2 (`#20`)
Standalone epic. Five surfaced gaps in `team-creator` (catalog
duplication, codenames, no consultants, person/clone confusion, no
budget model) — large enough to potentially split into 5 sub-WorkItems
during its own discovery step.

## 3. Sequencing — four waves

Selected to maximize early Haiku/Sonnet usage and defer Opus until the
synthesis-heavy wave is unavoidable.

### Wave 1 — quick docs (Haiku-heavy, ~1 session)
- **`#23` — pk-doctor SKILL.md docs** (BACK-…-FierceIvy)
- Outcome: documents the 6 missing check modules; unblocks Wave 2.

### Wave 2 — v1-drift code work (Sonnet-only, ~1–2 sessions)
- **`#21` — router v1 down-weight** (BACK-…-WarmOak)
- **`#22` — pk-doctor `v1_entity_drift` check** (BACK-…-KindSpruce)
- Outcome: clean tooling for v2-only project hygiene before tackling
  the higher-stakes contract changes.

### Wave 3 — agent-dispatch coherent shift (mixed, ~2–3 sessions)
- **`#18` — contract sentiment rebalance** (BACK-…-NobleLeaf) —
  starts the wave; brief Opus burst for the rewrite + bounded
  Sonnet review.
- **`#17` — TeamMember-based sub-agent dispatch enforcement**
  (BACK-…-WildPanda) — adds the positive clause produced in `#18`,
  plus router/doctor changes (P1, P2, P3, P5).
- **`#19` — Claude Code harness knobs** (BACK-…-DaringRaven) —
  ships the harness-side counterparts to the contract changes
  (compliance-refresh skill migration, skillOverrides, hook slim).
- Outcome: contract, primitives, and harness all aligned.

### Wave 4 — team-creator v2 epic (Opus-bounded, ~3–5 sessions)
- **`#20` — team-creator 5 design gaps** (BACK-…-VastVale)
- First step: split the epic into ≤5 sub-WorkItems with explicit
  owners. Then per-gap design + implementation.
- Outcome: single Opus burst for design synthesis, then Sonnet for
  per-gap implementation.

## 4. Per-WorkItem assignment table

| Wave | WorkItem ID                                     | GH  | Title                                                        | Owner                       | Effort   | Depends on |
|------|-------------------------------------------------|-----|--------------------------------------------------------------|-----------------------------|----------|------------|
| 1    | BACK-20260509_1318-FierceIvy                    | #23 | pk-doctor SKILL.md docs                                      | tech-writer/specialist (eph.) | small    | —          |
| 2    | BACK-20260509_1318-WarmOak                      | #21 | Router v1 down-weight                                        | TEAMMEMBER-finn (SE/senior) | medium   | —          |
| 2    | BACK-20260509_1318-KindSpruce                   | #22 | pk-doctor `v1_entity_drift` check                            | TEAMMEMBER-finn (SE/senior) | medium   | #23        |
| 3a   | BACK-20260509_1317-NobleLeaf                    | #18 | Contract sentiment rebalance                                 | ai-research-scientist/senior (eph.) + TEAMMEMBER-finn | medium   | —          |
| 3b   | BACK-20260509_1317-WildPanda                    | #17 | Force TeamMember-based sub-agent dispatch                    | TEAMMEMBER-finn (SE/senior) | large    | #18        |
| 3c   | BACK-20260509_1317-DaringRaven                  | #19 | Make processkit regulations 'louder' in Claude Code          | TEAMMEMBER-finn (SE/senior) | large    | #17, #18   |
| 4    | BACK-20260509_1318-VastVale                     | #20 | team-creator v2 — 5 design gaps                              | solutions-architect/senior (eph., design) + TEAMMEMBER-finn (impl) | xl       | —          |

Cora is implicit on every row as PM coordinator (kickoff, status,
decision sweeps); not listed in the owner column to keep the table
focused on the doer.

## 5. Token-budget projection

Targets from `context/team/roster.md` (xxl ≈ 5%, xl+l ≈ 85%, m+s ≈
10%) hold across the initiative end-to-end:

| Wave | Sonnet share (xl) | Haiku share (m) | Opus share (xxl) | Notes |
|------|-------------------|-----------------|------------------|-------|
| 1    | ≈ 20%             | ≈ 75%           | ≈ 5%             | Haiku writes the docs; Cora reviews on Sonnet |
| 2    | ≈ 90%             | ≈ 5%            | ≈ 5%             | Pure code work on Sonnet |
| 3    | ≈ 75%             | ≈ 5%            | ≈ 20%            | Opus burst for #18 contract rewrite, then Sonnet |
| 4    | ≈ 60%             | —               | ≈ 40%            | Design synthesis is Opus-heavy by nature; bound it |
| Mix  | ≈ 80%             | ≈ 10%           | ≈ 10%            | Within the ±10pp tolerance band |

If Wave 3 or 4 drifts beyond the ±10pp band, Cora surfaces it to the
owner before continuing.

## 6. Open questions / out-of-scope

- **Out-of-scope here:** P4 from `#17` (aibox-side PreToolUse hook to
  block bare `Agent()` dispatches) — belongs in the aibox repo;
  filed as a peer issue once `#17`'s P1 lands.
- **Open question:** for `#20`, do we ship a v2 of `team-creator`
  in-place or fork it as `team-planner` and deprecate v1? Decide at
  Wave-4 kickoff.
- **Open question:** for `#19` recommendation 1 (migrate compliance
  block from per-turn hook to once-per-session skill), this is a
  significant behavior shift — owner approval needed before
  implementation, not just at the WorkItem boundary.

## 7. Session-handover note

Container will be rebuilt after this session. On restart:
1. `/pk-resume` to confirm zero pending migrations and load this plan.
2. Start with Wave 1 (`#23` docs work) — short, validates the
   tech-writer/specialist dispatch path on Haiku.
3. Cora coordinates wave-by-wave, surfaces decisions for owner approval.
