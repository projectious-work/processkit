---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260426_1622-FierceOwl-v0-23-1-release
  created: '2026-04-26T16:22:23+00:00'
  updated: '2026-04-26T19:18:11+00:00'
spec:
  title: v0.23.1 — release-audit cleanup (106 ERRORs across 3 buckets)
  state: done
  type: epic
  priority: medium
  description: |
    First-run release-audit on v0.23.0 surfaced 106 ERRORs + 3 WARNs.
    Triage groups them into three workstreams, all collapsible into a
    single content-only v0.23.1 patch release.

    ## Findings by error code

    | code | count | bucket |
    |---|---|---|
    | skill.missing-field (metadata.processkit.layer) | 76 | B (real fixes) + C (policy) |
    | entity.no-frontmatter | 16 | A1 (validator gap) |
    | skill.missing-section | 3 | C (real fixes) |
    | entity.wrong-api-version | 3 | A2 (validator gap) |
    | entity.missing-metadata-id | 3 | A2 |
    | entity.unknown-kind (Persona) | 2 | A2 |
    | entity.id-filename-mismatch | 2 | A2 |
    | entity.missing-kind | 1 | A2 |

    ## Bucket A — Validator gaps (27 ERRORs, mostly false positives)

    **A1. Migration prose docs (16 ERRORs)** — Every `*-to-*.md` aibox CLI
    migration document under `context/migrations/` (14 historical + today's
    `20260426_1811_0.20.0-to-0.21.1.md`) plus `INDEX.md` are flagged for
    missing frontmatter. They are prose, not Migration entities. Real
    Migration entities live in `pending/MIG-RUNTIME-*.md` and DO have
    frontmatter. Fix: teach release-audit to excludelist the `*-to-*.md`
    and `INDEX.md` patterns under `context/migrations/`.

    **A2. Team-member alt schema (11 ERRORs across 8 files)** — The
    team-manager skill stores team members as a directory with three
    file types: `team-member.md` (TeamMember entity), `persona.md`
    (Persona kind), and `relations/<other-slug>.md` (Persona-related).
    The validator does not model: (a) `kind=Persona` as a registered kind,
    (b) the `team-member.md` filename stem → `TEAMMEMBER-{slug}` mapping,
    (c) the `relations/` subdirectory layout. Fix: extend the entity
    walker to understand the team-member directory convention.

    ## Bucket B — Real content fixes for processkit-category skills (7 ERRORs)

    7 processkit SKILL.md files lack `metadata.processkit.layer`:
    model-recommender, skill-builder, skill-finder, skill-gate,
    skill-reviewer, task-router, team-creator. Each has computable layer
    from declared `uses:` deps. Backfill in source.

    Plus 3 missing-section ERRORs (also real bugs, also real fixes):
    - team-creator: missing `## Full reference`
    - team-manager: missing `## Overview` AND `## Full reference`

    ## Bucket C — Layer policy for non-processkit skills (69 ERRORs)

    69 SKILL.md files outside `context/skills/processkit/` lack
    metadata.processkit.layer (engineering: 39, devops: 11, data-ai: 11,
    design: 5, documents: 3). These are reference/library-style skills with
    no compositional deps on processkit core. Two viable approaches:

    - Make `metadata.processkit.layer` optional for non-processkit category
      skills (validator change; no content edits needed)
    - Backfill all 69 with explicit layer values (content-only; tedious;
      semantically debatable)

    Recommendation: make optional. Layer is a processkit-DAG concept; it
    does not apply to library-style skills outside the processkit layer
    graph.

    ## Action items (proposed v0.23.1 scope)

    1. release-audit: add `entity_files` excludelist for `*-to-*.md` and
       `INDEX.md` under `context/migrations/` (closes A1, -16 ERRORs)
    2. release-audit: extend `entity_files` to model the team-member
       directory layout — register `Persona` kind, special-case
       `team-member.md` stem, walk `relations/` subdir (closes A2,
       -11 ERRORs)
    3. release-audit: make `metadata.processkit.layer` optional for skills
       where `metadata.processkit.category != "processkit"` (closes C,
       -69 ERRORs)
    4. Backfill `metadata.processkit.layer` on the 7 processkit SKILL.md
       files (closes part of B, -7 ERRORs)
    5. Add the missing `## Overview` and `## Full reference` sections to
       team-creator and team-manager SKILL.md (closes rest of B, -3 ERRORs)

    Net: 0 ERRORs / 3 WARNs (the 3 missing-dir WARNs are project-level —
    processkit doesn't currently use actors/scopes/gates entity dirs).

    ## Open design decision (DR pending)

    The split between "teach validator about reality" (A + C) vs "fix
    content to match validator" (B) is a cross-cutting recommendation. A
    DecisionRecord should be filed before code work starts, capturing
    the validator-strictness vs content-correctness tradeoff and the
    specific allowlist/optional-field rules being added.

    ## Sources

    - pk-release-audit run output (2026-04-26)
    - prior session handover next_recommended_action
  started_at: '2026-04-26T17:46:23+00:00'
  completed_at: '2026-04-26T19:18:11+00:00'
---

## Transition note (2026-04-26T17:46:23+00:00)

Starting v0.23.1 release-audit cleanup. Approach (b): roll incidental fixes (pk-doctor drift parser, drift-script provenance allowlist, PROVENANCE.toml stamping for GH#13) into FierceOwl commits.


## Transition note (2026-04-26T19:18:08+00:00)

All 5 action items shipped in commit 2f3b7c5: validator changes (A1/A2/C — closes 96 ERRORs), 7 SKILL.md layer-field backfills, team-creator + team-manager section additions. Tests 24/24 pass. Final pk-release-audit: 0 ERROR / 3 WARN / 999 INFO.


## Transition note (2026-04-26T19:18:11+00:00)

Reviewed and accepted. Closing for v0.23.1 release.
