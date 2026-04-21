---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
  created: 2026-04-14T14:30:00Z
spec:
  name: "processkit enforcement — implementation plan (hybrid: hooks + acknowledge_contract + tool-description 1% rule)"
  kind: document
  location: context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md
  format: markdown
  version: "1.0.0"
  tags: [architecture, enforcement, processkit, hooks, mcp, aibox]
  produced_by: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
  owner: ACTOR-sr-architect
  links:
    workitem: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
    inputs:
      - ART-20260414_1230-ReachReady-processkit-enforcement-research
      - ART-20260414_1230-ReachReady-processkit-enforcement-research-summary
      - ART-20260414_0935-AuditSurface-mcp-enforcement-surface
    related_decisions:
      - DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider
      - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
---

# processkit enforcement — implementation plan

**Author:** Senior Architect (Opus) · **Date:** 2026-04-14
**Input research:** `ART-20260414_1230-ReachReady-processkit-enforcement-research`
**Parent WorkItem:** `BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan`

## 0. Framing

Three parallel enforcement rails, each independently valuable so any one
can ship if the others slip:

- **Rail 1 — Compliance contract (canonical prose).** A single
  versioned source file inside processkit that carries the 15–30 line
  rule set: 1% rule, commit-immediately, MCP-not-hand-edit, log-after-
  state-change, route_task-before-create. Everything else below is a
  *transport* for this file's content.
- **Rail 2 — Transport A: hooks.** On harnesses with hook support
  (Claude Code, Codex CLI), a script reads the canonical contract and
  emits it to stdout on `SessionStart` and `UserPromptSubmit` so the
  content lands in the turn's context each time.
- **Rail 3 — Transport B: `acknowledge_contract()` MCP tool.** A
  provider-neutral fallback that works on any harness speaking MCP.
  The agent must call it once per session before any `create_*` /
  `transition_*` fires. The tool's *description* carries the contract,
  its return value re-states it, and it writes a session acknowledgement
  that other tool-side preconditions check.
- **Rail 4 — Transport C: 1%-rule sentences in 6–8 high-leverage MCP
  tool descriptions.** Always present in the tool list every turn at
  zero hook cost.

