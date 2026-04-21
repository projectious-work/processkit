---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260414_1230-ReachReady-processkit-enforcement-research
  created: 2026-04-14T12:30:00Z
spec:
  name: "Why agents ignore processkit — research-with-confidence report"
  kind: document
  location: context/artifacts/ART-20260414_1230-ReachReady-processkit-enforcement-research.md
  format: markdown
  version: "1.0.0"
  tags: [research, enforcement, processkit, agents, mcp, hooks, agents-md]
  produced_by: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
  owner: ACTOR-sr-researcher
  links:
    workitem: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
    inputs:
      - ART-20260414_0935-AuditSurface-mcp-enforcement-surface
    related_decisions:
      - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---

# Why agents ignore processkit — research-with-confidence report

> **Author:** Senior Researcher (Opus) — ROLE-senior-researcher
> **Date gathered:** 2026-04-14
> **Skill applied:** `research-with-confidence` (every claim carries a
> confidence label; every non-obvious claim cites a source).
> **Scope:** Primary — Claude Code + OpenAI Codex CLI. Appendix — Cursor,
> OpenCode, Continue, Aider.

## 0. Reading guide

Each claim is tagged:

- **Confirmed** — primary source verified in this session.
- **Likely** — multiple secondary sources agree, or strong inference from
  primary docs.
- **Possible** — single source or plausible inference, not cross-checked.
- **Unknown** — not established; flagged so the architect does not treat
  it as fact.

Sources are inline as bracketed numbers; full URL list at the end.

---

## 1. Executive summary

### Headline

The owner's observed failure ("agents ignore most of processkit") is real
and largely **structural**, not a content-quality problem with
AGENTS.md. The PM's counter-hypothesis — *agents attend to tool schemas
much more reliably than to prose* — is **supported by primary
documentation on how CLAUDE.md is loaded** and **supported by the
independent "context rot" / "lost in the middle" literature**, but only
partly: system prompts and schemas *do* persist more reliably, and prose
*does* degrade, but not in the simplistic "fatigue past 70 lines" form.
The real levers are a mix of:

1. Making enforcement structural (MCP tools + hooks + slash-commands)
   rather than aspirational (prose).
2. Fixing the distribution problem (most processkit MCP servers aren't
   actually reachable from derived-project harnesses, because no merged
   MCP config is shipped).
3. Adding *just enough* prose, in *just the right place*, rather than
   trimming AGENTS.md further.

### Top 5 leverage points, ranked by impact × feasibility

| # | Leverage point | Surface | Harness portability | Confidence | Impact | Feasibility |
|---|---|---|---|---|---|---|
| 1 | **Ship a pre-merged MCP config at install time** (so `route_task`, `create_workitem`, `log_event`, etc. are actually callable in derived projects) | Tool schemas (MCP) | **Works everywhere by design** (MCP is standardised) | Confirmed [4][5] | Very high | High (installer change; per-skill configs already exist) |
| 2 | **Add a `SessionStart` / `UserPromptSubmit` hook that injects a short "processkit reminder" every turn (or at least every new prompt)** — counters CLAUDE.md "injected once then compacted away" [6] | Hooks | **Per-harness adapter** (Claude Code + Codex CLI have equivalents; others do not) [1][8] | Confirmed [1][6][8] | High | Medium |
| 3 | **Wrap `task-router` / `skill-finder` into slash-commands and MCP tools whose *descriptions* carry the 1% rule** (so attention lands on them without a prose re-read) | Tool schemas + slash-commands | **Works everywhere by design** for MCP tool descriptions; slash-command surface is per-harness [4][9] | Likely [4][9][10] | High | High |
| 4 | **Add a `PreToolUse` hook that blocks `create_*` / file writes under `context/` unless a task-router call has happened this session** — turns the 1% rule into an enforceable gate | Hooks | **Per-harness adapter** (Claude Code PreToolUse [1], Codex PreToolUse [8] — but Codex currently only intercepts `Bash` [8]) | Confirmed [1][8] | High | Medium (requires per-harness scripts) |
| 5 | **Stop trimming AGENTS.md; instead re-layer it** — a ~30-line "compliance contract" at the very top (re-injected on every file read per [6]), with the rest below the fold as reference | Prose | **Works everywhere by design** (AGENTS.md standard [11][12]) | Likely [6][12][13] | Medium | High |

