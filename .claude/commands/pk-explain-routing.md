---
argument-hint: "<role-slug> [seniority] [scope]"
allowed-tools: [mcp__processkit-model-recommender__explain_routing]
---

Explain model routing for a (role, seniority) pair via the
model-recommender's `explain_routing` MCP tool.

Arguments are positional:

- `$1` — role slug (without the `ROLE-` prefix), e.g. `software-engineer`
- `$2` *(optional)* — seniority: `junior | specialist | expert | senior | principal`
- `$3` *(optional)* — scope: `SCOPE-<slug>` or project slug

Steps:

1. Parse `$ARGUMENTS`. If `$1` is empty, print:
   `Usage: /pk-explain-routing <role-slug> [seniority] [scope]` and stop.
2. Prepend `ROLE-` to `$1` if it is not already prefixed.
3. Call
   `mcp__processkit-model-recommender__explain_routing(role=<role>,
   seniority=<seniority-or-null>, scope=<scope-or-null>)`.
4. Render the response as a human-readable report:
   - A header with the inputs (role, seniority, scope).
   - The trace table (step | layer | action | count_before → count_after
     | details).
   - The final candidates list ordered by precedence (best first), with
     columns: rank | layer | model_id | version | effort | rationale.
   - Any warnings (e.g. `model.resolved.shim_fallback`) surfaced inline
     with a `⚠` prefix — but do not add decorative emoji otherwise.
   - If the response contains `error`, show it and stop.
5. End with a one-line summary: the winning model, effort, and the layer
   it came from (e.g. `Winner: MODEL-anthropic-claude-sonnet v4.6 at
   effort=high from layer 5 (role+seniority binding)`).
