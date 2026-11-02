---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider
  created: '2026-04-11T08:02:00+00:00'
spec:
  title: 'Reliable skill invocation: provider-independent five-track plan'
  state: accepted
  decision: 'Enforce reliable skill invocation via five provider-independent tracks:
    (A) skill-finder MCP server, (B) session-start meta-skill with 1% rule, (C) MCP
    tool description skill-consultation prompts, (D) AGENTS.md slimming and if/then
    guards, (E) skill description quality audit. Claude Code PreToolUse hooks are
    explicitly excluded as harness-specific.'
  context: 'Research (2026-04-11) confirms this is a well-documented, empirically
    measured problem. The AgentIF benchmark (NeurIPS 2025) shows best models perfectly
    follow fewer than 30% of complex multi-constraint agentic instructions. One org
    measured 56% reliable skill invocation from instruction files alone. Root causes:
    attention decay (Lost in the Middle), instruction capacity limits (~150-200 slots
    total of which Claude Code''s built-in system prompt consumes ~50), and tool schemas
    beating prose in every message turn. processkit must remain provider-neutral —
    Claude Code, Codex CLI, Cursor, Continue, and any future harness are all valid
    consumers.'
  rationale: Every track relies only on MCP (open standard, adopted by all major harnesses)
    or SKILL.md/AGENTS.md (provider-neutral content). Claude Code PreToolUse hooks,
    while the most reliable enforcement mechanism, are harness-specific and would
    silently not work for non-Claude consumers. The 1% rule meta-skill (Track B) is
    the provider-independent equivalent of hook-based enforcement. MCP tool descriptions
    (Track C) embed skill-consultation reminders in the tool schema itself — visible
    to every harness in every turn.
  alternatives:
  - option: Claude Code PreToolUse hooks only
    rejected_because: Harness-specific. Invisible to Codex CLI, Cursor, Continue,
      and any future harness. Contradicts processkit core design principle of provider
      neutrality.
  - option: AGENTS.md prose rules only
    rejected_because: Least reliable mechanism — subject to attention decay and instruction
      capacity limits. 56% observed reliability in comparable setups.
  - option: Make every skill MCP-backed
    rejected_because: Many skills are pure knowledge/workflow guides with no entities
      to manage. Adding artificial MCP servers to them adds complexity without value.
      The skill-finder MCP solves the discovery problem without forcing every skill
      to have a server.
  consequences: 'Track E (skill description quality audit) subsumes BACK-SpryBadger.
    Track B (meta-skill) subsumes BACK-SnappyTrout. Track A (skill-finder MCP) supersedes
    BACK-AmberCliff in scope. skill-builder will need two new steps after Tracks A-C
    ship: (1) add skill to session-start meta-skill checklist, (2) verify MCP tool
    descriptions carry consultation prompts where applicable.'
  decided_at: '2026-04-11T08:02:00+00:00'
---