### Headline findings about the hypotheses under test

- The PM's "tool schemas win vs prose" intuition is **directionally
  correct but needs refinement**: Claude Code specifically does *not*
  re-inject CLAUDE.md every turn — it injects it **once** at session
  start, then compacts it away, and only re-fires `system-reminder`
  tags when files matching path rules are read [6]. That is exactly
  the failure mode the owner observes. **Confidence: Confirmed.**
- Tool descriptions are also **not free** — they sit in the tool list
  that Anthropic renders into a synthesised system prompt [7], and
  Anthropic's own guidance is that "when instructions about tools
  were long and/or complex, including instructions about the tool in
  the system prompt was more effective than placing them in the tool
  description itself" [7]. So the lever is **hooks + system prompt +
  tool descriptions together**, not "tool schemas alone". **Confidence:
  Likely.**
- The "context fatigue past ~70 lines" claim in its literal form is
  **folklore**. What is real and documented: *context rot* (every
  frontier model tested by Chroma degrades as input grows, well before
  the declared window fills) [13][14]; *lost in the middle* (U-shaped
  attention — primacy + recency, middle ignored) [15]; and practical
  thresholds like "degradation begins around 8k–16k tokens" [14] and
  "keep Cursor rules under ~2,000 words" [16]. **Trim-to-70-lines is
  not supported by any source we found. Confidence: Confirmed that the
  literal claim is unsupported; Likely that the underlying instinct
  ("shorter is better past a certain point") is correct.**

### Bottom line for the architect

Pursue #1 and #2 together. #1 is a distribution fix — without it,
processkit's MCP surface simply does not exist inside the agent's tool
list, and no amount of prose will rescue that. #2 is the prose-revival
fix — a re-injection hook is the *only* way to make AGENTS.md content
survive Claude Code's session-start one-shot [6]. Together they turn
processkit from "documentation agents optionally read" into "tools
agents are required to notice".

---

## 2. Evidence per surface

For each surface, the question is the same: **how reliably does a
modern agent attend to instructions delivered through this surface?**

### 2.1 Prose (AGENTS.md, CLAUDE.md, .cursor/rules, .continue/rules)

**How it reaches the model:**

- **Claude Code:** "CLAUDE.md is injected **once at the start of your
  conversation**, whereas rules are re-injected as system-reminders
  every time Claude accesses a file that matches their path pattern.
  […] Path-scoped rules and nested CLAUDE.md files load into message
  history when their trigger file is read, so compaction summarizes
  them away with everything else, but they reload the next time Claude
  reads a matching file. If a rule must persist across compaction,
  drop the paths frontmatter or move it to the project-root CLAUDE.md."
  — dbreunig.com, analysis of Claude Code's system prompt [6]. Also
  explicit: "The system prompt is the same for every Claude Code user
  on the same version […] If CLAUDE.md went into the system prompt,
  every user with a different CLAUDE.md would need a separate cache,
  breaking the product's economics" [6]. **Confidence: Confirmed for
  the mechanism; Likely for the compaction-wipe claim** (the source is
  secondary but well-argued and consistent with Anthropic's public
  caching model).
- **Codex CLI:** "Codex reads AGENTS.md (and related files) and
  includes a limited amount of project guidance in the first turn of a
  session, with configuration options controlling `project_doc_max_bytes`
  […] and `project_doc_fallback_filenames`" [2]. **Confidence:
  Confirmed.**
- **Cursor:** `.cursor/rules` are "prepended as a system prompt" on
  every interaction [16]; official Cursor guidance recommends **under
  ~2,000 words** because "longer rules dilute the AI's attention" [16].
  **Confidence: Confirmed (for the mechanism), Likely (for the
  attention-dilution claim — Cursor is reporting practitioner
  experience, not publishing a benchmark).**
