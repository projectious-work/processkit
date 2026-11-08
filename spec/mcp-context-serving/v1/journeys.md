# MCP context serving — acceptance journeys

Journeys 1 and 2 are release acceptance journeys 5 and 7 of the #197
baseline. Every journey runs against the exact release artifacts, in a
temporary Git repository with synthetic data, no ambient credentials or user
configuration, and an MCP test client that records the server instructions,
`tools/list`, and every tool result. Identifiers are those of
`interfaces.yaml`; result shapes are those of `schemas/`.

Shared fixture "governed project": a project repository whose
`processkit.toml` declares `profiles = ["service", "documentation"]`, with:

- Standard `always-on`: `spec.alwaysOn` true, applicability `["*"]`, two
  rules;
- Standard `release-rules`: applicability `["service"]`, trigger
  `release checklist`;
- Standard `doc-style`: applicability `["documentation"]`, trigger
  `ticket`;
- ProcessSpecification `ticket-handling`: no applicability, label
  `area=support`, trigger `new ticket`, states `new`, `triaged`, `done`;
- Skill `triage-ticket`: applicability `["*"]`, trigger `ticket triage`;
- MCPServer entry `issue-tracker`: label `area=support`, trigger
  `issue tracker`.

All items are in the root Container, committed, locked, and fetched, with a
working-copy revision R1.

## 1. Harness over stdio without instruction or skill files (release journey 5)

Preconditions: the governed project; the harness configuration contains only
the processkit MCP server entry; no instruction file, skill directory, or
plugin exists in the repository or the harness configuration.

Steps:

1. Start the harness, which runs `processkit mcp serve --stdio`.
2. Read the server instructions at connection.
3. Call `get_context(task="triage a new ticket", profiles=["service"])`
   and run `processkit context --task "triage a new ticket" --profile
   service --json`.
4. Call `get(kind="Skill", name="triage-ticket", level=1)` and
   `get(kind="ProcessSpecification", name="ticket-handling", level=2,
   section="triaged")`.
5. List the repository tree and harness configuration directory.

Expected results:

- The instructions have the full form of `briefing.format`: the
  `Revision:` line names R1; `## Always-on rules` holds the two rules of
  `always-on`; `## Index` lists `always-on`, `release-rules`, `doc-style`,
  `ticket-handling`, `triage-ticket`, and `issue-tracker` in kind order;
  `## Start of a task` tells the agent to call `get_context`.
- The result validates against `schemas/tool-result.schema.json`, its
  `data` against `schemas/context-result.schema.json`, and `isError` is
  false. `data.items` are, in this order: `always-on` (bases `always-on`
  and `profile` `*`), `release-rules` (`profile` `service`),
  `triage-ticket` (`profile` `*`, `trigger` `ticket triage`), and
  `ticket-handling` (`trigger` `new ticket`). Every entry has trust
  `instruction`, level-0 `item` members, and `status` in the
  `listStatus` shape. `excluded.items` holds exactly `doc-style` with
  reason `profile`; there is no `excluded.pinned`. `issue-tracker` appears
  nowhere. `revision` names R1 and `data.cacheKey` matches
  `^sha256:[0-9a-f]{64}$`.
- The CLI envelope's `data` equals the tool's `data`, and its diagnostics
  equal the tool's diagnostics.
- Step 4 returns the skill with `disclosure.body` at level 1 and only the
  `triaged` state in `disclosure.section` at level 2, each with full
  `status`.
- No instruction file, skill directory, plugin, or vendor rule file was
  created; `git status --porcelain` is empty; the server opened no network
  listener and made no outbound connection.

Covers: PK-PROD-004, PK-PROD-008, PK-PROD-014, PK-PROD-023, PK-MCP-001,
PK-MCP-002, PK-MCP-010, PK-MCP-020, PK-MCP-033, PK-MCP-044, PK-MCP-052 (by
contrast: no pin, full index), PK-MCP-058, PK-MCP-059, PK-MCP-060,
PK-MCP-070, PK-MCP-082, PK-MCP-083, PK-MCP-084, PK-MCP-087.

## 2. Cache hit and invalidation (release journey 7)

Preconditions: the governed project served over stdio with an operator
configuration that sets `logging.level = "debug"`.

Steps:

1. Call `get_context(task="triage a new ticket", profiles=["service"],
   level=1)` twice, then once as `get_context(task="  Ticket NEW a
   triage!", profiles=["service", "service"], level=1)`.
2. Change one input at a time and repeat the call after each: (a) commit an
   edit to `release-rules` (new revision R2); (b) update the lock to a
   different upstream pin and fetch; (c) change the argument `level` to 0.
