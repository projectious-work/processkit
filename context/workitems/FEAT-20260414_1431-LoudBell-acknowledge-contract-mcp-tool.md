---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: FEAT-20260414_1431-LoudBell-acknowledge-contract-mcp-tool
  created: '2026-04-14T14:31:00+00:00'
  labels:
    component: skill-gate
    area: enforcement
spec:
  title: Add acknowledge_contract() / check_contract_acknowledged() MCP tools on skill-gate
  state: done
  type: feature
  priority: high
  size: M
  description: >
    Extend skill-gate from prose-only to MCP-bearing. Provider-neutral
    fallback for the compliance contract that works on any harness
    speaking MCP — including harnesses without SessionStart /
    UserPromptSubmit hooks. Do NOT create a new skill; the tool lives
    on skill-gate because it is the machine-readable face of the
    existing 1% rule.
  inputs:
    - /workspace/context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md  (§1.2)
    - /workspace/context/skills/processkit/skill-gate/SKILL.md
    - /workspace/context/skills/processkit/task-router/mcp/server.py  (reference for FastMCP + ToolAnnotations pattern)
    - /workspace/context/skills/processkit/skill-finder/mcp/mcp-config.json  (reference for per-skill config shape)
    - depends-on: FEAT-20260414_1430-CleanCharter-compliance-contract-canonical-source
  deliverables:
    - context/skills/processkit/skill-gate/mcp/server.py
    - context/skills/processkit/skill-gate/mcp/mcp-config.json
    - context/skills/processkit/skill-gate/mcp/SERVER.md
    - Updated context/skills/processkit/skill-gate/SKILL.md (add provides.mcp_tools frontmatter + "How the gate is enforced" section)
  tools:
    - acknowledge_contract(version: str) -> {ok, contract_hash, contract_text, expires_at}
    - check_contract_acknowledged() -> {acknowledged: bool, contract_hash: str?, age_seconds: int?}
  success_criteria:
    - `uv run scripts/smoke-test-servers.py` passes with the new server.
    - Calling acknowledge_contract("v1") returns ok=true and writes a marker file at context/.state/skill-gate/session-<SESSION_ID>.ack containing the contract hash.
    - Calling acknowledge_contract("v999") returns ok=false with a "version mismatch" error, no marker written.
    - Calling check_contract_acknowledged after a successful acknowledge returns acknowledged=true with the matching hash; calling it in a session without a prior acknowledge returns acknowledged=false.
    - The tool's MCP description (both acknowledge_contract and check_contract_acknowledged) contains the literal string "1% rule" and is ≤300 characters including the existing text.
    - mcp-config.json follows the same shape as task-router/mcp/mcp-config.json — PEP 723 `uv run` invocation.
    - skill-gate SKILL.md frontmatter has `provides.mcp_tools: [acknowledge_contract, check_contract_acknowledged]`.
    - skill-gate SKILL.md gains a section "How the gate is enforced" documenting the prose-vs-tool split.
  out_of_scope:
    - Enforcing check_contract_acknowledged() on the write-side tools (create_workitem, record_decision, ...). That is a follow-up WorkItem once the fallback has soaked.
    - Wiring into harness MCP config (aibox responsibility — issue 6.1 in the plan).
  progress_notes: |
    Prior agent timed out after implementing server.py and mcp-config.json.
    Completion (this pass) covers SERVER.md, SKILL.md updates, smoke-test
    addition, and WorkItem closure.

    Session-id resolution: env var PROCESSKIT_SESSION_ID takes precedence;
    falls back to os.getpid() (one stdio MCP process = one session).

    Marker file path:
      context/.state/skill-gate/session-<SESSION_ID>.ack

    Marker file JSON shape (SteadyHand contract):
      {
        "contract_hash": "<sha256 hex>",
        "acknowledged_at": "<ISO-8601 UTC>"
      }
    Both fields are always present when the file is written.
    File is only written on ok=True (version match); never written on error.

    Smoke-test: syntax validated via ast.parse; full runtime exercise added
    to scripts/smoke-test-servers.py (step 9, seeds assets dir, exercises
    bad-version path, pre-ack check, valid ack, marker file presence, and
    post-ack check; acknowledge_contract + check_contract_acknowledged also
    added to the 1% rule guard bringing the total to 10 locked tools).

    Runtime dependency on processkit lib (_find_lib()) and on
    assets/compliance-contract.md existing at install time; smoke-test
    seeds the assets dir from src/ tree.

    New files:
      context/skills/processkit/skill-gate/mcp/SERVER.md
      context/skills/processkit/skill-gate/SKILL.md (updated)
      scripts/smoke-test-servers.py (updated)
  related_artifacts:
    - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
    - context/skills/processkit/skill-gate/mcp/server.py
    - context/skills/processkit/skill-gate/mcp/SERVER.md
    - context/skills/processkit/skill-gate/mcp/mcp-config.json
    - context/skills/processkit/skill-gate/SKILL.md
  related_decisions:
    - DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider
  assigned_to: ACTOR-developer
  parent: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
---