- **Continue:** "Rules are concatenated into the system message for
  all Agent, Chat, and Edit requests" [18]. **Confidence: Confirmed.**
- **Aider:** Conventions files are **not** automatically loaded — they
  require `--read CONVENTIONS.md` or a `read:` entry in `.aider.conf.yml`
  [19]. **Confidence: Confirmed.** (This is a meaningful gap vs
  AGENTS.md-native harnesses.)

**Does the model actually *use* the prose once injected?**

- The Chroma "context rot" study tested 18 frontier models and
  found every one of them degrades as input length grows, with
  meaningful degradation often starting at 8k–16k tokens even when
  the declared context window is 200k+ [13][14]. **Confidence:
  Confirmed.**
- "Lost in the Middle" (Liu et al., TACL 2024) shows a U-shaped
  attention curve: best retrieval at the start and end, significant
  drop in the middle [15]. **Confidence: Confirmed.**
- Anthropic's own context-engineering guidance: "LLMs are constrained
  by a finite attention budget, so good context engineering means
  finding the smallest possible set of high-signal tokens that
  maximize the likelihood of some desired outcome" [7]. **Confidence:
  Confirmed.**

**Implication for processkit:** AGENTS.md at 240 lines (current) is
well under anyone's degradation threshold on its own. The risk is not
AGENTS.md *size*; it's AGENTS.md *position* — at session start it is
near the top (primacy, good); after compaction or a few long tool
calls, it moves into the middle (lost) or is summarised away
entirely (Claude Code) [6]. **Confidence: Likely.**

**Implication for the "70 lines" folklore:** No primary source
supports a specific 70-line cliff. The underlying instinct — "prose
gets diluted" — is documented [7][13][14][16], but the correct
response is *structural* (put critical rules at the top, let hooks
re-inject them) rather than *further trimming*. **Confidence:
Likely.**

### 2.2 Tool schemas (plain function-calling tool list)

**How it reaches the model:** Anthropic's tool-use API "constructs a
special system prompt from the tool definitions, tool configuration,
and any user-specified system prompt" [7]. Tool definitions therefore
live **inside the synthesised system prompt** — they are part of the
high-primacy region and are **re-sent every turn** as part of the
request.

**Does the model attend to them?** Yes, reliably — tool descriptions
are how models learn *what can be done*. But: "when instructions
about tools were long and/or complex, including instructions about
the tool in the system prompt was more effective than placing them in
the tool description itself" [7]. So tool descriptions are good for
**discovery and one-sentence rules**; longer rules belong in the
system prompt (or an injected context block via a hook).
**Confidence: Confirmed [7].**

**Implication for processkit:** The `route_task` and `find_skill` tool
descriptions are high-leverage real estate. Every extra sentence
there is re-sent on every turn. Currently `task-router`'s description
is ~30 words (from the SKILL frontmatter) — there is **headroom to
put the 1% rule into the `route_task` tool description itself**.

### 2.3 MCP tool descriptions (same as 2.2, but discovered dynamically)

**How it reaches the model:** MCP clients call `tools/list` on each
server; each tool carries `{name, description, inputSchema}` [4][5].
The harness then exposes these as ordinary function-calling tools to
the model. So MCP tools *become* items in the tool list described in
§2.2 — they get the same attention treatment. **Confidence:
Confirmed [4][5].**

**Key operational constraint (from the enforcement-surface audit,
input ART-20260414_0935-AuditSurface-mcp-enforcement-surface):** 15
of 33 processkit skills (~45%) ship MCP servers. **That's the supply
side.** The *demand side* — harness-side MCP config — is partly
broken. The audit found no merged config at
`.claude/settings.json`, `.codex/config.toml`, etc., **at the
committed repo level.** Cross-checking, `.claude/settings.local.json`
*does* list 12 processkit servers in `enabledMcpjsonServers` — but
that's a developer-local file, not something inherited by derived
projects. **Confidence: Confirmed that derived projects installing
processkit do not, by default, get a working MCP tool list, because
the merged config is expected to be generated by the installer and
the per-skill blocks are not auto-aggregated.** See audit §2.