Rails 2 and 3 are complementary, not redundant — Rail 2 is stronger
where it works (structural, out of the agent's control) but absent on
harnesses without hooks; Rail 3 is portable but depends on the agent
actually calling the tool. Shipping both is the owner-approved hybrid.

## 1. Bucket A — processkit's responsibility

What we build in this repo.

### 1.1 Canonical compliance contract (Rail 1)

- **Location:** `context/skills/processkit/skill-gate/assets/compliance-contract.md`.
- **Shape:** Plain Markdown. 15–30 lines of imperative, stand-alone
  rules, each one sentence. No headings below `##`. Leading
  `<!-- pk-compliance v1 -->` marker so hook scripts can sanity-check
  the file they are about to emit.
- **Content seed (to be finalised in the WorkItem):**
  1. Call `route_task(task_description)` before any `create_*`,
     `transition_*`, `link_*`, `record_*`, or `open_*` tool.
  2. If you decide to create a WorkItem / DecisionRecord / Note /
     Artifact, call the tool in the same turn. Deferred entity
     creation is lost.
  3. Write entities through MCP tools. Hand-editing `context/` files
     skips schema validation, state-machine enforcement, and the
     event-log auto-entry.
  4. Read entities through `index-management` (`query_entities`,
     `get_entity`, `search_entities`). No `ls` / `grep` / filesystem
     walks under `context/`.
  5. Log an event after any state change not already produced by an
     MCP write.
  6. After a cross-cutting recommendation is accepted, call
     `record_decision` in the same turn.
  7. On any processkit domain task, consult `skill-finder` / call
     `find_skill` before relying on general knowledge.
  8. Do not edit files under `context/templates/`.
  9. Do not edit the generated harness MCP config by hand — edit the
     per-skill `mcp-config.json` and let the installer re-merge.
- **Why this file, not AGENTS.md:** AGENTS.md is the installer-rendered
  top-of-project document and contains a lot of context. The
  compliance-contract needs to be (a) shorter and (b) version-pinned so
  hook scripts and the `acknowledge_contract()` tool have a single
  stable target to read.

### 1.2 `acknowledge_contract()` MCP tool (Rail 3)

- **Host skill:** extend `skill-gate` from prose-only to MCP-bearing.
  (`skill-gate` already contains the 1% rule; `acknowledge_contract()`
  is the machine-readable enforcement face of that same rule. No new
  skill.)
- **New files:**
  - `context/skills/processkit/skill-gate/mcp/server.py` — FastMCP
    script following the PEP 723 pattern used elsewhere in the repo.
  - `context/skills/processkit/skill-gate/mcp/mcp-config.json` — the
    per-skill config block the installer merges.
  - `context/skills/processkit/skill-gate/mcp/SERVER.md` — tool schema
    doc.
- **Tool surface:**
  - `acknowledge_contract(version: str) -> {ok, contract_hash, expires_at}`
    — the agent calls this once per session. The tool:
    1. Loads `assets/compliance-contract.md`.
    2. Compares the caller-supplied `version` string (first line of the
       contract, e.g. `v1`) with the on-disk value.
    3. Returns the full contract text in the response `contract` field
       so the agent sees it even if it ignored the description.
    4. Writes a session marker file at
       `context/.state/skill-gate/session-<PID>.ack` containing the
       current contract hash and a wall-clock timestamp.
  - `check_contract_acknowledged() -> {acknowledged: bool, ...}` —
    read-only; used by tool-side preconditions on the write-side
    processkit MCP servers in a later phase (see §1.4, optional).
- **SKILL.md change:** `skill-gate` frontmatter `provides.mcp_tools`
  becomes `[acknowledge_contract, check_contract_acknowledged]`; the
  SKILL.md body gets a new section "How the gate is enforced" distin-
  guishing prose enforcement (fallback) from tool-call acknowledgement.
- **Latency cost:** one extra turn at session start. Owner accepted.

### 1.3 1%-rule sentences in 6–8 MCP tool descriptions (Rail 4)

- Locked list of tools in `DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list`.
- **Tools chosen:** `route_task`, `find_skill`, `create_workitem`,
  `transition_workitem`, `record_decision`, `log_event`,
  `open_discussion`, `create_artifact`. (Rationale and rejected
  alternatives live in the DecisionRecord.)
- **Payload:** a single sentence appended to the existing docstring,
  roughly: "Call `route_task` first — if there is a 1% chance a
  processkit skill covers this task, route before acting." Each write-
  side tool also adds: "Commit to the write in the same turn as the
  decision; deferred writes are routinely dropped."
- **Constraints:** additions must be ≤ 120 characters so the tool list
  stays readable; no Markdown beyond plain prose (harnesses render tool
  descriptions differently).
- **Smoke-test hook:** `scripts/smoke-test-servers.py` gains an
  assertion that each tool's description contains the literal string
  "1% rule" — fails CI if someone drops it on an edit.

### 1.4 Provider-neutral hook scripts (Rail 2, neutral half)

- **Location:** `context/skills/processkit/skill-gate/scripts/` (this
  directory already exists and is the natural home for gate enforcement
  assets).
- **Files:**
  - `emit_compliance_contract.py` — a stdlib-only Python script. Reads
    `assets/compliance-contract.md` relative to its own location. Emits
    the contract on stdout. Exits 0. On both Claude Code and Codex CLI
    hooks, stdout is appended to the turn's context
    [Claude Code hooks guide; Codex hooks guide].
  - `check_route_task_called.py` — PreToolUse gate for Claude Code.
    Reads hook input JSON from stdin per the Claude Code hooks spec
    [Claude Code hooks guide, §"Hook input"], checks for a session
    marker at `context/.state/skill-gate/session-<SESSION_ID>.ack` or
    `.route`, exits 0 (pass) or 2 (block) accordingly. Prints a remedi-
    ation message to stderr when blocking.
- **Input/output shapes we honour** (from the Claude Code hooks docs
  at `https://code.claude.com/docs/en/hooks-guide`, verified 2026-04-14;
  re-verify at implementation time):
  - `SessionStart` / `UserPromptSubmit` — script stdout becomes
    additional context; a JSON `hookSpecificOutput.additionalContext`
    object is the preferred form for Claude Code 2.1.0+, plain stdout
    is the fallback.
  - `PreToolUse` — script receives a JSON blob with `tool_name`,
    `tool_input`, `session_id`, `cwd` on stdin; exit 2 blocks the tool
    call; stderr is shown to the user.
- **Why these scripts ship from processkit, not aibox:** the content
  (contract text, routing-marker check) is processkit-domain logic.
  aibox's job is only to wire their paths into the harness config at
  install time — see §2.

### 1.5 AGENTS.md compliance header (Rail 1, secondary transport)

- Re-layer the canonical AGENTS.md (`src/AGENTS.md` and the rendered
  `/workspace/AGENTS.md`) so the first ~30 lines under the title are a
  verbatim paste of the compliance contract body, behind an HTML
  comment marker so the installer can re-sync it on version bumps.
  The rest of today's AGENTS.md moves below the contract unchanged.
- The comment marker: `<!-- pk-compliance-contract v1 BEGIN -->` /
  `<!-- pk-compliance-contract v1 END -->`. A processkit sync step can
  later replace the block wholesale when the contract version bumps.
- **No further trimming.** The research is explicit that trimming is
  not the binding constraint; position is.

### 1.6 Per-harness surface, Bucket-A side

- **Claude Code (primary):** we ship the hook scripts + contract +
  MCP server. We do **not** ship `.claude/settings.json`. The installer
  writes it (Bucket B).
- **Codex CLI (primary):** same scripts, same contract. We do not ship
  `.codex/hooks.json` or `.codex/config.toml`. Installer writes them
  (Bucket B). Note: Codex `PreToolUse` today only intercepts `Bash`
  [OpenAI Codex hooks docs; github.com/openai/codex issue 16732] — the
  gate script at §1.4 is a no-op on Codex until that limitation lifts.
  We still ship the script; aibox wires it where it can and logs a
  known-limitation warning on `aibox sync` for Codex-only projects.
- **Cursor / OpenCode / Aider (follow-up):** content is the same
  compliance-contract file. Per-harness adapter logic (e.g. a
  `.cursor/rules/processkit-compliance.md` generator) is an aibox
  concern — see §2 and WorkItem `FEAT-…-WideNet-cursor-opencode-aider-adapter-scoping`.

### 1.7 What we explicitly do NOT build in processkit

- No installer binary, no `aibox sync` code path, no harness-path
  writers, no merge step for MCP configs, no devcontainer hook wiring.
  All of that is Bucket B.
- No new skill. `acknowledge_contract()` lives on `skill-gate`.

## 2. Bucket B — aibox's responsibility

Everything about *installing*, *merging*, *placing on disk*, or
*wiring into a harness-specific path*. These surface as GitHub issues
against the aibox repo. processkit ships the content; aibox ships the
delivery.

Each item below has a matching issue draft in §5 ready for
`gh issue create`.

### 2.1 Ship a pre-merged MCP config per harness on `aibox sync`

aibox already knows `[ai].harnesses`. On sync, walk
`context/skills/*/*/mcp/mcp-config.json`, merge, and emit the harness-
native file (Claude Code: `.claude/settings.json#/mcpServers`; Codex:
`.codex/config.toml [mcp_servers.*]`; Cursor follow-up). Without this,
the MCP tools are invisible to the agent — the single highest-leverage
fix per research §5.1.

### 2.2 Wire the `processkit-compliance` hook scripts on `aibox sync`

Write `.claude/settings.json#/hooks` entries for `SessionStart` and
`UserPromptSubmit` (and optionally `PreToolUse` on `Write|Edit|MultiEdit`
under `context/**`) that invoke the scripts shipped by processkit at
`context/skills/processkit/skill-gate/scripts/*`. Do the equivalent
for Codex in `.codex/hooks.json`.

### 2.3 Kernel MCP fallback

When the full merge fails (bad JSON in a per-skill config, missing
`uv`, etc.), emit a minimum "kernel" MCP config covering the 8
always-needed servers (`index-management`, `id-management`,
`workitem-management`, `decision-record`, `event-log`, `skill-finder`,
`task-router`, `skill-gate`) so the enforcement stack is always alive
even when a domain skill is broken. Research §5.1.b.

### 2.4 Devcontainer rebuild integration

Anything that touches `.claude/settings.json` or `.codex/` needs to be
written into the rebuild path so these files land in freshly-built
containers, not just on the developer's host.

### 2.5 Per-harness adapter: Cursor / OpenCode / Aider

- **Cursor:** generate `.cursor/rules/processkit-compliance.md` at sync
  time from the canonical contract. MCP config generation is optional
  (Cursor has its own MCP UI). No PreToolUse-equivalent exists at our
  research horizon — prose-only enforcement is the ceiling.
- **OpenCode:** AGENTS.md compliance already works via the re-layered
  header. MCP and hooks need researching — scope-only issue.
- **Aider:** write `.aider.conf.yml` with a `read: [AGENTS.md,
  context/skills/processkit/skill-gate/assets/compliance-contract.md]`
  entry so the contract is loaded on startup (Aider does not auto-load
  AGENTS.md; see research §4.3).

### 2.6 `aibox sync` diagnostic: compliance drift report

When the rendered AGENTS.md has drifted from the versioned
compliance-contract marker block (edited by hand and no longer matches
the processkit source), print a warning and a one-liner `aibox sync
--fix-compliance-contract` remediation hint.

## 3. WorkItems (Bucket A only)

Filed under `context/workitems/` in the same turn as this plan. IDs
point at the exact files.

| WorkItem | Title | Size |
|---|---|---|
| `BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source` | Write canonical `compliance-contract.md` under `skill-gate/assets/` | S |
| `BACK-20260414_1431-LoudBell-acknowledge-contract-mcp-tool` | Add `acknowledge_contract()` / `check_contract_acknowledged()` MCP tools on `skill-gate` | M |
| `BACK-20260414_1432-InkStamp-mcp-tool-description-1pct-rule` | Embed the 1% rule in 8 locked MCP tool descriptions + CI guard | S |
| `BACK-20260414_1433-SteadyHand-provider-neutral-hook-scripts` | Write `emit_compliance_contract.py` + `check_route_task_called.py` under `skill-gate/scripts/` | M |
| `BACK-20260414_1434-RightPath-agents-md-compliance-header` | Re-layer AGENTS.md (canonical + scaffolding) with a compliance-contract header block | S |
| `BACK-20260414_1435-QuietProbe-codex-reinjection-probe` | Probe Codex CLI AGENTS.md re-injection behaviour and record findings | S |
| `BACK-20260414_1436-WideNet-cursor-opencode-aider-adapter-scoping` | Scope processkit-side content requirements for Cursor, OpenCode, Aider adapters | S |

Each WorkItem file is self-contained — input files, success criteria,
and explicit guardrails against scope creep. A Sonnet Developer can
execute them without returning for more design.

## 4. Open questions (residual uncertainty)

Re-verified the research file's residual-uncertainty list; three items
are still open at plan time and fold into WorkItems rather than
blocking:

1. **Codex AGENTS.md turn-by-turn re-injection.** Research source says
   "first turn only, limited bytes" [OpenAI Codex AGENTS.md docs] but
   was not instrumented. → `FEAT-…-QuietProbe-codex-reinjection-probe`.
   If Codex does re-render AGENTS.md each turn, the hook transport on
   Codex drops to secondary priority (the tool-description rail still
   matters). This does not block any other WorkItem.
2. **Cursor / OpenCode / Aider PreToolUse-equivalents.** Research could
   not confirm from public docs. → `FEAT-…-WideNet-cursor-opencode-aider-adapter-scoping`
   is explicitly scope-only: produce a capability matrix, file the
   build-side work as aibox issues once scoped.
3. **Exact Claude Code hook JSON shape for 2.1.0+.** We cite
   `hookSpecificOutput.additionalContext` from the hooks guide but the
   scripts should be written against a sample payload captured at
   implementation time. Mitigation: `FEAT-…-SteadyHand` success
   criterion 4 requires a dry-run against a real Claude Code install
   (captured stdin JSON committed as a golden-file fixture under the
   script directory).

Non-uncertainties I want the owner aware of:
- The `acknowledge_contract()` tool latency cost (one turn per
  session) is accepted but should be measured once in real sessions —
  I have noted it as a post-ship metric, not a WorkItem.
- If the tool-description edits (Rail 4) land before the merged MCP
  config (Bucket B 2.1), they are invisible in derived projects. Not a
  blocker for processkit; surface in the aibox issue's acceptance
  criteria.

## 5. Rollout order

The order that maximises "first useful enforcement the owner sees,
fastest" while keeping the rails independent:

1. **Week 1, processkit side.**
   1. `FEAT-CleanCharter` (canonical contract file). Blocks every
      other rail but is trivial.
   2. `FEAT-InkStamp` (tool-description 1% rule). Zero-dependency,
      zero-risk, always-on once shipped. Useful the moment aibox
      merges the MCP config.
   3. `FEAT-RightPath` (AGENTS.md header). Also zero-dependency; this
      is the "prose at primacy" win while hooks are landing.
2. **Week 1–2, processkit side.**
   4. `FEAT-LoudBell` (`acknowledge_contract()` MCP). Works on any
      harness that speaks MCP, independent of the hook work.
   5. `FEAT-SteadyHand` (hook scripts). Shipped as files; no harness
      wiring yet.
3. **Week 2, aibox side — file the issues in §6 (next section).** Each
   one is standalone; issue 6.1 (merged MCP config on sync) unblocks
   every other bucket-B item.
4. **Week 2–3, processkit side.**
   6. `FEAT-QuietProbe` (Codex re-injection probe) — closes the
      largest residual uncertainty before we invest in Codex-specific
      adapter polish.
   7. `FEAT-WideNet` (follow-up-harness scoping) — produces the
      capability matrix that drives Bucket-B issues 6.5+.
5. **Measure.** After hooks + MCP tool descriptions + acknowledge
   contract are all in a single derived project, run the 20-session
   A/B the research report recommends (research §6 row 4). Feed
   findings back as a WorkItem.

## 6. GitHub issues to file against aibox

Drafted here, not filed — the owner decides what to open. Each block
is ready to paste into `gh issue create`.

### 6.1 Ship a merged MCP config per harness on `aibox sync`

**Title:** `Merge processkit per-skill MCP configs into harness files on sync`

**Labels:** `area/sync`, `area/mcp`, `priority/high`, `processkit-upstream`

**Body:**

processkit ships per-skill MCP config blocks at
`context/skills/*/*/mcp/mcp-config.json`. Today nothing aggregates
them into the harness-readable file (Claude Code:
`.claude/settings.json#/mcpServers` + `/enabledMcpjsonServers`; Codex:
`.codex/config.toml [mcp_servers.*]`). Without aggregation the 15+
enforcement MCP tools are invisible to agents in derived projects —
this is the single highest-leverage fix per the processkit enforcement
research (`ART-20260414_1230-ReachReady`).

Scope: on `aibox sync`, walk the per-skill configs listed in the
installed processkit content, merge them, and write the harness-native
file for every harness in `[ai].harnesses`. Respect existing non-
processkit entries on merge (owner may already have custom MCP
servers). Fail loudly and leave existing config untouched if any
per-skill block is malformed — do not silently drop servers.

**Acceptance criteria:**
- After `aibox sync` on a fresh project with `harnesses = ["claude",
  "codex"]`, `.claude/settings.json` and `.codex/config.toml` both
  list every processkit MCP server shipped by the installed skill set.
- Running the Claude Code `mcp` panel / Codex `codex mcp list` shows
  each server as live.
- Non-processkit MCP entries already in the file are preserved.
- Malformed per-skill config produces a clear error and leaves existing
  files untouched.

---

### 6.2 Wire processkit compliance-contract hooks into harness config

**Title:** `Wire processkit SessionStart / UserPromptSubmit hooks on sync`

**Labels:** `area/sync`, `area/hooks`, `priority/high`, `processkit-upstream`

**Body:**

processkit ships provider-neutral hook scripts under
`context/skills/processkit/skill-gate/scripts/`
(`emit_compliance_contract.py`, `check_route_task_called.py`) that
re-inject a short compliance contract per turn and, on Claude Code,
optionally gate `Write|Edit|MultiEdit` under `context/**` until
`route_task` has been called.

aibox should, on `sync`, register these scripts as hooks in the
harness-native locations:
- Claude Code: `.claude/settings.json#/hooks` — events `SessionStart`
  (matcher `startup,resume,compact`), `UserPromptSubmit`, and
  (optional) `PreToolUse` with tool matcher `Write|Edit|MultiEdit`
  and path starting with `context/`.
- Codex CLI: `.codex/hooks.json` — events `SessionStart`,
  `UserPromptSubmit`. Note: Codex `PreToolUse` today only intercepts
  `Bash` (upstream issue openai/codex#16732); skip the PreToolUse wire
  on Codex and log a known-limitation note during sync.

**Acceptance criteria:**
- After sync, a new Claude Code session prints the contract's
  distinctive marker line in every turn's context.
- Codex equivalent works for `SessionStart` / `UserPromptSubmit`.
- Pre-existing user hooks are preserved and not clobbered.

---

### 6.3 Kernel MCP fallback when per-skill merge fails

**Title:** `Emit kernel MCP config when per-skill merge fails`

**Labels:** `area/sync`, `area/mcp`, `priority/medium`, `processkit-upstream`

**Body:**

When the full per-skill merge (issue 6.1) fails — bad JSON, missing
`uv`, unreadable path — aibox should still emit a minimum "kernel" MCP
config covering the eight always-needed servers:
`index-management`, `id-management`, `workitem-management`,
`decision-record`, `event-log`, `skill-finder`, `task-router`,
`skill-gate`. The enforcement rail (`skill-gate` +
`acknowledge_contract()`) must survive a broken domain skill.

**Acceptance criteria:**
- Intentionally corrupt one per-skill `mcp-config.json`. `aibox sync`
  warns, falls through to the kernel config, and the agent session
  still has the eight kernel servers available.

---

### 6.4 Aibox sync: compliance-contract drift report

**Title:** `Warn on drift between rendered AGENTS.md and processkit compliance contract`

**Labels:** `area/sync`, `area/agents-md`, `priority/low`, `processkit-upstream`

**Body:**

processkit embeds its compliance contract into the rendered AGENTS.md
inside a versioned `<!-- pk-compliance-contract v1 BEGIN/END -->`
block. If a project owner edits within the block by hand, the block
drifts from the canonical source at
`context/skills/processkit/skill-gate/assets/compliance-contract.md`.
On `aibox sync`, compare the block content to the source; if it has
drifted, print a warning and an `aibox sync --fix-compliance-contract`
hint. Do not overwrite without the flag.

**Acceptance criteria:**
- Drifting AGENTS.md prints a clear warning on sync.
- Opt-in flag restores the block; non-block AGENTS.md content stays
  untouched.

---

### 6.5 Per-harness adapter: Cursor

**Title:** `Generate .cursor/rules/processkit-compliance.md on sync`

**Labels:** `area/sync`, `area/cursor`, `priority/low`, `processkit-upstream`

**Body:**

For projects with `cursor` in `[ai].harnesses`, generate
`.cursor/rules/processkit-compliance.md` from the canonical contract
shipped by processkit. Cursor has no PreToolUse-equivalent hook point
at our research horizon (2026-04-14) — prose-in-rules is the ceiling.
Cursor has MCP client support; scoping MCP config generation is a
follow-up.

**Acceptance criteria:**
- After sync, `.cursor/rules/processkit-compliance.md` exists and
  matches the canonical contract content.

---

### 6.6 Per-harness adapter: Aider

**Title:** `Register processkit compliance contract via .aider.conf.yml`

**Labels:** `area/sync`, `area/aider`, `priority/low`, `processkit-upstream`

**Body:**

Aider does not auto-load AGENTS.md or CONVENTIONS.md; files must be
declared via `--read` or a `.aider.conf.yml` `read:` entry
(aider.chat/docs/usage/conventions.html). On `aibox sync` for projects
with `aider` in `[ai].harnesses`, add the canonical compliance-contract
path (and AGENTS.md if not already present) to `.aider.conf.yml`.

**Acceptance criteria:**
- After sync, a fresh `aider` session shows the contract content in
  its context.
- Existing `.aider.conf.yml` entries are preserved.

---

### 6.7 OpenCode adapter — scoping issue

**Title:** `Scope OpenCode adapter: MCP + hooks capability matrix`

**Labels:** `area/sync`, `area/opencode`, `priority/low`, `processkit-upstream`, `type/research`

**Body:**

processkit ships a canonical compliance contract, an
`acknowledge_contract()` MCP tool on `skill-gate`, and provider-
neutral hook scripts. OpenCode supports AGENTS.md natively
(opencode.ai/docs/rules/) but its MCP client capability and hook-point
set are unverified at 2026-04-14. This issue is scope-only: produce a
capability matrix and open follow-up implementation issues.

**Acceptance criteria:**
- A `docs/` note or issue comment landing the matrix: AGENTS.md,
  MCP client, hook points, limitations.
- Follow-up implementation issues opened for any supported surface.

---

## 7. Provenance

- Research: `ART-20260414_1230-ReachReady-processkit-enforcement-research`
- Audit: `ART-20260414_0935-AuditSurface-mcp-enforcement-surface`
- Parent WorkItem: `BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan`
- DecisionRecord (this plan): `DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list`
- Earlier related decision: `DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider`
  (this plan is the hybrid-approved update — hooks are now in scope for
  the supported harnesses alongside the original five tracks).
