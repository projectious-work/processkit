---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260411_0723-LivelySwan-how-should-processkit-ensure
  created: '2026-04-11T07:23:20+00:00'
  updated: '2026-04-11T08:02:57+00:00'
spec:
  question: How should processkit ensure agents reliably invoke skills that have no
    MCP server, particularly skill-finder?
  state: resolved
  opened_at: '2026-04-11T07:23:20+00:00'
  outcomes:
  - DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider
  closed_at: '2026-04-11T08:02:57+00:00'
---

## Context

Research commissioned 2026-04-11. The problem is well-documented and
empirically measured. Five-track plan proposed.

## Root causes

1. **Attention decay ("Lost in the Middle")** — LLMs underweight tokens
   in the middle of long contexts. AGENTS.md instructions compete with
   everything and lose. One org measured 56% reliable skill invocation
   from instruction files alone.
2. **Instruction capacity** — Claude Code's built-in system prompt uses
   ~50 of the ~150–200 instruction slots a model can reliably follow.
3. **Tool schemas beat prose** — MCP-backed skills appear as callable
   tool schemas in every turn. A SKILL.md competes for attention once at
   session start and can be deprioritised.
4. **AgentIF (NeurIPS 2025)** — best models perfectly follow <30% of
   complex multi-constraint agentic instructions.

## Proposed plan

**Track A — skill-finder MCP server** (highest leverage)
`find_skill(task_description)` → matching skill name + SKILL.md path.
`list_skills(category)` → catalog browsing. Moves skill-finder from
"prose in session start" to "callable tool in every turn."

**Track B — Claude Code PreToolUse hook**
Hook fires before Write/Edit on context/ paths. Checks if skill-finder
was consulted for the relevant domain. Injects a reminder or blocks the
call. Deterministic — model cannot override a cancelled tool call.

**Track C — session-start meta-skill (1% rule)**
New processkit skill modeled on obra/superpowers mandatory skill-check
protocol. "If there is even a 1% chance a processkit skill applies, you
MUST check skill-finder first." Includes DOT graph decision flow and
pre-empts rationalizations.

**Track D — AGENTS.md slimming + if/then skill guards**
Push domain-specific instructions into their skills. Add explicit guards:
"If editing context/ → check skill-finder first." Keep root AGENTS.md
under 60 lines.

**Track E — Skill description quality audit**
The description field is the semantic trigger. Audit all 128+ skills:
does the description alone tell the model exactly when to invoke this
skill and what it protects against?

## Decision needed

Approve the plan and prioritise the tracks. Track A (skill-finder MCP)
is highest leverage but requires a new MCP server. Track C (meta-skill)
is purely content and can ship immediately. Tracks can be parallelised.
