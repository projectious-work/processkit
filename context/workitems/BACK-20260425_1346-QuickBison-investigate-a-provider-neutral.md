---
apiVersion: processkit.projectious.work/v1
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
  description: "## What\n\nAdd a new processkit entity kind — `SubAgent` — modelled\
    \ on Claude Code's `/agents` system. A SubAgent is a portable definition of an\
    \ autonomous, context-isolated worker: name, when-to-delegate description, tool\
    \ allowlist, model preference, optional isolation mode (e.g. git worktree), and\
    \ a markdown system prompt body. `aibox sync` materializes the canonical primitive\
    \ into harness-native files (Claude Code first; other harnesses as they ship equivalents).\n\
    \n## Why\n\nprocesskit currently has three primitives in this space, but none\
    \ of them cover *runtime-isolated execution*:\n\n| Primitive | Role | Runtime\
    \ semantics |\n|---|---|---|\n| Skill | Instruction set | Injected into main conversation\
    \ context |\n| TeamMember | Role/seniority bookkeeping | Routing metadata, not\
    \ executable |\n| Binding | Role → model mapping | Routing metadata, not executable\
    \ |\n\nWhat is missing: a primitive for \"spawn a worker in fresh context with\
    \ these tools, this prompt, this model.\" Claude Code's `/agents` has shipped\
    \ this and is now the de facto convention. Authoring it as a processkit primitive\
    \ captures the pattern *once*, then renders it per-harness, instead of teaching\
    \ every derived project to maintain `.claude/agents/` by hand.\n\nThis shows up\
    \ concretely in the Claude Code agents already used in this repo (claude-code-guide,\
    \ Explore, Plan, statusline-setup, general-purpose). They are valuable but harness-specific\
    \ and not version-controlled by processkit. With a SubAgent primitive, processkit\
    \ could ship analogues like:\n\n- `pk-status-briefer` — wraps the `status-briefing`\
    \ skill in an isolated-context worker.\n- `pk-doctor-runner` — wraps `pk-doctor`\
    \ with restricted tool allowlist (Read, Bash for `uv run`).\n- `pk-research-worker`\
    \ — wraps `research-with-confidence` with WebSearch + WebFetch only.\n\n## Reference\
    \ (Claude Code subagent spec, 2026-04-25)\n\nFile format — markdown with YAML\
    \ frontmatter, lower-kebab-case `name` field, `description` drives auto-delegation,\
    \ `tools` allowlist (omit to inherit), `model` (`inherit`/`sonnet`/`opus`/`haiku`/full\
    \ ID), `permissionMode`, `maxTurns`, `memory` (user/project/local), `isolation:\
    \ worktree`, `mcpServers`, `hooks`, `skills` (preload), `effort`, `background`,\
    \ `color`. Discovery walks `.claude/agents/` upward from cwd; user-level fallback\
    \ at `~/.claude/agents/`.\n\nAuthoritative source: https://code.claude.com/docs/en/subagents.md\n\
    \n## How (proposed phases)\n\n**Phase 1 — Spec + materialization stub** (this\
    \ WorkItem):\n- Define `src/context/schemas/subagent.yaml` (canonical frontmatter,\
    \ intersection of Claude-Code-supported and harness-portable fields).\n- Document\
    \ the contract in `AGENTS.md`.\n- Ship one example SubAgent (e.g. `pk-status-briefer`)\
    \ in `src/context/subagents/` to validate the round-trip.\n- Add a `pk-doctor`\
    \ check (`subagent_consistency`) — every SubAgent has a valid spec and is materialized\
    \ to `.claude/agents/` if a Claude Code harness is detected.\n- Materialization\
    \ itself can be a small `scripts/materialize-subagents.py` invoked by aibox sync,\
    \ before promoting to a full MCP server.\n\n**Phase 2 — MCP server** (separate\
    \ WorkItem; only if Phase 1 sees usage):\n- `processkit-subagent-management` server\
    \ with `create_subagent`, `get_subagent`, `query_subagents`, `update_subagent`.\n\
    - Event log entries on create/update.\n- Optional: `query_subagents(for_task=...)`\
    \ mirroring task-router so the model can self-select a SubAgent for a given task.\n\
    \n**Phase 3 — Cross-harness materialization** (separate WorkItem):\n- Codex CLI:\
    \ subagent equivalent doesn't exist as of 2026-04-14 (per skill-gate README's\
    \ Codex limitation note). Block on upstream.\n- Continue, OpenCode: investigate.\n\
    \n## Provider-independence guardrails\n\n- The canonical schema must include only\
    \ fields that have a sane fallback when the harness lacks the feature. E.g.:\n\
    \  - `tools` allowlist → Claude Code honors; Codex (no subagent feature) ignores\
    \ entirely.\n  - `isolation: worktree` → Claude Code honors; on harnesses without\
    \ isolation, materializer emits a WARN and downgrades to \"no isolation.\"\n-\
    \ Document a \"harness capability matrix\" in the schema reference — which fields\
    \ each harness honors.\n- Materialization is one-way (canonical → harness file),\
    \ not bidirectional. Harness-specific fields stay out of the canonical schema.\n\
    \n## Open questions (research deliverables of Phase 1)\n\n1. **Overlap with TeamMember.**\
    \ Should SubAgents reference an existing TeamMember (e.g. `subagent.team_member:\
    \ TEAMMEMBER-cora`) for role inheritance, or stay strictly separate? Recommend\
    \ **separate** — TeamMember is role/seniority bookkeeping; SubAgent is executable\
    \ shape. Linking via metadata is enough.\n2. **Skill ↔ SubAgent.** Should a Skill\
    \ be auto-promotable to a SubAgent (one-line opt-in via SKILL.md `metadata.processkit.subagent:\
    \ { name: pk-status-briefer, tools: [...] }`)? Probably yes — saves duplication.\n\
    3. **Permission inheritance.** Claude Code subagents inherit parent permissions\
    \ plus optional restrictions. Document this so processkit-shipped SubAgents don't\
    \ accidentally need a separate preauth list (interacts with BACK-WildGrove preauth\
    \ WorkItem).\n4. **Plugin scope.** Claude Code disallows `hooks` / `mcpServers`\
    \ / `permissionMode` for plugin-scoped subagents (security). If processkit ships\
    \ SubAgents via aibox sync, decide whether they materialize into project-scope\
    \ `.claude/agents/` (full feature set) or plugin-scope (restricted). Recommend\
    \ project-scope.\n5. **Discovery for Claude Code's /agents UI.** Materialized\
    \ files must show up in `.claude/agents/` with no extra registration; verify `aibox\
    \ sync` writes the file with correct permissions.\n\n## Acceptance criteria for\
    \ Phase 1\n\n- `subagent.yaml` schema lands in `src/context/schemas/`.\n- One\
    \ example SubAgent ships under `src/context/subagents/` and renders correctly\
    \ to `.claude/agents/<name>.md` after `aibox sync` (verify by spawning it via\
    \ the Agent tool / `/agents` library).\n- `pk-doctor subagent_consistency` check\
    \ is registered, runs clean on the example.\n- AGENTS.md gains a \"SubAgents\"\
    \ section explaining the canonical primitive and the harness capability matrix.\n\
    \n## Cross-references\n\n- Claude Code subagent docs: https://code.claude.com/docs/en/subagents.md\n\
    - BACK-20260425_1316-WildGrove (preauth shipping) — same `aibox sync` materialization\
    \ surface; coordinate.\n- BACK-20260423_0829-TrueQuail (`.mcp.json` reconcile)\
    \ — same surface; coordinate.\n- `skill-builder` skill — natural partner for \"\
    promote skill to subagent.\"\n- `team-manager` skill — distinct concern; do not\
    \ merge."
---
