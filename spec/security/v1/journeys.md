# Security — acceptance journeys

The release acceptance journeys of the baseline contain no security
journey. Journeys 1 to 5 are built from the cases that the baseline's
security test requirement lists: path traversal, symlink escape, oversized
and malformed input, instructions embedded in content, and credential
patterns in catalog entries. Journeys 6 to 9 cover the remaining
requirements. Every journey runs in a temporary Git repository with
synthetic data, no ambient credentials, and no user configuration, from the
exact release artifacts. Limits, codes, headers, and statuses are those of
`interfaces.yaml`; with no operator configuration, the defaults apply.

## 1. Path traversal from content and arguments

Preconditions: a governing repository initialized with `processkit init
--governing`; a file `outside.txt` with a known marker string next to the
repository root (outside it); a stdio MCP client connected with
`processkit mcp serve --stdio`.

Steps:

1. Run `processkit create Standard ../../outside`.
2. Add a skill whose `skill.json` and `SKILL.md` are valid and request, over
   MCP `get`, a level-2 file of that skill with a section or file name
   `../../outside.txt`.
3. Add a Markdown document whose front matter names a related path
   `../../outside.txt`, and run `processkit validate -o json`.

Expected results:

- Step 1 fails and writes no file outside or inside the content directory.
- Step 2 returns an error or a missing-item result; the marker string of
  `outside.txt` appears in no result, diagnostic, or log.
- Step 3 reports a diagnostic; no file outside the repository is read into
  any output.
- Tool names, descriptions, and schemas are unchanged throughout.

Covers: PK-SEC-001 (also exercises PK-STORE-013 of `repository-storage@v1`)

## 2. Symlink escape in a skill and an upstream

Preconditions: the repository from journey 1; a skill directory containing
a symbolic link `notes.md` pointing to `outside.txt`; an upstream governing
repository whose content directory contains a symbolic link to a file
outside that upstream, locked and fetched.

Steps:

1. Over MCP, `get` the skill at level 2 for `notes.md`.
2. Run `processkit get Skill -o json` and `processkit get context -o json`.
3. Run `processkit validate -o json`.

Expected results:

- Step 1 does not return the content of `outside.txt`; it returns an error
  or a missing-item result.
- Steps 2 and 3 never include content from a symlink target outside the
  repository or the upstream copy; step 3 reports a diagnostic for each
  escaping link.
- No marker string from outside files appears in any output or log.

Covers: PK-SEC-001 (also exercises PK-STORE-013 of `repository-storage@v1`)

## 3. Oversized and malformed input

Preconditions: the repository from journey 1; synthetic inputs: a JSON
Standard of 2 MiB and one of 100 MiB (both over `limits.file-bytes`), a
JSON file nested 65 levels deep, a JSON object with 10 001 members, a JSON
string of 262 145 bytes, a Markdown decision record with unterminated front
matter, front matter using YAML outside the safe subset (an anchor or a
tag), a truncated JSON file, and a truncated TOML operator configuration.

Steps:

1. Run `processkit validate -f FILE -o json` for each input file
   separately.
2. Pass each input as draft content to `processkit validate -f -` and to the
   MCP `validate` tool.
3. Send an MCP request larger than the request size limit of
   `mcp-context-serving@v1`.
4. Add `[limits]` with `file-bytes = 100` to `processkit.toml` and run
   `processkit config view -o json`.
5. Remove it. Run `processkit config view -o json` with an operator file
   that sets `limits.file-bytes = 0`, then `16777217`, then `4194304`, and
   repeat step 1 for the 2 MiB Standard with the last file.
6. Run any command with the truncated TOML file as `--config`.

Expected results:

- Every failing step fails with a diagnostic; no step hangs, crashes, or
  exhausts memory.
- The oversized and too-deep, too-wide, and too-long inputs fail with
  `security.limit-exceeded` (exit 1) and name `evidence.limit` and
  `evidence.maximum`; the truncated JSON fails with
  `security.malformed-input` (exit 1); the front matter inputs fail with
  `storage.front-matter-delimiter` and `storage.unsafe-yaml`.
- Each input gives exactly one diagnostic. Each diagnostic is at most 4096
  bytes, has the same size for the 2 MiB and the 100 MiB inputs apart from
  the file name, and contains no 16-byte sequence of the input body.
- The MCP server keeps serving other requests after step 3.
- Step 4 fails with `cli.config-forbidden-key`.
- In step 5, `0` and `16777217` fail with `cli.config-invalid-value` and
  the command does not run; with `4194304` the report shows
  `limits.file-bytes` with source `operator`, and the 2 MiB Standard is
  accepted by the size check.
