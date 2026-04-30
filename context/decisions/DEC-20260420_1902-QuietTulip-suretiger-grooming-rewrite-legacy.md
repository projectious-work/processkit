---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260420_1902-QuietTulip-suretiger-grooming-rewrite-legacy
  created: '2026-04-20T19:02:49+00:00'
spec:
  title: SureTiger grooming — rewrite legacy WorkItems (strict schema); relax null/empty;
    exempt CLI migrations
  state: accepted
  decision: |
    Five-track grooming:

    **Track 1 — Rewrite legacy WorkItems (owner's strict choice):** map `type` to valid enum (`research→spike`, `feature→story`, `architecture→epic`, `audit→chore`); rename IDs from legacy prefixes (RES-, FEAT-, ARCH-, AUDIT-) to canonical `BACK-` via `git mv`; update `metadata.id`; update every reference across `blocks`/`parent`/`blocked_by`/`related_workitems` (WorkItems) and `related_workitems` (DecisionRecords); add `metadata.legacy_id` for audit trail. Skip `context/templates/` and LogEntry `subject` fields (history is verbatim).

    **Track 2 — Schema null/empty relaxation (owner confirmed):** extend schemas for optional object/string fields to accept `null` and `[]` as equivalent to absent. Dual-tree mirror.

    **Track 3 — CLI-migration sharding exemption:** `check_sharding.py` exempt filenames matching `^\d{8}_\d{4}_\d+\.\d+\.\d+-to-\d+\.\d+\.\d+\.md$` — aibox-CLI docs, not processkit entities. Dual-tree mirror.

    **Track 4 — Hand-fix ~17 YAML parse errors:** backtick-in-block-scalar + unquoted-colon repairs. Not fixable via MCP (parser fails). Hand-edit is the repair.

    **Track 5 — Move misplaced log + leave process rename for Phase 2:** `LOG-loyal-vale.md` → `logs/2026/04/`. Leave 5 filename-id-mismatch WARNs (processes/, artifact .summary) for pk-doctor Phase 2 rename.

    Acceptance: `/pk-doctor` returns 0 ERROR / 5 WARN; dual-tree drift guard passes.</parameter>
    <parameter name="rationale">Owner's strict-schema principle trumps PM pragmatism — the schema is the contract; legacy data adapts. Rewriting IDs is painful but one-time; leaving regex relaxed would burden every future schema author. Null/empty coercion is a JSON-Schema-pre-2019 expressivity gap and a principled schema fix. CLI-migration exemption is a code fix because those files aren't processkit entities.</parameter>
    <parameter name="consequences">~20 WorkItem files renamed; ~30 cross-entity references updated; ~2 schemas extended; 1 script +3 lines; ~17 YAML files hand-repaired; 1 log moved. Git history preserved via `git mv`. Clean baseline at 0 ERROR / 5 WARN (residual WARNs scoped to pk-doctor Phase 2).</parameter>
    <parameter name="deciders">["ACTOR-owner", "ACTOR-pm-claude"]</parameter>
    <parameter name="related_workitems">["BACK-20260420_1729-SureTiger-groom-the-153-error"]
  context: First full `/pk-doctor` run surfaced 164 ERROR / 17 WARN (LOG-20260420_1720-GentleHill-doctor-report).
    Epic BACK-20260420_1729-SureTiger tracks the sweep. PM proposed two pragmatic
    relaxations (extend WorkItem type enum with legacy values; relax blocks/parent
    regex). Owner explicitly rejected the type-enum relaxation in favor of strict
    schema conformance, but confirmed schema-relaxation for the null/empty-coercion
    family.
  decided_at: '2026-04-20T19:02:49+00:00'
---