3. Restart the server and repeat the step-1 call against R1 content.

Expected results:

- The three step-1 calls return byte-identical results with the same cache
  key, revision, and `generation`. The log has one
  `mcp-context-serving.cache-miss` and then two
  `mcp-context-serving.cache-hit` records for that cache key; the results
  carry no cache state.
- Each change in step 2 yields a new cache key and a fresh result reflecting
  the change (new revision R2 or the new lock); no stale entry is returned.
- Entries are ordered by basis tier, kind, namespace, and name, identically
  on every call.
- Time of day and the history of earlier calls do not change any result or
  cache key.
- Step 3 returns output byte-identical to step 1 for equal inputs.

Covers: PK-PROD-006, PK-PROD-007, PK-MCP-030, PK-MCP-031, PK-MCP-032,
PK-MCP-033, PK-MCP-042, PK-MCP-078, PK-MCP-080, PK-MCP-086.

## 3. Level-by-level disclosure, resources, prompts, and explain

Preconditions: the governed project served over stdio.

Steps:

1. Call `list(kind="Standard")` and `processkit list Standard --json`;
   repeat with the selector `area=support` on `ProcessSpecification`.
2. Call `get` for `release-rules` without `level`, at levels 0 and 1, and
   with `section` set to one section id; call it with `level=2` and no
   section, and with `level=0` and a section; compare with
   `processkit show`.
3. Read the resource `processkit://root/Standard/release-rules`.
4. List the MCP prompts and get `Skill/triage-ticket`.
5. Call `explain(kind="Standard", name="release-rules")` and
   `get_context(kinds=["Role"])`.

Expected results:

- `list` returns level-0 entries ordered by name, `nextCursor` null, and
  equals the CLI result; the selector filters identically.
- `get` without `level` returns level 1; with `section` it returns level 2;
  `level=2` without a section and `level=0` with a section fail with
  `mcp-context-serving.invalid-argument`. Each result equals the CLI.
- The resource content equals the `data` of `get` at level 1.
- The prompts are named `ProcessSpecification/ticket-handling` and
  `Skill/triage-ticket`, have no arguments, and the prompt message text
  equals the item's resource content (recommended behavior).
- `explain` data validates against `schemas/explain-result.schema.json`
  with `applicability.profiles` `["service"]` and `withinPin` null.
- `get_context(kinds=["Role"])` fails with
  `mcp-context-serving.invalid-argument`.

Covers: PK-PROD-008, PK-PROD-014, PK-MCP-021, PK-MCP-023, PK-MCP-061,
PK-MCP-065, PK-MCP-067, PK-MCP-068, PK-MCP-082.

## 4. Fixed, read-only tool set

Preconditions: the governed project, plus a Standard named `write_file`
whose content describes a tool, and an MCPServer entry with a reachable test
endpoint that records connections.

Steps:

1. Run `initialize`, call `tools/list`, and compare it to the release's
   published tool schemas.
2. Call `validate(kind="Standard", content=<draft text>)` with a valid and
   an invalid draft.
3. Call `get_context` and `list(kind="MCPServer")`.
4. Inspect the repository and the test endpoint.

Expected results:

- `initialize` accepts protocol versions `2025-06-18` and `2025-11-25`.
- `tools/list` returns exactly `get_context`, `list`, `get`, `explain`,
  `validate`, `ontology` with the published names, descriptions, input
  schemas (`schemas/tool-inputs.schema.json`), output schema, and the
  annotations of `protocol.tool_annotations`; the `write_file` item adds
  or changes nothing.
- `validate` returns outcome `valid`, then outcome `invalid` with the
  violations as diagnostics and `isError` true; it writes no file
  (`git status --porcelain` empty, no new files under `.processkit/`
  holding the draft).
- The catalogued endpoint received no connection.

Covers: PK-MCP-003, PK-MCP-022, PK-MCP-024, PK-MCP-064, PK-MCP-066,
PK-PROD-022, PK-PROD-025.

## 5. Briefing budget and stability

Preconditions: the governed project with 200 additional synthetic skills,
each with one label, and `briefing.budget-bytes` set below the size of the
full form but above the summarized form.

Steps:

1. Connect three times as the same principal at the same revision and
   record the instructions.
2. Raise the budget above the full form size and reconnect.
3. Set the budget to 4096 and give `always-on` rules of 5000 bytes in
   total; reconnect.
4. Set `briefing.budget-bytes = 1000` and run `processkit config show`.

Expected results:

- The three briefings are byte-identical, at most the budget in UTF-8
  bytes, and in the summarized form: `## Index (summarized)` with one
  count line per kind and one per label, the always-on rules, and the
  `get_context` instruction.
