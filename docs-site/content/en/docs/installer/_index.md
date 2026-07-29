---
title: Installer and releases
linkTitle: Installer
weight: 60
description: Standalone installation, trust, compatibility, and integrations.
---

The v1 standalone installer makes processkit independently installable,
updatable, verifiable, and removable. Release policy is carried by the
signed processkit distribution rather than hard-coded into downstream
tools.

`v1.0.0-alpha.4` implements the local lifecycle and trust boundary. It
publishes one Linux ARM64 GNU executable and still requires an explicit local
distribution. Online resolution, bootstrap installation, four-platform
assets, native runtime diagnosis, and MCP supervision remain planned.

- [Install and use alpha.4](../getting-started/v1-alpha-tutorial/)
- [Installer contract](./contract/)
- [CLI and automation interfaces](./cli/)
- [Python MCP runtime contract](./runtime/)
- [Local release production](./local-release/)
- [Threat model](./threat-model/)
- [v0 compatibility](./v0-compatibility/)
- [aibox consumer integration](./aibox-integration/)
- [Issue #135 implementation
  review](../development/v1-version/issue-135-status/)
