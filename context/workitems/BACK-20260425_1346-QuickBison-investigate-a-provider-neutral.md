---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1346-QuickBison-investigate-a-provider-neutral
  created: '2026-04-25T13:46:45+00:00'
spec:
  title: Investigate a provider-neutral SubAgent primitive (modelled on Claude Code
    /agents, targets .claude/agents/, .codex/, ...)
  state: backlog
  type: story
  priority: medium
  description: |
    ## What

    Add a new processkit entity kind — `SubAgent` — modelled on Claude Code's `/agents` system. A SubAgent is a portable definition of an autonomous, context-isolated worker: name, when-to-delegate description, tool allowlist, model preference, optional isolation mode (e.g. git worktree), and a markdown system prompt body. `aibox sync` materializes the canonical primitive into harness-native files (Claude Code first; other harnesses as they ship equivalents).

    ## Why

    processkit currently has three primitives in this space, but none of them cover *runtime-isolated execution*:

    | Primitive | Role | Runtime semantics |
    |---|---|---|
    | Skill | Instruction set | Injected into main conversation context |
    | TeamMember | Role/seniority bookkeeping | Routing metadata, not executable |
    | Binding | Role → model mapping | Routing metadata, not executable |

    What is missing: a primitive for "spawn a worker in fresh context with these tools, this prompt, this model." Claude Code's `/agents` has shipped this and is now the de facto convention. Authoring it as a processkit primitive captures the pattern *once*, then renders it per-harness, instead of teaching every derived project to maintain `.claude/agents/` by hand.

    This shows up concretely in the Claude Code agents already used in this repo (claude-code-guide, Explore, Plan, statusline-setup, general-purpose). They are valuable but harness-specific and not version-controlled by processkit. With a SubAgent primitive, processkit could ship analogues like:

    - `pk-status-briefer` — wraps the `status-briefing` skill in an isolated-context worker.
    - `pk-doctor-runner` — wraps `pk-doctor` with restricted tool allowlist (Read, Bash for `uv run`).
    - `pk-research-worker` — wraps `research-with-confidence` with WebSearch + WebFetch only.

    ## Reference (Claude Code subagent spec, 2026-04-25)

    File format — markdown with YAML frontmatter, lower-kebab-case `name` field, `description` drives auto-delegation, `tools` allowlist (omit to inherit), `model` (`inherit`/`sonnet`/`opus`/`haiku`/full ID), `permissionMode`, `maxTurns`, `memory` (user/project/local), `isolation: worktree`, `mcpServers`, `hooks`, `skills` (preload), `effort`, `background`, `color`. Discovery walks `.claude/agents/` upward from cwd; user-level fallback at `~/.claude/agents/`.

    Authoritative source: https://code.claude.com/docs/en/subagents.md

    ## How (proposed phases)

    **Phase 1 — Spec + materialization stub** (this WorkItem):
    - Define `src/context/schemas/subagent.yaml` (canonical frontmatter, intersection of Claude-Code-supported and harness-portable fields).
    - Document the contract in `AGENTS.md`.
    - Ship one example SubAgent (e.g. `pk-status-briefer`) in `src/context/subagents/` to validate the round-trip.
    - Add a `pk-doctor` check (`subagent_consistency`) — every SubAgent has a valid spec and is materialized to `.claude/agents/` if a Claude Code harness is detected.
    - Materialization itself can be a small `scripts/materialize-subagents.py` invoked by aibox sync, before promoting to a full MCP server.

    **Phase 2 — MCP server** (separate WorkItem; only if Phase 1 sees usage):
    - `processkit-subagent-management` server with `create_subagent`, `get_subagent`, `query_subagents`, `update_subagent`.
    - Event log entries on create/update.
    - Optional: `query_subagents(for_task=...)` mirroring task-router so the model can self-select a SubAgent for a given task.

    **Phase 3 — Cross-harness materialization** (separate WorkItem):
    - Codex CLI: subagent equivalent doesn't exist as of 2026-04-14 (per skill-gate README's Codex limitation note). Block on upstream.
    - Continue, OpenCode: investigate.

    ## Provider-independence guardrails

    - The canonical schema must include only fields that have a sane fallback when the harness lacks the feature. E.g.:
      - `tools` allowlist → Claude Code honors; Codex (no subagent feature) ignores entirely.
      - `isolation: worktree` → Claude Code honors; on harnesses without isolation, materializer emits a WARN and downgrades to "no isolation."
    - Document a "harness capability matrix" in the schema reference — which fields each harness honors.
    - Materialization is one-way (canonical → harness file), not bidirectional. Harness-specific fields stay out of the canonical schema.

    ## Open questions (research deliverables of Phase 1)

    1. **Overlap with TeamMember.** Should SubAgents reference an existing TeamMember (e.g. `subagent.team_member: TEAMMEMBER-cora`) for role inheritance, or stay strictly separate? Recommend **separate** — TeamMember is role/seniority bookkeeping; SubAgent is executable shape. Linking via metadata is enough.
    2. **Skill ↔ SubAgent.** Should a Skill be auto-promotable to a SubAgent (one-line opt-in via SKILL.md `metadata.processkit.subagent: { name: pk-status-briefer, tools: [...] }`)? Probably yes — saves duplication.
    3. **Permission inheritance.** Claude Code subagents inherit parent permissions plus optional restrictions. Document this so processkit-shipped SubAgents don't accidentally need a separate preauth list (interacts with BACK-WildGrove preauth WorkItem).
    4. **Plugin scope.** Claude Code disallows `hooks` / `mcpServers` / `permissionMode` for plugin-scoped subagents (security). If processkit ships SubAgents via aibox sync, decide whether they materialize into project-scope `.claude/agents/` (full feature set) or plugin-scope (restricted). Recommend project-scope.
    5. **Discovery for Claude Code's /agents UI.** Materialized files must show up in `.claude/agents/` with no extra registration; verify `aibox sync` writes the file with correct permissions.

    ## Acceptance criteria for Phase 1

    - `subagent.yaml` schema lands in `src/context/schemas/`.
    - One example SubAgent ships under `src/context/subagents/` and renders correctly to `.claude/agents/<name>.md` after `aibox sync` (verify by spawning it via the Agent tool / `/agents` library).
    - `pk-doctor subagent_consistency` check is registered, runs clean on the example.
    - AGENTS.md gains a "SubAgents" section explaining the canonical primitive and the harness capability matrix.

    ## Cross-references

    - Claude Code subagent docs: https://code.claude.com/docs/en/subagents.md
    - BACK-20260425_1316-WildGrove (preauth shipping) — same `aibox sync` materialization surface; coordinate.
    - BACK-20260423_0829-TrueQuail (`.mcp.json` reconcile) — same surface; coordinate.
    - `skill-builder` skill — natural partner for "promote skill to subagent."
    - `team-manager` skill — distinct concern; do not merge.
---