- With the larger budget the full form appears.
- Step 3 gives the fallback form and logs
  `mcp-context-serving.briefing-over-budget`.
- Step 4 fails with `cli.config-invalid-value`.

Covers: PK-MCP-010, PK-MCP-011, PK-MCP-012, PK-MCP-069, PK-MCP-070.

## 6. Excluded items respect access

Preconditions: a shared server (`access-control@v1`) serving the governed
project; principal A may get and list all Standards; principal B may get
and list `release-rules` but not `doc-style`.

Steps:

1. As A and as B, call `get_context(task="ticket", profiles=["service"])`
   and `list(kind="Standard")`.

Expected results:

- A's `get_context` result reports `doc-style` in `excluded.items` with
  reason `profile`.
- B's results do not mention `doc-style` in any field, count, or reason;
  B's result is identical to one from a repository without `doc-style`.

Covers: PK-MCP-044, PK-MCP-045, PK-MCP-041, PK-MCP-091.

## 7. Pagination

Preconditions: the governed project with 250 synthetic Standards.

Steps:

1. Call `list(kind="Standard")` without `limit`; follow `nextCursor` to the
   end.
2. Repeat step 1.
3. Call `list(kind="Standard", limit=7)` and follow cursors, changing
   `limit` to 9 for one page.
4. Commit a change, then reuse a cursor from step 3.
5. Call `list` with `limit=0`, with `limit=201`, with a cursor from step 1
   on `kind="Skill"`, and with the cursor `abc`.

Expected results:

- Step 1 pages hold 50 entries each except the last; every Standard
  appears exactly once; the last page has `nextCursor` null.
- Step 2 returns byte-identical pages and cursors.
- Step 3 pages hold at most 7 (or 9) entries, in the same order as step 1,
  with no gap or repeat.
- Step 4 fails with `mcp-context-serving.cursor-stale`; no page mixes
  generations.
- Step 5 fails with `mcp-context-serving.invalid-argument` twice, then
  `mcp-context-serving.cursor-invalid` twice.

Covers: PK-MCP-049, PK-MCP-050, PK-MCP-042, PK-MCP-062, PK-MCP-063.

## 8. Serve-time pinned profiles

Preconditions: the governed project. For steps 5 and 6, a shared server
with operator configuration `mcp.group-profiles` binding group
`release-eng` to `["service"]` and group `writers` to
`["documentation"]`; principals C (in `release-eng`), D (in no listed
group, may read everything except `release-rules`), and E (in both
groups).

Steps:

1. Run `processkit mcp serve --stdio --profile marketing`.
2. Run `processkit mcp serve --stdio --profile service`; connect twice and
   record the briefing.
3. Call `get_context(task="triage a new ticket")`,
   `get_context(task="ticket", excluded=true)`, `list(kind="Standard")`,
   `list(kind="Standard", excluded=true, limit=2)`, and
   `get_context(profiles=["documentation"])`.
4. Run `processkit mcp serve --http --listen <addr> --profile service`;
   connect as D and call `list(kind="Standard")`.
5. Run the shared server without `--profile`; connect as C and as E and
   call `get_context(task="ticket")`.
6. Run the shared server with `--profile documentation`; connect as C and
   call `get_context(task="ticket")`.

Expected results:

- Step 1 exits with code 2 and `mcp-context-serving.unknown-profile`.
- Both briefings are byte-identical, carry the line `Pinned profiles:
  service` and the revision, and index only `always-on`, `release-rules`,
  `ticket-handling`, `triage-ticket`, and `issue-tracker`.
- In step 3, `doc-style` is never an entry. Without `excluded`, results
  carry `excluded.pinned` with `count` 1 (for `get_context(task="ticket")`
  and `list`), `listed` false, and a `reference` equal to the sha256 of
  `["service"]` in RFC 8785; `excluded.items` is empty. With
  `excluded=true`, `doc-style` appears in `excluded.items` with reason
  `pinned-profile`, and in `list` it counts against `limit=2`.
  `get_context(profiles=["documentation"])` returns no item with a
  `profile` basis and reports the warning
  `mcp-context-serving.profiles-outside-pin`. Cache keys differ from the
  unpinned server's keys for the same caller arguments.
- Step 4: D does not receive `release-rules` despite the pin, and the
  pinned count does not include it.
- Step 5: C receives only items within `service`; E receives items within
  `service` or `documentation`, including `doc-style`.
- Step 6: C receives items within `documentation` only.

Covers: PK-MCP-051, PK-MCP-052, PK-MCP-053, PK-MCP-054, PK-MCP-055,
PK-MCP-056, PK-MCP-057, PK-MCP-072, PK-MCP-073, PK-MCP-074, PK-MCP-075,
PK-MCP-076, PK-MCP-077, PK-MCP-090.

