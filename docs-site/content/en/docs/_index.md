---
weight: 1
title: "Introduction"
---

**processkit is a provider-neutral process and memory layer for
AI-assisted projects.**

It keeps durable project state in Git-reviewable files, validates that state
through schemas and lifecycle rules, and exposes project workflows through
Python MCP servers.

## Release lines

| Line | Status | Use |
| --- | --- | --- |
| v0.x | Stable and default | Existing projects and normal production use |
| `v1.0.0-alpha.5` | Exact-pin prerelease | Evaluation of the native lifecycle CLI and v1 contracts |

The v1 alpha is opt-in. It does not replace the supported v0 line, and it
must not be selected through an unverified `latest` URL.

## v1 product boundary

| Layer | Responsibility |
| --- | --- |
| Native Rust CLI | Verify releases; plan, install, update, recover, verify, and uninstall project content |
| Python MCP runtime | Serve tools, validate entity operations, enforce transitions, route skills, and maintain the derived index |
| Visible content | Skills, schemas, state machines, processes, adapters, and configuration remain reviewable files |
| Project-owned state | WorkItems, Decisions, Artifacts, Notes, Logs, and local overrides belong to the consuming project |

Python is intentionally retained for MCP. The Rust CLI is the lifecycle and
trust boundary, not a second MCP implementation.

Within this repository, `context/` is processkit's own dogfood project state.
`src/context/` is the producer-owned payload installed into other projects.
They have different ownership and must not be merged.

## Start with v1

The currently published native executable supports Linux ARM64 GNU systems.
The CLI still requires an explicitly downloaded distribution directory; an
online resolver and bootstrap installer are planned but not implemented.

Follow the
[v1 alpha installation and first-project tutorial](./getting-started/v1-alpha-tutorial/)
for a verified, step-by-step installation.

## Documentation map

- [Getting Started](./getting-started/) covers installation and first use.
- [Installer](./installer/) documents trust, transactions, automation, and
  runtime requirements.
- [MCP Servers](./mcp-servers/) explains gateway and per-skill operation.
- [Primitives](./primitives/) describes durable project entities.
- [Skills](./skills/) describes reusable process knowledge.
- [Packages](./packages/) describes installable content profiles.
- [v1 implementation status](./development/v1-version/issue-135-status/)
  maps issue #135 to alpha.5 evidence and remaining gaps.
