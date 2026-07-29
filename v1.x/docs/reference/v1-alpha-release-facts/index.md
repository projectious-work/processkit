# v1 Alpha Release Facts

> Verified facts for processkit v1.0.0-alpha.4.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

These facts describe the published `v1.0.0-alpha.4` release.

| Fact | Value |
| --- | --- |
| Release | `v1.0.0-alpha.4` |
| Status | Exact-pin prerelease |
| Release commit | `a703afe714faf2b154b1c0f74b52829d067e5ca6` |
| Content archive | `processkit-v1.0.0-alpha.4.tar.gz` |
| Native target | `aarch64-unknown-linux-gnu` |
| Installer asset | `processkit-v1.0.0-alpha.4-aarch64-unknown-linux-gnu` |
| Signature | Ed25519 |
| Public key ID | `035a31564b52ca7c6e0b7b4c4a37b4fcf94fb3dd178d98473af8a9242dafdeee` |
| Gateway tool count in release acceptance | 199 |
| Installer protocol | `processkit.projectious.work/installer/v1alpha1` |
| Entity API version | `processkit.projectious.work/v2` |

The release publishes seven assets: the content archive and checksum, native
installer and checksum, signed JSON envelope, signature, and public key.

## Profiles

The distribution exposes these profiles:

- `minimal`
- `managed`
- `software`
- `research`
- `product`

## Supported CLI Surface

```text
plan
install
update
verify
verify-release
inspect-compatibility
recover
uninstall
execute --request
```

`init`, `doctor`, `inspect`, `migrate`, `package`, `harness`, and `mcp` are
target commands from issue #135, not alpha.4 commands.

## Source of Truth

- [Published release](https://github.com/projectious-work/processkit/releases/tag/v1.0.0-alpha.4)
- [Implementation review](../development/v1-version/issue-135-status/)
- [Installation tutorial](../getting-started/v1-alpha-tutorial/)
