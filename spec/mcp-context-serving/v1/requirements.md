# MCP context serving — requirements

This specification defines processkit's agent interface: the MCP server in
its two serving modes (stdio for one working copy, and the shared server),
the level-0 connection briefing, the fixed set of six read-only tools, MCP
resources and prompts, per-request context assembly with deterministic
output and caching, serve-time pinned profiles, reporting of excluded items,
pagination, runtime bounds, the health and diagnostics contract, and the
performance objectives for serving. Authentication, access rules, and the
shared server's TLS and listen configuration are specified in
`access-control@v1`; the content kinds and their disclosure levels in
`content-kinds@v1`; command syntax and result envelopes in `cli@v1`.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Agent interface

The MCP server replaces the governance part of harness instruction files and
skill directories. The harness remains responsible for its system prompt,
memory, conversation history, and code-base context.

- **PK-PROD-004:** processkit shall use MCP as the agent interface. processkit
  shall make every capability an agent needs available over MCP. processkit
  shall not require harness-specific instruction files, skill directories,
  or plugin formats.
- **PK-PROD-014:** processkit shall be able to carry, in the level-0
  briefing, the always-on rules a project would otherwise keep in a harness
  instruction file. processkit shall make skills and standards discoverable
  and loadable on demand over MCP, so that a harness needs no copied
  instruction or skill files for governance content.
- **PK-PROD-023:** processkit shall not generate harness-specific outputs such
  as instruction files, skill directories, plugin marketplaces, or vendor
  rule formats as a product requirement.
- **PK-PROD-025:** processkit shall not proxy, aggregate, or invoke other MCP
  servers.
- **PK-PROD-022:** processkit shall not write repository content over MCP in
  v1. Content changes are file edits reviewed through Git.

## Serving modes

| Mode | Purpose | Callers | Access control |
|---|---|---|---|
| stdio | a project's agents, against the local working copy | the harness that started it | the local principal sees everything; Git hosting decides who has the working copy |
| shared server | a governing repository served to many readers | authenticated people and agents over HTTPS | per-caller access rules (`access-control@v1`) |

- **PK-MCP-001:** When started with `processkit mcp serve --stdio`, the MCP
  server shall serve exactly one repository working copy.
- **PK-MCP-002:** The shared server, specified in `access-control@v1`, shall
  be the only network transport of the MCP server.
- **PK-MCP-003:** The MCP server shall be read-only. The MCP server shall not
  expose tools that write repository files, call external systems, or invoke
  other MCP servers.

## Connection briefing

At connection time the MCP server returns the level-0 briefing as MCP server
instructions. It replaces the always-on part of a harness instruction file.

- **PK-PROD-008:** The MCP server shall provide a bounded level-0 briefing at
  connection time and shall let the agent request more detail one level at a
  time.
- **PK-MCP-010:** The briefing shall contain, in this order: the rules of
  always-on standards; a level-0 index of the applicable standards,
  processes, skills, and catalogued MCP servers; and the instruction to call
  `get_context` at the start of a task.
- **PK-MCP-011:** The briefing shall stay within a configured size budget.
  If the level-0 index exceeds the budget, then the briefing shall summarize
  the index by kind and label and rely on `list` and `get_context`.
- **PK-MCP-012:** The MCP server shall produce a byte-identical briefing
  across connections for one principal and one resolved revision.

## Tools

The tool set is small and generic, because every tool definition occupies
the caller's context.

```text
get_context(task?, profiles?, paths?, kinds?, level?, excluded?)
list(kind, selector?, namespace?, limit?, cursor?, excluded?)
get(kind, name, namespace?, level?, section?)
explain(kind, name, namespace?)
validate(kind, content)
ontology(concept?)
```

<!-- changed by owner decision: #213 finding 2 (argument `excluded` of
     get_context and list) -->

