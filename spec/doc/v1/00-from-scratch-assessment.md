# From-scratch product and implementation assessment

## Method

This assessment begins with the product outcomes in this specification. It
does not assume that existing v0 behavior, the earlier v1 RFC, the 89-concept
ontology, released alpha artifacts, the Rust installer, or Python MCP servers
are the correct solution.

Existing material was reviewed only to answer:

- which user problems have demonstrated value;
- which failure modes and compatibility obligations are real;
- which architecture choices created duplicated authority or release cost;
- which experiments provide reusable evidence; and
- what existing adopters would need from an explicit migration.

## Durable product findings

The strongest validated product idea is not a particular ontology or
installer. It is a Git-native, human-readable process layer with validated
agent operations and durable evidence. WorkItems, decisions, discussions,
events, skills, and repository-local policy have repeatedly supported real
coordination. MCP is the appropriate provider-neutral agent boundary.

These findings survive a clean redesign:

1. Canonical project memory should remain in inspectable repository files.
2. Normal mutations need validated tools and lifecycle enforcement.
3. Derived indexes are valuable but must never become canonical state.
4. Installed content needs explicit ownership and safe three-way updates.
5. Harness projections should derive from one provider-neutral catalog.
6. A project must be usable without aibox or a hosted processkit service.
7. Cross-repository coordination requires explicit handoffs and ownership,
   not a global shared writable context.

## Root causes of drift

### No single normative product baseline

Product claims are distributed across an RFC, planning pages, architecture
notes, issue-status pages, release scripts, schemas, skills, MCP servers,
installer contracts, and observed dogfood behavior. Several development pages
explicitly describe themselves as historical while remaining the nearest
thing to a product specification. This makes conformance circular: current
code can be interpreted as the intended contract when prose is incomplete.

### Ontology-first scope

The former v1 effort made an 89-concept T/P/D/C ontology and first-ART coverage
central success measures. That work contains useful modeling research, but it
committed product scope before proving that each kernel concept required
cross-domain lifecycle enforcement. Vocabulary breadth increased schema,
migration, documentation, query, and agent-training obligations at once.

The replacement uses a kernel test: a core concept must have cross-domain
lifecycle semantics that packages cannot safely express. Other vocabulary is
an extension, not a v1 release blocker.

### Split behavioral authority

The experimental architecture divided lifecycle installation and filesystem
mutation into Rust while leaving entity behavior, MCP, schema handling,
indexing, and skills in Python. This produced two model systems, two error
surfaces, two dependency and release toolchains, and machine contracts between
components whose ownership boundary followed implementation history rather
than product semantics.

The replacement has one Python application core shared by CLI and MCP. Native
components remain possible only behind a measured, narrow contract.

### Release machinery ahead of product closure

The former branch invested substantially in native artifact signing,
installer requests, platform bootstrap, prerelease promotion, and recovery
while foundational entity, package, extension, and runtime semantics were
still evolving. Supply-chain and recovery work remains mandatory, but it
should prove an accepted product contract rather than stabilize an accidental
one.

### Producer, dogfood, generated, and project state ambiguity

The repository has needed repeated drift controls between producer content,
installed `context/`, generated schemas, MCP manifests, harness configuration,
and derived-project customizations. The replacement makes ownership class and
source-of-truth status part of package and installation contracts rather than
inferring them from directory conventions.

## Language assessment

The following weighting reflects this specification, not a generic language
comparison.

| Criterion | Weight | Python | Go | Rust |
|---|---:|---:|---:|---:|
| Contract iteration and content tooling | 20 | 5 | 4 | 3 |
| MCP and agent ecosystem fit | 15 | 5 | 4 | 3 |
| Filesystem correctness and testability | 15 | 4 | 5 | 5 |
| Cross-platform application installation | 10 | 4 | 5 | 5 |
| Contributor and extension accessibility | 15 | 5 | 4 | 3 |
| Runtime performance and concurrency | 5 | 3 | 5 | 5 |
| One-language architectural coherence | 10 | 5 | 5 | 5 |
| Dependency and release simplicity | 10 | 4 | 5 | 3 |
| **Weighted result out of 500** | **100** | **455** | **450** | **380** |

The numerical difference between Python and Go is intentionally small. Go is
the better choice for a native executable product; Python is the better choice
for the processkit product as specified because rapid contract iteration,
MCP integration, structured-content tooling, and contributor accessibility
slightly outweigh native distribution. `uv tool install` weakens the main Go
distribution advantage sufficiently to make Python the recommended choice.

Rust offers excellent local safety but does not provide enough additional
product value to offset implementation and cross-ecosystem cost. The previous
work remains valuable as test cases for transactions, archives, trust, and
recovery, not as a language commitment.

## Reuse, replace, and retire

| Existing evidence | Treatment |
|---|---|
| Git-backed canonical entities | Preserve the product principle; re-specify formats. |
| MCP gateway and domain tools | Reuse behavior only where new conformance fixtures approve it. |
| SQLite/FTS indexing | Retain as the default derived adapter; rewrite behind a port. |
| Rust installer | Mine adversarial fixtures and transaction cases; replace implementation. |
| Python per-skill servers | Consolidate semantics into one application core; adapters may remain thin. |
| 89-concept ontology | Retain as optional package research; do not make it the kernel or GA gate. |
| v0 and v1-alpha corpora | Preserve as migration fixtures and compatibility evidence. |
| Signed release and recovery tests | Adapt to Python artifacts and the new ownership contract. |
| Existing public documentation | Archive by version; rewrite v1 docs from accepted behavior. |

## Recommendation

Accept this specification as a new baseline, reconcile the existing v1 branch
through a separate non-destructive branch plan, and implement the phases in
`roadmap.yaml` using Python 3.12+, uv, one shared application core, strict
public schemas, Git-native canonical state, and derived local indexes.

Do not begin by porting Rust modules to Python. Begin with conformance fixtures
for the kernel, repository transaction, ownership, machine-result, and MCP
contracts. Existing code may then be retained only when it passes those
fixtures without redefining them.
