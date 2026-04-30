---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260424_0127-QuickPine-split-sharpbrook-ship-schema
  created: '2026-04-24T01:27:55+00:00'
spec:
  title: 'Split SharpBrook: ship schema reload_schemas MCP tool in v0.21.0; defer
    PEP 723 dep drift to v0.22+'
  state: accepted
  decision: For the schema-edit half of SharpBrook, ship a small `reload_schemas`
    MCP tool on each schema-active server (workitem-management, decision-record, event-log,
    artifact-management) that calls a shared `_lib/processkit/schema.py` helper invalidating
    `load_schema` and `load_state_machine` lru_caches. For the PEP 723 dep-edit half,
    do not attempt in-process reload — the uv-resolved venv is immutable in-process
    — and instead add a pk-doctor `server_header_drift` check that hashes each server's
    PEP 723 header, compares against a manifest, and WARNs with a restart hint. Do
    not build watchdog/inotify auto-reload.
  context: 'DISC-20260424_0101-DaringBird surfaced four options. Research confirmed:
    (1) schema hot-reload is a ~20-line wrapper per server since `@lru_cache` is already
    used and the smoke test already clears caches explicitly; (2) PEP 723 dep reload
    is fundamentally impossible in-process since `uv run` resolves the venv once at
    process start; (3) offline tests already cover schema edits in under 10s so the
    runtime pain is narrow. The original WI bundled two problems without a common
    solution. Splitting matches the actual cost curves and lets v0.21.0 ship the part
    that is cheap.'
  rationale: Shared `_lib` helper keeps the tool surface small (one helper, four thin
    tool wrappers). Per-server tool placement is deliberate — servers are separate
    processes, so a cross-process admin tool cannot clear caches elsewhere. Deferring
    dep-drift detection to a pk-doctor WARN keeps v0.21.0 focused; the detection pays
    for itself independently and is additive.
  alternatives:
  - option: watchdog-based hot-reload
    why_rejected: adds dep + race risk with in-flight requests; explicit reload is
      safer
  - option: single admin MCP server that reloads all others
    why_rejected: servers are separate processes; cross-process cache-clear is not
      possible in the stdio transport
  - option: ship only the dep-drift check, skip schema reload
    why_rejected: the cheap high-value half (schema) is explicitly what the retro
      flagged
  consequences: Schema edits become observable live in ≤1 MCP call. Dep edits still
    require full harness restart, but the user gets a clear warning instead of a cryptic
    ModuleNotFound. Original SharpBrook WI is superseded by two narrower WIs.
  deciders:
  - TEAMMEMBER-cora
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas
  decided_at: '2026-04-24T01:27:55+00:00'
---
