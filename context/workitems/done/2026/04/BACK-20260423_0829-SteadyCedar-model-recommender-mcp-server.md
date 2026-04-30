---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260423_0829-SteadyCedar-model-recommender-mcp-server
  created: '2026-04-23T08:29:25+00:00'
  updated: '2026-04-23T09:01:57+00:00'
spec:
  title: 'model-recommender MCP server: resolve_model fails with ''No module named
    yaml'''
  state: done
  type: bug
  priority: high
  description: '**Symptom.** Calling `mcp__processkit-model-recommender__resolve_model(role="ROLE-product-manager",
    seniority="senior", team_member="TEAMMEMBER-cora", explain=True)` on the live
    MCP transport returns:\n\n    Error executing tool resolve_model: No module named
    ''yaml''\n\n**Impact.** All live model-routing calls fail. Blocks the Cora routing
    dogfood (explicit next-recommended-action from LOG-20260423_0818-ProudStone-session-handover)
    and any runtime use of the 8-layer precedence ladder. Pricing/config/list tools
    in the same server may also be affected — not yet verified.\n\n**Likely cause.**
    The `processkit-model-recommender` MCP server''s Python environment is missing
    PyYAML. Either the installer did not include PyYAML in the server''s venv, or
    the server is invoked against a Python interpreter that lacks it.\n\n**Target
    release.** v0.19.2 (treat as release-blocker — a core MCP tool is broken on downstream
    harnesses).\n\n**Reproduction.**\n1. Harness with `.mcp.json` loaded post-hand-merge
    on 2026-04-23.\n2. Call any resolve_model / explain_routing / similar routing
    tool.\n3. Server returns ImportError for `yaml`.\n\n**Suggested fix.** Add `PyYAML`
    to the server''s pyproject/requirements; verify `pk-doctor` can catch missing
    required Python deps in MCP server environments as a release-integrity check.'
  started_at: '2026-04-23T08:38:24+00:00'
  completed_at: '2026-04-23T09:01:57+00:00'
---

## Transition note (2026-04-23T08:38:24+00:00)

Root cause found: PEP 723 header in context/skills/processkit/model-recommender/mcp/server.py declares only mcp[cli] + httpx, but line 70 does `import yaml` to parse Role artifact frontmatter. Sister servers (migration-management, team-manager) correctly declare pyyaml>=6.0. Fix is a one-line addition.


## Transition note (2026-04-23T08:52:58+00:00)

Fix applied to PEP 723 header of model-recommender/mcp/server.py in both canonical (context/) and release mirror (src/context/). Added `pyyaml>=6.0` alongside existing mcp[cli] and httpx deps. Verification out-of-band (uv run --script) succeeds: resolver chain imports cleanly, yaml 6.0.3 installs. Live harness still runs the pre-fix server process; next harness restart will pick up the new env (uv caches by PEP 723 hash, so the hash change guarantees a fresh resolve). Transitioning to review for a live-transport smoke test after restart — resolve_model(role="ROLE-product-manager", seniority="senior", team_member="TEAMMEMBER-cora") should succeed.


## Transition note (2026-04-23T09:01:57+00:00)

Verified on live transport post-harness-restart: resolve_model(role="ROLE-product-manager", seniority="senior", team_member="TEAMMEMBER-cora", explain=true) returned 1 candidate (MODEL-anthropic-claude-sonnet v4.6, Layer 5 role+seniority binding) with full 8-layer trace. pyyaml loaded cleanly via PEP 723 header.
