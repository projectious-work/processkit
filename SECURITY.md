# Security Policy

## What processkit is, security-wise

processkit is a content and runtime layer that agents read and write through
MCP tools. It ships schemas, skills, package tiers, MCP servers, and — on the
v1 line — a standalone installer that writes into a target repository.

Two things follow from that:

- **processkit runs with whatever privileges your agent harness gives it.** The
  MCP servers read and write files under `context/` in the project that
  installed them. They do not sandbox themselves.
- **The installer modifies a target tree.** It reconciles against target-side
  provenance and refuses to remove paths whose ownership it cannot prove, but
  it is still a program that writes to your repository. The
  [threat model](https://projectious-work.github.io/processkit/v1.x/docs/installer/threat-model/)
  documents what it defends against and what it does not.

processkit does not call model-provider APIs, does not store credentials, and
does not open network listeners unless you explicitly start the gateway in
HTTP mode — in which case it binds where you tell it to. Binding it to a
non-loopback address exposes every processkit tool to anything that can reach
that port; there is no authentication layer.

## Supported versions

| Line | Status | Fixes |
|------|--------|-------|
| `v0.x` | Released, maintained | Current minor line |
| `v1.x` | Prerelease | Newest prerelease only; no backports |

processkit is pre-1.0. Breaking changes land in minor releases and are called
out in [`CHANGELOG.md`](CHANGELOG.md). Pin an exact version and read the
release notes before upgrading.

## Reporting a vulnerability

For anything that could affect someone who has already installed processkit —
path traversal in the installer, a tool that escapes the `context/` boundary,
a credential written somewhere it should not be — please report privately.

**Use GitHub's private reporting:**
[Report a vulnerability](https://github.com/projectious-work/processkit/security/advisories/new)

Or email **info@projectious.work**.

Please include:

- What the weakness is and where — file, tool name, or installer phase.
- How it could be exploited, concretely.
- The processkit version and, if relevant, the harness you were running.
- Whether you are willing to be credited.

For everything else — a hardening idea, a suspicious pattern you are not sure
about, a documentation gap that could mislead someone — a public issue is fine
and usually more useful, because the reasoning gets shared.

## What to expect

This is a small project, so response times are best-effort rather than
contractual. You can expect an acknowledgement within a week. If a report is
valid, the fix and the disclosure timeline get agreed with you before anything
is published.

## Out of scope

- Findings that require an already-compromised host or harness.
- The absence of authentication on the HTTP gateway. That is documented
  behaviour: bind it to loopback, or put your own authentication in front.
- Vulnerabilities in agent harnesses, model providers, or aibox. Report those
  to their maintainers.
