# Review decisions

This draft is internally coherent but intentionally does not manufacture
approval for consequential choices. Review must accept, amend, or reject each
item before the specification becomes the implementation baseline.

## D1 — Small mandatory kernel with optional ontology packages

**Accepted:** ship a small repository-memory kernel as mandatory v1 scope and
move non-universal organizational, scaling-framework, communication,
location, scheduling, portfolio, and evaluation concepts into optional
first-party packages.

**Reason:** v0 proves the Git-native validated kernel, not market demand for
all 89 internally shaped concepts. Optional packages preserve broader value
without encoding one operating model as universal.

**Impact:** Phase 0 produces a concept disposition matrix. Core conformance is
independent of optional-package conformance.

## D2 — Python as the sole required implementation language

**Accepted:** implement CLI, MCP, domain services, reconciliation, migrations,
generation, and indexing in Python 3.12+, installed as an isolated application
with uv or an equivalent tool.

**Reason:** Python narrowly outranks Go for this contract- and integration-heavy
product once uv weakens the native single-executable advantage. Rust does not
justify its additional delivery cost for the specified workload.

**Impact:** the Rust installer is replaced, but its security, transaction, and
recovery fixtures remain implementation evidence. A native component requires
a later measured justification and versioned boundary.

No prior source code is retained by default. A v0 and alpha capability
disposition matrix preserves useful behavior and failure evidence through
requirements and black-box fixtures rather than code reuse.

## D13 — Minimal semantic-standard reuse

**Accepted:** reuse only the smallest best-fitting established semantics,
initially Dublin Core Terms for generic metadata and W3C PROV for provenance
where meanings fit. Keep canonical Git files, JSON Schema, and state machines.

**Reason:** Processkit should avoid redefining mature generic concepts without
becoming an RDF, ontology-reasoning, or vocabulary-integration product.

**Impact:** Phase 0 includes a versioned mapping/disposition matrix. General
RDF, JSON-LD, OWL, SHACL, Wikidata, DBpedia, and other export or integration
work is deferred until a concrete use case justifies it.

## D14 — Bounded ICM-inspired workflow profile

**Accepted:** cite
[Interpretable Context Methodology (ICM)][icm] as prior art and
provide an optional `linear-reviewed` Processkit profile for sequential,
repeatable, human-reviewed processes. Its simple authoring view distinguishes
accepted instructions, stable reference context, and per-run working context,
and exposes human-editable intermediate artifacts.

**Reason:** explicit `Inputs`, `Process`, and `Outputs` contracts plus staged
context disclosure are a natural fit for simple research, assessment,
documentation, and content workflows. ICM's folder-presence state model does
not replace Processkit's typed lifecycle, trust, provenance, gates, evidence,
or recovery semantics.

**Impact:** Processkit may generate a provider-neutral human-readable stage
projection, but canonical Processkit records remain authoritative. The first
use is a measured internal research-to-assessment pilot across two provider
harnesses. v1 does not implement an ICM importer or exporter.

[icm]: https://github.com/RinDig/Interpretable-Context-Methodology

## D15 — Graph projection and hybrid retrieval

**Accepted:** treat Processkit's canonical entities and typed relations as a
graph-shaped domain model, project them into the disposable SQLite index, and
combine lexical or vector seed discovery with bounded typed-relation expansion
for attributed context assembly.

**Reason:** vectors find content that looks relevant; typed relations express
dependency, authority, supersession, provenance, and lifecycle that similarity
cannot. The accepted local scale and bounded traversals do not justify a
dedicated graph database.

**Impact:** canonical and probabilistically inferred edges remain visibly
distinct. Graph storage is behind a replaceable index port, but another adapter
requires measured failure of the indexed SQLite implementation against an
accepted requirement. A graph database is not a v1 dependency.

## D3 — One application core

**Accepted:** CLI and MCP become adapters over one application and domain core.
Earlier per-skill servers are migration evidence, not another v1 runtime.

**Reason:** one mutation, validation, event, and recovery path prevents the
current split authority from recurring.

**Impact:** module and process boundaries may change substantially even when a
public tool name survives.

## D4 — Compatibility posture

**Proposal:** support explicit migrations from maintained v0 corpora and
released earlier-v1-alpha corpora, while refusing to preserve alpha behavior
that conflicts with the accepted new contract.

**Reason:** users deserve preservation and transparent incompatibility, not an
assumption that prerelease implementation details define the replacement.

**Impact:** each source line needs golden corpora, field-level preservation
reports, manual-blocker behavior, and migration documentation.

## D5 — Existing v1 branch reconciliation

**Proposal:** keep this specification PR non-destructive. After acceptance,
prepare a separate reviewed reconciliation plan for the existing `v1.x-dev`
history and promotion branches.

The plan must identify whether implementation proceeds by removing/replacing
experimental files through ordinary commits, introducing a new version line,
or another ancestry-preserving method. Force-push, tag movement, and unique
commits on promotion branches remain prohibited.