- **PK-MCP-020:** When `get_context` is called, the MCP server shall return
  the items that apply to the given arguments, ranked by declared triggers,
  profiles, labels, and path applicability, each at the requested level,
  with the basis for each match.
- **PK-MCP-021:** The MCP server shall serve every kind through `list` and
  `get` with the same selector grammar and disclosure levels as the
  processkit CLI.
- **PK-MCP-022:** When `validate` is called, the MCP server shall validate the
  draft content passed as an argument and shall not write it.
- **PK-MCP-023:** The MCP server shall make every item available as an MCP
  resource at `processkit://<namespace>/<kind>/<name>`. The MCP server should
  offer skills and processes as MCP prompts so users can invoke them by name.
- **PK-MCP-024:** The tool names, descriptions, and schemas of the MCP server
  shall be fixed by the release. Repository content shall not change them.

## Excluded items

- **PK-MCP-044:** When `get_context` or `list` leaves out an item because of
  its profiles or its applicability, the MCP server shall report that item in
  the result with its identity and the reason it was excluded, rather than
  omitting it silently. For items that only the pinned profile set leaves
  out, the MCP server shall instead report their count and a stable
  reference, and shall list them only on explicit request (PK-MCP-072).
  <!-- changed by owner decision: #213 finding 2 -->
  <!-- from governance draft: 04-content-packages-and-extensions.md PK-STD-011;
       06-agent-protocol-and-query-surface.md PK-MCP-053 -->
- **PK-MCP-045:** The MCP server shall report excluded items only when the
  caller may read them. If an item the caller may not read is excluded, then
  the MCP server shall not report it, count it, or otherwise reveal its
  existence in the excluded-item report.
  <!-- from governance draft: 04-content-packages-and-extensions.md PK-STD-011;
       06-agent-protocol-and-query-surface.md PK-MCP-053 -->

## Health and diagnostics

- **PK-MCP-043:** processkit shall provide the MCP server as a foreground
  server process together with the health contract of PK-MCP-046 to
  PK-MCP-048. processkit shall not provide a service manager.
- **PK-MCP-046:** The MCP server shall report its health as exactly one of
  the states `healthy`, `degraded`, and `blocked`.
  <!-- from governance draft: 14-performance-and-operations.md PK-OPS-002 -->
- **PK-MCP-047:** If a health check is unavailable or cannot run, then the
  MCP server shall not count that check as a success.
  <!-- from governance draft: 14-performance-and-operations.md PK-OPS-002 -->
- **PK-MCP-048:** The MCP server shall give every diagnostic a stable code, a
  severity, a scope, evidence, and a next action.
  <!-- from governance draft: 14-performance-and-operations.md PK-OPS-003 -->

## Pagination

- **PK-MCP-049:** The MCP server shall bound every `list` result by a
  documented result limit. When `list` is called without `limit`, the MCP
  server shall apply the documented default limit.
  <!-- from governance draft: 14-performance-and-operations.md PK-PERF-010 -->
- **PK-MCP-050:** While the served generation is unchanged, the MCP server
  shall order `list` results and produce cursors deterministically: equal
  calls shall return equal pages and equal cursors, and following the
  cursors from the first page shall return every matching item exactly
  once.
  <!-- from governance draft: 06-agent-protocol-and-query-surface.md PK-MCP-011;
       14-performance-and-operations.md PK-PERF-010 -->

## Assembly and caching

Context is assembled per request, deterministic, and ordered for caching.

- **PK-PROD-006:** processkit shall assemble context per request from the
  repository revision, the resolved inheritance lock, the caller's access
  grants, and the caller's arguments such as task description, profiles,
  paths, kinds, and disclosure level.
- **PK-PROD-007:** processkit shall assemble context deterministically: equal
  inputs shall produce byte-identical output, ordered so that stable content
  precedes caller-specific content. processkit shall make results cacheable
  under a key derived from content digests, the lock, the caller's access
  set, and normalized arguments.
