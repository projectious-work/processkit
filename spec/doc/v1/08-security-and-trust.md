# Security and trust

## Assets and boundaries

Protected assets include project entities, unpublished discussions and notes,
credentials referenced by integrations, Git history, release packages,
ownership manifests, migration evidence, harness configuration, and generated
agent instructions. Derived embedding text and vectors are protected at the
highest sensitivity of their canonical sources because they may reveal source
meaning even when the original text is absent.

Trust boundaries exist between:

- release publisher and installer;
- processkit-owned and project-owned content;
- project policy and user/system authority;
- MCP clients and the local runtime;
- canonical files and untrusted indexes or caches;
- package instructions and executable tools;
- one repository and external repositories or services.
- one clone or worktree and another clone or worktree of the same repository.

## Release trust

- **PK-SEC-001:** installers MUST verify package integrity and authenticated
  release provenance before mutation when signature material is supplied.
- **PK-SEC-002:** trust anchors MUST be configured independently of the
  untrusted release being verified.
- **PK-SEC-003:** a checksum downloaded from the same unauthenticated location
  as an artifact proves integrity in transit only, not publisher identity.
- **PK-SEC-004:** package manifests MUST bind every installed file digest,
  ownership class, contract version, and dependency.
- **PK-SEC-005:** downgrade, prerelease adoption, and trust-anchor replacement
  require explicit policy and confirmation.

## Input and filesystem safety

- **PK-SEC-010:** parsers MUST bound document size, nesting, collection counts,
  string lengths, archive expansion, and decompression ratio.
- **PK-SEC-011:** archives MUST reject absolute paths, traversal, duplicate
  normalized paths, symlink/hardlink escape, devices, sockets, and unsupported
  metadata before extraction.
- **PK-SEC-012:** filesystem checks MUST be race-aware and repeated at commit
  boundaries; validation of a path string alone is insufficient.
- **PK-SEC-013:** processkit MUST preserve restrictive permissions for private
  runtime state and MUST not broaden permissions silently.
- **PK-SEC-014:** subprocesses, when unavoidable, use argument arrays,
  controlled working directories, allowlisted environment, bounded IO,
  timeout, and cancellation; shell evaluation is prohibited by default.

## MCP and instruction safety

- **PK-SEC-020:** stdio is the universal local transport. The optional v1 HTTP
  daemon MUST bind to loopback, authenticate every client using credentials
  kept outside project-controlled files, enforce origin and request-isolation
  controls applicable to the selected MCP transport, and disclose residual
  same-host risks. Non-loopback binding is outside v1.
- **PK-SEC-028:** daemon and proxy diagnostics MUST redact bearer material and
  MUST NOT place credentials in command arguments, repository configuration,
  generated skill projections, or MCP discovery responses. Credential files
  require owner-only permissions where the platform supports them.
- **PK-SEC-021:** mutating and destructive capabilities MUST be labeled for
  harness policy and independently checked by processkit.
- **PK-SEC-022:** content from packages, entities, external references, and
  imported bundles is untrusted data; it MUST NOT silently acquire executable
  or higher-authority semantics because an agent reads it.
- **PK-SEC-023:** imported skills and processes remain disabled until package
  trust and project policy accept them.
- **PK-SEC-024:** diagnostics MUST not recommend bypassing containment,
  signature, validation, approval, or recovery checks.
- **PK-SEC-025:** repository content, including processkit entities changed by
  another participant, MUST be treated as untrusted input until normal project
  review and validation policy accepts it. A valid schema does not establish
  the truth, authorization, or safety of its claims.
- **PK-SEC-026:** processkit MUST NOT infer caller identity or mutation
  authority solely from mutable TeamMember files, Git author metadata, harness
  prompts, or environment variables. Authority-sensitive operations require an
  authenticated runtime principal or an explicit local policy decision.
- **PK-SEC-027:** project TeamMember records MUST NOT be used as storage for
  model-provider credentials, harness session secrets, or private conversational
  memory.

## Dependencies and privacy

- **PK-SEC-030:** every direct runtime dependency MUST have a documented
  purpose and reviewed license, maintenance, provenance, and transitive cost.
- **PK-SEC-031:** dependency and application lockfiles are committed and release
  builds fail on unresolved or mutable dependency inputs.
- **PK-SEC-032:** default operation emits no telemetry and performs no network
  egress.
- **PK-SEC-033:** tests use synthetic data, reserved domains, temporary roots,
  and no ambient credentials or user configuration.
- **PK-SEC-034:** security defects add permanent negative regression coverage
  and follow coordinated disclosure without moving published tags.
- **PK-SEC-035:** embedding generation and semantic retrieval MUST run locally
  by default. Sending source text or derived representations to a remote model
  or vector service requires explicit configuration, disclosure of affected
  data classes and destination, and project policy authorization.
- **PK-SEC-036:** private or excluded canonical content MUST remain excluded
  from embedding, similarity search, context assembly, logs, and exports unless
  the same caller is explicitly authorized for that content.

## Threat-driven acceptance

- **PK-SEC-040:** the release suite MUST include adversarial archives, symlink
  races where the platform permits testing, malformed YAML/JSON, oversized
  inputs, untrusted Markdown instructions, MCP request flooding, stale plans,
  interrupted writes, signature failures, malicious package paths, and
  redaction boundary cases.
