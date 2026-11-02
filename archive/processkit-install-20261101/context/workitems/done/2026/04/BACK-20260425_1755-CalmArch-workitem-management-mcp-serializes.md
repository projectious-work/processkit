---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1755-CalmArch-workitem-management-mcp-serializes
  created: '2026-04-25T17:55:47+00:00'
  updated: '2026-04-26T14:54:49+00:00'
spec:
  title: workitem-management MCP serializes long descriptions with fragile double-quoted
    scalars
  state: done
  type: bug
  priority: medium
  description: |
    ## What

    `create_workitem` / `update_workitem` write the `description:` frontmatter field using YAML double-quoted scalar style. For long markdown bodies containing tables, backslashes, or pipes, this serialization is fragile and can produce documents that PyYAML refuses to re-parse.

    ## Repro

    `context/workitems/BACK-20260425_1346-QuickBison-investigate-a-provider-neutral.md` was created via the MCP and triggered a YAML parse error around line 13 col 16. Hand-fixed today by rewriting `description:` as a YAML literal block scalar (`description: |`). Affected pk-doctor schema_filename (1 of 3 ERRORs in v0.22.0 pre-release sweep).

    ## Suggested fix

    Have the MCP serializer emit `description:` (and any other multi-line string field) as a literal block scalar `|` whenever the value contains a newline. The block scalar is unescaped, so markdown bodies — including tables and code fences — round-trip safely.

    Reference: `yaml.dump(..., default_style='|')` for the multi-line case, or a custom representer that picks `|` only when the string contains `\n`.

    ## Done when

    - New WI/update with multi-line description writes `|` block scalar style.
    - Test fixture covering a markdown body with a pipe-table round-trips through YAML safely.
    - The QuickBison style of error stops happening for new entities.

    ## Out of scope

    - Re-serializing existing WI files. The QuickBison fix is sufficient for this release; older WIs that happen to have parseable double-quoted descriptions stay as-is.
  started_at: '2026-04-26T12:27:22+00:00'
  completed_at: '2026-04-26T14:54:49+00:00'
---

## Transition note (2026-04-26T12:27:22+00:00)

Starting work — fix lands in context/skills/_lib/processkit/frontmatter.py (the shared serializer used by every entity-writing MCP, not just workitem-management). Custom SafeDumper subclass with a str representer that picks "|" block-scalar style when the string contains a newline.


## Transition note (2026-04-26T14:54:46+00:00)

Fix landed in context/skills/_lib/processkit/frontmatter.py (mirrored to src/). Custom SafeDumper subclass with str representer that emits "|" literal block scalar style for any string containing a newline; data is normalized to single trailing newline (canonical clip-chomp shape). parse() also fixed to re-attach the trailing "\n" the regex consumed at the "\n---" boundary, otherwise block scalars at end-of-frontmatter lose their final newline. 8 tests in test_frontmatter.py cover the QuickBison repro shape, pipe-tables, fenced code, backslashes, nested mappings, and trailing-newline normalization. Smoke-tested across 50 existing entity files: round-trip is idempotent after first normalization. pk-doctor schema_filename: 0 ERROR / 0 WARN / 1 INFO (636 files).


## Transition note (2026-04-26T14:54:49+00:00)

Closed. Implementation in main, tested, schema-clean. Will ship in v0.23.0.
