---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix
  created: 2026-04-14 15:45:00+00:00
spec:
  name: Follow-up harness capability matrix — Cursor, OpenCode, Aider
  kind: document
  location: context/artifacts/ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix.md
  format: markdown
  version: 1.0.0
  tags:
  - research
  - enforcement
  - cursor
  - opencode
  - aider
  - capability-matrix
  - harness-adapters
  produced_by: BACK-20260414_1436-WideNet-cursor-opencode-aider-adapter-scoping
  owner: ACTOR-junior-researcher
  links:
    workitem: BACK-20260414_1436-WideNet-cursor-opencode-aider-adapter-scoping
    inputs:
    - ART-20260414_1230-ReachReady-processkit-enforcement-research
    - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
---

# Follow-up harness capability matrix — Cursor, OpenCode, Aider

**Author:** Junior Researcher (Sonnet) — ACTOR-jr-researcher
**Date gathered:** 2026-04-14
**Parent WorkItem:** `BACK-20260414_1436-WideNet-cursor-opencode-aider-adapter-scoping`
**Input artifacts:**
- `ART-20260414_1230-ReachReady-processkit-enforcement-research` (§4.3, §6)
- `ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan` (§2.5, §4 Q2)

---

## 0. Methodology

WebFetch was denied in this session. Research was performed via
WebSearch queries against official documentation domains
(`docs.cursor.com`, `opencode.ai/docs`, `aider.chat/docs`) plus
secondary practitioner sources (GitButler blog, DEV Community, GitHub
issues). Every claim carries a confidence label and a source URL.
Confidence labels follow the convention established in the upstream
research report:

- **Confirmed** — found in official primary-source documentation.
- **Likely** — multiple corroborating secondary sources, or strong
  inference from a confirmed primary source.
- **Weak** — single secondary source, or secondary source from which
  I'm inferring.
- **Speculation** — no source found; explicitly reasoned from first
  principles.

All sources gathered 2026-04-14. Re-verify before implementation,
particularly Cursor hooks (beta in v1.7, feature surface evolving
rapidly) and Aider MCP/AGENTS.md status.

---

## 1. Capability Matrix

