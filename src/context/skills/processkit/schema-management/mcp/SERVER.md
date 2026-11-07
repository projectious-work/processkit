# schema-management MCP server

Exposes deterministic generated-schema rebuilding and runtime contract
inspection without duplicating the shared schema-generation implementation.

## Tools

| Tool | Purpose |
|---|---|
| `regenerate_schemas(kinds?)` | Rebuild all or selected generated schemas |
| `get_schema_contract(kind, discriminator?)` | Return a runtime Schema spec |
| `get_validation_mode(kind, discriminator?)` | Return strict or tolerant mode |

`regenerate_schemas` is idempotent but overwrites derived generated files.
It requires canonical `context/schemas/src/` sources. Run it from a processkit
checkout or a complete installed distribution.

Regeneration clears schema caches in this MCP process. Other granular MCP
processes retain their own caches until reloaded or restarted.
