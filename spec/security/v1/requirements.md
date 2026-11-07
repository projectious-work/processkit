# Security — requirements

This specification defines processkit's security baseline: how content from
a repository and its upstreams is treated as untrusted data, which actions
processkit never takes on content, input limits and malformed-input
handling, network and telemetry defaults, release signing and verified
installation, dependency and defect handling, and the hardening of the
shared server's HTTP transport and of credentials. Authentication and
authorization belong to `access-control@v1`; configuration layering,
output, logging, and redaction belong to `cli@v1`; path containment and
safe parsing of repository files belong to `repository-storage@v1`; the MCP
tools and request limits belong to `mcp-context-serving@v1`.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Threat model

processkit serves content that agents treat as instructions. The main
assets are the integrity of served content, the confidentiality of
restricted content on the shared server, and the caller's credentials.

| Threat | Control |
|---|---|
| tampered upstream content | locked commits and digests, explicit fetch |
| instructions smuggled through content | content is data; tool definitions fixed by the release |
| unauthorized reading on the shared server | authenticators, deny-by-default access, filter-before-rank |
| credential leakage | no credentials in content, redaction, no token pass-through |
| path and parser attacks | containment checks, safe YAML subset, size limits |
| compromised release | signed releases and verified installation |

## Content as untrusted data

- **PK-SEC-001:** processkit shall treat content from the repository and its
  upstreams as untrusted data. Serving that content shall not give it
  authority over tool definitions, configuration, access rules of other
  repositories, or processkit behavior.
- **PK-SEC-002:** processkit shall label served content with its kind and
  provenance so an agent can distinguish an organization's rule from
  arbitrary text.
- **PK-SEC-003:** processkit shall not execute content, run scripts from
  skills, evaluate templates with code, or follow URLs found in content.

## Inputs and limits

- **PK-SEC-004:** processkit shall apply size limits to its inputs. If JSON,
  YAML, or Markdown input is malformed, then processkit shall fail with a
  bounded diagnostic.
- **PK-SEC-017:** processkit shall let request and parser limits be
  configured only through operator configuration and the invocation layer.
  Project configuration and repository content shall not raise, remove, or
  disable a request or parser limit.
  <!-- from governance draft: 14-performance-and-operations.md PK-PERF-015 -->

## Network and telemetry

- **PK-SEC-005:** processkit shall not access the network or emit telemetry
  in default operation. processkit shall access the network only for
  `processkit fetch` and the shared server.

## Release trust

- **PK-SEC-010:** processkit releases shall be signed. The documented
  installation shall verify the integrity and authenticity of a release
  before use. The documented installation shall not treat a checksum
  downloaded from the same location as the artifact as authentication.
- **PK-SEC-011:** The processkit source repository shall commit its
  dependency lockfiles. If a release build has an unresolved or mutable
  dependency input, then the release build shall fail. Every direct runtime
  dependency shall have a documented purpose and a reviewed license.
- **PK-SEC-012:** Every security defect shall receive a permanent negative
  regression test and shall follow coordinated disclosure.

## Shared server transport hardening

The shared server is the only HTTP transport; stdio is the local transport.
TLS and authentication of every client are required by `access-control@v1`.

- **PK-SEC-013:** The shared server shall enforce the Origin validation that
  the MCP specification requires for the HTTP transport of each supported
  MCP protocol version. If an HTTP request carries an Origin header that the
  shared server does not accept, then the shared server shall reject the
  request without serving content.
  <!-- from governance draft: 08-security-and-trust.md PK-SEC-020 -->
- **PK-SEC-014:** The shared server shall enforce the request-isolation
  controls that the MCP specification requires for the HTTP transport of
  each supported MCP protocol version. The shared server shall authenticate
  every HTTP request and shall not accept an MCP session identifier as proof
  of identity. If a request presents a session identifier that was
  established for a different principal, then the shared server shall
  reject the request without serving content.
  <!-- from governance draft: 08-security-and-trust.md PK-SEC-020 -->

## Credentials

- **PK-SEC-015:** processkit shall not accept a credential value as a
  command-line argument, shall not place a credential value in the command
  arguments of a process it starts, and shall not place a credential value
  in an MCP discovery response.
  <!-- from governance draft: 08-security-and-trust.md PK-SEC-028 -->
- **PK-SEC-016:** Where the platform supports owner-only file permissions,
  processkit shall require owner-only permissions on every credential file
  it reads. If a credential file is readable or writable by a user other
  than its owner, then processkit shall refuse to use it and shall report
  the file path and the reason without the file's content.
  <!-- from governance draft: 08-security-and-trust.md PK-SEC-028 -->
