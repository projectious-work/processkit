---
title: "Generated CLI Reference"
description: "Generated from the processkit v1.0.0-alpha.5 executable."
weight: 11
---

Do not edit this page by hand. Regenerate it with
`uv run scripts/generate-v1-docs.py`.

```text
Native lifecycle CLI for processkit projects

Usage: processkit <COMMAND>

Commands:
  plan                   Produce a deterministic, non-mutating installation plan
  install                Install a verified release into a new or empty target project
  recover                Roll back or finalize incomplete installer transactions
  uninstall              Remove unchanged files owned by a prior installation
  update                 Update unchanged managed files from a verified release
  verify-release         Verify a signed local release against an explicit local trust store
  verify                 Verify installed provenance and report managed-path drift
  inspect-compatibility  Inspect a legacy processkit tree without mutating it
  migrate-v0             Transition an exact v0 release into a fresh v1 target
  doctor                 Diagnose the installed project and Python MCP runtime without mutation
  mcp                    Verify or supervise the shipped Python MCP gateway
  execute                Execute one versioned installer request and emit one result envelope
  help                   Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```
