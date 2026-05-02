---
sidebar_position: 2
title: "Harness Compatibility"
---

# Harness Compatibility

processkit's MCP servers are provider-neutral Python programs. They do
not require aibox at runtime. aibox can install processkit, merge MCP
configuration, pre-authorize processkit tools where a harness supports
that, and supervise a managed devcontainer. Those are convenience and
lifecycle features; they are not a processkit dependency.

For a direct install, point the harness at the desired server command
inside the installed `context/skills` tree. The recommended one-process
entry point is:

```json
{
  "mcpServers": {
    "processkit-gateway": {
      "command": "uv",
      "args": [
        "run",
        "context/skills/processkit/processkit-gateway/mcp/server.py"
      ],
      "env": {
        "PROCESSKIT_MCP_MODE": "gateway"
      }
    }
  }
}
```

## Current modes

| Mode | Use when | Harness impact |
|---|---|---|
| Per-skill servers | You need fine-grained tool registration or the broadest compatibility. | The harness launches one stdio process per registered skill. |
| `aggregate-mcp` | You already use the legacy aggregate server. | One stdio process, compatibility name, no daemon behavior. |
| `processkit-gateway` stdio | You want the provider-neutral gateway surface now. | One stdio process, eager tool import, richer gateway metadata. |
| Daemon plus stdio proxy | You want a long-lived daemon with lightweight harness proxies. | One shared daemon plus one lightweight stdio proxy per harness. |

The current gateway command is equivalent to:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport stdio
```

Daemon mode starts a localhost streamable HTTP MCP server:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport streamable-http --host 127.0.0.1 --port 8000 \
  --path /mcp
```

Harnesses that only support stdio can connect through the proxy:

```json
{
  "mcpServers": {
    "processkit-gateway": {
      "command": "uv",
      "args": [
        "run",
        "context/skills/processkit/processkit-gateway/mcp/server.py",
        "stdio-proxy",
        "--url",
        "http://127.0.0.1:8000/mcp"
      ],
      "env": {
        "PROCESSKIT_MCP_MODE": "gateway"
      }
    }
  }
}
```

For lower daemon startup memory, generate a tool catalog and enable lazy
registration:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  catalog --write

PROCESSKIT_GATEWAY_IMPORT_MODE=lazy-catalog \
  uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport streamable-http
```

## Harness notes

| Harness | Recommended direction | Compatibility notes |
|---|---|---|
| Claude Code | Register `processkit-gateway` as an MCP stdio server, or keep per-skill servers when permission granularity matters. | Claude Code can launch command-backed MCP servers. aibox may also merge `.mcp.json`, settings, hooks, and preauthorization entries for managed projects. |
| Codex | Register `processkit-gateway` as an MCP stdio server. | Codex benefits from the one-process gateway because many per-skill stdio servers increase startup and approval overhead. Codex preauthorization support is narrower than Claude Code, so users may still see approval prompts depending on local policy. |
| OpenCode | Use stdio gateway mode when OpenCode is configured for MCP command servers. | Treat processkit as a normal MCP server command. aibox-specific supervision is optional and not required for direct use. |
| Hermes | Use stdio gateway mode when Hermes can launch MCP command servers. | The gateway is provider-neutral; Hermes-specific configuration should map the command and args exactly as shown above. |
| Aider | Use processkit skills and files directly; MCP gateway support depends on the surrounding Aider integration. | Aider is not a full MCP harness in the same sense as Claude Code or Codex. It may not enforce processkit tool-use contracts or call MCP tools without an adapter. |

## Choosing a mode

Use `processkit-gateway` stdio for the simplest one-process harness
configuration. Use daemon plus stdio proxy when the environment can
supervise one long-lived gateway process and the harness frequently
restarts command-backed MCP servers. Use per-skill servers when a
harness policy model needs separate permission surfaces. Keep
`aggregate-mcp` only for existing configs that already depend on that
server name.