- Step 6 fails with `security.malformed-input`.

Covers: PK-SEC-004, PK-SEC-017, PK-SEC-019, PK-SEC-020, PK-SEC-021,
PK-SEC-022

## 4. Instructions embedded in content

Preconditions: the repository from journey 1 with: a Standard whose rule
text says to ignore previous instructions, to call a tool named
`write_file`, to treat the reader as an administrator, and to download a
URL on a reserved domain (`https://attacker.example/payload`); a skill with
a script `setup.sh` that would create a marker file when run; a template
containing code syntax; and a Role-like text inside a document that claims
to grant access to another repository. Outbound network connections are
observed.

Steps:

1. Connect a stdio MCP client; read the server instructions (briefing),
   `tools/list`, and `resources/list`.
2. Call `get_context` with a task matching the Standard and the skill, and
   `get` the skill at level 2 for `setup.sh`.
3. Run `processkit config view -o json` and `processkit get context -o json`.

Expected results:

- The tool set, tool names, descriptions, and schemas equal those of a
  repository without this content; no `write_file` tool exists.
- Every served item carries its kind and provenance; the injected text
  appears only inside the labelled item.
- `setup.sh` is returned as labelled content; no marker file exists; no
  template was evaluated.
- No connection to `attacker.example` or any other host is attempted.
- The effective configuration and the access behavior are unchanged.

Covers: PK-SEC-001, PK-SEC-002, PK-SEC-003, PK-SEC-005

## 5. Credential patterns in catalog entries, arguments, and discovery

Preconditions: the repository from journey 1 with an operator
configuration that defines a secret pattern; an MCP server entry whose
`spec.authentication.notes` field contains a value matching that pattern;
the shared server configured with TLS material and an `oidc` authenticator
(synthetic issuer).

Steps:

1. Run `processkit validate -f FILE -o json` on the entry's file.
2. Remove the credential value and start `processkit mcp serve --http
   --listen ADDRESS`; while it runs, read the argument vectors of the
   processkit process and of every child process.
3. Connect a client with a valid token and read the initialize result,
   server instructions, `tools/list`, `resources/list`, and `prompts/list`.
4. Run `processkit fetch` against a synthetic private upstream whose
   credentials only a recording Git credential helper of the test user
   provides; read the argument vectors and environments of every child
   process.
5. Inspect the documented options of every command.
6. Declare an upstream source `https://user:token@git.example/repo.git` in
   `processkit.toml` and run `processkit validate -o json`.

Expected results:

- Step 1 fails; the diagnostic names the field and does not contain the
  credential value (`content-kinds@v1` PK-CAT-003, `cli@v1` PK-OUT-004).
- No argument vector in steps 2 and 4 contains a credential value.
- Step 4 succeeds through the credential helper; no Git child process has
  a credential value that processkit added to its arguments, environment,
  or configuration.
- Step 6 fails with `cli.config-forbidden-key`; the diagnostic does not
  contain `token`.
- No discovery response in step 3 contains a credential value, a token, or
  key material.
- No documented option takes a credential value.

Covers: PK-SEC-015, PK-SEC-028

## 6. Shared server Origin, request isolation, and credentials in URLs

Preconditions: the shared server running with TLS and an `oidc`
authenticator, and the operator setting
`transport.allowed-origins = ["https://ui.example"]`;
two principals A and B with valid synthetic tokens and different Bindings;
an HTTP client that can set arbitrary headers.

Steps:

1. Send an otherwise valid request from A with `Origin:
   https://attacker.example`, and one with `Origin: null`.
2. Send the same request from A without `Origin`, and with `Origin:
   https://UI.example:443`.
3. Send a request from A with header `Mcp-Session-Id: abc`; then with that
   header and no credentials; then with that header and B's token.
4. Send `GET` and `OPTIONS` to the MCP endpoint with A's token.
5. Send A's request with the token in the query parameter `access_token`
   instead of the `Authorization` header.
6. Send concurrent requests from A and B.
7. Start a second server with `transport.allowed-origins = ["*"]`.

Expected results:

- Step 1 gets HTTP 403 with `security.origin-rejected` in `error.data.code`
  and serves no content; both are rejected before authentication.
- Step 2 is served; no response carries `Mcp-Session-Id`.
- Every request of step 3 gets HTTP 404 with `security.session-rejected`
  and no content.
- Step 4 gets HTTP 405 with `security.method-not-allowed` and the `Allow`
  header `POST`.
- Step 5 gets HTTP 400 with `security.credential-in-url`; the token appears
  in no log record.
