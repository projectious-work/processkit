---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260411_1738-DeepBadger-what-is-the-right
  created: '2026-04-11T17:38:24+00:00'
  updated: '2026-04-11T17:57:54+00:00'
spec:
  question: What is the right architecture for a `task-router` MCP server that reliably
    maps task descriptions to processkit skills, process overrides, and MCP tools?
  state: active
  opened_at: '2026-04-11T17:38:24+00:00'
  outcomes:
  - DEC-20260411_1738-BraveStream-build-task-router-mcp
---

# Task-Router Design: Research Summary and Proposal

## Problem Statement

processkit agents reliably load the wrong skill (or no skill) because:
1. Session-start prose instructions (AGENTS.md) suffer context drift in long sessions.
2. skill-finder's trigger-phrase table is useful but requires the agent to choose to consult it.
3. `context/processes/` process overrides are invisible to the skill lookup chain — no link from skill → process override exists.
4. MCP tool prerequisite prompts (Track C) help per-turn but don't solve the initial routing problem.

## Five-Track Remediation Already Applied

- **Track A**: skill-finder MCP server (`find_skill`, `list_skills`) — implemented and smoke-tested.
- **Track B**: skill-gate meta-skill — 1% rule, provider-neutral prose, decision graph, rationalization pre-emption.
- **Track C**: Prerequisite sentences added to all 20 entity-mutating MCP tool docstrings.
- **Track D**: AGENTS.md slimmed from 337 → 88 lines; load-bearing items preserved.
- **Track E**: One-sentence imperative description convention enforced; skill-builder and skill-reviewer updated.

## Remaining Gap: Process Overrides

Agents following skill-finder reach the right generic skill (e.g., `release-semver`) but have no reliable signal to then check `context/processes/release.md` for the project-specific overrides. Three proposed levels:
1. AGENTS.md pointer (done).
2. Step 0 added to process-category skills: "check context/processes/<name>.md first."
3. `find_skill()` returns a `process_override` field alongside the skill match.

## Research Findings (External Sources)

### MetaMCP
NOT a semantic router. Purely mechanical aggregation with namespace prefixing (`{Server}__{tool}`). Key lessons: (a) `{server}__{tool}` is the de facto collision-free naming standard; (b) Namespace → Middleware pipeline pattern (filter inactive tools before LLM sees them) is directly applicable.

### PulseMCP Router (adamwattis)
Config-driven Rust aggregator. Purely mechanical. Key insight from PulseMCP community: "any tool matching algorithm will never match LLM inference performance, AS LONG AS the context window is constrained." Recommended pattern: agentic server-selection as a discrete step — select server first, then expose only that server's tools.

### MasRouter (ACL 2025, arxiv 2502.11133)
Academic multi-agent routing. Three-controller cascade: (1) Collaboration Mode Determiner (variational latent model), (2) Role Allocator (structured probabilistic cascade), (3) LLM Router (multinomial over backbone LLMs). Key insight: routing decisions are made by lightweight proxy networks, NOT by the main LLM — making routing millisecond-cheap. The specific ML machinery is academic overkill; the cascaded coarse-to-fine pattern is directly applicable.

### Tool-Schema-as-Always-Available-Context
Tool schemas are re-injected by the harness every API call — this is a harness property, not an MCP protocol property. The claim that "schemas survive context saturation" is technically wrong but operationally valid: the harness re-supplies them even if the model context rolls over. Token cost is severe: MCP costs 4–32x more tokens than CLI; 43 tool definitions can consume 20% of context window. Anthropic's `defer_loading: true` + Tool Search Tool (BM25/regex) reduces context 85% and improves accuracy from 49% → 74%. Elastic Path's four-layer pattern: Optimizer (pattern match, no LLM) → Router (LLM for ambiguous) → Tool Groups (domain clusters) → Single Endpoint.

## Cross-Cutting Design Patterns

- **Pattern A: Cascaded coarse-to-fine.** Stage 1: cheap keyword match eliminates 90% of options. Stage 2: LLM selects from survivors. Never ask LLM to select from 200 tools in one shot.
- **Pattern B: Groups as routing unit, not individual tools.** Route to server/group, not tool. Group fits in context; LLM selects tool normally within it.
- **Pattern C: Tool descriptions carry routing weight.** BM25/embedding/LLM selection all key on description. Description quality > algorithmic sophistication.
- **Pattern D: Routing must NOT call an LLM per query.** Optimizer layer uses pattern matching or lightweight classifier. LLM handles only ambiguous residual.
- **Pattern E: Name collision solved by prefix.** `{server}__{tool}` is universal.

## Proposed `task-router` Implementation

`route_task(task_description)` → returns skill + process_override + ranked candidate tools + confidence.

Architecture: two-phase heuristic routing (keyword → group → tool) with LLM escalation only when confidence < threshold. No ML training required. Uses `find_skill()` internally for skill lookup and reads `context/processes/` index for process override.

Return shape includes: `server`, `tool`, `tool_qualified` (`{server}__{tool}`), `confidence`, `domain_group`, `routing_basis`, `candidate_tools[]`, `process_override` (optional), `params_hint` (optional).

## Discussion Status

Open — implementation plan to be finalized.
