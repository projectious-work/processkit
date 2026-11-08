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

## Tool results

- **PK-MCP-058:** The MCP server shall return the result of every tool call
  as `structuredContent` that validates against
  `schemas/tool-result.schema.json`, and as one text content item that
  holds the same JSON document. The MCP server shall serialize the document
  with RFC 8785 (JSON Canonicalization Scheme). The MCP server shall set
  `isError` to true if and only if a diagnostic has severity `error`.
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->
- **PK-MCP-059:** The `data` member of a tool result shall validate against
  the schema that `interfaces.yaml` lists for the tool under `tools`. The
  processkit CLI command that maps to the tool (cli@v1 `mcp_mapping`) shall
  carry the same `data` and the same diagnostics.
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->
- **PK-MCP-060:** Every entry of a `get_context` or `list` result shall
  carry the item's identity, its trust class (PK-MCP-087), the served item
  at the entry's level with the `disclosure` members of content-kinds@v1,
  and `status` in the shape of ontology@v1 `schemas/status.schema.json`
  `$defs/listStatus`. Entries shall not carry the full `status` of
  single-item results.
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->
- **PK-MCP-061:** The `level` argument of `get_context` shall accept 0 and 1
  and shall default to 0. The `level` argument of `get` shall accept 0, 1,
  and 2 and shall default to 1, or to 2 when `section` is given. If `get` is
  called with level 2 and without `section`, or with `section` and level 0
  or 1, then the MCP server shall fail with
  `mcp-context-serving.invalid-argument`.
  <!-- agent proposal: OPEN-mcp-context-serving-02 -->
- **PK-MCP-062:** The documented default `limit` of `list` shall be 50, or
  the operator maximum `mcp.list-max-items` when that is lower. If `limit`
  is less than 1 or greater than `mcp.list-max-items`, then the MCP server
  shall fail with `mcp-context-serving.invalid-argument` and shall not
  clamp the value.
  <!-- agent proposal: OPEN-mcp-context-serving-02 -->
- **PK-MCP-063:** The MCP server shall make a `list` cursor an opaque string
  that depends only on the generation, the access-set digest, the
  normalized arguments other than `limit` and `cursor`, and the position in
  the ordered result. If a cursor belongs to an earlier generation, then the
  MCP server shall fail with `mcp-context-serving.cursor-stale`. If a cursor
  is malformed or belongs to other arguments or another access set, then
  the MCP server shall fail with `mcp-context-serving.cursor-invalid`.
  <!-- agent proposal: OPEN-mcp-context-serving-03 -->
- **PK-MCP-064:** The `content` argument of `validate` shall be a string
  that holds the complete draft text in the draft form of content-kinds@v1
  for the given `kind`. The `validate` result shall report the outcome
  `valid` or `invalid` and the draft's diagnostics.
  <!-- agent proposal: OPEN-mcp-context-serving-12 -->
- **PK-MCP-065:** The `explain` result shall carry the item at level 0 with
  its full `status` and an `applicability` member with the item's declared
  profiles, labels, triggers, always-on flag, and whether the item is
  within the pinned profile set.
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->
- **PK-MCP-066:** The MCP server shall support the MCP protocol versions,
  the tool annotations, and the tool contract version listed in
  `interfaces.yaml` (`protocol`). The tool contract version shall be the
  value of `mcpToolContractVersion` in `processkit version --json`
  (cli@v1).
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->

## Resources and prompts

- **PK-MCP-067:** When a resource `processkit://<namespace>/<kind>/<name>`
  is read, the MCP server shall return one JSON text content item that
  equals the `data` of `get` for that item at level 1. The namespace of an
  item in the root Container shall be `root`. `resources/list` shall list
  the readable items within the pinned profile set, in the order of
  PK-MCP-083, with the cursor rules of PK-MCP-063.
  <!-- agent proposal: OPEN-mcp-context-serving-12 -->
- **PK-MCP-068:** Where the MCP server offers prompts, it shall name the
  prompt of a Skill or ProcessSpecification by the ontology@v1 reference
  form `<kind>/<name>` for the root Container and `<kind>/<namespace>/<name>`
  otherwise. The prompt shall have no arguments, its description shall be
  the item's `spec.summary`, and `prompts/get` shall return one user message
  whose text equals the resource content of the item.
  <!-- agent proposal: OPEN-mcp-context-serving-12 -->

## Context matching and ordering