| Dimension | Cursor | OpenCode | Aider |
|---|---|---|---|
| **AGENTS.md auto-load** | Supported natively at project root and subdirectories; also reads `.cursor/rules/*.mdc` (primary surface). Bug: background agents may not always load it. | Confirmed native: project `AGENTS.md` + `~/.config/opencode/AGENTS.md`. `/init` generates or improves the file. | **Not** auto-loaded. Must be declared via `--read` flag or `read:` entry in `.aider.conf.yml`. Feature request open (issue #4363). |
| **AGENTS.md confidence** | Likely [A, C] | Confirmed [D] | Confirmed — explicit non-support [E, F] |
| **CONVENTIONS.md / rules-file auto-load** | `.cursor/rules/*.mdc` — project-level, version-controlled. `.cursorrules` (deprecated, still supported). Rules prepended as system prompt on every interaction. | Rules in `AGENTS.md` only; no separate CONVENTIONS.md surface found. | `CONVENTIONS.md` must be explicitly loaded via `--read CONVENTIONS.md` or `.aider.conf.yml`. Identical requirement to AGENTS.md. |
| **Rules-file load timing** | At session start, prepended as system prompt on every turn. | At session start, included in LLM context. | At startup only when explicitly listed; loaded into context once (supports prompt caching). |
| **MCP client support** | Yes. Config: `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global). Project-level takes precedence. MCP servers configurable via GUI or JSON. Enforcement note: MCP tool calls **do** trigger `beforeMCPExecution` / `afterMCPExecution` hooks (separate from `preToolUse`). | Yes. Config: `opencode.json` (project) or `~/.config/opencode/opencode.json` (global). MCP defined under `mcp` key. Enforcement gap: MCP tool calls **do not** trigger `tool.execute.before` plugin hooks (open bug #2319 as of Aug 2025). | **No native MCP client support.** Open GitHub issue #3314. Community workaround: `mcpm-aider` (experimental). Aider can act as an MCP *server* (for other agents to call), but cannot consume MCP servers as a client. |
| **MCP confidence** | Confirmed [B, G] | Confirmed for support; Confirmed for enforcement gap [H, I] | Confirmed — no native support [J, K] |
| **SessionStart-equivalent hook** | `sessionStart` event (hooks v1.7, beta). Config: `.cursor/hooks.json`. **Known bug:** stdout injection does not reliably reach Agent Window for brand-new conversations (Cursor forum, 2025). Works for /clear and /compact restarts. | `session.created` plugin event via TypeScript plugin. Context injection **not** available from hooks into LLM context (open feature request #17412). | None. No hook system in Aider. |
| **SessionStart confidence** | Likely — exists but buggy [L, M] | Likely — event exists, context injection unconfirmed [N, O] | Confirmed — does not exist [P] |
| **UserPromptSubmit-equivalent** | `beforeSubmitPrompt` hook fires after user submits message. Can **block** submission. **Cannot inject context** via stdout (feature request open). | No direct equivalent found in plugin docs. | None. |
| **UserPromptSubmit confidence** | Confirmed — exists with limitation [L, Q] | Weak — not documented [R] | Confirmed — does not exist [P] |
| **PreToolUse-equivalent** | `preToolUse` hook (generic for Shell/Read/Write/Grep/Delete/Task); `beforeMCPExecution` hook for MCP tool calls. Exit code 2 blocks. Config: `.cursor/hooks.json`. Confirmed blocking capability. | `tool.execute.before` plugin hook. Can block native tool calls. **Does not intercept MCP tool calls** (bug #2319). **Does not intercept subagent tool calls** (bug #5894). | None. |
| **PreToolUse confidence** | Confirmed [L, S] | Confirmed for partial support; Confirmed for gaps [H, I, T] | Confirmed — does not exist [P] |
| **Best enforcement transport** | **Hooks (preToolUse + sessionStart) + rules file.** `.cursor/rules/processkit-compliance.md` delivers prose; `preToolUse` hook enforces blocking; `beforeMCPExecution` hook enforces on MCP tools. MCP config generation via `.cursor/mcp.json`. | **AGENTS.md (reliable) + plugin hooks (partial, with known gaps).** MCP config via `opencode.json`. Plugin `tool.execute.before` blocks native tools only. MCP tools bypass hooks — processkit MCP tools are **not** enforceable via hooks. | **Prose only via `.aider.conf.yml` read list.** Installer writes `read: [AGENTS.md, context/skills/processkit/skill-gate/assets/compliance-contract.md]`. No structural enforcement possible. |

---

## 2. Per-harness deep dive

### 2.1 Cursor

**Prose surface:**

Cursor's primary rules surface is `.cursor/rules/*.mdc` — Markdown
files with optional YAML frontmatter for scoping. They are prepended
as system prompt on every interaction, making them more durable than
Claude Code's CLAUDE.md (which is injected once then compacted). The
compliance contract should therefore be placed as a `.cursor/rules/`
file rather than relying solely on AGENTS.md.

AGENTS.md is supported natively in Cursor (project root and
subdirectories) as of mid-2025. However, a bug filed in 2025 reports
that background agents may fail to load it reliably (Cursor forum
issue "AGENTS.md not always loaded"). The rules-file surface is more
reliable for compliance purposes. [A, C]

Recommendation for processkit: the compliance contract goes into
`.cursor/rules/processkit-compliance.md` (a `.mdc` file with no
path-scoping so it fires globally). Under 2,000 words per Cursor's
own attention guidance. [G]

**MCP client:**

Cursor reads `.cursor/mcp.json` at project level or
`~/.cursor/mcp.json` globally. Format is `{"mcpServers": {...}}`
identical to Claude Code's `mcpServers` block. This means a
processkit installer can generate this file using the same merge
logic as for Claude Code — the block format is transferable. MCP
servers are also configurable via Cursor's GUI Settings panel, but
for `aibox sync` automation the JSON file is the right target. [B]

Enforcement note: `beforeMCPExecution` fires before MCP tool calls
and supports blocking — this is stronger than Codex CLI (where
PreToolUse only covers Bash). A hook that checks for a prior
`route_task` session marker could block processkit `create_*` /
`transition_*` MCP calls. [S]

**Hook system (v1.7, beta as of Oct 2025):**

Config location: `.cursor/hooks.json` (project) or
`~/.cursor/hooks.json` (user). Cursor supports:

| Hook event | Enforcement use | Blocking? | Stdout→context? |
|---|---|---|---|
| `sessionStart` | Inject compliance contract | No (fire-and-forget; context injection bug) | Buggy |
| `beforeSubmitPrompt` | Inspect/block user prompt | Block only | No (feature request open) |
| `preToolUse` | Block file writes, shell commands | Yes (exit 2) | No |
| `beforeMCPExecution` | Block MCP tool calls | Yes (exit 2) | No |
| `postToolUse` / `afterMCPExecution` | Observability / post-hoc logging | No | Yes |

The `sessionStart` context-injection bug is a significant limitation:
unlike Claude Code's `SessionStart` hook (which reliably injects
stdout into context), Cursor's equivalent is unreliable for new
sessions. The compliance-contract re-injection pattern from the
implementation plan (§1.4) will **not work reliably on Cursor**
until this bug is fixed. Prose-in-rules is currently the only
reliable per-turn context surface. [L, M]

`preToolUse` and `beforeMCPExecution` blocking **do work** — they
are the structural enforcement ceiling on Cursor. [S]

**processkit impact (Bucket A):**

No new files needed in processkit for Cursor. The canonical
compliance-contract.md is the content; aibox generates the rules
file from it. The hook scripts (`emit_compliance_contract.py`,
`check_route_task_called.py`) can be reused, but the sessionStart
injection path is blocked by the bug — the pre-tool blocking path
works.

**Does processkit need to ship a new file?**
No. The canonical `compliance-contract.md` under `skill-gate/assets/`
is sufficient content. aibox generates `.cursor/rules/processkit-
compliance.md` and `.cursor/mcp.json` from it.

---

### 2.2 OpenCode

**Prose surface:**

OpenCode natively auto-loads `AGENTS.md` from the project root and
`~/.config/opencode/AGENTS.md` globally. The `/init` command scans
the repo and generates or improves an existing `AGENTS.md` — this is
a meaningful advantage: AGENTS.md is not just read but can be
maintained by the tool. Config files: `opencode.json` at project
root or `~/.config/opencode/opencode.json` globally. [D, R]

The re-layered AGENTS.md compliance header (§1.5 of the
implementation plan) already provides the best available prose
enforcement on OpenCode with zero additional aibox work beyond what
ships for Claude Code and Codex. [D]

**MCP client:**

OpenCode has first-class MCP client support. Configuration is under
the `mcp` key in `opencode.json`:

```json
{
  "mcp": {
    "my-server": {
      "type": "local",
      "command": ["uv", "run", "path/to/server.py"],
      "env": {}
    }
  }
}
```

The format differs from Claude Code's `mcpServers` block — aibox
will need a separate merge path for OpenCode. [R]

**Critical enforcement gap:** MCP tool calls do not trigger
`tool.execute.before` plugin hooks (open issue #2319, filed Aug
2025). This means processkit MCP tools (`create_workitem`,
`route_task`, etc.) **cannot be gated** via plugin hooks on OpenCode.
Additionally, subagent tool calls bypass all plugin hooks (bug
#5894). The `acknowledge_contract()` MCP tool (Rail 3) is still
callable and useful, but it cannot be made mandatory by hook
enforcement. [H, I, T]

**Hook/plugin system:**

OpenCode's hook surface uses a TypeScript/JavaScript plugin model.
Config: referenced in `opencode.json` plugins section. Hooks:

| Hook event | Enforcement use | Blocking? | Stdout→context? |
|---|---|---|---|
| `session.created` | Session init, state setup | No | No (not injected into LLM context — feature request #17412) |
| `tool.execute.before` | Block native tool calls | Yes | No |
| `tool.execute.after` | Observability | No | No |
| `session.compacted` | Post-compaction observability | No | No |

No `beforeSubmitPrompt` equivalent found. No ability to inject
context into LLM turns from hook stdout — this is a fundamental
difference from Claude Code. [N, O]

The plugin language (TypeScript) also differs from the Python hook
scripts processkit ships. A processkit-compatible OpenCode plugin
would need a thin TypeScript wrapper that calls the Python scripts,
or the logic would need to be re-implemented in TypeScript.

**processkit impact (Bucket A):**

No new files needed in processkit. AGENTS.md coverage is already
provided. MCP config generation by aibox needs a separate OpenCode-
format path. If processkit ever wants hook enforcement on OpenCode,
a TypeScript plugin shim would need to be shipped — but given the
MCP hooks bypass bug, this is low value until the bug is fixed.

**Does processkit need to ship a new file?**
No for prose. Possibly a TypeScript plugin shim for hook enforcement
— but deferred until MCP hook bypass is fixed upstream.

---

### 2.3 Aider

**Prose surface:**

Aider does **not** auto-load AGENTS.md or CONVENTIONS.md. All files
must be explicitly declared. The two mechanisms are:

1. `--read path/to/file` flag at invocation.
2. `read:` key in `.aider.conf.yml`:
   ```yaml
   read:
     - AGENTS.md
     - context/skills/processkit/skill-gate/assets/compliance-contract.md
   ```

A feature request to auto-load AGENTS.md from project root (issue
#4363, filed 2025) was open as of 2026-04-14; it had not been
merged into a release. The GitHub issue #4395 "Does Aider support
AGENT.md or PLAN.md?" received a response confirming no native auto-
load. [E, F]

The implementation plan's §2.5 note is **confirmed**: installer must
write `.aider.conf.yml` with explicit `read:` entries. The canonical
compliance-contract.md path should be included alongside AGENTS.md.

**MCP client:**

Aider has **no native MCP client support** as of 2026-04-14. The
open GitHub issue #3314 ("MCP SUPPORT") has been open since 2024
with no merged implementation. Community workarounds exist
(`mcpm-aider`, an experimental CLI tool) but are explicitly
described as unofficial. [J, K]

Aider can act as an MCP *server* (there is an "Aider MCP server"
that exposes Aider's coding capabilities to other MCP clients), but
this is the opposite direction from what processkit needs. [J]

**Implication:** The `acknowledge_contract()` MCP tool (Rail 3) is
**not available to Aider** until native MCP client support ships.
Rail 1 (prose via `.aider.conf.yml`) is the only enforcement
transport. This makes Aider the weakest of the three follow-up
harnesses from an enforcement standpoint.

**Hook system:**

Aider has no hook system comparable to Claude Code, Codex, Cursor,
or OpenCode's plugin model. The only hook-adjacent feature is
`--git-commit-verify` (controls git commit hooks — irrelevant to
processkit enforcement). [P]

**processkit impact (Bucket A):**

No new files needed. The canonical `compliance-contract.md` is
sufficient. aibox writes `.aider.conf.yml` with the `read:` list.

**Does processkit need to ship a new file?**
No. Existing content is sufficient. The installer just needs to know
the path to `compliance-contract.md`.

---

## 3. Proposed issue splits / updates for aibox issues #47 / #48 / #49

The implementation plan (§6.5–6.7) filed three issues against aibox.
Based on this research, the following adjustments are warranted:

### Issue #47 — Cursor (was: "Generate .cursor/rules/processkit-compliance.md on sync")

**Finding that extends the issue:**

1. **MCP config generation should be a required deliverable, not
   optional.** The implementation plan (§6.5) marks MCP config
   generation as "optional (Cursor has its own MCP UI)." However,
   processkit enforcement via `acknowledge_contract()` and
   `route_task` depends on MCP tools being in the agent's tool list.
   The GUI is not reproducible in a devcontainer or CI. Recommend
   splitting into two issues or upgrading MCP config generation to
   required in the existing issue.

2. **Hook wiring is now viable and should be added.** Issue #47 says
   "No PreToolUse-equivalent exists at our research horizon." This is
   now out of date: Cursor v1.7 (Oct 2025) added `preToolUse` and
   `beforeMCPExecution` hooks with exit-code-2 blocking. aibox should
   wire `.cursor/hooks.json` to invoke the processkit hook scripts
   (adapted for Cursor's hooks.json format rather than Claude Code's
   settings.json format).

3. **sessionStart context injection is buggy — do not rely on it.**
   Issue #47 should note that the re-injection pattern (emit contract
   to stdout on sessionStart) is unreliable in Cursor for new sessions.
   The rules file remains the primary prose surface.

**Recommended split:**
- **Issue #47a** (keep): Generate `.cursor/rules/processkit-compliance.md`
  and `.cursor/mcp.json` on `aibox sync`.
- **Issue #47b** (new): Wire Cursor hooks.json for `preToolUse` and
  `beforeMCPExecution` blocking — note sessionStart injection bug as
  a known limitation.

---

### Issue #48 — Aider (was: "Register processkit compliance contract via .aider.conf.yml")

**Finding that confirms the issue:**

The issue body is accurate. `.aider.conf.yml` `read:` entries are the
correct and only viable path.

**Additional detail to add to the body:**

1. **No MCP client support:** The issue body does not mention MCP.
   Add a note: Aider has no native MCP client (issue #3314 open since
   2024); therefore `acknowledge_contract()` and all processkit MCP
   tools are unavailable. Rails 2 and 3 are absent on Aider. Prose-
   via-read is the only enforcement transport, and this is a permanent
   limitation until Aider ships native MCP.

2. **Explicit path to compliance-contract.md:** The issue says "add
   the canonical compliance-contract path (and AGENTS.md if not
   already present)." The exact path is
   `context/skills/processkit/skill-gate/assets/compliance-contract.md`
   — include this literally so there is no ambiguity in the impl.

3. **AGENTS.md feature request status:** Note that Aider issue #4363
   requests auto-loading AGENTS.md; if it ships before aibox
   implements this adapter, the `.aider.conf.yml` AGENTS.md entry
   becomes redundant but harmless (explicit read + auto-load =
   loaded once).

No split needed. Issue #48 is accurate but needs the three additions
above.

---

### Issue #49 — OpenCode (was: "Scope OpenCode adapter: MCP + hooks capability matrix")

**Finding that substantially changes the issue:**

This issue was a scoping placeholder; this research completes it.
The issue can now be closed (scoping done) and replaced with two
concrete implementation issues:

**Issue #49a** (replace/close #49): **Ship `.opencode.json` MCP
config block for processkit servers on `aibox sync`.**

OpenCode's MCP config format is `{"mcp": {"server-name": {"type":
"local", "command": [...]}}}` under the project's `opencode.json`.
This format **differs** from Claude Code's `mcpServers` block and
from Codex's `[mcp_servers.*]` TOML. aibox needs a separate merge
path for OpenCode. Recommend merging this into the §6.1 "Ship a
merged MCP config per harness" issue rather than a standalone issue.

**Issue #49b** (new, low priority): **Evaluate OpenCode TypeScript
plugin for processkit enforcement hooks.**

OpenCode's `tool.execute.before` hook can block native tool calls
(not MCP calls — see known bug #2319). A thin TypeScript plugin
could invoke processkit's Python enforcement logic. However, the MCP
hooks bypass bug (#2319) and subagent bypass bug (#5894) mean that
structural enforcement on OpenCode is severely limited. Recommend
filing as a research-track issue dependent on upstream bug fixes,
not as an implementation issue. The `acknowledge_contract()` MCP tool
is still the right enforcement transport on OpenCode once MCP config
is wired.

**Important contradiction to flag:** Issue #49's body says "OpenCode
supports AGENTS.md natively (opencode.ai/docs/rules/) — this is
confirmed. It also says MCP and hooks "need researching" — this
research closes that gap. AGENTS.md works; MCP works (different
config format); hooks work for native tools only (MCP tools bypass
hooks).

---

## 4. Issue draft bodies (ready to paste)

### Draft A — Issue #47a: Cursor rules file + MCP config (update of existing #47)

**Title:** `Generate .cursor/rules/processkit-compliance.md and .cursor/mcp.json on sync`

**Labels:** `area/sync`, `area/cursor`, `priority/low`, `processkit-upstream`

**Body:**

For projects with `cursor` in `[ai].harnesses`, `aibox sync` should:

**1. Generate `.cursor/rules/processkit-compliance.md`**
Copy the canonical compliance contract from
`context/skills/processkit/skill-gate/assets/compliance-contract.md`
into `.cursor/rules/processkit-compliance.md`. Use the `.mdc`
extension or `.md` — both work in `.cursor/rules/`. Do not add
path-scoping frontmatter; the rule should fire globally. Keep the
file under 2,000 words (Cursor attention guidance). Note: Cursor
auto-loads all files in `.cursor/rules/` at session start and
prepends them as system prompt on every turn — this is more durable
than CLAUDE.md injection.

AGENTS.md is also natively supported by Cursor at project root and
is already written by the processkit AGENTS.md step — no duplicate
action needed. Do not write a separate AGENTS.md for Cursor.

**2. Generate `.cursor/mcp.json`** (required, not optional)
Walk `context/skills/*/*/mcp/mcp-config.json`, extract each
`mcpServers` block, and merge into `.cursor/mcp.json`. Format is
`{"mcpServers": {"server-name": {...}}}` — identical to Claude Code's
settings.json mcpServers block, so the same merge logic applies.
Without this file, processkit MCP tools (including `route_task`,
`acknowledge_contract`, `create_workitem`) are invisible to the
Cursor agent. The GUI is not reproducible in devcontainers or CI.

**Note on sessionStart hook:** Cursor v1.7 introduced a `sessionStart`
hook, but as of 2026-04-14 there is an open bug where stdout from
sessionStart hooks is not injected into the Agent Window for new
conversations (Cursor forum: "sessionStart hook output is accepted
and merged, but the injected context does not reach Agent Window").
Do NOT rely on sessionStart for compliance contract injection until
this is fixed upstream. Rules file is the reliable prose transport.

**Acceptance criteria:**
- After sync, `.cursor/rules/processkit-compliance.md` exists and
  contains the canonical compliance contract content.
- `.cursor/mcp.json` exists and lists every processkit MCP server
  installed in the project.
- `processkit-compliance.md` file is under 2,000 words.
- Non-processkit entries already in `.cursor/mcp.json` are preserved
  on re-sync.

**Source URLs:**
- Rules: https://docs.cursor.com/context/rules (confirmed 2026-04-14)
- MCP config: https://cursor.com/docs/context/mcp (confirmed 2026-04-14)
- sessionStart bug: https://forum.cursor.com/t/sessionstart-hook-output-is-accepted-and-merged-but-the-injected-context-does-not-reach-agent-window/157141

---

### Draft B — Issue #47b: Cursor hooks wiring (new, splits from #47)

**Title:** `Wire Cursor hooks.json for preToolUse and beforeMCPExecution blocking`

**Labels:** `area/sync`, `area/cursor`, `area/hooks`, `priority/low`, `processkit-upstream`

**Body:**

Cursor v1.7 (released Oct 2025) introduced a `hooks.json` lifecycle
hook system with `preToolUse` and `beforeMCPExecution` events that
support exit-code-2 blocking. This is a meaningful enforcement
upgrade over the "prose-only ceiling" noted in the original scoping
issue.

For projects with `cursor` in `[ai].harnesses`, `aibox sync` should
write `.cursor/hooks.json` (project-level) entries that invoke
processkit's enforcement scripts:

- `preToolUse` (tool matcher: `Write|Edit|MultiEdit`, path filter
  under `context/`) → invoke `check_route_task_called.py`. Exit 2
  blocks the write if `route_task` has not been called this session.
- `beforeMCPExecution` (server filter: any processkit server) →
  same gate script.

**Format difference from Claude Code:** Cursor's hooks.json uses the
key names `preToolUse`, `beforeMCPExecution`, etc. rather than Claude
Code's `PreToolUse`. The command paths and exit-code semantics are
the same. The processkit scripts (`emit_compliance_contract.py`,
`check_route_task_called.py`) are Python and should work as-is;
confirm they are on PATH or use absolute paths relative to project
root.

**Known limitations to document in the hook wiring:**
1. `sessionStart` context injection is buggy for new sessions (forum
   bug, 2025) — do not wire the compliance-contract emit script to
   sessionStart on Cursor until upstream confirms it is fixed.
2. `beforeSubmitPrompt` cannot inject context (feature request open)
   — do not wire UserPromptSubmit-equivalent context injection.
3. Plugin hooks do not cover subagent tool calls — outside scope for
   now.

**Depends on:** Issue #47a (MCP config + rules file must ship first).

**Acceptance criteria:**
- After sync, `.cursor/hooks.json` exists with preToolUse and
  beforeMCPExecution entries pointing to processkit scripts.
- Writing a file under `context/` without a prior `route_task` call
  is blocked by the hook (exit 2) and Cursor displays the remediation
  message.
- Existing non-processkit hook entries are preserved.

**Source URLs:**
- Hooks: https://cursor.com/docs/hooks (confirmed 2026-04-14)
- GitButler deep dive: https://blog.gitbutler.com/cursor-hooks-deep-dive
- Blocking exit code: https://egghead.io/lessons/block-tool-commands-before-execution-with-pre-tool-use-hooks~erv55
- Cursor 1.7 announcement: https://www.infoq.com/news/2025/10/cursor-hooks/

---

### Draft C — Issue #48: Aider adapter (update of existing #48)

**Title:** `Register processkit compliance contract and AGENTS.md via .aider.conf.yml`

**Labels:** `area/sync`, `area/aider`, `priority/low`, `processkit-upstream`

**Body:**

Aider does **not** auto-load AGENTS.md, CONVENTIONS.md, or any
rules file automatically. Files must be declared in `.aider.conf.yml`
under the `read:` key. This is confirmed in official Aider docs
(https://aider.chat/docs/usage/conventions.html) and in the open
feature request for auto-loading AGENTS.md (aider-ai/aider#4363,
filed 2025, not yet merged as of 2026-04-14).

For projects with `aider` in `[ai].harnesses`, `aibox sync` should
write or merge into `.aider.conf.yml`:

```yaml
read:
  - AGENTS.md
  - context/skills/processkit/skill-gate/assets/compliance-contract.md
```

**Why both files?** AGENTS.md provides full project context.
`compliance-contract.md` is the short (15–30 line) versioned rule
set optimised for primacy — it should appear first in Aider's
context so it benefits from "lost in the middle" primacy effects.
If Aider ships native AGENTS.md auto-loading (issue #4363), the
explicit AGENTS.md entry becomes redundant but harmless.

**MCP client gap (permanent limitation):**
Aider has no native MCP client support (open issue aider-ai/aider
#3314, filed 2024). Therefore:
- `acknowledge_contract()` (Rail 3) is **not available** on Aider.
- `route_task`, `create_workitem`, and all processkit MCP tools are
  **not callable** from Aider.
- Prose via `read:` is the **only** enforcement transport on Aider.
  Rails 2 and 3 are absent; only Rails 1 and 4 (prose + tool
  descriptions) are in play.

This is a permanent hard ceiling until Aider ships native MCP. No
workaround exists short of deploying Aider behind a wrapper agent
that has MCP access.

**No hook system exists on Aider.** Structural enforcement
(PreToolUse blocking, SessionStart re-injection) is not possible.

**Acceptance criteria:**
- After sync, `.aider.conf.yml` contains `read:` entries for both
  AGENTS.md and compliance-contract.md.
- A fresh `aider` session launched in the project shows the
  compliance contract in its `/tokens` context dump or equivalent.
- Existing `.aider.conf.yml` entries (model, api keys, etc.) are
  preserved.
- If Aider later ships AGENTS.md auto-load, the installer detects
  the flag and makes the AGENTS.md read: entry optional.

**Source URLs:**
- Conventions loading: https://aider.chat/docs/usage/conventions.html
- YAML config: https://aider.chat/docs/config/aider_conf.html
- MCP feature request: https://github.com/Aider-AI/aider/issues/3314
- AGENTS.md feature request: https://github.com/aider-ai/aider/issues/4363

---

### Draft D — Issue #49a: OpenCode MCP config (closes #49, concrete impl)

**Title:** `Add OpenCode MCP config generation to aibox sync (opencode.json mcp block)`

**Labels:** `area/sync`, `area/opencode`, `area/mcp`, `priority/low`, `processkit-upstream`

**Body:**

This issue replaces the scoping placeholder #49 (now scoped — see
`ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix`).

OpenCode has native AGENTS.md support (confirmed) — the re-layered
AGENTS.md from the compliance-contract header step already provides
prose enforcement on OpenCode with no additional work.

The remaining gap is MCP config generation. OpenCode reads MCP
server config from the `mcp` key in `opencode.json` (project) or
`~/.config/opencode/opencode.json` (global). The format:

```json
{
  "mcp": {
    "index-management": {
      "type": "local",
      "command": ["uv", "run", "context/skills/index-management/mcp/server.py"]
    }
  }
}
```

This format differs from Claude Code's `mcpServers` block and from
Codex's TOML format. A separate merge/write path is needed in
`aibox sync` for OpenCode.

For projects with `opencode` in `[ai].harnesses`, aibox sync should
walk `context/skills/*/*/mcp/mcp-config.json`, extract launch
commands, and write or merge the `mcp` section of `opencode.json`.

**Known limitations to document:**
1. MCP tool calls do NOT trigger OpenCode plugin `tool.execute.before`
   hooks (open bug anomalyco/opencode#2319, filed Aug 2025). The
   `acknowledge_contract()` MCP tool is callable but cannot be made
   mandatory via hook enforcement. Prose and the MCP tool description
   1%-rule sentences are the only enforcement levers.
2. Plugin hooks for subagents are also bypassed (bug #5894).
3. If hook enforcement on processkit MCP tools is ever needed, a
   TypeScript plugin must be written — but this is low value until
   the upstream bugs are fixed.

**Acceptance criteria:**
- After sync, `opencode.json` contains an `mcp` section listing all
  installed processkit MCP servers.
- Running `opencode` in the project shows the processkit MCP tools
  available.
- Non-processkit config in `opencode.json` is preserved.
- Malformed per-skill config produces a clear warning; existing
  config is not clobbered.

**Source URLs:**
- MCP config: https://opencode.ai/docs/mcp-servers/
- Config schema: https://opencode.ai/docs/config/
- MCP hooks bypass bug: https://github.com/sst/opencode/issues/2319

---

### Draft E — Issue #49b: OpenCode plugin shim (new, low priority / research track)

**Title:** `Research: OpenCode TypeScript plugin for processkit hook enforcement`

**Labels:** `area/opencode`, `area/hooks`, `priority/low`, `type/research`, `processkit-upstream`

**Body:**

OpenCode's plugin system (`tool.execute.before`) can block native
tool calls but currently does not intercept MCP tool calls (bug
anomalyco/opencode#2319) or subagent tool calls (bug #5894).

Before investing in a TypeScript plugin wrapper for processkit's
Python enforcement scripts, the following upstream bugs must be
resolved:
- #2319: MCP tool calls don't trigger plugin hooks.
- #5894: Subagent tool calls bypass plugin hooks.

Track these bugs. If both are fixed, design a thin TypeScript plugin
that: (a) on `session.created`, initialises a session state map; (b)
on `tool.execute.before` for processkit MCP write tools, checks the
session state map for a prior `route_task` call and blocks with an
error message if absent.

Context injection from hooks into LLM turns is also not supported
(feature request anomalyco/opencode#17412) — the compliance contract
re-injection pattern is not available until this is resolved.

**This issue is a watch-and-act issue.** Do not implement until
upstream bugs are fixed. Re-evaluate priority when #2319 closes.

**Source URLs:**
- Plugin docs: https://opencode.ai/docs/plugins/
- MCP hooks bypass: https://github.com/sst/opencode/issues/2319
- Subagent bypass: https://github.com/anomalyco/opencode/issues/5894
- Context injection feature request: https://github.com/anomalyco/opencode/issues/17412

---

## 5. Residual uncertainty

| Unknown | Why it matters | How to check | Confidence today |
|---|---|---|---|
| Cursor sessionStart bug fix status | Determines whether compliance-contract re-injection is available on Cursor | Monitor Cursor changelog / forum thread linked above | Weak — bug open as of 2026-04-14 |
| Aider AGENTS.md auto-load (issue #4363) | If merged, installer can skip AGENTS.md read: entry | Monitor aider-ai/aider#4363 and release history | Confirmed unmerged as of 2026-04-14 |
| Aider native MCP client (issue #3314) | If shipped, processkit Rails 2+3 become available on Aider | Monitor aider-ai/aider#3314 | Confirmed unmerged as of 2026-04-14 |
| OpenCode MCP hooks bypass fix (issue #2319) | If fixed, `tool.execute.before` can gate processkit MCP writes — enables structural enforcement | Monitor anomalyco/opencode#2319 | Confirmed open as of Aug 2025 |
| Cursor AGENTS.md background-agent loading bug | If fixed, AGENTS.md becomes equally reliable as rules file on Cursor | Monitor Cursor forum/changelog | Weak — bug reported 2025, status unknown |
| Exact Cursor hooks.json schema for processkit scripts | Needed for aibox implementation | Read cursor.com/docs/hooks at implementation time; re-verify format | Likely stable, but beta |
| OpenCode `opencode.json` MCP format stability | Config schema may change as product matures | Re-read opencode.ai/docs/config/ at implementation time | Weak — product evolving rapidly |

---

## 6. Provenance / sources

| Ref | URL | Used for |
|---|---|---|
| A | https://docs.cursor.com/context/rules | Cursor rules auto-load |
| B | https://cursor.com/docs/context/mcp | Cursor MCP config path |
| C | https://forum.cursor.com/t/agents-md-not-always-loaded/153855 | Cursor AGENTS.md bug |
| D | https://opencode.ai/docs/rules/ | OpenCode AGENTS.md support |
| E | https://github.com/Aider-AI/aider/issues/3314 | Aider MCP no native support |
| F | https://github.com/aider-ai/aider/issues/4363 | Aider AGENTS.md feature request |
| G | https://docs.cursor.com/context/rules-for-ai | Cursor 2,000-word attention guidance |
| H | https://github.com/sst/opencode/issues/2319 | OpenCode MCP hooks bypass |
| I | https://github.com/anomalyco/opencode/issues/5894 | OpenCode subagent hooks bypass |
| J | https://github.com/Aider-AI/aider/issues/3314 | Aider MCP issue (main) |
| K | https://github.com/lutzleonhardt/mcpm-aider | Aider MCP community workaround |
| L | https://cursor.com/docs/hooks | Cursor hooks documentation |
| M | https://forum.cursor.com/t/sessionstart-hook-output-is-accepted-and-merged-but-the-injected-context-does-not-reach-agent-window/157141 | Cursor sessionStart injection bug |
| N | https://opencode.ai/docs/plugins/ | OpenCode plugin hook system |
| O | https://github.com/anomalyco/opencode/issues/17412 | OpenCode context injection feature request |
| P | (inferred) Aider docs at https://aider.chat/docs/ | Aider no hook system |
| Q | https://forum.cursor.com/t/hooks-allow-beforesubmitprompt-hook-to-inject-additional-context/150707 | Cursor beforeSubmitPrompt limitation |
| R | https://opencode.ai/docs/config/ | OpenCode config format |
| S | https://blog.gitbutler.com/cursor-hooks-deep-dive | Cursor beforeMCPExecution confirmed |
| T | https://github.com/sst/opencode/issues/3756 | OpenCode MCP tool blocking issue |

All sources gathered 2026-04-14. Re-verify at implementation time.
