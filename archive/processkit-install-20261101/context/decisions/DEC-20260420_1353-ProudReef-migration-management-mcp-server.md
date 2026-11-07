---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260420_1353-ProudReef-migration-management-mcp-server
  created: '2026-04-20T13:53:27+00:00'
spec:
  title: Migration-management MCP server — 5 implementation refinements within DEC-20260420_1342-WarmClover
  state: accepted
  decision: |
    1. **Naming.** Use `spec.rejected_reason` (matches existing schema at `context/schemas/migration.yaml`) — the issue text's `rejection_reason` is renamed for schema consistency; note this in SERVER.md.
    2. **Implicit start in `apply_migration`.** When called on a `pending` migration, silently walk `pending → in-progress → applied`, emitting two LogEntries (`migration.transitioned` then `migration.applied`). State machine edges validated individually; no loosening of the state machine.
    3. **Schema addition.** Add `started_at` field (ISO-8601 UTC) to `context/schemas/migration.yaml` and its `src/context/schemas/migration.yaml` mirror. Written by `start_migration` and by the implicit-start path of `apply_migration`.
    4. **INDEX.md "Notes" column preservation.** The regenerator reads the existing Applied-section rows keyed by migration ID and preserves the human-written Notes verbatim where the row already exists; for newly-applied rows it writes `spec.applied_by` + truncated `notes` parameter. Preserves the hand-crafted context that cannot be reconstructed.
    5. **Rejected section.** Add a new `## Rejected (N)` section in INDEX.md between `## Applied` and `## CLI Migrations`, rather than mixing rejected migrations into the Applied table. Visually separates terminal success from terminal failure.

    Implementation scope: both trees must land together — `context/skills/processkit/migration-management/mcp/*` and `src/context/skills/processkit/migration-management/mcp/*`, plus mirrored schema + SKILL.md + mirror entries in `src/PROVENANCE.toml`. Reference implementation: `discussion-management/mcp/server.py` (closest shape). Testing: extend `scripts/smoke-test-servers.py` with seed fixtures exercising all 5 tools.
  context: Owner-approved refinements to the migration-management MCP server shape
    established in DEC-20260420_1342-WarmClover. These five points were surfaced by
    the Plan agent's dive into the existing codebase (schema, state machine, INDEX.md
    format, reference servers) and required explicit owner sign-off before implementation
    dispatch. Owner confirmed all 5 on 2026-04-20 with the additional directive that
    implementation must land in both `context/` (installed tree) and `src/context/`
    (source-of-truth tree for downstream consumers).
  rationale: |
    (1) Schema is authoritative; renaming the issue's term avoids a second migration cycle later. (2) The issue explicitly calls out "in-progress (or pending via implicit start)" as expected behavior — matching the issue preserves the user's mental model. (3) Symmetric with `applied_at` + `rejected_reason`; without it `start_migration` would have no timestamp to record. (4) The Notes column holds information that is not reconstructable from spec fields; destroying it on each regenerate would erode trust. (5) Rejected ≠ applied; collapsing them loses signal that operators rely on when triaging history.</rationale>
    <parameter name="consequences">Implementation can proceed as a single-worker dispatch. No additional schema migrations beyond `started_at` addition. CHANGELOG entry under v0.19.0-candidate will reference both DEC-20260420_1342-WarmClover and this refinement decision. Downstream consumers (aibox) will need to pick up the schema extension when they pull v0.19.0; `started_at` is optional so existing documents stay valid (backward-compatible addition).
  deciders:
  - ACTOR-owner
  - ACTOR-pm-claude
  related_workitems:
  - BACK-20260420_1339-TidyJay-add-migration-management-mcp
  decided_at: '2026-04-20T13:53:27+00:00'
---
