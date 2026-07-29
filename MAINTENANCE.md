# Maintenance and support

processkit is maintained in two version lines:

| Line | Status | Branches | Policy |
| --- | --- | --- | --- |
| v0.x | Supported and default | `v0.x-dev` → `v0.x-release` | Receives maintenance releases and compatibility fixes |
| v1.x | Alpha preview | `v1.x-dev` → `v1.x-pre-release` | Exact-pin evaluation; contracts may change between prereleases |

The default `main` branch is published history, not the development branch
for either line. Release tags are cut only from the designated protected
integration branch and promoted through pull requests.

## Maintenance posture

- Development is active.
- v0 remains the supported/default line until the v1 migration, platform,
  runtime, rollback, and downstream parity gates pass.
- v1 prereleases currently support the native Linux ARM64 GNU target.
- Python 3.10+ and `uv` remain intentional MCP runtime dependencies.
- GitHub Actions are not used. Tests, release evidence, signing,
  documentation builds, and publication run through repository-owned local
  scripts.

## Reporting problems

- Use [GitHub Issues](https://github.com/projectious-work/processkit/issues)
  for reproducible bugs and feature requests.
- Follow [SECURITY.md](SECURITY.md) for vulnerabilities; do not disclose
  security issues publicly.
- Read [SUPPORT.md](SUPPORT.md) before requesting usage help.

## Release operation

Maintainers use:

```sh
./scripts/maintain.sh release-check-state vX.Y.Z
./scripts/maintain.sh release-doctors vX.Y.Z
./scripts/maintain.sh release vX.Y.Z --steps phase0,checks,build,docs
./scripts/maintain.sh release vX.Y.Z --steps publish,verify
```

Evidence is stored under
`dist/release-evidence/<version>/<candidate-commit>/`. Reuse is allowed only
when the exact version, commit, tree state, toolchain, and environment binding
still match.
