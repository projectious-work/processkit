# MCP server and context assembly

MCP is processkit's agent interface. A harness connects to the processkit
MCP server and obtains the organization's governance context from it instead
of from copied instruction and skill files. The harness remains responsible
for its system prompt, memory, conversation history, and code-base context.

## Serving modes

| Mode | Purpose | Callers | Access control |
|---|---|---|---|
| stdio | a project's agents, against the local working copy | the harness that started it | the local principal sees everything; Git hosting decides who has the working copy |
| shared server | a governing repository served to many readers | authenticated people and agents over HTTPS | per-caller access rules |

A typical project agent uses both: the project's processkit over stdio, which
inherits upstream content through the lock, or the company's shared server
directly when the project has no processkit configuration of its own.

- **PK-MCP-001:** `processkit mcp serve --stdio` MUST serve exactly one
  repository working copy.
- **PK-MCP-002:** the shared server is defined in
  [Identity and access control](08-identity-and-access.md#shared-server). It
  is the only network transport.
- **PK-MCP-003:** the MCP server MUST be read-only: it MUST NOT expose tools
  that write repository files, call external systems, or invoke other MCP
  servers.

## Connection briefing

At connection time the server returns the level-0 briefing as MCP server
instructions. It replaces the always-on part of a harness instruction file.

- **PK-MCP-010:** the briefing MUST contain, in this order: the rules of
  always-on standards, a level-0 index of the applicable standards,
  processes, skills, and catalogued MCP servers, and the instruction to call
  `get_context` at the start of a task.
- **PK-MCP-011:** the briefing MUST stay within a configured size budget. When
  the index exceeds it, the briefing MUST summarize by kind and label and
  rely on `list` and `get_context`.
- **PK-MCP-012:** the briefing for one principal and one resolved revision MUST
  be byte-identical across connections.

## Tools

The tool set is small and generic, because every tool definition occupies
the caller's context.

```text
get_context(task?, profiles?, paths?, kinds?, level?)
list(kind, selector?, namespace?, limit?, cursor?)
get(kind, name, namespace?, level?, section?)
explain(kind, name, namespace?)
validate(kind, content)
ontology(concept?)
```

- **PK-MCP-020:** `get_context` MUST return the items that apply to the given
  arguments, ranked by declared triggers, profiles, labels, and path
  applicability, each at the requested level, with the basis for each match.
- **PK-MCP-021:** `list` and `get` MUST serve every kind with the same
  selector grammar and disclosure levels as the CLI.
- **PK-MCP-022:** `validate` MUST validate draft content passed as an argument
  and MUST NOT write it.
- **PK-MCP-023:** every item MUST also be available as an MCP resource at
  `processkit://<namespace>/<kind>/<name>`, and skills and processes SHOULD
  be offered as MCP prompts so users can invoke them by name.
- **PK-MCP-024:** tool names, descriptions, and schemas MUST be fixed by the
  release. Repository content MUST NOT change them.

## Assembly and caching

Context is assembled per request, deterministic, and ordered for caching.

- **PK-MCP-030:** assembly inputs are the working-copy revision, the lock,
  the caller's access set, and the normalized arguments. No other input,
  including time of day or prior requests, MAY influence the result.
- **PK-MCP-031:** equal inputs MUST produce byte-identical results. Items MUST
  be ordered by a stable key, with content shared by many callers before
  caller-specific content, so harness and model prompt caches can reuse the
  common prefix.
- **PK-MCP-032:** the server MUST cache assembled results under a key derived
  from content digests, the lock digest, the access-set digest, and the
  normalized arguments, and MUST invalidate entries when any input changes.
- **PK-MCP-033:** results MUST report their cache key and revision so callers
  and tests can verify reuse.
- **PK-MCP-034:** in v1, argument matching MUST be limited to declared
  triggers, profiles, labels, and paths. Lexical or semantic ranking added
  later MUST NOT override declared applicability and MUST report its basis.

## Runtime

- **PK-MCP-040:** requests MUST have size, concurrency, and time limits and
  bounded error payloads.
- **PK-MCP-041:** concurrent requests MUST NOT share request context or leak
  data or diagnostics between callers.
- **PK-MCP-042:** the server MUST detect changes to the working copy, the
  lock, and the local cache and serve a consistent new generation, never a
  mix of two generations within one result.
- **PK-MCP-043:** processkit provides a foreground server process and a health
  contract, not a service manager.
