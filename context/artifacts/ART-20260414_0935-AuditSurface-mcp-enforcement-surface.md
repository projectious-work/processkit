---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260414_0935-AuditSurface-mcp-enforcement-surface
  created: 2026-04-14T09:35:00Z
spec:
  name: MCP Enforcement Surface Audit — processkit Skills Catalog
  kind: document
  location: context/artifacts/ART-20260414_0935-AuditSurface-mcp-enforcement-surface.md
  format: markdown
  version: "1.0.0"
  tags: [audit, mcp, enforcement, processkit]
  produced_by: AUDIT-20260414_0930-SwiftSurvey-mcp-enforcement-surface-audit
  links:
    workitem: AUDIT-20260414_0930-SwiftSurvey-mcp-enforcement-surface-audit
---

# MCP Enforcement Surface Audit — processkit Skills Catalog

## Executive Summary

This audit maps the enforcement surface of processkit: which skills ship MCP servers, what tools they expose, and whether those servers are wired into harness configs. The audit reveals **15 MCP-bearing skills in the processkit category** with a total of **71+ MCP tools** spanning create, transition, record, query, and discovery patterns. However, **no merged MCP config currently exists for any harness in this repository** — each skill ships its own `mcp-config.json`, but they are not aggregated into a single harness-readable file at `.claude/`, `.cursor/`, `.codex/`, or top-level paths.

---

## Skills Audit Table

| Skill Name | Category | MCP Server | MCP Tools | Tool Kinds | Config Present | Notes |
|---|---|---|---|---|---|---|
| task-router | processkit | Yes | `route_task` | discovery | Yes | Core skill; routing entry point for all domain tasks |
| workitem-management | processkit | Yes | `create_workitem`, `transition_workitem`, `query_workitems`, `link_workitems`, `get_workitem` | create, transition, link, query, read | Yes | Foundation primitive; critical write-side enforcement |
| decision-record | processkit | Yes | `record_decision`, `query_decisions`, `link_decision`, `supersede_decision` | record, query, transition, link | Yes | ADR pattern as primitive; consequence tracking |
| discussion-management | processkit | Yes | `open_discussion`, `get_discussion`, `transition_discussion`, `add_outcome`, `list_discussions` | create, read, transition, state-change | Yes | Multi-turn conversation with decision linkage |
| index-management | processkit | Yes | `reindex`, `query_entities`, `get_entity`, `search_entities`, `query_events`, `list_errors`, `stats` | discovery, query, read | Yes | Layer 0; read-side foundation for all queries |
| event-log | processkit | Yes | `log_event`, `query_events`, `recent_events` | record, query, read | Yes | Layer 0; append-only audit trail for all state changes |
| id-management | processkit | Yes | `generate_id`, `validate_id`, `list_used_ids`, `format_info` | discovery, read | Yes | Layer 0; write-side foundation for ID allocation |
| skill-finder | processkit | Yes | `find_skill`, `list_skills` | discovery | Yes | Core skill; navigation aid for skill catalog |
| actor-profile | processkit | Yes | `create_actor`, `get_actor`, `update_actor`, `deactivate_actor`, `list_actors` | create, read, transition, query | Yes | Layer 1; identity and role holder management |
| role-management | processkit | Yes | `create_role`, `get_role`, `update_role`, `list_roles`, `link_role_to_actor` | create, read, transition, link | Yes | Layer 1; named responsibility sets |
| scope-management | processkit | Yes | `create_scope`, `get_scope`, `transition_scope`, `list_scopes` | create, read, transition, query | Yes | Layer 2; bounded work containers (sprint, milestone) |
| binding-management | processkit | Yes | `create_binding`, `query_bindings`, `end_binding`, `resolve_bindings_for` | create, query, transition, read | Yes | Layer 2; scoped temporal relationships |
| artifact-management | processkit | Yes | `create_artifact`, `get_artifact`, `query_artifacts`, `update_artifact` | create, read, query, write | Yes | Layer 2; tangible deliverables catalog |
| gate-management | processkit | Yes | `create_gate`, `get_gate`, `list_gates`, `evaluate_gate` | create, read, query, discovery | Yes | Layer 3; validation checkpoints |
| model-recommender | processkit | Yes | `list_models`, `get_profile`, `compare_models`, `query_models`, `get_pricing`, `check_availability`, `get_config`, `set_config` | query, read, config | Yes | Model scoring and recommendation; 8 tools |

---

## Summary Findings

