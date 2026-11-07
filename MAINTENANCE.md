# Maintenance and support

processkit is maintained in two version lines:

| Line | Status | Branch | Policy |
| --- | --- | --- | --- |
| v0.x | Supported and default | `lts/v0` | Receives maintenance releases and compatibility fixes |
| v1.x | Alpha preview | `main` | Exact-pin evaluation; contracts may change between prereleases |

Branching follows GitHub Flow with Conventional Commits (company
`git-branching-and-releases` standard). Every change is made on a short-lived
`feat/`, `fix/`, `chore/`, or `spec/` branch and squash-merged into `main`, or
into `lts/v0` for a v0 change. A fix that applies to both lines lands on
`main` first and is cherry-picked to `lts/v0` with `git cherry-pick -x`. A
release is prepared on `release/vX.Y.Z`, squash-merged, and tagged on the
squash commit.

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
