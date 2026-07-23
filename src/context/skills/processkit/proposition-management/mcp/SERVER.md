# proposition-management MCP server

Record and query claims and risks through the v1 Proposition interface.

## Tools

| Tool | Purpose |
|---|---|
| `create_proposition` | Create a claim or Risk discriminator |
| `get_proposition` | Read one Proposition |
| `update_proposition` | Update fields without changing discriminator |
| `query_propositions` | Query by discriminator and status |

Every successful write returns index and event status.
