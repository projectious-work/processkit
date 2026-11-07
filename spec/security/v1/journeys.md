# Security — acceptance journeys

The release acceptance journeys of the baseline contain no security
journey. Journeys 1 to 5 are built from the cases that the baseline's
security test requirement lists: path traversal, symlink escape, oversized
and malformed input, instructions embedded in content, and credential
patterns in catalog entries. Journeys 6 to 8 cover the remaining
requirements. Every journey runs in a temporary Git repository with
synthetic data, no ambient credentials, and no user configuration, from the
exact release artifacts. Where an identifier or value is still open (see
`interfaces.yaml`), the journey states the observable effect, not the
identifier.

## 1. Path traversal from content and arguments

Preconditions: a governing repository initialized with `processkit init
--governing`; a file `outside.txt` with a known marker string next to the
repository root (outside it); a stdio MCP client connected with
`processkit mcp serve --stdio`.

Steps:

1. Run `processkit new Standard ../../outside`.
2. Add a skill whose `skill.json` and `SKILL.md` are valid and request, over
   MCP `get`, a level-2 file of that skill with a section or file name
   `../../outside.txt`.
3. Add a Markdown document whose front matter names a related path
   `../../outside.txt`, and run `processkit validate --json`.

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
2. Run `processkit list Skill --json` and `processkit context --json`.
3. Run `processkit validate --json`.

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
Standard larger than the documented size limit, a JSON file nested deeper
than the documented limit, a Markdown decision record with unterminated
front matter, front matter using YAML outside the safe subset (an anchor or
a tag), a truncated JSON file, and a project configuration that sets a
request or parser limit.

Steps:

1. Run `processkit validate --json` for each input file separately.
2. Pass each input as draft content to `processkit validate -` and to the
   MCP `validate` tool.
3. Send an MCP request larger than the documented request size limit.
4. Add the limit setting to `processkit.toml`, run `processkit config show
   --json`, and repeat step 1 for the oversized input.

Expected results:

- Every step fails with a diagnostic; no step hangs, crashes, or exhausts
  memory.
- Each diagnostic is bounded in size independently of the input size and
  does not echo the full input.
- The MCP server keeps serving other requests after step 3.
- In step 4 the project configuration does not change the effective limit
  (it fails as an unknown key or is rejected); the oversized input still
  fails.

Covers: PK-SEC-004, PK-SEC-017

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
3. Run `processkit config show --json` and `processkit context --json`.

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

1. Run `processkit validate --json` on the entry.
2. Remove the credential value and start `processkit mcp serve --http
   --listen ADDRESS`; while it runs, read the argument vectors of the
   processkit process and of every child process.
3. Connect a client with a valid token and read the initialize result,
   server instructions, `tools/list`, `resources/list`, and `prompts/list`.
4. Run `processkit fetch` against a synthetic upstream that requires
   credentials and read the argument vectors of every child process.
5. Inspect the documented options of every command.

Expected results:

- Step 1 fails; the diagnostic names the field and does not contain the
  credential value (`content-kinds@v1` PK-CAT-003, `cli@v1` PK-OUT-004).
- No argument vector in steps 2 and 4 contains a credential value.
- No discovery response in step 3 contains a credential value, a token, or
  key material.
- No documented option takes a credential value.

Covers: PK-SEC-015

## 6. Shared server Origin and request isolation

Preconditions: the shared server running with TLS and an `oidc`
authenticator; two principals A and B with valid synthetic tokens and
different Bindings; an HTTP client that can set arbitrary headers.

Steps:

1. Send an otherwise valid request from A with an Origin header the server
   does not accept.
2. Send the same request from A with an accepted Origin, or without one if
   the release documents that as accepted.
3. If the server issues an MCP session identifier to A, send a request with
   that session identifier and no credentials, then with B's token.
4. Send concurrent requests from A and B.

Expected results:

- Step 1 is rejected and serves no content.
- Step 2 is served.
- In step 3 neither request is served as A; the request without
  credentials is rejected, and B's request is rejected or served only as B
  without any content of A's session.
- In step 4 no result or diagnostic for A appears in B's responses and
  vice versa.

Covers: PK-SEC-013, PK-SEC-014

## 7. Owner-only credential files

Preconditions: a release target with POSIX permissions (Linux or macOS);
operator configuration for the shared server with a TLS key file.

Steps:

1. Set the key file to mode 0644 and start `processkit mcp serve --http
   --listen ADDRESS`.
2. Set it to mode 0640 and start again.
3. Set it to mode 0600 and start again.

Expected results:

- Steps 1 and 2 refuse to start; the report names the file path and the
  permission reason and contains no key material.
- Step 3 starts.

Covers: PK-SEC-016

## 8. Verified installation and offline default

Preconditions: release candidate artifacts with signatures; a tampered copy
of the wheel; a copy with its signature removed and only a checksum file
next to it; outbound network connections observed after installation.

Steps:

1. Install the tampered copy with the documented installation.
2. Install the copy that has only a same-location checksum.
3. Install the genuine artifacts.
4. Run `processkit init --governing`, `new`, `validate`, `list`, `show`,
   `context`, `explain`, `ontology list`, `config show`, `version`, and
   `processkit mcp serve --stdio` with a client session.
5. Run `processkit fetch` with a locked upstream.

Expected results:

- Steps 1 and 2 fail before anything is installed.
- Step 3 succeeds after verification.
- Step 4 makes no network connection and sends no telemetry.
- Step 5 connects only to the locked upstream's source.

Covers: PK-SEC-005, PK-SEC-010

## Verified by component tests only

- PK-SEC-011 (lockfiles, immutable dependency inputs, dependency record):
  a property of the processkit source repository and its release build,
  checked by the release gate (a build with a mutable input must fail), not
  by a user journey.
- PK-SEC-012 (regression tests per security defect, coordinated
  disclosure): a process obligation, checked by the release gate inspecting
  the test suite against the security advisories and the published
  disclosure policy.
