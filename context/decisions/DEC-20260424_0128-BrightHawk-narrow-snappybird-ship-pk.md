---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260424_0128-BrightHawk-narrow-snappybird-ship-pk
  created: '2026-04-24T01:28:13+00:00'
spec:
  title: 'Narrow SnappyBird: ship pk-doctor --fix=schema_filename for CalmAnt-class
    only; do not build general data-fix migration kind'
  state: accepted
  decision: 'For SnappyBird, do not build a general data-fix migration kind. Instead
    (1) add a `run_fix` function to `pk-doctor/scripts/checks/schema_filename.py`
    that applies known-safe narrow patches — initially only `actor: system` for pre-TeamMember
    LogEntries missing the required `actor` field — gated behind the existing `--fix`
    opt-in; (2) add a two-line AGENTS.md note declaring that direct edit of a schema-invalid
    LogEntry is permitted for known-safe patches, committed with a clear reference.
    Revisit the general migration-kind path only if more than two similar repairs
    are needed in a calendar quarter.'
  context: 'DISC-20260424_0101-WiseLily surfaced four options. Research confirmed
    CalmAnt is the only malformed LogEntry in 252 files — a one-off from the pre-TeamMember
    schema-drift window (v0.19.2 or earlier) that is now closed. `append_only: true`
    is already a soft convention, not MCP-enforced, so a hand-edit doesn''t break
    a technical invariant. pk-doctor''s aggregator already dispatches `run_fix` if
    present. A general data-fix migration kind would require new schema additions,
    new gate wiring, and a new MCP tool — meaningful surface for a hypothetical future
    recurrence.'
  rationale: 'YAGNI + cost ratio: single known instance, no evidence of recurrence,
    schema drift that caused it is already fixed. The narrow `--fix=schema_filename`
    path is ~2 hours and targets the exact pattern we saw. The general migration kind
    is ~2 days of design + build. If the rare case becomes common we can always build
    the general path then — the narrow fix is not load-bearing and can be replaced.'
  alternatives:
  - option: build the general data-fix migration kind
    why_rejected: premature abstraction for a one-off; ~2 days of build for a hypothetical
      future
  - option: log_event --repair=<id> override
    why_rejected: blurs the append-only convention for a single case; the convention
      is more valuable intact
  - option: do nothing, leave hand-edit as the only path
    why_rejected: missing the AGENTS.md note leaves ambiguity; the narrow run_fix
      is so cheap it's worth having
  consequences: Future repairs of the CalmAnt-class pattern are one `--fix` call away.
    The AGENTS.md note removes ambiguity about whether hand-edits of schema-invalid
    logs are allowed. SnappyBird WI is superseded by one narrow replacement WI. We
    trade a theoretical-completeness win for a realized-scope win.
  deciders:
  - TEAMMEMBER-cora
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260424_0038-SnappyBird-data-repair-path-for
  decided_at: '2026-04-24T01:28:13+00:00'
---
