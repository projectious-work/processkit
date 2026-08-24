# Agent-native product posture

## Why processkit exists in an agentic software world

An AI agent can reason about work and write Markdown without processkit. That
does not provide durable shared context, validated entity semantics, lifecycle
enforcement, attribution, retrieval boundaries, package trust, or recovery
across agents, models, conversations, clones, and time.

processkit is the agent-native context and workflow layer for durable,
governed project operations. It does not make human or model decisions
deterministic. It makes their accepted representation, validation, transition,
provenance, retrieval, and audit explicit and reproducible.

The product follows the company
[agent-native product interfaces standard][agent-standard]. MCP is the primary
agent interface, CLI is the complete human, automation, administration, and
recovery interface, and both adapt one application and domain core.

- **PK-AGENT-001:** model reasoning, conversation history, and proposed
  interpretation MUST NOT become canonical project state without a validated
  product operation.
- **PK-AGENT-002:** processkit MUST preserve deterministic contracts for
  validation, transition, attribution, event recording, package trust,
  recovery, and derived-index rebuild around probabilistic agent reasoning.
- **PK-AGENT-003:** processkit MUST NOT own an agent loop, infer private
  reasoning, or make model confidence an authorization or truth signal.

## Division of labour

| Activity | Primary mode | Boundary |
|---|---|---|
| Interpret project context and propose action | Agent reasoning | Proposal has no canonical effect or authority. |
| Select relevant context and skills | Agent-assisted retrieval and routing | Sources, sensitivity, scores, and limits are attributable. |
| Create or change an entity | Deterministic product operation | Schema, identity, lifecycle, authorization, atomicity, and event rules apply. |
| Make a consequential decision | Human or authorized agent reasoning | Accepted outcome becomes a DecisionRecord through a validated operation. |
| Execute a process or gate | Mixed | Agent performs reasoning; processkit enforces declared state and evidence rules. |
| Install or update skills and MCP capabilities | Deterministic package lifecycle | Provenance, ownership, policy, plan, conflict, and verification apply. |
| Explain state or suggest next work | Agent reasoning | Canonical facts and permitted next actions come from typed results. |
| Collaborate across clones | Git-mediated human/agent workflow | processkit does not claim distributed transactions or shared database authority. |

## Interface and capability posture

MCP exposes bounded ontology, retrieval, lifecycle, package, and diagnostic
operations. It does not expose arbitrary filesystem or shell access. CLI and
MCP operations that overlap have equivalent validation, effects, events,
diagnostics, and recovery.

Every result SHOULD identify applicability, stable outcome and finding codes,
affected root and entity, authority requirements, durable mutation identity,
permitted next actions from a closed set, evidence, and recovery state where
relevant. Human explanation may accompany but cannot replace the typed result.

- **PK-AGENT-010:** MCP tool descriptions, schemas, annotations, namespaces,
  and capability membership MUST be versioned trusted package assets and MUST
  NOT be derived from entity bodies or external-reference prose.
- **PK-AGENT-011:** the gateway MUST reject duplicate, ambiguous, shadowed, or
  provenance-conflicting tool identities across core, installed package, and
  extension capabilities.
- **PK-AGENT-012:** a running MCP server or daemon MUST use a stable capability
  snapshot; package or configuration changes require explicit refresh with a
  reported before/after manifest or restart.
- **PK-AGENT-013:** structured next actions MUST reference registered product
  operations and MUST NOT contain arbitrary executable instructions obtained
  from untrusted project content.
- **PK-AGENT-014:** loss of an MCP client or proxy session MUST NOT lose,
  duplicate, or ambiguously repeat a repository mutation; status and recovery
  remain available through CLI or another authorized client.

## Instruction trust

Processkit manages both data and instructions, so classification is explicit:

| Content | Agent semantics |
|---|---|
| Verified processkit package skill | Trusted instruction within its declared package capabilities and project policy. |
| Project-owned skill or process | Instruction only after project policy accepts its provenance and enabled state. |
| Imported package or extension | Untrusted and disabled until package trust and project policy accept it. |
| Entity body, external reference, search result, log, or handoff | Data; never promoted automatically to agent instruction. |
| TeamMember or persona content | Attributed project context; not authentication or mutation authority. |
| MCP tool definition | Trusted runtime asset bound to its package manifest and released implementation. |

Schema validity proves structure, not truth, safety, authority, or instruction
trust. Context assembly preserves source identity, sensitivity, content class,
and trust classification so a harness can keep data distinct from accepted
instructions.

- **PK-AGENT-020:** packages MUST declare which files are agent instructions,
  executable tools, templates, reference data, or ordinary documentation.
- **PK-AGENT-021:** importing or indexing content MUST NOT change its trust or
  executable classification.
- **PK-AGENT-022:** project policy MUST be able to disable an installed skill
  or capability without deleting its canonical source or falsifying package
  provenance.
- **PK-AGENT-023:** context assembly MUST keep accepted instructions, stable
  reference material, and per-run working material distinguishable even when
  all three are stored as human-readable files.
- **PK-AGENT-024:** context MAY be disclosed or enriched stepwise, but every
  increment MUST retain source identity, revision or digest, sensitivity,
  trust classification, selection reason, and applicable size limits.
- **PK-AGENT-025:** a process step SHOULD receive the smallest sufficient
  context selected by its declared inputs. Absence, truncation, fallback
  retrieval, and later enrichment MUST be visible rather than silently
  changing the effective step contract.
- **PK-AGENT-026:** directory placement under `references`, `working`,
  `output`, or an equivalent projection MUST NOT grant instruction trust,
  mutation authority, completion, or approval semantics.

## Identity, attribution, and authority

An authenticated runtime principal, a logical TeamMember, an entity author, a
Git author, and the agent or human described in prose are different facts.
Processkit records the distinctions it can verify and does not invent the
others.

Ordinary low-risk entity creation need not require independent human approval
when project policy authorizes the caller. Consequential transitions, package
changes, policy acceptance, destructive reconciliation, and other elevated
operations may require a separate plan, confirmation, gate, or authenticated
approver according to product and project policy.

- **PK-AGENT-030:** MCP capability discovery MUST remain distinct from mutation
  authority; visible or enabled tools are not self-authorizing.
- **PK-AGENT-031:** private chain-of-thought MUST NOT be requested or stored as
  evidence. Records contain decisions, rationale, sources, actors, and outcomes
  needed for project accountability.
- **PK-AGENT-032:** one identity MAY fill requester and approver roles only
  where explicit policy permits it; the result records that policy basis.

## Documentation and positioning

Public documentation leads with the agent-native context/workflow posture and
presents an MCP first-use journey beside an equivalent CLI journey. It explains
why durable repository context remains valuable when models can reason and
write files directly, and distinguishes probabilistic project decisions from
deterministic product enforcement.

The posture does not imply that every process should be formalized or every
agent action recorded. Processkit remains useful only where durable shared
context, lifecycle, provenance, retrieval, or governance justifies the added
structure.

[agent-standard]: https://github.com/projectious-work/internal/blob/main/docs/standards/agent-native-product-interfaces.md