- **PK-MCP-082:** When `get_context` is called, the MCP server shall select
  each readable item of the requested kinds that has at least one match
  basis, after the profile filter of PK-MCP-074 and PK-MCP-076. The match
  bases shall be exactly those listed in `interfaces.yaml` (`matching`):
  `always-on`, `profile`, `path`, `label`, and `trigger`. Without `kinds`,
  the requested kinds shall be the six content kinds of content-kinds@v1.
  If `kinds` names another kind, then the MCP server shall fail with
  `mcp-context-serving.invalid-argument`.
  <!-- agent proposal: OPEN-mcp-context-serving-13 -->
- **PK-MCP-083:** The MCP server shall order `get_context` entries by tier
  of their most shared basis (`always-on`, then `profile`, `path`, `label`,
  `trigger`), then by kind in the order of content-kinds@v1 `kind_tokens`,
  then by namespace, then by name, comparing strings by Unicode code
  point. The MCP server shall order `list` entries by namespace, then by
  name. No weight or score shall influence the order.
  <!-- agent proposal: OPEN-mcp-context-serving-13 -->
- **PK-MCP-084:** The MCP server shall report every match basis of an
  entry, each with its type and the declared value that matched.
  <!-- agent proposal: OPEN-mcp-context-serving-13 -->

## Normalization and cache key

- **PK-MCP-078:** Before assembly, the MCP server shall normalize the
  arguments by the rules in `interfaces.yaml` (`normalization`). Two calls
  whose normalized arguments are equal shall be equal inputs.
  <!-- agent proposal: OPEN-mcp-context-serving-11 -->
- **PK-MCP-079:** The MCP server shall form the cache key as `sha256:`
  followed by 64 lowercase hexadecimal digits of the SHA-256 of the RFC 8785
  serialization of the preimage in `interfaces.yaml` (`cache_key`).
  <!-- agent proposal: OPEN-mcp-context-serving-11 -->
- **PK-MCP-080:** The MCP server shall take the caller's access set, and the
  access-set digest of the cache key, from access-control@v1 `access_set`.
  The MCP server shall use one access set for the whole of one request. The
  request time shall be an input of authorization only, and shall not be an
  assembly input or a cache-key input. This clarifies PK-MCP-030 and
  PK-MCP-032 and does not change them.
  <!-- agent proposal: alignment with access-control@v1 PK-ACC-043,
       PK-ACC-044 -->
- **PK-MCP-086:** When the MCP server answers a `get_context` or `list` call
  from its cache, it shall write an operational log record with the event
  `mcp-context-serving.cache-hit`. When it assembles the result, it shall
  write the event `mcp-context-serving.cache-miss`. The cache state shall not
  appear in the tool result.
  <!-- agent proposal: OPEN-mcp-context-serving-01 -->

## Profiles and pinning rules

- **PK-MCP-090:** processkit shall read the profiles a repository declares
  from the top-level key `profiles` of `processkit.toml`
  (`schemas/project-config.schema.json`). The profiles known to a served
  instance shall be those of the serving repository and of every locked
  upstream.
  <!-- agent proposal: OPEN-mcp-context-serving-09 -->
- **PK-MCP-074:** An item shall be within a profile set if it declares no
  `spec.applicability`, if its `spec.applicability.profiles` contains `*`,
  or if its `spec.applicability.profiles` and the set share a profile.
  <!-- agent proposal: OPEN-mcp-context-serving-09 -->
- **PK-MCP-075:** If `processkit mcp serve` is started with a `--profile`
  that is not a known profile, then processkit shall refuse to start and
  shall fail with `mcp-context-serving.unknown-profile` (usage, exit 2). If
  the `profiles` argument of `get_context` names a profile that is not
  known, then the MCP server shall fail with
  `mcp-context-serving.unknown-profile`.
  <!-- agent proposal: OPEN-mcp-context-serving-09 -->
- **PK-MCP-076:** While profiles are pinned, the profile filter of
  `get_context` shall be the intersection of the `profiles` argument and
  the pinned set, or the pinned set when `profiles` is absent. If a
  profile of the `profiles` argument is not pinned, then the MCP server
  shall report the warning `mcp-context-serving.profiles-outside-pin`.
  While no profile is pinned, the profile filter shall be the `profiles`
  argument; without it, `get_context` shall apply no profile filter.
  <!-- agent proposal: OPEN-mcp-context-serving-09 -->
- **PK-MCP-077:** The shared server shall read group default pinned profiles
  from the operator key `mcp.group-profiles`. The pinned set of a principal
  in several listed groups shall be the union of their profiles. Where
  `--profile` is given, the shared server shall pin the `--profile` set for
  every principal and shall not apply `mcp.group-profiles`. The stdio
  server shall not apply `mcp.group-profiles`.
  <!-- agent proposal: OPEN-mcp-context-serving-10 -->

## Excluded-item reporting

