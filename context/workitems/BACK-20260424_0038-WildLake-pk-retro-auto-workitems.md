---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0038-WildLake-pk-retro-auto-workitems
  created: '2026-04-24T00:38:25+00:00'
  updated: '2026-04-24T00:59:06+00:00'
spec:
  title: pk_retro --auto-workitems fails with "No module named 'mcp'"
  state: review
  type: bug
  priority: low
  assignee: TEAMMEMBER-cora
  description: "**Reproduction (v0.19.2 session):** running `uv run context/skills/processkit/retrospective/scripts/pk_retro.py\
    \ --release v0.19.2 --auto-workitems` emits:\n\n    [pk-retro] WARNING: in-process\
    \ MCP loader failed: No module named 'mcp'. Use --dry-run to preview or --no-mcp\
    \ to skip.\n\n`--dry-run` works fine and produces the expected retro body, but\
    \ the action-items-as-WorkItems path is unusable from the script.\n\n**Root cause\
    \ (suspected):** the PEP 723 header of `pk_retro.py` either (a) doesn't declare\
    \ the `mcp` dep or (b) the in-process loader is looking for an `mcp` Python package\
    \ that isn't shipped by the standard processkit uv env.\n\n**Done criteria:**\n\
    - `--auto-workitems` completes and creates proposed WorkItems via the same MCP\
    \ path that `/pk-work` would use.\n- OR the script prints a clear \"you must run\
    \ X to enable --auto-workitems\" hint rather than a raw ModuleNotFoundError.\n\
    \n**Target:** v0.19.3 or next release. **Owner:** cora."
  started_at: '2026-04-24T00:53:42+00:00'
---

## Transition note (2026-04-24T00:53:42+00:00)

Picked up for v0.20.0 implementation per DEC-GentleDove.


## Transition note (2026-04-24T00:59:06+00:00)

Fix: added mcp[cli]>=1.0 and jsonschema>=4.0 to pk_retro.py PEP 723 header. Loader smoke-tested end-to-end (returns 3 callables: create_artifact, log_event, create_workitem). 4/4 TestProductionMcpLoader tests pass when run with the new env. Mirrored to src/context/. Drift guard green.