- In step 6 no result or diagnostic for A appears in B's responses and
  vice versa.
- Every rejection body validates against
  `schemas/http-rejection.schema.json`; every response carries
  `Cache-Control: no-store`, `X-Content-Type-Options: nosniff`, and
  `Strict-Transport-Security: max-age=31536000`, and no
  `Access-Control-Allow-*` header; every rejection has one log record at
  level `warning` with the code as event.
- Step 7 fails to start with `cli.config-invalid-value`.

Covers: PK-SEC-013, PK-SEC-014, PK-SEC-023, PK-SEC-024, PK-SEC-026,
PK-SEC-027

## 7. Owner-only credential files

Preconditions: a release target with POSIX permissions (Linux or macOS);
operator configuration for the shared server with a TLS key file.

Steps:

1. Set the key file to mode 0644 and start `processkit mcp serve --http
   --listen ADDRESS`.
2. Set it to mode 0640 and start again.
3. Set it to mode 0600 and start again; then to mode 0400.
4. Replace the key file with a symbolic link at mode 0777 that points to a
   key file at mode 0600, and start again.

Expected results:

- Steps 1 and 2 refuse to start with `security.credential-file-permissions`
  and exit code 3; the diagnostic names the file path in `evidence.path`
  and the mode in `evidence.mode`, and contains no key material.
- Steps 3 and 4 start.

Covers: PK-SEC-016, PK-SEC-029

## 8. Verified installation and offline default

Preconditions: release candidate artifacts with their `.sigstore.json`
bundles; a tampered copy of the wheel; a copy without its bundle and with
only `SHA256SUMS` next to it; a copy whose bundle was signed by another
identity; outbound network connections observed after installation; a
repository with one declared upstream.

Steps:

1. Install the tampered copy with the documented installation.
2. Install the copy that has only a same-location checksum.
3. Install the copy with the other identity's bundle.
4. Install the genuine artifacts.
5. Run `processkit init --governing`, `create`, `validate`, `get TYPE`,
   `get TYPE NAME`, `get context`, `describe`, `api-resources`,
   `config view`, `version`, and `processkit mcp serve --stdio` with a
   client session.
6. Run `processkit lock` before any fetch.
7. Run `processkit fetch`, then `processkit lock --yes`.

Expected results:

- Steps 1 to 3 fail at the `sigstore verify identity` step;
  `uv tool list` does not show processkit afterwards.
- Step 4 succeeds after verification.
- Step 5 makes no network connection and sends no telemetry.
- Step 6 fails with `cli.upstream-not-fetched` (exit 3), makes no network
  connection, and writes no lock.
- In step 7, `fetch` connects only to the declared upstream's source;
  `lock` makes no network connection and writes the lock.

Covers: PK-SEC-005, PK-SEC-010, PK-SEC-018, PK-SEC-030

## 9. Shared server transport limits

Preconditions: the shared server running with TLS and an `oidc`
authenticator and an operator file that sets
`transport.max-header-bytes = 4096`, `transport.header-timeout-seconds =
2`, `transport.idle-timeout-seconds = 5`, and `transport.max-connections =
2`; a raw TLS client.

Steps:

1. Send a request whose request line and headers have 5000 bytes.
2. Open a connection and send half a header block, then wait 3 seconds.
3. Open two idle connections, then a third connection with a valid request.
4. Keep a connection idle for 6 seconds after a served request.
5. Start a server with `transport.max-connections = 5000`.

Expected results:

- Step 1 gets HTTP 431 with `security.header-too-large`.
- In step 2 the server closes the connection without a response and writes
  a log record with event `security.header-timeout`.
- Step 3's third connection gets HTTP 503 with `Retry-After: 1` and
  `security.connection-limit`, and is closed.
- In step 4 the server closes the connection and writes no rejection
  record.
- Step 5 fails to start with `cli.config-invalid-value` (above the ceiling
  4096).
- No step serves content; rejection bodies validate against
  `schemas/http-rejection.schema.json`.

Covers: PK-SEC-020, PK-SEC-025, PK-SEC-026

## Verified by component tests only

- PK-SEC-011 and PK-SEC-031 (lockfiles, immutable dependency inputs,
  dependency record in `docs/dependencies.md`, `uv lock --check`):
  a property of the processkit source repository and its release build,
  checked by the release gate (a build with a mutable input must fail), not
  by a user journey.
- PK-SEC-012 (regression tests per security defect, coordinated
  disclosure): a process obligation, checked by the release gate inspecting
  the test suite against the security advisories and the published
  disclosure policy.