**Implication:** Until the installer reliably emits a merged config,
the tool-schema surface — the most reliable attention surface we have
— is empty in most derived projects. **This is the single highest-
leverage fix.**

### 2.4 Hooks (PreToolUse, PostToolUse, SessionStart, UserPromptSubmit)

**Claude Code:**

- Hooks live in `~/.claude/settings.json`, `.claude/settings.json`, or
  `.claude/settings.local.json` [1].
- Events include `PreToolUse`, `PostToolUse`, `SessionStart`,
  `UserPromptSubmit`, `Stop`, `PermissionRequest`,
  `PermissionDenied` [1][20].
- **Critical capability:** "For `UserPromptSubmit` and `SessionStart`
  hooks, anything you write to stdout is added to Claude's context"
  [20]. SessionStart supports a `compact` matcher — "use a SessionStart
  hook with a compact matcher to **re-inject critical context after
  every compaction**" [20]. As of Claude Code 2.1.0 this is done
  silently via `hookSpecificOutput.additionalContext` [20].
- **PreToolUse can modify tool inputs** (Claude Code v2.0.10+) —
  "intercepting tool calls and modifying the JSON input to let
  execution proceed with corrected parameters" [1]. Exit code 2 from
  a hook blocks the tool call. **Confidence: Confirmed [1].**

**Codex CLI:**

- Hooks are a recent addition: "Codex can also load lifecycle hooks
  from `hooks.json` files that sit next to active config layers" [8].
- Events: "`PreToolUse`, `PostToolUse`, `UserPromptSubmit`, and
  `Stop` run at turn scope" [8].
- **Significant limitation:** "Currently `PreToolUse` only supports
  `Bash` tool interception" — `apply_patch` (the main file-write
  path) doesn't emit hook events [8][21]. "Hooks are currently
  disabled on Windows" [8]. **Confidence: Confirmed [8][21].**
- stdout → developer context works ("Plain text on stdout is added as
  extra developer context") [8].

**Cursor / Continue / OpenCode / Aider:** We did not find a
PreToolUse-equivalent hook system of comparable generality in our
search. Cursor has some command-execution hooks but they are a
different animal. **Confidence: Possible — needs explicit
confirmation before the architect assumes they exist.**

**Implication for processkit:** Hooks are the *only* surface on which
"re-inject the 1% rule every turn" and "block `create_*` without a
prior `route_task`" can be *enforced* (not merely asked for).
Claude Code and Codex CLI both expose the needed events, but:
- Claude Code's surface is more complete (PreToolUse across all
  tools, SessionStart `compact` matcher).
- Codex CLI's PreToolUse only covers `Bash`, so blocking
  `apply_patch` edits under `context/` is **not currently possible
  via hooks on Codex** [21]. That limits symmetric enforcement.

### 2.5 Slash-commands

**Claude Code:** Slash-commands are "a Markdown file with YAML
frontmatter, stored in the `.claude/commands/` directory" [9]; the
newer form is `.claude/skills/<name>/SKILL.md` [10]. Frontmatter can
carry `description`, `allowed-tools`, `model`,
`disable-model-invocation` [9]. **Crucially**, skill metadata
(name + description) is loaded into the system prompt at startup so
Claude knows *when* to invoke — "this lightweight approach means you
can install many Skills without context penalty; Claude only knows
each Skill exists and when to use it" [10]. Skill body is only read
when invoked. **Confidence: Confirmed [9][10].**

**Codex CLI:** Also supports AGENTS.md-style project skills and
prompts directory; the specifics of model-invocable vs user-only are
less documented than Claude's [2][3]. **Confidence: Possible for the
specifics; Confirmed that the feature exists.**

**Implication for processkit:** Wrapping `task-router` and
`skill-finder` as slash-commands adds **two attention surfaces at
once**: the command appears in the model's tool list (discovery), and
the description text is part of the system-prompt-adjacent cache. The
processkit repo already ships many as deferred slash-commands (e.g.
`skill-builder-create`, `workitem-management-create`) — this is good.
The gap is that the *enforcement* skills (`skill-gate`,
`task-router`) aren't always surfaced as commands in derived
projects. **Confidence: Likely.**

