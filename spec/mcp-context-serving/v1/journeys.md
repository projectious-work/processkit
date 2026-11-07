# MCP context serving — acceptance journeys

Journeys 1 and 2 are release acceptance journeys 5 and 7 of the #197
baseline. Every journey runs against the exact release artifacts, in a
temporary Git repository with synthetic data, no ambient credentials or user
configuration, and an MCP test client that records the server instructions,
`tools/list`, and every tool result. Where an identifier is still open (see
`interfaces.yaml`), the journey states the observable effect, not the
identifier.

Shared fixture "governed project": a project repository with one Standard
`always-on` with two rules, one further Standard `release-rules` for profile
`service`, one Standard `doc-style` for profile `documentation`, one
ProcessSpecification `ticket-handling` with states `new`, `triaged`, `done`,
one Skill `triage-ticket` triggered by ticket triage, and one MCPServer entry
`issue-tracker`; committed, locked, and fetched, with a working-copy
revision R1.

## 1. Harness over stdio without instruction or skill files (release journey 5)

Preconditions: the governed project; the harness configuration contains only
the processkit MCP server entry; no instruction file, skill directory, or
plugin exists in the repository or the harness configuration.

Steps:

1. Start the harness, which runs `processkit mcp serve --stdio`.
2. Read the server instructions at connection.
3. Call `get_context(task="triage a new ticket", profiles=["service"])`.
4. Call `get(kind="Skill", name="triage-ticket", level=1)` and
   `get(kind="ProcessSpecification", name="ticket-handling", level=2,
   section="triaged")`.
5. List the repository tree and harness configuration directory.

Expected results:

- The instructions contain, in order, the two always-on rules, a level-0
  index naming `release-rules`, `doc-style`, `ticket-handling`,
  `triage-ticket`, and `issue-tracker`, and the instruction to call
  `get_context` at the start of a task.
- `get_context` returns `ticket-handling`, `triage-ticket`, and
  `release-rules`, each with its match basis (trigger or profile), the
  revision R1, and a cache key; `doc-style` is reported as excluded with
  a reason naming its profile mismatch.
- Step 4 returns the skill body at level 1 and only the `triaged` section at
  level 2.
- No instruction file, skill directory, plugin, or vendor rule file was
  created; `git status --porcelain` is empty; the server opened no network
  listener and made no outbound connection.

Covers: PK-PROD-004, PK-PROD-008, PK-PROD-014, PK-PROD-023, PK-MCP-001,
PK-MCP-002, PK-MCP-010, PK-MCP-020, PK-MCP-033, PK-MCP-044, PK-MCP-052 (by
contrast: no pin, full index).

## 2. Cache hit and invalidation (release journey 7)

Preconditions: the governed project served over stdio.

Steps:

1. Call `get_context(task="triage a new ticket", profiles=["service"],
   level=1)` twice, then once with the same arguments in a different
   argument order or equivalent normalized form.
2. Change one input at a time and repeat the call after each: (a) commit an
   edit to `release-rules` (new revision R2); (b) update the lock to a
   different upstream pin and fetch; (c) change the argument `level` to 0.
3. Restart the server and repeat the step-1 call against R1 content.

Expected results:

- The three step-1 calls return byte-identical results with the same cache
  key and revision; the second and third are served from cache.
- Each change in step 2 yields a new cache key and a fresh result reflecting
  the change (new revision R2 or the new lock); no stale entry is returned.
- Results order shared items (always-on and profile-matched standards)
  before caller-specific items, by a stable key, identically on every call.
- Time of day and the history of earlier calls do not change any result.
- Step 3 returns output byte-identical to step 1 for equal inputs.

Covers: PK-PROD-006, PK-PROD-007, PK-MCP-030, PK-MCP-031, PK-MCP-032,
PK-MCP-033, PK-MCP-042.

## 3. Level-by-level disclosure, resources, and prompts

Preconditions: the governed project served over stdio.

