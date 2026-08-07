# Review decisions

This draft is internally coherent but intentionally does not manufacture
approval for consequential choices. Review must accept, amend, or reject each
item before the specification becomes the implementation baseline.

## D1 — Product kernel instead of ontology breadth

**Proposal:** adopt the small kernel and standard managed EntityTypes in this
specification. Treat the former 89-concept T/P/D/C ontology as optional package
research, not the v1 kernel or release gate.

**Reason:** only concepts requiring consistent cross-domain lifecycle
enforcement belong in the core. Vocabulary breadth multiplies migration,
schema, query, documentation, and agent-training obligations without proving
user value.

**Impact:** previous ontology-first alpha behavior is not automatically carried
forward. Useful domain concepts can return through versioned packages.

## D2 — Python as the sole required implementation language

**Proposal:** implement CLI, MCP, domain services, reconciliation, migrations,
generation, and indexing in Python 3.12+, installed as an isolated application
with uv or an equivalent tool.

**Reason:** Python narrowly outranks Go for this contract- and integration-heavy
product once uv weakens the native single-executable advantage. Rust does not
justify its additional delivery cost for the specified workload.

**Impact:** the Rust installer is replaced, but its security, transaction, and
recovery fixtures remain implementation evidence. A native component requires
a later measured justification and versioned boundary.

## D3 — One application core

**Proposal:** CLI and MCP become adapters over one application and domain core;
per-skill servers may remain compatibility adapters but own no semantics.

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