## 9. Change detection and consistent generations

Preconditions: the governed project served over stdio; a client issuing
`get_context` in a loop.

Steps:

1. While the loop runs, commit a change touching two items, then update the
   lock, then delete and rebuild `.processkit/` via `processkit fetch`.

Expected results:

- Every result reflects entirely the old or entirely the new state of each
  change; no result mixes items from two generations; the first request
  that starts after a change reflects it without restarting the server.
- `generation` changes with each content change and is equal for results
  of equal content, including after the cache rebuild.

Covers: PK-MCP-042, PK-MCP-092.

## 10. Health and diagnostics

Preconditions: the governed project; variants (a) all upstreams fetched,
(b) one locked upstream not fetched, (c) the working copy removed after
start, (d) one invalid Standard added.

Steps:

1. Start the stdio server in each variant and read `processkit:health`.
2. In variant (a) and (b), start the shared server and request
   `GET /healthz`.
3. Call `get(kind="Standard", name="release-rules", level=3)` twice.

Expected results:

- The report validates against `schemas/health-report.schema.json` and
  lists the five checks in order. (a) `healthy`, every check `passed`;
  (b) `blocked`, `upstreams-fetched` `failed` with code
  `cli.upstream-not-fetched` and `content` `unavailable`; (c) `blocked`,
  `working-copy` `failed` and every later check `unavailable`; (d)
  `degraded`, `content` `failed`. No report contains an item name or a
  count.
- `GET /healthz` reports the same state.
- The server runs in the foreground and exits with its parent; no service
  unit, daemon, or background process remains.
- Step 3 returns `mcp-context-serving.invalid-argument` in the cli@v1
  diagnostic shape with category, scope, and next action, identical on
  both calls.

Covers: PK-MCP-043, PK-MCP-046, PK-MCP-047, PK-MCP-048, PK-MCP-085,
PK-MCP-088, PK-MCP-089.

## 11. Request limits and caller isolation

Preconditions: a shared server serving the governed project with operator
configuration `mcp.max-request-bytes = 4096`,
`mcp.max-concurrent-requests = 2`, `mcp.request-timeout-seconds = 1`;
principals A and B with different access; a test hook that slows assembly
beyond one second.

Steps:

1. Send a 5000-byte request, a slowed request, and three concurrent
   slowed requests; call an unknown tool.
2. Run interleaved concurrent `get_context` calls as A and B, including
   calls that produce diagnostics.
3. Put `[mcp]` with `max-request-bytes = 1` in `processkit.toml`; set
   `mcp.max-request-bytes = 0` in the operator file.

Expected results:

- The oversized request gets HTTP 413 and a body valid against
  `schemas/rpc-error.schema.json` with code -32600 and
  `mcp-context-serving.request-too-large`; the slowed request gets -32001
  `mcp-context-serving.request-timeout`; the third concurrent request gets
  HTTP 503 with `Retry-After: 1` and -32000
  `mcp-context-serving.concurrency-limit`; the unknown tool gets -32602
  `mcp-context-serving.unknown-tool`. Each body is at most 8192 bytes and
  the server keeps serving.
- No result or diagnostic for A contains B's data or diagnostics, and vice
  versa.
- Step 3 fails with `cli.config-unknown-key` and then
  `cli.config-invalid-value`.

Covers: PK-MCP-040, PK-MCP-041, PK-MCP-071, PK-MCP-081.

## 12. Performance objectives

Preconditions: the corpus and reference host of `performance.method`.

Steps:

1. Measure stdio start to served briefing.
2. Measure uncached and cached `get_context` latencies.
3. Run the shared server with 50 concurrent principals issuing
   `get_context`.

Expected results (recommended objectives; a miss is reported, not a
failure of correctness):

- Startup under 2 s; cached within 50 ms; uncached within 500 ms; the same
  latencies hold with 50 concurrent principals.
- The release evidence records every item of `performance.method.evidence`.

Covers: PK-PERF-001, PK-PERF-002, PK-PERF-003, PK-PERF-004.

## Verified by component tests only

- **PK-MCP-034:** the v1 half (matching limited to declared triggers,
  profiles, labels, and paths) is observed through match bases in journeys 1
  and 2, but proving that no lexical or semantic signal influenced ranking
  needs assembly tests over crafted inputs; the clause about later ranking
  applies only once such ranking exists.
- **PK-MCP-079:** journeys observe the cache key's form, equality, and
  change; recomputing the exact preimage needs the generation's file
  digests, which an assembly test computes directly.
