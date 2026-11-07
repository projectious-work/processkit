# processkit v1

processkit v1 is a provider-neutral context framework. Its normative
contract is a set of feature specifications under [`spec/`](../../spec/),
laid out per the company specification-layout standard
(`.standards/specification-layout-and-lifecycle.md`). This directory holds
the non-normative product documentation around them.

Until #206 the contract was one monolithic draft in `spec/doc/v1/`
(baseline #197). It was cut into the specifications below without changing
any requirement's meaning; every requirement kept its ID. All
specifications are drafts until the owner freezes them.

## Specifications

| Specification | Scope | Roadmap |
| --- | --- | --- |
| [`ontology@v1`](../../spec/ontology/v1/overview.md) | Ontology, registry, resource envelope, labels, selectors, Containers | PK1-P1 |
| [`repository-storage@v1`](../../spec/repository-storage/v1/overview.md) | Repository layout, files, serialization, the Git boundary | PK1-P1 |
| [`content-kinds@v1`](../../spec/content-kinds/v1/overview.md) | Standards, skills, process specifications, decisions, documents, MCP catalog | PK1-P1, PK1-P6 |
| [`cli@v1`](../../spec/cli/v1/overview.md) | Commands, root discovery, reviewed plans, configuration, output, platforms | PK1-P2 |
| [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/overview.md) | MCP tools, briefing, deterministic assembly, pinned profiles, health | PK1-P3 |
| [`inheritance@v1`](../../spec/inheritance/v1/overview.md) | Upstreams, lock, overrides, final items, provenance | PK1-P4 |
| [`access-control@v1`](../../spec/access-control/v1/overview.md) | Authenticators, Roles, Bindings, the shared server | PK1-P5 |
| [`security@v1`](../../spec/security/v1/overview.md) | Threat model, input limits, release trust, transport hardening | PK1-P2, P3, P5 |
| [`v0-migration@v1`](../../spec/v0-migration/v1/overview.md) | Contract versioning and conversion of v0 content | PK1-P7 |

The roadmap is [`roadmap.yaml`](../../roadmap.yaml). Each phase lists the
specifications it delivers.

## Documentation

- [Product definition](product-definition.md): purpose, scope, non-goals.
- [Architecture](architecture.md): language and module structure.
- [Verification and release](verification-and-release.md): test strategy,
  release-wide acceptance journeys, and release rules.
- [Decisions](decisions.md): the decisions C1–C10 the specifications cite.
- Product profiles and Twelve-Factor deviations:
  [applicability record](../applicability-record.md).

## Contract hierarchy

Where documents disagree, a specification's schemas and fixtures govern
structure, its numbered requirements govern semantics, and prose explains
intent. Documentation in this directory never overrides a specification. A
contradiction is a specification defect and needs a new specification
version before affected implementation continues.

## Validation

```sh
python3 .standards/standards.py check-specs
uv run scripts/validate-v1-spec.py
```
