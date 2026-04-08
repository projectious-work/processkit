---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-dependency-audit
  name: dependency-audit
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Audit project dependencies for vulnerabilities and outdated packages."
  category: security
  layer: null
  when_to_use: "Use when checking the security posture of dependencies, planning updates, or running a pre-release dependency review."
---

# Dependency Audit

## Level 1 — Intro

Third-party dependencies are the largest part of most codebases'
attack surface. A dependency audit runs the ecosystem's vulnerability
scanner, triages findings by severity, and produces a concrete update
plan.

## Level 2 — Overview

### Run the right tool

Each ecosystem ships its own audit command:

| Ecosystem | Audit command                       | Outdated check          |
|-----------|-------------------------------------|-------------------------|
| Rust      | `cargo audit`                       | `cargo outdated`        |
| Python    | `pip-audit` or `safety check`       | `pip list --outdated`   |
| Node.js   | `npm audit` or `pnpm audit`         | `npm outdated`          |
| Go        | `govulncheck ./...`                 | `go list -u -m all`     |

Install the tool if it's missing (e.g. `cargo install cargo-audit`),
then run it from the project root with the lockfile present.

### Triage by severity

- **Critical / High** — fix immediately. Update or replace the
  dependency before merging anything else.
- **Medium** — schedule a fix within the current sprint.
- **Low** — track and address when convenient.

For each finding, check whether a patched version exists, whether the
vulnerable code path is actually reached, and whether a workaround
(config, version pin) buys time.

### Update strategy

- Update one dependency at a time so breakage is easy to attribute.
- Run the full test suite after each update.
- Read changelogs before any major version bump.
- Use lockfiles to pin exact versions across environments.

### Ongoing maintenance

- Schedule monthly dependency reviews on the calendar.
- Enable Dependabot, Renovate, or equivalent for automated update PRs.
- Document any deliberately pinned versions inline with the reason.

## Level 3 — Full reference

### What "audit" actually checks

Audit tools cross-reference the lockfile against vulnerability
databases (RustSec, OSV, GitHub Advisory, npm advisory). They report
direct and transitive dependencies, but they only catch known
vulnerabilities — a clean audit is not the same as a secure
dependency tree.

### When the fix isn't trivial

- **No patched version exists.** Pin the current version, file an
  upstream issue, and look for an alternative library. Document the
  acceptance in the lockfile or a `SECURITY.md` exception list.
- **Patched version is a major bump.** Branch off, run the upgrade in
  isolation, and address breaking changes before merging.
- **Vulnerability is in a transitive dep.** Force-resolve the
  transitive version (npm `overrides`, pnpm `overrides`, Cargo
  `[patch]`, pip constraints) until the parent dependency catches up.
- **The vulnerable code path is unreachable in your usage.** Note the
  rationale alongside the suppression. Do not silently ignore.

### Anti-patterns

- Running the audit once and never again.
- Bumping a dozen dependencies in a single PR.
- Suppressing findings without writing down the reason.
- Trusting "0 vulnerabilities" as proof of security — supply-chain
  risk extends beyond known CVEs (typosquats, malicious updates,
  abandoned maintainers).
- Auto-merging Dependabot PRs without running tests.

### Output expectations

A useful audit summary identifies the package manager, lists each
vulnerable dependency with its severity and recommended fix, calls
out anything without a maintained alternative, and proposes a single
ordered update sequence.
