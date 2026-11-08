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
- **PK-SEC-019:** processkit shall read request and parser limits only
  from operator configuration in v1. No invocation option and no
  `PROCESSKIT_` environment variable shall set a limit. Project
  configuration shall not set a limit, also not a lower one. If project
  configuration contains a limit key, then processkit shall fail with
  `cli.config-forbidden-key`.
  <!-- agent proposal: OPEN-security-09 -->
- **PK-SEC-020:** Each limit key of `interfaces.yaml` (`limits`) shall
  have the default and the release-defined ceiling listed there. If
  operator configuration sets such a limit below 1 or above its ceiling,
  then
  processkit shall fail with `cli.config-invalid-value` and shall not run
  the command. processkit shall not clamp the value. No value shall disable
  a limit.
  <!-- agent proposal: OPEN-security-09 -->
- **PK-SEC-021:** When processkit reads a repository file, a file of the
  local cache, draft content, or a configuration file, processkit shall
  check the size limit before it parses the input. processkit shall stop
  reading at the limit. If an input exceeds a limit, then processkit shall
  report `security.limit-exceeded` as a validation failure. If JSON, YAML,
  or TOML input is not syntactically valid, then processkit shall report
  `security.malformed-input` as a validation failure.
  <!-- agent proposal: OPEN-security-07 -->
- **PK-SEC-022:** For each input that fails a limit or a syntax check,
  processkit shall report exactly one diagnostic and shall not parse the
  rest of that input. The diagnostic shall not quote input content. It
  shall name the file, the line and column where known, and the limit key
  and value where a limit failed. Its JSON serialization shall be at most
  4096 bytes.
  <!-- agent proposal: OPEN-security-01 -->

## Network and telemetry

- **PK-SEC-005:** processkit shall not access the network or emit telemetry
  in default operation. processkit shall access the network only for
  `processkit fetch` and the shared server.
- **PK-SEC-018:** When `processkit lock` runs, processkit shall not access
  the network. `lock` shall resolve upstreams only from the local cache
  (`cli@v1` PK-CLI-044).
  <!-- owner decision: #213 finding 3 (2026-11-08);
       docs/adr/0002-lock-resolves-from-fetched-data.md -->

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
- **PK-SEC-030:** Every release artifact shall have a Sigstore bundle,
  published next to it, that is signed by the release workflow identity
  listed in `interfaces.yaml` (`release.signing`). The documented
  installation shall verify the bundle against that identity and issuer
  before it installs the artifact. If the verification fails, then the
  documented installation shall stop and shall install nothing.
  <!-- agent proposal: OPEN-security-04 -->
- **PK-SEC-031:** The processkit source repository shall commit `uv.lock`
  and shall keep the dependency record in `docs/dependencies.md`, with one
  row per direct runtime dependency. If `uv lock --check` fails, or if a
  direct runtime dependency has no row, then the release build shall fail.
  <!-- agent proposal: OPEN-security-05 -->

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
- **PK-SEC-023:** The shared server shall accept an HTTP request without an
  `Origin` header, and a request whose `Origin` value is listed in the
  operator key `transport.allowed-origins`. The default of that key shall
  be the empty list. The shared server shall check the `Origin` header
  before authentication and before it reads the request body. If the
  `Origin` value is not listed, then the shared server shall respond with
  HTTP status 403 and `security.origin-rejected`. If operator
  configuration lists `*`, `null`, or a value that is not an origin, then
  processkit shall fail with `cli.config-invalid-value`.
  <!-- agent proposal: OPEN-security-02 -->
- **PK-SEC-024:** The shared server shall use the stateless form of the MCP
  Streamable HTTP transport. The shared server shall not issue an
  `Mcp-Session-Id` header. If a request carries an `Mcp-Session-Id` header,
  then the shared server shall respond with HTTP status 404 and
  `security.session-rejected`. If a request to the MCP endpoint uses a
  method other than POST, then the shared server shall respond with HTTP
  status 405 and `security.method-not-allowed`.
  <!-- agent proposal: OPEN-security-03 -->
- **PK-SEC-025:** The shared server shall enforce the transport limits
  `transport.max-header-bytes`, `transport.header-timeout-seconds`,
  `transport.idle-timeout-seconds`, and `transport.max-connections` with
  the defaults and ceilings in `interfaces.yaml` (`limits`). If the request
  headers exceed `transport.max-header-bytes`, then the shared server shall
  respond with HTTP status 431 and `security.header-too-large`. If the
  headers are not complete within `transport.header-timeout-seconds`, or a
  connection is idle for `transport.idle-timeout-seconds`, then the shared
  server shall close the connection without serving content. If a new
  connection would exceed `transport.max-connections`, then the shared
  server shall respond with HTTP status 503, the header `Retry-After: 1`,
  and `security.connection-limit`, and shall close the connection.
  <!-- agent proposal: OPEN-security-01 -->
- **PK-SEC-026:** Every HTTP response that rejects a request by
  PK-SEC-023, PK-SEC-024, PK-SEC-025, or PK-SEC-027 shall have the body of
  `schemas/http-rejection.schema.json`. Every rejection by these
  requirements, also a connection closed at the header timeout, shall
  produce one operational log record (`cli@v1` PK-OUT-008) at level
  `warning` whose event is the rejection code. The close of an idle
  connection is not a rejection. Every response of the shared
  server shall carry `Cache-Control: no-store`,
  `X-Content-Type-Options: nosniff`, and
  `Strict-Transport-Security: max-age=31536000`. The shared server shall not
  send `Access-Control-Allow-*` headers and shall respond to `OPTIONS`
  with HTTP status 405.
  <!-- agent proposal: OPEN-security-02 -->

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
- **PK-SEC-027:** The shared server shall accept a bearer credential only in
  the `Authorization` request header. If the request URL has a query
  parameter named `access_token`, then the shared server shall respond with
  HTTP status 400 and `security.credential-in-url` and shall not
  authenticate the request. processkit shall not log the `Authorization`
  header or the query component of a request URL.
  <!-- agent proposal: OPEN-security-10 -->
- **PK-SEC-028:** processkit shall not read, store, or pass credentials for
  upstream Git sources. During `processkit fetch`, Git shall use only its
  own credential configuration of the operating-system user (for example a
  credential helper or an SSH agent). processkit shall add no credential to
  the arguments, the environment, or the configuration of a Git process. If
  an upstream source is an `http` or `https` URL with user information,
  then processkit shall fail with `cli.config-forbidden-key`.
  <!-- agent proposal: OPEN-security-10 -->
- **PK-SEC-029:** The credential files of PK-SEC-016 shall be the files that
  operator configuration names for secret material: in v1, the TLS private
  key of the shared server (`access-control@v1`) and every other file that
  an operator key marks as a credential file. processkit shall check the
  permission bits of the file after it follows symbolic links. processkit
  shall refuse the file if any read or write bit for group or others is
  set. On refusal, processkit shall report
  `security.credential-file-permissions` as an environment failure.
  processkit shall not check the containing directory.
  <!-- agent proposal: OPEN-security-06 -->
