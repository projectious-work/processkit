---
apiVersion: processkit.projectious.work/v2
kind: Note
metadata:
  id: NOTE-20260411_1758-StagedMind-cascaded-coarse-to-fine-routing-paradigm
  created: 2026-04-11
spec:
  body: Any system that must select from a large candidate space under a context or
    cost constraint should narrow that space in stages, using the cheapest mechanism
    at…
  title: 'Cascaded coarse-to-fine: the universal paradigm for effective context management
    under constraint'
  type: insight
  state: captured
  tags:
  - architecture
  - routing
  - context-management
  - paradigm
  - llm-efficiency
  review_due: 2026-07-11
  promotes_to: null
---

## Core insight

Any system that must select from a large candidate space under a context
or cost constraint should narrow that space in stages, using the cheapest
mechanism at each stage. Each stage handles only the survivors of the
previous stage. The LLM (or most expensive resolver) acts last, on a
small constrained set — not on the full universe.

This is the single most transferable architectural pattern from
multi-agent routing research (MasRouter, Elastic Path, PulseMCP) and
from production MCP deployments.

## Why it matters for processkit (and AI systems generally)

LLM context windows are finite and expensive. Prose instructions loaded
at session start drift in attention weight as context grows. Tool
schemas injected every turn cost tokens whether used or not. The
failure mode is always the same: the model is asked to select from too
many options, quality degrades, and the system looks unreliable.

The solution is never "write better instructions." It is: reduce the
options meaningfully before the LLM is involved at all.

## The pattern (three levels)

```
Level 1 — Heuristic filter (zero LLM cost)
   Input:  full candidate space (128+ skills, 14 MCP servers, ...)
   Method: keyword match, prefix match, config-declared categories
   Output: 1–3 domain groups (e.g., workitem | decision | event)
   Cost:   microseconds, no API call

Level 2 — Lightweight classifier (cheap or no LLM)
   Input:  tools within the matched domain group (3–8 options)
   Method: token overlap, BM25, or cheap model (Haiku/Flash)
   Output: top-1 tool with confidence score + ranked candidates
   Cost:   milliseconds; cheap model if needed

Level 3 — Resolving LLM (main model, on-demand only)
   Input:  top-3 candidates when confidence < threshold
   Method: full LLM reasoning, presented with full context
   Output: confirmed selection
   Cost:   normal LLM call, but over a tiny candidate set
   Trigger: only when Level 2 confidence < 0.5
```

The key property: each level narrows the space by ~90%. Level 3 is
invoked for only ~10–20% of tasks, and when invoked, it works on
3 candidates, not 200.

## Where this paradigm appears in the literature

- **MasRouter (ACL 2025, arxiv 2502.11133)**: Three cascaded
  controllers (Collaboration Mode → Role Allocator → LLM Router).
  Each is a lightweight proxy network, not a full LLM call.
- **Elastic Path four-layer MCP architecture**: Optimizer (pattern
  match) → Router (LLM for ambiguous) → Tool Groups → Single Endpoint.
- **PulseMCP community best practice**: "agentic server selection as
  a discrete step" — select server first (full list fits in context),
  then expose only that server's tools.
- **Anthropic Tool Search Tool**: defer_loading + BM25/regex search
  — 85% context reduction, 49%→74% accuracy improvement on MCP evals.
- **MetaMCP namespace filtering**: inactive tools filtered out before
  LLM sees the tool list.

## Where to apply this in processkit

| Current system | Staged reduction applied |
|---|---|
| `route_task()` v0.1 | Phase 1 (keyword → group) + Phase 2 (token overlap → tool) ✓ |
| `route_task()` v0.2 | Phase 2 with embeddings; Phase 3 with cheap model escalation |
| Skill description quality | Dense task vocabulary → better heuristic match at Phase 1/2 |
| AGENTS.md instruction set | Replace prose enumeration with single `route_task()` call |
| Any skill that makes sub-agent calls | Declare routing_model_class; harness maps to cheapest capable model |

## Antipattern to avoid

**"Ask the LLM to select from everything"** — loading all tool schemas,
all skill descriptions, and all process overrides into a single context
turn and asking the model to choose. This is exactly what the full MCP
tool list pattern does. The model handles it, but at 4–32x token cost
and degraded accuracy (documented). The fix is always: reduce before
you ask.

## Decision record

DEC-20260411_1738-BraveStream-build-task-router-mcp

## Related discussion

DISC-20260411_1738-DeepBadger-what-is-the-right