### 1. MCP-bearing vs Prose-only Skills

**Enforcement count:**
- **15 skills ship MCP servers** with `mcp/server.py` present
- **~18 processkit skills are prose-only** (no MCP server): `session-handover`, `owner-profiling`, `skill-reviewer`, `note-management`, `skill-builder`, `agent-management`, `process-management`, `schedule-management`, `state-machine-management`, `category-management`, `migration-management`, `constraint-management`, `cross-reference-management`, `skill-gate`, `status-update-writer`, `context-grooming`, `morning-briefing`, `standup-context`
- **Ratio: 15 enforcement / 33 total processkit skills ≈ 45% enforce via MCP**

### 2. Merged MCP Config in Harness Configs

**Search results:**
- `/workspace/.claude/settings.json` — **does not exist**
- `/workspace/.claude/mcp.json` — **does not exist**
- `/workspace/mcp.json` (top-level) — **does not exist**
- `/workspace/.codex/` — **does not exist**
- `/workspace/.cursor/` — **does not exist**
- `aibox.toml` — **deployment config; contains no MCP block**

**Finding:** There is **no merged MCP config** in this repository. Each of the 15 MCP-bearing skills ships its own `mcp/mcp-config.json` block (e.g., `/workspace/context/skills/processkit/workitem-management/mcp/mcp-config.json`), but they are **not aggregated**. The project relies on **installer responsibility** — the installer (aibox sync, manual tooling, CI/CD) is responsible for merging these blocks into the harness-specific path (e.g., `.claude/settings.json` for Claude Code) at container build time.

### 3. Critical processkit Tools Missing from Any Config

**Confirmed in SKILL.md frontmatter `provides.mcp_tools`:**

These tools are documented as provided but depend on external harness wiring for availability:

| Tool | Skill | Kind | Status |
|---|---|---|---|
| `create_workitem` | workitem-management | create | Not merged into any harness config in this repo |
| `transition_workitem` | workitem-management | state-change | Not merged into any harness config in this repo |
| `record_decision` | decision-record | record | Not merged into any harness config in this repo |
| `open_discussion` | discussion-management | create | Not merged into any harness config in this repo |
| `find_skill` | skill-finder | discovery | Not merged into any harness config in this repo |
| `route_task` | task-router | discovery | Not merged into any harness config in this repo |
| `query_entities` | index-management | query | Not merged into any harness config in this repo |
| `generate_id` | id-management | discovery | Not merged into any harness config in this repo |
| `log_event` | event-log | record | Not merged into any harness config in this repo |
| `create_actor` | actor-profile | create | Not merged into any harness config in this repo |
| `create_scope` | scope-management | create | Not merged into any harness config in this repo |
| `create_binding` | binding-management | create | Not merged into any harness config in this repo |
| `create_artifact` | artifact-management | create | Not merged into any harness config in this repo |
| `create_gate` | gate-management | create | Not merged into any harness config in this repo |
| `create_role` | role-management | create | Not merged into any harness config in this repo |

**Why this matters:** An agent running in Claude Code, Cursor, or Codex within this repository **cannot reach any of these tools** unless:
1. The parent environment (aibox devcontainer, IDE harness) merged the configs before starting the agent.
2. The agent manually instantiates the MCP servers via environment config.
3. The agent reads the skill SKILL.md files and recommends the tools without actually invoking them.

This is the likely reason the Researcher observes agents ignoring processkit: the tools exist, documented, and wired in the skill files, but they are not discoverable through the harness's MCP interface because no merged config has been placed where the harness looks for MCP servers.

---

## Recommendations

1. **Generate a merged MCP config at build time** — The aibox installer or a processkit-provided script should walk `/workspace/context/skills/processkit/*/mcp/mcp-config.json`, merge all blocks into one, and write it to `/workspace/.claude/settings.json` (or the appropriate harness path) so MCP tools are immediately discoverable.

2. **Document the wiring step explicitly** — In `AGENTS.md` or a processkit README, clarify that the per-skill `mcp-config.json` files are source files, not runtime configs, and must be merged at deployment time.

3. **Consider a "kernel" MCP config** — The 15 core enforcement skills (task-router, workitem-management, decision-record, index-management, id-management, event-log) could ship a pre-merged config block to ensure the Layer 0/Layer 1 stack is always wired, even if domain-specific skills remain optional.

---

*Audit conducted 2026-04-14. Data extracted from SKILL.md frontmatter and mcp/ directory trees.*