- **PK-MCP-030:** The MCP server shall use as assembly inputs the
  working-copy revision, the lock, the caller's access set, and the
  normalized arguments. No other input, including time of day or prior
  requests, shall influence the result.
- **PK-MCP-031:** When given equal inputs, the MCP server shall produce
  byte-identical results. The MCP server shall order items by a stable key,
  with content shared by many callers before caller-specific content, so
  harness and model prompt caches can reuse the common prefix.
- **PK-MCP-032:** The MCP server shall cache assembled results under a key
  derived from content digests, the lock digest, the access-set digest, and
  the normalized arguments. When any of these inputs changes, the MCP server
  shall invalidate the affected cache entries.
- **PK-MCP-033:** The MCP server shall report the cache key and the revision
  in every assembled result, so callers and tests can verify reuse.
- **PK-MCP-034:** In v1, the MCP server shall limit argument matching to
  declared triggers, profiles, labels, and paths. Where lexical or semantic
  ranking is added in a later version, it shall not override declared
  applicability and shall report its basis.

## Pinned profiles

A served instance can be pinned to a set of profiles, so a role sees only
relevant content without its harness passing the right profiles on every
call. Pinning limits relevance; it is not a confidentiality control.

- **PK-MCP-051:** Where `processkit mcp serve` is started with one or more
  `--profile <name>` options, the MCP server shall pin those profiles for
  the served instance. This shall apply to both `--stdio` and the shared
  server.
  <!-- from proposal: #204 P1 -->
- **PK-MCP-052:** While profiles are pinned, the MCP server shall include in
  `get_context` and `list` results only items within the pinned profiles,
  and the briefing's level-0 index shall index only those items.
  <!-- from proposal: #204 P1 -->
- **PK-MCP-053:** While profiles are pinned, when a caller passes a
  `profiles` argument, the MCP server shall narrow the result within the
  pinned set. A caller-supplied profile shall never widen the result beyond
  the pinned set.
  <!-- from proposal: #204 P1 -->
- **PK-MCP-054:** The MCP server shall apply pinned profiles after access
  rules. Pinning shall never grant access to an item.
  <!-- from proposal: #204 P1 -->
- **PK-MCP-055:** While profiles are pinned, the briefing shall name the
  pinned profiles and the resolved revision. The MCP server shall produce a
  byte-identical briefing across connections for one principal, one resolved
  revision, and one pinned profile set.
  <!-- from proposal: #204 P1 -->
- **PK-MCP-056:** The MCP server shall treat the pinned profile set as part
  of the normalized arguments, so that it enters assembly and the cache key
  like a caller-supplied `profiles` argument.
  <!-- from proposal: #204 P1 -->
  <!-- confirmed by owner decision: #213 finding 1 -->
- **PK-MCP-057:** Where the shared server's operator configuration binds a
  group to default pinned profiles, the shared server shall pin those
  profiles for principals in that group without the caller passing them.
  <!-- from proposal: #204 P1 -->

## Runtime

- **PK-MCP-040:** The MCP server shall enforce size, concurrency, and time
  limits on requests, and shall bound the size of error payloads.
- **PK-MCP-041:** The MCP server shall not share request context between
  concurrent requests and shall not leak data or diagnostics between
  callers.
- **PK-MCP-042:** When the working copy, the lock, or the local cache
  changes, the MCP server shall detect the change and serve a consistent new
  generation. The MCP server shall never mix two generations within one
  result.

## Performance

These are release objectives measured on a repository with 500 items and
two locked upstreams.

- **PK-PERF-001:** The MCP server should take under two seconds from stdio
  startup to a served briefing for a repository with 500 items and two
  locked upstreams.
- **PK-PERF-002:** For that repository, the MCP server should answer a cached
  `get_context` within 50 ms and an uncached one within 500 ms.
- **PK-PERF-003:** The shared server should sustain 50 concurrent principals
  on one host with these latencies.
