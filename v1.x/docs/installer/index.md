# Installer and releases

> Standalone installation, trust, compatibility, and integrations.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

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
- [Evidence-bound release process](./release-process/)
- [Threat model](./threat-model/)
- [v0 compatibility](./v0-compatibility/)
- [aibox consumer integration](./aibox-integration/)
- [Issue #135 implementation
  review](../development/v1-version/issue-135-status/)

---

Section pages:

- [CLI and automation interfaces](/processkit/v1.x/docs/installer/cli/): Human lifecycle commands and the stable automation protocol.
- [Installer Contract](/processkit/v1.x/docs/installer/contract/): Trust, ownership, transaction, and automation guarantees for the v1 lifecycle CLI.
- [Python MCP runtime contract](/processkit/v1.x/docs/installer/runtime/): Supported Python, uv, dependency, cache, and transport behavior.
- [Local Release Production](/processkit/v1.x/docs/installer/local-release/): Build, sign, verify, and publish processkit releases without hosted CI.
- [Evidence-bound Release Process](/processkit/v1.x/docs/installer/release-process/): Repository-owned, resumable release orchestration for processkit maintainers.
- [Installer Threat Model](/processkit/v1.x/docs/installer/threat-model/): Trust boundaries and adversarial requirements for release and target inputs.
- [v0 Compatibility](/processkit/v1.x/docs/installer/v0-compatibility/): Read-only evidence and migration boundary for v0 projects.
- [aibox Integration](/processkit/v1.x/docs/installer/aibox-integration/): Consume the processkit v1 machine protocol without duplicating lifecycle policy.