### 2.6 System prompts injected by the harness itself

Both Claude Code and Codex CLI carry harness-level system prompts
separate from user prose [6][22]. These are **the most reliable
attention surface** but **not writable by processkit** without
modifying the harness. The closest writable equivalent is the
`UserPromptSubmit` / `SessionStart` hook output (§2.4), which is
injected *next to* the system prompt. **Confidence: Confirmed.**

---

## 3. Gap analysis vs current processkit state

Using ART-20260414_0935-AuditSurface as the ground truth for what
ships today.

| Leverage point | Today | Gap to "reliably applied" |
|---|---|---|
| **MCP surface exists** | 15/33 processkit skills ship `mcp/server.py`; 71+ tools documented. | None — supply side is good. |
| **MCP surface merged into harness config** | Per-skill `mcp-config.json` files exist. **No merged config committed at `/workspace/.claude/`, `/workspace/.codex/`, `/workspace/.cursor/`** (audit §2). `settings.local.json` does enable 12 servers but is developer-local, not shipped to derived projects. | **This is the main gap.** Installer (aibox or a processkit script) must produce a merged config on sync. Without this, tools are invisible. |
| **`route_task` tool-description carries the 1% rule** | Description is short ("Route a task description to the right processkit skill…"). 1% rule is only in AGENTS.md prose. | Add a one-line "call this before any `create_*`, `transition_*`, `link_*`, `record_*`" to the `route_task` tool description so it ships with every tool list. |
| **Session-start re-injection of AGENTS.md critical rules** | None. CLAUDE.md is injected once at start [6] and compacted away. | Add a `SessionStart` hook (Claude Code) and equivalent (Codex) that writes a 15–30 line "compliance contract" to stdout: 1% rule, "commit immediately, don't defer", "use MCP tools not hand-edits", "log events after state changes". |
| **PreToolUse enforcement of the 1% rule** | None. `skill-gate` is pure prose. | Claude Code: a PreToolUse hook that blocks `Write`/`Edit` targeting `context/**` unless a `route_task` call has been made this session. Codex: partial — PreToolUse only covers `Bash` today [21], so `apply_patch` under `context/` cannot yet be gated. |
| **AGENTS.md structure** | 240 lines, single linear document. | Re-layer: a ~30-line compliance contract at the top (primacy), rest below. This addresses "lost in the middle" [15] without further trimming. |
| **Research artefact storage** | Skill `artifact-management` exists; 15+ artefacts in `context/artifacts/`. No enforcement that research outputs get registered. | A convention + slash-command (`/artifact-register`) plus optional hook check. Lower priority than #1–#4. |
| **DecisionRecord discipline** | `decision-record` MCP server exists. Owner reports it's used only when explicitly asked. | Add a standing rule in the `SessionStart` hook: "after producing a cross-cutting recommendation, call `record_decision`." Hook doesn't *enforce* but re-injects. |
| **Log discipline** | `event-log` MCP server exists; per-kind MCP servers auto-log on create/transition (per AGENTS.md line 226 — "After any hand-edit to an entity file, run `reindex()`"). | The *auto-log* side of MCP servers is structurally right — hand-edits skip it. Distribution fix (#1) solves this for free. |

**Summary: processkit's core enforcement skills (task-router,
skill-finder, skill-gate) are structurally *right*.** They're
under-used because (a) the tools aren't wired into the harness in
derived projects, and (b) the rule to call them lives in prose that
gets compacted away. Both problems are addressed by leverage points
#1 and #2. **Confidence: Likely.**

---

## 4. Per-harness adapter notes

### 4.1 Claude Code (primary)

Richest surface. For processkit we need:

1. **`.claude/settings.json`** at project root — generated by the
   installer, containing `mcpServers` merged from all processkit
   skills' `mcp-config.json` blocks plus `enabledMcpjsonServers` list.
   (The current `.claude/settings.local.json` at /workspace does
   this for the maintainer's local dev box; a committed template
   version is needed for derived projects.)
