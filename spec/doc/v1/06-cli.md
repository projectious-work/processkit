# Command-line interface

The CLI serves humans, authoring agents that use shell tools, and
automation. It uses the same application core as the MCP server.

## Commands

| Command | Purpose |
|---|---|
| `processkit init [--governing \| --project]` | Create configuration and the content directory in the current repository from a reviewed plan. |
| `processkit new KIND NAME` | Create an item from the published template. |
| `processkit validate [PATH...]` | Validate items, references, overrides, and the lock. Reads draft content from standard input with `-`. |
| `processkit format [PATH...]` | Rewrite items in deterministic serialization. |
| `processkit list KIND [--selector S] [--namespace N]` | List resolved items at level 0. |
| `processkit show KIND NAME [--level L] [--section S]` | Show one resolved item at a level, or one section. |
| `processkit context [--task T] [--profile P] [--path PATH]` | Assemble the context an agent would receive for the given arguments. |
| `processkit explain KIND NAME` | Show provenance, overrides, applicability basis, and validation status. |
| `processkit lock [--update [NAME]]` | Resolve upstreams and write the lock. |
| `processkit fetch` | Fetch locked upstream commits into the local cache. |
| `processkit ontology list\|show` | Read the published ontology registry. |
| `processkit access whoami\|can-i` | Show the current principal or explain an access decision. |
| `processkit mcp serve --stdio` | Serve the repository over stdio MCP. |
| `processkit mcp serve --http --listen ADDRESS` | Run the read-only shared server. |
| `processkit migrate [--from v0]` | Rewrite content to a newer content API version, or convert v0 governance content, from a reviewed plan. |
| `processkit config show` | Show effective configuration with value sources and secrets redacted. |
| `processkit version` | Report the release, ontology, and schema versions. |

## Behavior

- **PK-CLI-001:** every command available in both CLI and MCP MUST call the
  same application operation and produce equivalent results and diagnostics.
- **PK-CLI-002:** every data-bearing command MUST support `--json` with a
  versioned result envelope. Text output is a projection and MUST NOT be the
  only way to obtain names, digests, provenance, or diagnostics.
- **PK-CLI-003:** exit codes MUST distinguish success, validation failure,
  usage error, and environment failure, and MUST be documented.
- **PK-CLI-004:** commands that write MUST print their plan and support
  `--dry-run`. Only `init`, `new`, `format`, `lock`, and `migrate` write
  repository files; `fetch` writes only the local cache.
- **PK-CLI-005:** read commands MUST work offline from committed files, the
  lock, and the local cache, and MUST report a missing upstream fetch as an
  environment failure with the fix.
- **PK-CLI-006:** the CLI MUST NOT stage, commit, push, or open pull requests.
- **PK-CLI-007:** `processkit context` MUST return exactly what the MCP
  server would return for the same principal and arguments, so authors can
  inspect what agents receive.
