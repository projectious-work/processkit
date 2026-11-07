---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 20
description: "Install a verified processkit release and use its MCP tools."
aliases:
  - "/docs/getting-started/overview/"
---

Choose the path that matches your release line:

- **v1 alpha:** use the native CLI and signed local-release envelope. Start
  with the [v1 alpha tutorial](./v1-alpha-tutorial/).
- **v0 stable:** retain the supported v0 installer or managed aibox workflow.
  See [Installing](./installing/) for the compatibility path.

## What v1 installs

A v1 distribution contains visible, reviewable project content:

- `context/skills/` and the Python MCP servers shipped with those skills;
- `context/schemas/`, generated contracts, and state machines;
- `.processkit/` profiles, installer contracts, and release metadata;
- harness projections owned at individual managed keys; and
- `AGENTS.md`, the provider-neutral agent entry point.

The installer records managed ownership in `.processkit/state.json`. New
project entities and local overrides remain owned by the consuming project.

## Runtime requirements

- Linux ARM64 GNU for the published alpha.5 native executable.
- Python 3.10 or newer and `uv` for the Python MCP runtime.
- Git and an MCP-capable harness for the normal agent workflow.
- `curl`, `tar`, and `sha256sum` for the tutorial.

Linux x86_64 and macOS native assets, a bootstrap installer, online release
resolution, and native `processkit doctor`/`processkit mcp` commands are
future work.

## Learning path

1. Complete the [v1 alpha tutorial](./v1-alpha-tutorial/).
2. Create [your first entity](./first-entity/) through MCP.
3. Review [installer guarantees](../installer/contract/).
4. Choose a [package profile](../packages/).
5. Read the
   [v1 implementation status](../development/v1-version/issue-135-status/).