Steps:

1. Call `list(kind="Standard")` and the equivalent `processkit list
   Standard --json`; repeat with a selector on a label.
2. Call `get` for `release-rules` at levels 0, 1, and 2 (one section), and
   the equivalent `processkit show`.
3. Read MCP resource `processkit://<namespace>/Standard/release-rules`.
4. List MCP prompts.

Expected results:

- `list` returns level-0 entries only (no rule text, no section bodies) and
  equals the CLI result item for item; the selector filters identically.
- Each `get` level adds only the next level's content and equals the CLI.
- The resource returns the same item.
- Prompts include `triage-ticket` and `ticket-handling` (recommended).

Covers: PK-PROD-008, PK-PROD-014, PK-MCP-021, PK-MCP-023.

## 4. Fixed, read-only tool set

Preconditions: the governed project, plus a Standard named `write_file`
whose content describes a tool, and an MCPServer entry with a reachable test
endpoint that records connections.

Steps:

1. Call `tools/list` and compare it to the release's published tool
   schemas.
2. Call `validate(kind="Standard", content=<draft>)` with a valid and an
   invalid draft.
3. Call `get_context` and `list(kind="MCPServer")`.
4. Inspect the repository and the test endpoint.

Expected results:

- `tools/list` returns exactly `get_context`, `list`, `get`, `explain`,
  `validate`, `ontology` with the published names, descriptions, and
  schemas; the `write_file` item adds or changes nothing.
- `validate` reports success and the violations respectively and writes no
  file (`git status --porcelain` empty, no new files under `.processkit/`
  holding the draft as content).
- The catalogued endpoint received no connection.

Covers: PK-MCP-003, PK-MCP-022, PK-MCP-024, PK-PROD-022, PK-PROD-025.

## 5. Briefing budget and stability

Preconditions: the governed project with 200 additional synthetic skills
and a briefing budget configured below the size of the full level-0 index.

Steps:

1. Connect three times as the same principal at the same revision and
   record the instructions.
2. Raise the budget above the full index size and reconnect.

Expected results:

- The three briefings are byte-identical and within the budget; the index
  is summarized by kind and label and still includes the always-on rules and
  the `get_context` instruction.
- With the larger budget the full level-0 index appears.

Covers: PK-MCP-010, PK-MCP-011, PK-MCP-012.

## 6. Excluded items respect access

Preconditions: a shared server (`access-control@v1`) serving the governed
project; principal A may read all Standards; principal B may read
`release-rules` but not `doc-style`.

Steps:

1. As A and as B, call `get_context(profiles=["service"])` and
   `list(kind="Standard", selector=<profile service>)`.

Expected results:

- A's results report `doc-style` as excluded with its reason.
- B's results do not mention `doc-style` in any field, count, or reason;
  B's result is identical to one from a repository without `doc-style`.

Covers: PK-MCP-044, PK-MCP-045, PK-MCP-041.

## 7. Pagination

Preconditions: the governed project with 250 synthetic Standards.

Steps:

1. Call `list(kind="Standard")` without `limit`; follow cursors to the end.
2. Repeat step 1.
3. Call `list(kind="Standard", limit=7)` and follow cursors.
4. Commit a change, then reuse a cursor from step 3.

Expected results:

- Step 1 pages contain at most the documented default limit each; every
  Standard appears exactly once across pages.
- Step 2 returns byte-identical pages and cursors.
- Step 3 pages hold at most 7 items, in the same order as step 1.
- Step 4 behaves as documented for a changed generation (open item
  OPEN-mcp-context-serving-03) and never mixes generations within a page.

Covers: PK-MCP-049, PK-MCP-050, PK-MCP-042.

## 8. Serve-time pinned profiles

Preconditions: the governed project. For step 4, a shared server with
operator configuration binding group `release-eng` to default pinned profile
`service`, and principals C (in `release-eng`) and D (not in it, but allowed
to read everything except `release-rules`).