- **PK-MCP-072:** While profiles are pinned, every `get_context` and `list`
  result shall carry `excluded.pinned` with the count of readable items
  that the result would contain without the pin and that the pin leaves
  out, and with the pinned set's digest as a stable reference. The MCP
  server shall list these items only when the `excluded` argument is true.
  <!-- changed by owner decision: #213 finding 2 -->
- **PK-MCP-073:** The MCP server shall report an item that the profile
  filter of `get_context` leaves out with the reason `profile`, and an item
  that only the pin leaves out with the reason `pinned-profile`. When `list`
  is called with `excluded` true, the MCP server shall page the
  pin-excluded entries together with the items in one order, and each
  shall count against `limit`.
  <!-- agent proposal: OPEN-mcp-context-serving-08 -->
- **PK-MCP-091:** In PK-MCP-045 and PK-MCP-072, the MCP server shall treat
  an item as readable if the caller holds the verb that access-control@v1
  `operation_declarations` declares for the reporting operation on that
  item.
  <!-- agent proposal: alignment with access-control@v1 PK-ACC-045 -->

## Briefing format

- **PK-MCP-069:** processkit shall read the briefing budget from the key
  `briefing.budget-bytes` of `processkit.toml`, in UTF-8 bytes of the server
  instructions, with the default and range in `interfaces.yaml`
  (`briefing`).
  <!-- agent proposal: OPEN-mcp-context-serving-04 -->
- **PK-MCP-070:** The MCP server shall build the briefing in the text form
  of `interfaces.yaml` (`briefing.format`). If the full form exceeds the
  budget, then the MCP server shall use the summarized form. If the
  summarized form exceeds the budget, then the MCP server shall use the
  fallback form and shall log the warning
  `mcp-context-serving.briefing-over-budget`.
  <!-- agent proposal: OPEN-mcp-context-serving-04 -->

## Runtime limits and errors

- **PK-MCP-071:** The MCP server shall read the request limits only from the
  operator keys listed in `interfaces.yaml` (`limits`), each with its
  default and ceiling, under the rules of security@v1 PK-SEC-019 and
  PK-SEC-020. On the shared server, the MCP server shall check these limits
  after authentication and after the limits of access-control@v1.
  <!-- agent proposal: OPEN-mcp-context-serving-05 -->
- **PK-MCP-081:** If a request exceeds a request limit, then the MCP server
  shall answer with a JSON-RPC error response that validates against
  `schemas/rpc-error.schema.json`, carries exactly one diagnostic, and is at
  most 8192 bytes, and shall keep serving other requests.
  <!-- agent proposal: OPEN-mcp-context-serving-05 -->
- **PK-MCP-085:** Every diagnostic of the MCP server shall have the shape of
  cli@v1 `schemas/diagnostic.schema.json`. The MCP server shall use the
  codes of `interfaces.yaml` (`errors`) and the codes of the specifications
  that own the operation, and shall report the same codes as the processkit
  CLI for the same input (cli@v1 PK-CLI-001).
  <!-- agent proposal: OPEN-mcp-context-serving-07 -->

## Health

- **PK-MCP-088:** The MCP server shall expose its health report as the MCP
  resource `processkit:health`, which validates against
  `schemas/health-report.schema.json`, over both transports. The shared
  server's `GET /healthz` (access-control@v1 PK-ACC-052) shall report the
  same state.
  <!-- agent proposal: OPEN-mcp-context-serving-06 -->
- **PK-MCP-089:** The MCP server shall run the health checks listed in
  `interfaces.yaml` (`health.checks`) when health is read. The state shall
  be `blocked` if a blocking check failed or was unavailable, else
  `degraded` if a degrading check failed or was unavailable, else
  `healthy`. The health report shall not contain item names or counts.
  <!-- agent proposal: OPEN-mcp-context-serving-06 -->

## Generations

- **PK-MCP-092:** The MCP server shall check the working copy, the lock, and
  the local cache for changes at the start of each request. Every tool
  result shall carry the identifier of its generation in `generation`.
  <!-- agent proposal: OPEN-mcp-context-serving-15 -->

## Trust classes

- **PK-MCP-087:** The MCP server shall give every `get_context` and `list`
  entry a trust class: `instruction` for a valid Standard,
  ProcessSpecification, or Skill, and `reference` for every other item.
  The trust class shall come from kind and validation outcome only and
  shall not grant any authority over tools, configuration, or access
  (security@v1 PK-SEC-001).
  <!-- agent proposal: gap row 5, owner decision pending -->

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
- **PK-PERF-004:** The release process shall measure PK-PERF-001 to
  PK-PERF-003 by the method in `interfaces.yaml` (`performance.method`) on
  the reference host. It shall record the results in the release evidence.
  <!-- agent proposal: OPEN-mcp-context-serving-14 -->
