---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260414_1230-ReachReady-processkit-enforcement-research-summary
  created: 2026-04-14T12:30:00Z
spec:
  name: "Executive summary — why agents ignore processkit"
  kind: document
  location: context/artifacts/ART-20260414_1230-ReachReady-processkit-enforcement-research-summary.md
  format: markdown
  version: "1.0.0"
  tags: [research, enforcement, processkit, summary]
  produced_by: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
  owner: ACTOR-sr-researcher
  links:
    workitem: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
    full_report: ART-20260414_1230-ReachReady-processkit-enforcement-research
---

# Executive summary — why agents ignore processkit

**Author:** Sr Researcher (Opus) · **Date:** 2026-04-14
**Full report:** `ART-20260414_1230-ReachReady-processkit-enforcement-research.md`

## The finding in one paragraph

The owner's observation is real and mostly **structural**. The PM's
hypothesis — agents attend to tool schemas more reliably than to prose —
is **directionally correct and primary-source supported**, but the real
lever is not "tool schemas vs prose"; it is **(a) the distribution of
processkit's MCP tools into harness configs is broken, so the tool
schemas the agent should see aren't there, and (b) Claude Code injects
CLAUDE.md exactly once and then compacts it away, so the prose rules
that do exist evaporate mid-session** [Breunig, dbreunig.com, 2026].
The "70-line context-fatigue" claim in its literal form is folklore;
the underlying mechanics (context rot, lost in the middle) are real
and documented. The fix is not more trimming — it's **hooks + a merged
MCP config + richer tool descriptions**, with AGENTS.md re-layered
last.

## Top 3 leverage points (see §1 + §5 of the full report)

| # | Leverage point | Portability | Confidence | Why it's top-3 |
|---|---|---|---|---|
| 1 | **Ship a pre-merged MCP config at install time** (wire `route_task`, `create_workitem`, `log_event`, etc. into `.claude/settings.json` and `.codex/config.toml` via the installer). | Works everywhere by design (MCP is standardised). | Confirmed | Without this, the enforcement tools literally don't exist in the agent's tool list in derived projects. Highest-impact, highest-feasibility item. |
| 2 | **Add a `SessionStart` + `UserPromptSubmit` hook that re-injects a 15–30 line "compliance contract"** (the 1% rule, commit-immediately, use-MCP-not-hand-edits, log-events-after-state-change). | Per-harness adapter — Claude Code and Codex both support the required hook events [Claude Code hooks docs; OpenAI Codex hooks docs]. | Confirmed | Only way to make top-of-AGENTS.md rules survive Claude Code's one-shot CLAUDE.md loading + compaction. |
| 3 | **Move the 1% rule *into the MCP tool descriptions*** of `route_task`, `create_workitem`, `record_decision`, `log_event`, `open_discussion`, `create_artifact` — each gets a one-sentence rule that ships with every tool list every turn. | Works everywhere by design (MCP schema field). | Likely | Cheapest, most persistent reminder — tool definitions sit in the synthesised system prompt per Anthropic docs, so they're primacy-region + cached. |

Leverage points 4 (PreToolUse enforcement) and 5 (re-layer AGENTS.md
with a compliance-contract header) are in the full report.

## What this refutes, what it supports

- **Supports:** PM's "agents attend to tools more than prose" intuition
  (qualified — tool *descriptions* are where prose actually survives;
  tool *schemas* without description text win on discovery).
- **Supports:** Owner's "prose gets ignored" observation — documented
  via Claude Code's CLAUDE.md-injected-once-then-compacted mechanism.
- **Refutes:** Owner's "~70 lines" threshold as written. No primary
  source supports a specific line count. Context rot is real [Chroma
  research] and "lost in the middle" is real [Liu et al., TACL 2024],
  but the right response is *structural* (position + re-injection),
  not further trimming.

## What the architect should design next

1. An installer step that generates a merged MCP config for each
   harness (Claude Code `.claude/settings.json`, Codex
   `.codex/config.toml`, follow-up Cursor/OpenCode/Aider adapters).
2. A single `compliance-contract.md` canonical file + a script that
   emits it on stdout as a hook response, wired into SessionStart and
   UserPromptSubmit for both Claude Code and Codex.
3. A PR updating the `description` fields of the 6–8 high-leverage
   MCP tools to carry the 1% rule inline.

## Residual uncertainty the architect should re-verify

- Exact Codex CLI re-injection behaviour of AGENTS.md per turn
  (vs only first turn) — our evidence is "limited amount in the first
  turn" [OpenAI Codex AGENTS.md docs] but the architect should
  probe before committing.
- Whether Cursor / OpenCode / Continue have PreToolUse-equivalent
  hook points — unknown from our search; scope as future WorkItems.
- Quantitative effect-size of the hook-injected contract vs
  prose-only — no A/B test run; recommend one on a fixed task
  set before declaring victory.

## Inputs

- Full report: `ART-20260414_1230-ReachReady-processkit-enforcement-research.md`
- Audit input: `ART-20260414_0935-AuditSurface-mcp-enforcement-surface.md`
- WorkItem: `BACK-20260414_0930-ReliableReach-processkit-enforcement-research`
