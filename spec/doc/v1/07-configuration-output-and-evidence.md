# Configuration, output, and evidence

## Configuration hierarchy

Configuration resolves from lower to higher precedence:

```text
compiled defaults
→ system configuration
→ user configuration
→ project policy
→ environment variables
→ command-line or MCP invocation
```

- **PK-CONFIG-000:** the application MAY omit a system layer on platforms
  without an appropriate location but MUST NOT reorder layers.

- **PK-CONFIG-001:** configuration files MUST use a closed, versioned schema.
- **PK-CONFIG-002:** environment variables use the `PROCESSKIT_` prefix.
- **PK-CONFIG-003:** relative paths resolve against the file declaring them or
  another explicitly documented anchor, never an accidental working directory.
- **PK-CONFIG-004:** project policy MUST NOT select executables, add
  credentials, weaken user/system security, enable network listeners, or
  redirect state outside allowed roots without higher-authority approval.
- **PK-CONFIG-005:** processkit MUST expose deterministic redacted effective
  configuration with winning and overridden sources and rejected settings.
- **PK-CONFIG-006:** invocation overrides are ephemeral unless a dedicated
  write command explicitly changes project-owned configuration.
- **PK-CONFIG-007:** project configuration is
  `<repository-root>/processkit.toml` by
  default; project policy and mutable operational state MUST NOT share one
  file.
- **PK-CONFIG-008:** system and user files use the operating system's published
  application configuration locations and are reported by `doctor` and the
  effective-configuration result even when absent.
- **PK-CONFIG-009:** environment and invocation layers MUST NOT change the
  selected root after root discovery has loaded project policy; root selection
  is resolved before other project configuration.
- **PK-CONFIG-010:** project configuration MUST declare the desired profile,
  packages, skills, MCP capabilities, and harness-adapter targets needed for
  deterministic reconciliation. Machine-local daemon addresses, credentials,
  and supervisor state MUST remain in higher-authority local configuration.

## Result envelope

Every machine result uses a closed versioned envelope containing:

```text
apiVersion, command, outcome, result, diagnostics, correlationId
```

`outcome` distinguishes `succeeded`, `refused`, `failed`, `cancelled`,
`timed_out`, `partial`, and `recovery_required` where applicable.

- **PK-OUTPUT-001:** JSON stdout MUST contain exactly one declared result
  object and no logs, progress, banners, or child output.
- **PK-OUTPUT-002:** requested human results go to stdout and diagnostics to
  stderr; non-interactive output is plain and colorless by default.
- **PK-OUTPUT-003:** result schemas, examples, and negative fixtures MUST cover
  every command and outcome category.
- **PK-OUTPUT-004:** unknown fields and unsupported result API versions MUST
  fail strict consumers.
- **PK-OUTPUT-005:** `version` output MUST report product version, source
  commit, build/package provenance, Python runtime, platform, and supported
  entity, package, plan, event, and machine-result contract versions.
- **PK-OUTPUT-006:** repository-scoped results MUST identify the normalized
  repository root, context path, observed Git revision when available, and
  canonical or index generation relevant to the operation.

## Operational logging

- **PK-LOG-001:** logs are structured semantic events rendered to configured
  sinks after redaction.
- **PK-LOG-002:** events SHOULD include time, level, name, component, operation,
  correlation ID, outcome, duration, and attributed dependency.
- **PK-LOG-003:** default level is `warning`; verbosity changes operational
  detail, not result semantics.
- **PK-LOG-004:** file and network sinks require authorized configuration and
  declare rotation, retention, failure, and privacy behavior.
- **PK-LOG-005:** sink failure MUST be surfaced without corrupting requested
  output or canonical domain evidence.

## Domain evidence

- **PK-EVIDENCE-001:** entity events, migration journals, ownership manifests,
  release records, and accepted gate results are durable evidence, not logs.
- **PK-EVIDENCE-002:** evidence retention and deletion follow project policy;
  rotating logs MUST NOT erase authoritative evidence.
- **PK-EVIDENCE-003:** evidence must distinguish observed facts, user claims,
  inferred conclusions, skipped checks, and unavailable dependencies.
- **PK-EVIDENCE-004:** export requires an explicit selection and redaction
  policy; private context is excluded by default.

## Redaction

- **PK-REDACT-001:** secrets, secret-shaped values, personal data, sensitive
  paths, and project-declared protected fields MUST be redacted before any
  renderer, buffer, log sink, response, telemetry, or test artifact.
- **PK-REDACT-002:** redaction MUST cover structured values, free text, chunks,
  exception chains, and concurrent streams.
- **PK-REDACT-003:** raw modes require explicit invocation and MUST still block
  known secrets; their residual risk is documented.
