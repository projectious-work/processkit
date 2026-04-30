---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260424_0101-WiseLily-how-do-we-allow
  created: '2026-04-24T01:01:42+00:00'
  updated: '2026-04-24T01:29:05+00:00'
spec:
  question: How do we allow data-repair of malformed append-only LogEntries without
    breaking the append-only invariant — data-fix migration kind, log_event --repair
    override, pk-doctor autofix, or all three?
  state: resolved
  opened_at: '2026-04-24T01:01:42+00:00'
  participants:
  - TEAMMEMBER-cora
  outcomes:
  - DEC-20260424_0128-BrightHawk-narrow-snappybird-ship-pk
  closed_at: '2026-04-24T01:29:05+00:00'
---

## Context

During the v0.19.2 cycle, `LOG-20260422_1643-CalmAnt-workitem-created.md` was written by a pre-TeamMember MCP server without populating the required `actor` field. `pk-doctor --category=schema_filename` reported a schema ERROR. LogEntries are declared `append_only: true` and `log_event` only creates new entries — there is no MCP path to repair an existing malformed LogEntry. Fix had to be a direct hand-edit (tolerated because the file was already schema-invalid, but still friction and still technically a contract violation).

Scope: WorkItem BACK-20260424_0038-SnappyBird-data-repair-path-for.

## Options under consideration

1. **Data-fix migration kind** — extend `migration-management` with a new migration kind that declares a repair, routes through a review gate, and applies as a proper channel. Preserves append-only by routing all repairs through migrations/ (which are an allowed write surface).
2. **`log_event --repair=<existing_id>` flag** — overwrite a single malformed entry in place, auto-appending a `repaired_from` field that points at a *new* log entry recording the repair. Narrow, purpose-built; easier to audit per-repair.
3. **pk-doctor `--fix=schema_filename` path** — offer to patch known-safe missing fields (e.g. `actor: system` for pre-TeamMember logs). Only covers well-known failure modes; low risk but limited scope.
4. **Combination** — (3) for the narrow retroactive sweep that already exists today; (1) as the general-purpose future mechanism; (2) avoided as it blurs append-only semantics.

## Key questions

- Is "append-only" semantically about the file or about the *history* (file + any repair entries)? Answer determines whether (2) is acceptable.
- For (1), what does the review gate look like — an interactive prompt, a DecisionRecord, a scope owner signing?
- Audit-trail question: must a repair emit a new LogEntry itself, and how do we prevent repair-of-repair recursion?
- Backward compatibility: should the in-place patch format match the current schema exactly or introduce a marker field (`repaired: true`)?
- How rare is this really — is this a one-off from a pre-TeamMember schema drift, or do we expect more?

## Done when

Discussion emits one or more outcomes that scope the v0.21.0 implementation of SnappyBird concretely — ideally with a clear rule on whether append-only is preserved and a single chosen approach.