**Reason:** accepting a new product baseline does not authorize rewriting
published alpha history or protected branches.

**Impact:** implementation cannot begin until the target branch and handling of
existing alpha support are explicit.

## D6 — Specification artifact location

**Proposal:** use `spec/doc/v1/` and `spec/schemas/v1/` for this baseline while
the company discussion on OpenSpec, specifications, and processkit remains
open. Treat this as a project-local choice, not a company-wide directory
standard.

**Reason:** the implementation needs a bounded reviewable baseline now, while
the broader question of representing specifications as processkit artifacts is
still unresolved.

**Impact:** a later accepted company model may migrate these files without
changing their normative meaning or history.

## D7 — Contract namespaces

**Proposal:** use surface-qualified identifiers such as
`processkit.projectious.work/entity/v1` and
`processkit.projectious.work/result/v1` instead of continuing the old
unqualified `processkit.projectious.work/v2` value.

**Reason:** product release, entities, packages, machine results, plans,
events, configuration, and extensions have independent compatibility
lifecycles. One unqualified counter cannot express or evolve those contracts
safely.

**Impact:** existing `processkit.projectious.work/v2` entities require an
explicit source adapter. The apparent numeric move from `v2` to a qualified
`entity/v1` is a namespace change, not a claim that old data has been silently
downgraded.

## D8 — Repository-scoped process memory

**Accepted company architecture:** one repository represents one project or
coordination scope and contains one authoritative processkit context. The
context is shared project memory for any number of human and AI participants,
not an agent-private memory repository.

**Reason:** the repository already supplies the authority, deliverable,
history, collaboration, and review boundary. Agents can use ordinary clones
and branches while processkit gives their shared context typed semantics and
validated operations.

**Impact:** root means repository root; local indexes are per working copy;
TeamMember is project-local participation state; and processkit does not own
Airunner runtime memory, heartbeat, Git synchronization, or Kaits company
orchestration.

## D9 — Python command surface

**Proposal:** ship one Python application with lifecycle, catalog, entity,
event, context, skill, handoff, index, generation, package, and MCP command
groups. CLI and MCP are adapters over identical application operations; typed
MCP tools and optional convenience commands do not create separate semantics.

**Reason:** humans, scripts, harnesses, and conformance tests need the same
repository capabilities without reproducing validation in shell scripts or
requiring MCP for local administration. Namespaced generic commands avoid a
flat CLI containing one command for every EntityType and skill.

**Impact:** generic entity and retrieval commands move into mandatory v1
scope. The tool changes only one selected working copy and never implies Git
commit, review, push, or cross-repository acceptance.

## D10 — Canonical skills with generated harness adapters

**Proposal:** processkit continues to own and version skills. Each skill has
one harness-neutral source contract; versioned adapters generate native
discovery files, command aliases, and MCP configuration for selected harnesses.
Initialization may detect and propose supported targets, while the ordinary
plan/apply lifecycle performs changes. There is no top-level command per
harness and no implicit installation of all known adapters.

**Reason:** harnesses differ in file locations, metadata, invocation syntax,
and MCP configuration, but those differences do not justify divergent copies
of a skill's purpose, safety rules, inputs, or outputs. A generated projection
keeps processkit authoritative while making loss of semantics visible.

**Impact:** skill authoring and harness projection are v1 capabilities rather
than post-v1 ideas. The release requires adapter support matrices, provenance,
idempotent regeneration, conflict preservation, and cross-harness conformance
fixtures.

## D11 — Retain the efficient local MCP daemon

**Proposal:** support both an on-demand stdio server and the useful v0-style
long-lived local gateway daemon with lightweight stdio proxies. The v1 daemon
executes the unified application core directly, serves exactly one repository
root, binds only to loopback, authenticates every client, and refreshes its
catalog safely. Process supervision remains external.

**Reason:** repeated interpreter startup and registration of a large tool
catalog is avoidable overhead, especially when several harness sessions use
the same working copy. Removing the daemon would discard a proven operational
benefit merely to obtain a smaller topology diagram.

**Impact:** daemon and proxy are v1 surfaces with root-isolation, credential,
catalog-refresh, concurrency, health, shutdown, and adapter-equivalence tests.
They do not restore per-skill runtime authority, create a shared project
database, or make a hosted service necessary.

## D12 — Declarative harness reconciliation

**Proposal:** desired profiles, packages, skills, MCP capabilities, and harness
targets live in versioned project configuration. `plan reconcile` computes the
drift and `apply --plan` converges it. `plan adapter --harness ...` is an
onboarding convenience that proposes the desired-state change as well as the
projection actions.

**Reason:** adding Tau or another harness later should use the same reviewed,
idempotent plan/apply model as installation and upgrade. A declarative source
also permits future CI/CD or GitOps controllers to run reconciliation without
embedding a separate imperative command sequence.

**Impact:** v1 does not need to ship a controller, Argo CD integration, or
continuous reconciler. It must provide stable desired-state, plan, machine
result, drift, idempotence, and verification contracts from which those
systems can be built.
