---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260411_1738-BraveStream-build-task-router-mcp
  created: '2026-04-11T17:38:36+00:00'
spec:
  title: Build task-router MCP server as the primary routing mechanism for processkit
    agents
  state: accepted
  decision: 'Build a `processkit-task-router` MCP server exposing `route_task(task_description)`.
    It maps natural-language task descriptions to: (a) the matching processkit skill,
    (b) the project-specific process override from `context/processes/` if one exists,
    and (c) a ranked list of candidate MCP tools. The router uses two-phase heuristic
    routing (keyword match → domain group → tool) without calling an LLM. LLM escalation
    is reserved for confidence < threshold cases. AGENTS.md references `task-router`
    as the primary routing entry point, replacing the direct `find_skill()` reference.'
  context: Agents reliably invoke wrong skills or skip process overrides because session-start
    prose (AGENTS.md) drifts in long contexts, and no single call maps task → skill
    + process override + MCP tool. Five remediation tracks (A–E) improved the situation
    but left a gap in process override discoverability. External research (MetaMCP,
    PulseMCP Router, MasRouter ACL 2025, Anthropic Tool Search Tool, Elastic Path)
    confirmed the cascaded routing pattern and tool-group architecture as industry
    standard.
  rationale: 'Research confirmed five cross-cutting patterns from independent sources:
    (1) cascaded coarse-to-fine routing, (2) groups as routing unit (not individual
    tools), (3) tool descriptions carry routing weight, (4) routing must not call
    an LLM per query, (5) name collision solved by `{server}__{tool}` prefix. A single
    `route_task()` call that bundles skill + process_override + tool is the minimal
    increment that closes the process-override gap without adding prose to AGENTS.md.
    The MCP tool schema is re-injected every turn by the harness, making it more reliable
    than session-start prose instructions.'
  alternatives:
  - option: Keep skill-finder only (find_skill + list_skills)
    rejected_because: Does not surface process overrides; agents must still choose
      to call it; adds nothing to per-turn tool schema enforcement
  - option: Add Step 0 to all process-category skills pointing to context/processes/
    rejected_because: Requires editing 10-15 skills; fragile — agent must reach the
      skill first before seeing the pointer
  - option: Extend find_skill() to return process_override field
    rejected_because: Partial fix — still doesn't route to MCP tools; still doesn't
      use cascaded routing patterns identified in research
  consequences: 'AGENTS.md shrinks further: `find_skill()` reference replaced by `route_task()`.
    skill-gate prose becomes a fallback/backup rather than primary mechanism. New
    MCP server required (processkit-task-router). All process-category skills get
    a note pointing to the router. skill-finder remains but is called internally by
    task-router, not directly by agents in normal flow.'
  decided_at: '2026-04-11T17:38:36+00:00'
---
