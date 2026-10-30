# Security, configuration, and output

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

- **PK-SEC-001:** content from the repository and its upstreams is untrusted
  data. Serving it MUST NOT give it authority over tool definitions,
  configuration, access rules of other repositories, or processkit behavior.
- **PK-SEC-002:** served content MUST be labelled with its kind and
  provenance so an agent can distinguish an organization's rule from
  arbitrary text.
- **PK-SEC-003:** processkit MUST NOT execute content, run scripts from
  skills, evaluate templates with code, or follow URLs found in content.
- **PK-SEC-004:** inputs MUST have size limits; malformed JSON, YAML, or
  Markdown MUST fail with a bounded diagnostic.
- **PK-SEC-005:** default operation MUST NOT access the network or emit
  telemetry. Network access happens only for `fetch` and the shared server.

## Release trust

- **PK-SEC-010:** releases MUST be signed, and the documented installation
  MUST verify integrity and authenticity before use. A checksum downloaded
  from the same location as the artifact is not authentication.
- **PK-SEC-011:** dependency lockfiles MUST be committed, and release builds
  MUST fail on unresolved or mutable dependency inputs. Every direct runtime
  dependency MUST have a documented purpose and reviewed license.
- **PK-SEC-012:** security defects MUST receive permanent negative regression
  tests and follow coordinated disclosure.

## Configuration

Configuration has three layers, lowest precedence first:

1. project configuration `processkit.toml`, committed: content directory,
   profiles, document sources, upstreams, override winners, briefing budget;
2. operator configuration, outside the repository: listen address, TLS
   material, authenticators, imported access rules, limits, log sinks;
3. invocation flags and `PROCESSKIT_` environment variables.

- **PK-CONFIG-001:** every configuration file MUST use a closed, versioned
  schema; unknown keys MUST fail.
- **PK-CONFIG-002:** project configuration MUST NOT configure authenticators,
  credentials, listen addresses, or executables.
- **PK-CONFIG-003:** `processkit config show --json` MUST report the effective
  configuration with the source of every value and secrets redacted.

## Output and logging

- **PK-OUT-001:** JSON output MUST contain exactly one versioned result
  envelope with outcome, data, diagnostics, and revision.
- **PK-OUT-002:** results go to standard output and diagnostics to standard
  error.
- **PK-OUT-003:** operational logs MUST be structured, default to level
  `warning`, and go to standard error unless an operator configures another
  sink.
- **PK-OUT-004:** logs, diagnostics, and errors MUST redact bearer material,
  certificates, and values matching configured secret patterns.
- **PK-OUT-005:** `processkit version --json` MUST report the release, source
  commit, ontology version, supported content API versions, and supported MCP
  protocol versions.
