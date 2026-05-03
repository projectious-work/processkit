---
sidebar_position: 2
title: "Installing"
---

# Installing

processkit is distributed as versioned GitHub releases. Each release
contains a tarball with the shipped `context/`, `.processkit/`, and
agent entrypoint files. You can install those files manually or let a
managed environment tool do it.

## Manual install

Download and unpack the release tarball:

```bash
curl -L \
  https://github.com/projectious-work/processkit/releases/download/v0.25.0/processkit-v0.25.0.tar.gz \
  -o processkit-v0.25.0.tar.gz
tar -xzf processkit-v0.25.0.tar.gz
```

Copy the shipped files into your project:

```bash
cp -a processkit-v0.25.0/context ./context
cp -a processkit-v0.25.0/.processkit ./.processkit
cp processkit-v0.25.0/AGENTS.md ./AGENTS.md
```

Then register the gateway with your harness. For stdio MCP:

```json
{
  "mcpServers": {
    "processkit-gateway": {
      "command": "uv",
      "args": [
        "run",
        "context/skills/processkit/processkit-gateway/mcp/server.py",
        "serve",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

For a long-running local daemon:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

For harnesses that only support stdio, connect to that daemon through
the included proxy:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  stdio-proxy --url http://127.0.0.1:8000/mcp
```

## Per-skill MCP servers

You can also register individual MCP servers when you want a smaller
tool surface or per-server permissions:

```bash
uv run context/skills/processkit/workitem-management/mcp/server.py
uv run context/skills/processkit/decision-record/mcp/server.py
uv run context/skills/processkit/index-management/mcp/server.py
```

Use the gateway for the normal one-process setup. Use per-skill servers
when your harness or security model benefits from narrower registration.

## Managed install

aibox can install and wire processkit automatically for managed
devcontainer projects:

```toml
[processkit]
source = "https://github.com/projectious-work/processkit.git"
version = "v0.25.0"

[context]
packages = ["managed"]
```

In that mode aibox fetches the pinned processkit release, installs the
selected package tier, writes harness MCP configuration, and records the
resolved source in `aibox.lock`.

This path is optional. processkit remains usable anywhere the files can
be installed and the MCP server command can be launched.

## Package tiers

The shipped tiers are:

- `minimal` — smallest useful context for individual work.
- `managed` — default team context with backlog, decisions, scopes,
  handovers, release, and documentation workflows.
- `software` — engineering-heavy production software workflows.
- `research` — data, ML, and research-heavy workflows.
- `product` — product, design, frontend, and product-ops workflows.

See [Packages](../packages/overview) for details.

## Verify

Run the docs build and MCP smoke test from a processkit checkout:

```bash
npm --prefix docs-site run build
uv run scripts/smoke-test-servers.py
```

Inside a consuming project, use your installer's validation command if
one is available, and prefer processkit MCP tools for entity writes so
schema validation and LogEntry side effects happen automatically.