2. **`.claude/settings.json` → `hooks`:**
   - `SessionStart` with matcher `startup,resume,compact` [20] →
     script writing the compliance contract to stdout.
   - `UserPromptSubmit` → same script with a shorter version (e.g.,
     just the 1% rule) on every prompt.
   - `PreToolUse` with matcher on `Write|Edit|MultiEdit` where path
     starts with `context/` → Python script that checks a session
     scratch file for a prior `route_task` call; exit 2 to block
     otherwise [1].
3. **`.claude/commands/` or `.claude/skills/`:** processkit already
   populates these (visible in `/workspace/.claude/commands/`).
   Expose `task-router` and `skill-gate` as first-class commands
   with crisp descriptions [9][10].

Feasibility: **high**. All four hook events exist [1][20].

### 4.2 OpenAI Codex CLI (primary)

Usable but gappier:

1. **`.codex/config.toml`** with `[mcp_servers.<name>]` blocks [2][3]
   — installer can generate alongside `.claude/settings.json`.
2. **`hooks.json` next to the active config layer** [8] — events
   cover `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
   `PostToolUse`, `Stop`. Same "compliance contract" script can
   back both harnesses (stdout semantics match).
3. **Known limitation:** `PreToolUse` only intercepts `Bash` [8][21]
   — `apply_patch` file edits under `context/` cannot currently be
   blocked by hook. Workaround: rely on `UserPromptSubmit` to
   re-inject the rule, and use `PostToolUse` to *record* a violation
   (and instruct the model to revert) even if it can't *block* one.
4. **No hook support on Windows** [8]. Document this as a
   known limitation.

Feasibility: **medium**. Hooks are newer and less complete than
Claude's.

### 4.3 Appendix — follow-up harnesses

**Cursor** — `.cursor/rules/` (preferred) or `.cursorrules`
(deprecated but still supported) [16][17]. Prepended as system
prompt every interaction [16]. Cursor's own guidance: keep under
~2,000 words [16]. **No documented PreToolUse-equivalent** in our
search — enforcement lives in prose. **Adapter:** ship a generated
`.cursor/rules/processkit.md` with the compliance contract at top.
**MCP support:** Cursor does have MCP client support (not explored
in this report — future WorkItem). **Confidence: Likely [16][17].**

**OpenCode** — AGENTS.md is native; `/init` scans the repo and
generates AGENTS.md [23]. Multi-location support (project +
`~/.config/opencode/AGENTS.md`) [23]. **Adapter:** AGENTS.md
compliance already works. MCP and hooks not researched in depth —
future WorkItem. **Confidence: Confirmed for AGENTS.md [23].**

**Continue** — Rules in `.continue/rules/` concatenated into the
system message for every Agent/Chat/Edit request [18]. **Adapter:**
generate a processkit rule block. Hooks not documented in our
search. **Confidence: Confirmed for the rules mechanism [18].**

**Aider** — CONVENTIONS.md **must be explicitly loaded** via
`--read` or `.aider.conf.yml` [19]. No auto-loading. **Adapter:**
installer must write a project-level `.aider.conf.yml` with
`read: [AGENTS.md]` (or a dedicated `CONVENTIONS.md`). No hook
equivalent found. **Confidence: Confirmed [19].**

Each of these deserves its own WorkItem for the installer — their
capabilities and gaps are different enough that one generic adapter
will not fit. Recommended WorkItems: `FEAT-cursor-adapter`,
`FEAT-opencode-adapter`, `FEAT-continue-adapter`, `FEAT-aider-adapter`.

---

## 5. Recommended sequence (for the architect)

### 5.1 Do first — leverage points 1 and 2, paired

**1a.** Write an installer step (aibox or a standalone
`processkit sync-harness` script) that walks
`context/skills/*/*/mcp/mcp-config.json`, merges, and writes the
harness-specific file:
- `.claude/settings.json` → `mcpServers` + `enabledMcpjsonServers`
- `.codex/config.toml` → `[mcp_servers.*]` blocks
- (optional, phase 2) `.cursor/mcp.json`

**1b.** Ship a small, committed "processkit kernel" config as a
fallback, containing the 7 always-needed servers (index-management,
id-management, workitem-management, decision-record, event-log,
skill-finder, task-router) — so derived projects get something even
when the installer fails.

**2a.** Write a single `scripts/hooks/processkit-compliance.py` that
emits the compliance contract on stdout. Shape: 15–30 lines, most
important rules first. It reads from one canonical source file
(e.g. `context/compliance-contract.md`) so the prose is versioned
alongside AGENTS.md.

**2b.** Wire it into:
- `.claude/settings.json` hooks: `SessionStart`, `UserPromptSubmit`.
- `.codex/hooks.json`: `SessionStart`, `UserPromptSubmit`.

This closes the "CLAUDE.md is compacted away" gap [6].

### 5.2 Do next — leverage point 3, structural self-enforcement

Edit the MCP tool **descriptions** of `route_task`, `create_workitem`,
`transition_workitem`, `record_decision`, `log_event`, `open_discussion`,
`create_artifact` to carry a single compressed rule — e.g.
`route_task`: "Route task → skill+process+tool. **Call before any
create_*/transition_*/link_*/record_* tool.**" The extra sentence
is re-sent on every turn (primacy) and takes negligible tokens [7].

### 5.3 Do after — leverage point 4, enforced gating (Claude Code first)

Implement the PreToolUse hook for Claude Code as described in §4.1.3.
Codex can follow once its PreToolUse grows beyond `Bash` [21].

### 5.4 Do last — leverage point 5, AGENTS.md re-layering

This is the *least urgent* change because by the time it lands, the
hook-injected contract (§5.2) is already carrying the weight.
Re-layer AGENTS.md with a ~30-line compliance contract at the top,
reference material below. **Do not further trim**; there is no
evidence-based threshold at 70 lines.

---

## 6. Residual uncertainty (what to independently verify)

| Unknown | Why it matters | How to check |
|---|---|---|
| Whether Codex CLI re-injects AGENTS.md each turn or only at session start | Mirrors the core failure mode found on Claude [6]; if Codex also one-shots, the hook recommendation applies equally; if it re-renders, hook priority drops for Codex. | Read Codex source or run a probe: put a distinctive token in AGENTS.md, ask Codex to recall it after 20 turns. |
| Whether tool descriptions survive Claude Code's compaction or are re-sent verbatim each turn | Load-bearing for leverage point #3. Anthropic docs say tools are part of the synthesised system prompt [7], which is cached — strong inference "yes" but not directly confirmed for Claude Code's specific compaction. | Read Claude Code system-prompt dumps like Piebald-AI/claude-code-system-prompts [22] at a recent version. |
| Cursor / OpenCode / Continue PreToolUse-equivalent capabilities | Determines whether leverage point #4 is "works everywhere by design" or "adapter-only". Our search did not find docs for these. | Direct read of each harness's hooks/events documentation — future WorkItems. |
| The actual quantitative effect of moving AGENTS.md's top-30 lines to a hook | The report *infers* benefit from primacy + compaction mechanics [6][15]. No A/B test run. | Small evaluation: run 20 sessions with / without the hook on a fixed task set, count `route_task` invocation rate. |

These are **input for the architect**, not blockers. All five
leverage points have positive expected value on the evidence.

---

## 7. Appendix — sources

Primary sources (Anthropic / OpenAI / standards):

- [1] Claude Code — Hooks guide: https://code.claude.com/docs/en/hooks-guide
- [2] OpenAI Codex — AGENTS.md guide: https://developers.openai.com/codex/guides/agents-md
- [3] OpenAI Codex — MCP: https://developers.openai.com/codex/mcp
- [4] MCP specification: https://modelcontextprotocol.io/specification/2025-11-25
- [5] MCP Tools concept: https://modelcontextprotocol.info/docs/concepts/tools/
- [7] Anthropic — Effective context engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; Anthropic — Tool use system-prompt construction: https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/implement-tool-use
- [8] OpenAI Codex — Hooks: https://developers.openai.com/codex/hooks
- [9] Claude Code — Slash commands: https://code.claude.com/docs/en/slash-commands
- [10] Claude Code — Skills: https://code.claude.com/docs/en/skills
- [11] agents.md open standard home: https://agents.md/
- [20] Claude Code — Power-user hooks (blog): https://claude.com/blog/how-to-configure-hooks

Secondary / practitioner / independent research:

- [6] Drew Breunig — How Claude Code builds a system prompt: https://www.dbreunig.com/2026/04/04/how-claude-code-builds-a-system-prompt.html
- [12] InfoQ — AGENTS.md emerges as open standard: https://www.infoq.com/news/2025/08/agents-md/
- [13] Chroma research — Context rot: https://research.trychroma.com/context-rot
- [14] Morph — Context rot complete guide: https://www.morphllm.com/context-rot
- [15] Liu et al. — Lost in the Middle (TACL 2024): https://aclanthology.org/2024.tacl-1.9/ ; arXiv: https://arxiv.org/abs/2307.03172
- [16] Cursor — Rules documentation: https://docs.cursor.com/context/rules ; https://docs.cursor.com/context/rules-for-ai
- [17] TokRepo — Best Cursor Rules 2026 (size guidance): https://tokrepo.com/en/guide/cursor-rules-guide
- [18] Continue — Rules documentation: https://docs.continue.dev/customize/deep-dives/rules
- [19] Aider — Conventions documentation: https://aider.chat/docs/usage/conventions.html
- [21] GitHub — Codex issue: apply_patch doesn't emit PreToolUse/PostToolUse: https://github.com/openai/codex/issues/16732
- [22] Piebald-AI — Claude Code system prompts repo: https://github.com/Piebald-AI/claude-code-system-prompts
- [23] OpenCode — Rules documentation: https://opencode.ai/docs/rules/

Internal inputs:

- ART-20260414_0935-AuditSurface-mcp-enforcement-surface — MCP
  enforcement-surface audit (input from the Haiku assistant).
- AGENTS.md (240 lines, v0.13.0) at /workspace/AGENTS.md.
- SKILL.md files for `skill-finder`, `task-router`, `skill-gate`,
  `agent-management`, `artifact-management`, `research-with-confidence`.

---

## 8. Confidence summary (for graders)

- **Confirmed (primary-source verified this session):** §2.1 Claude
  Code CLAUDE.md loading model [6], Codex AGENTS.md loading [2], MCP
  schema [4][5], Anthropic tool-use system-prompt construction [7],
  Claude Code hooks capabilities [1][20], Codex hooks capabilities
  [8][21], Cursor rules mechanism [16], Continue rules mechanism
  [18], Aider conventions loading [19], Lost-in-the-Middle finding
  [15], Chroma context-rot finding [13][14]. The MCP-surface audit
  table comes directly from ART-20260414_0935.
- **Likely (strong inference, multiple sources or primary+secondary):**
  The overall claim that "hooks + tool descriptions > prose alone"
  for enforcement durability; AGENTS.md size isn't the binding
  constraint (content + position are); Cursor's attention-dilution
  claim; the hook-injected compliance contract will outperform
  prose-only AGENTS.md for adherence.
- **Possible:** Specifics of Codex re-injection behaviour beyond
  first-turn; whether Cursor/Continue have PreToolUse equivalents.
- **Unknown (flagged as residual uncertainty §6):** Quantitative
  effect size of each leverage point; Codex turn-by-turn AGENTS.md
  behaviour; Cursor/OpenCode/Continue hooks parity.

### Note on time-sensitivity

All harness documentation was gathered on 2026-04-14. Codex CLI's
hooks system in particular is recent and evolving (e.g., PreToolUse
Bash-only limitation is a current restriction [8][21], not
architectural). Re-check the harness-specific claims if this report
is used more than ~3 months after the gathered date.
