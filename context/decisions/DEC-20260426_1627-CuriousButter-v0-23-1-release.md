---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260426_1627-CuriousButter-v0-23-1-release
  created: '2026-04-26T16:27:13+00:00'
  updated: '2026-04-26T19:00:01+00:00'
spec:
  title: v0.23.1 release-audit cleanup — hybrid validator + content approach
  state: superseded
  decision: |
    For the 106 ERRORs surfaced by first-run release-audit on v0.23.0, ship a single content+code v0.23.1 patch with a hybrid fix:

    1. **Validator changes (closes 96 ERRORs):**
       a. Excludelist `*-to-*.md` and `INDEX.md` under `context/migrations/` in the `entity_files` walker (closes 16 A1 false positives — these are aibox CLI prose docs, not Migration entities).
       b. Teach the `entity_files` walker about the team-member directory layout: register `Persona` kind, special-case the `team-member.md` filename stem → `TEAMMEMBER-{slug}` mapping, and walk `relations/` subdirs as Persona-related (closes 11 A2 false positives).
       c. Make `metadata.processkit.layer` optional when `metadata.processkit.category != "processkit"` (closes 69 C false positives — non-processkit skills are library-style with no processkit-DAG deps).

    2. **Content fixes (closes 10 ERRORs):**
       a. Backfill `metadata.processkit.layer` on the 7 processkit-category SKILL.md files lacking it (model-recommender, skill-builder, skill-finder, skill-gate, skill-reviewer, task-router, team-creator); compute each from declared `uses:` deps.
       b. Author the missing `## Full reference` section in team-creator and the missing `## Overview` + `## Full reference` sections in team-manager.

    Net: 106 ERROR → 0 ERROR; 3 WARN unchanged (project doesn't currently use actors/scopes/gates entity dirs — informational).

    Both `context/` and `src/context/` mirrors are updated for every code or SKILL.md change.</decision>
    <rationale>The 96 false-positive findings are validator over-strictness (aibox migration docs and team-member alt schemas pre-date the validator; library-style non-processkit skills are deliberately outside the DAG layer model). Mass-backfilling 76 layer fields on skills that don't participate in processkit's compositional layer graph would add noise without semantic benefit. The 10 real findings (7 layer fields on processkit-core skills + 3 missing required sections on team-creator/team-manager) are unambiguous content debt and ship-blocking quality issues that should be fixed.

    Splitting at the natural boundary — `category == "processkit"` enforces strict, others optional — preserves the validator's enforcement value where it matters (the processkit DAG) without forcing a model on every reference skill.</rationale>
    <context>First-run pk-release-audit on v0.23.0 surfaced 106 ERROR / 3 WARN / 903 INFO. Triage groups them into 8 error codes across 3 root causes (validator gaps, real layer-backfill needs, real missing-section bugs). Owner accepted the hybrid recommendation in the same session. WorkItem BACK-20260426_1622-FierceOwl carries the full triage and action items.</context>
    <consequences>release-audit becomes more permissive in two specific, documented ways (migration-doc allowlist + team-member layout awareness + optional layer outside processkit category). The strict layer enforcement is preserved for the processkit DAG (where layer composition matters). Future skills outside category=processkit can omit layer without an audit failure. Future Migration entities continue to require frontmatter (only `*-to-*.md` and `INDEX.md` are allowlisted). The 3 unaddressed WARNs (missing actors/scopes/gates dirs) become the next-most-visible issue — flag for v0.24.0 if those entity kinds get used.</consequences>
    <alternatives>[{"option": "Pure content fix", "description": "Backfill metadata.processkit.layer on all 76 SKILL.md files; add frontmatter to all 16 migration prose docs; rewrite team-member files to the standard schema.", "rejected_reason": "Forces the processkit DAG layer model onto library-style skills where it has no semantic meaning; creates 76 mechanical edits across 5 categories of unrelated skills; rewriting team-member alt schema breaks the team-manager skill's documented sub-file layout."}, {"option": "Pure validator relaxation", "description": "Make metadata.processkit.layer optional everywhere; add no entity-walker awareness for team-member dir.", "rejected_reason": "Loses real enforcement value for the processkit core DAG (where layer composition is load-bearing) and silently swallows the 10 real content bugs (7 layer + 3 missing sections)."}, {"option": "Split into two releases", "description": "v0.23.1 ships validator changes only; v0.23.2 ships content backfill.", "rejected_reason": "No technical reason to split — the changes are independent and small. Two releases doubles release overhead for no incremental signal."}]</alternatives>
    <deciders>["TEAMMEMBER-thrifty-otter"]</deciders>
    <related_workitems>["BACK-20260426_1622-FierceOwl-v0-23-1-release"]</related_workitems>
    <state>accepted</state>
    </invoke>
    <invoke name="Read">
    <parameter name="file_path">/workspace/context/skills/processkit/release-audit/scripts/release_audit.py
  decided_at: '2026-04-26T16:27:32+00:00'
  related_workitems:
  - BACK-20260426_1622-FierceOwl-v0-23-1-release
  superseded_by: DEC-20260426_1859-MightyRobin-v0-23-1-release
---