Steps:

1. Run `processkit mcp serve --stdio --profile service`; connect twice and
   record the briefing.
2. Call `get_context(task="triage a new ticket")`, `list(kind="Standard")`,
   and `get_context(profiles=["documentation"])`.
3. Run `processkit mcp serve --http --listen <addr> --profile service`;
   connect as D and call `list(kind="Standard")`.
4. Run the shared server without `--profile`; connect as C and call
   `get_context()` without `profiles`.

Expected results:

- Both briefings are byte-identical, name the pinned profile `service` and
  the resolved revision, and index only items within `service`.
- Step 2 returns only items within `service`; `doc-style` is never
  returned; the `documentation` argument does not widen the result. Cache
  keys differ from the unpinned server's keys for the same caller
  arguments.
- Step 3: D does not receive `release-rules` despite the pin (pinning grants
  nothing).
- Step 4: C receives only items within `service` without passing it.

Covers: PK-MCP-051, PK-MCP-052, PK-MCP-053, PK-MCP-054, PK-MCP-055,
PK-MCP-056, PK-MCP-057.

## 9. Change detection and consistent generations

Preconditions: the governed project served over stdio; a client issuing
`get_context` in a loop.

Steps:

1. While the loop runs, commit a change touching two items, then update the
   lock, then delete and rebuild `.processkit/` via `processkit fetch`.

Expected results:

- Every result reflects entirely the old or entirely the new state of each
  change; no result mixes items from two generations; after each change
  later results reflect it without restarting the server.

Covers: PK-MCP-042.

## 10. Health and diagnostics

Preconditions: the governed project; variants (a) all upstreams fetched,
(b) one locked upstream not fetched, (c) the working copy removed after
start.

Steps:

1. Start the server in each variant and query health through the documented
   channel (OPEN-mcp-context-serving-06).
2. Trigger a diagnostic (for example, call `get` with an invalid level).

Expected results:

- Each variant reports exactly one of `healthy`, `degraded`, `blocked`;
  variant (a) is `healthy`; in no variant is a check that could not run
  counted as passed.
- The server runs in the foreground and exits with its parent; no service
  unit, daemon, or background process remains.
- Every diagnostic carries a code, severity, scope, evidence, and next
  action, and the code is the same on every repetition.

Covers: PK-MCP-043, PK-MCP-046, PK-MCP-047, PK-MCP-048.

## 11. Request limits and caller isolation

Preconditions: a shared server serving the governed project with small
configured request limits; principals A and B with different access.

Steps:

1. Send an oversized request, a request exceeding the time limit, and more
   concurrent requests than allowed.
2. Run interleaved concurrent `get_context` calls as A and B, including
   calls that produce diagnostics.

Expected results:

- Each over-limit request is rejected with a bounded error payload; the
  server keeps serving.
- No result or diagnostic for A contains B's data or diagnostics, and vice
  versa.

Covers: PK-MCP-040, PK-MCP-041.

## 12. Performance objectives

Preconditions: a synthetic repository with 500 items and two locked,
fetched upstreams on the reference host (OPEN-mcp-context-serving-14).

Steps:

1. Measure stdio start to served briefing.
2. Measure uncached and cached `get_context` latencies.
3. Run the shared server with 50 concurrent principals issuing
   `get_context`.

Expected results (recommended objectives; a miss is reported, not a
failure of correctness):

- Startup under 2 s; cached within 50 ms; uncached within 500 ms; the same
  latencies hold with 50 concurrent principals.

Covers: PK-PERF-001, PK-PERF-002, PK-PERF-003.

## Verified by component tests only

- **PK-MCP-034:** the v1 half (matching limited to declared triggers,
  profiles, labels, and paths) is observed through match bases in journeys 1
  and 2, but proving that no lexical or semantic signal influenced ranking
  needs assembly tests over crafted inputs; the clause about later ranking
  applies only once such ranking exists.
