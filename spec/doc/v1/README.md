# processkit v1.x product specification

Status: **draft for review**

This directory defines the proposed normative baseline for a clean processkit
v1.x implementation. Existing v0 code, the earlier v1 alpha implementation,
and its Rust/Python architecture are evidence only. They do not define this
contract unless a requirement below deliberately preserves their behavior.

Normative terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` have the
meanings defined by RFC 2119 and RFC 8174.

## Reading order

1. [Product definition](01-product-definition.md)
2. [Conceptual model and ontology](02-conceptual-model.md)
3. [Project storage and ownership](03-project-storage-and-ownership.md)
4. [Content, packages, and extensions](04-content-packages-and-extensions.md)
5. [Application and lifecycle](05-application-and-lifecycle.md)
6. [Agent protocol and query surface](06-agent-protocol-and-query-surface.md)
7. [Configuration, output, and
   evidence](07-configuration-output-and-evidence.md)
8. [Security and trust](08-security-and-trust.md)
9. [Architecture and language](09-architecture-and-language.md)
10. [Verification strategy](10-verification-strategy.md)
11. [Compatibility, migration, and
    release](11-compatibility-migration-and-release.md)
12. [Documentation and acceptance](12-documentation-and-acceptance.md)
13. [Ontology contracts](13-standard-entity-types.md)
14. [Performance and operations](14-performance-and-operations.md)
15. [Review decisions](15-review-decisions.md)
16. [Roadmap](roadmap.yaml)

## Contract hierarchy

Where documents disagree, executable schemas and fixtures govern structural
shape, numbered normative requirements govern semantics, and explanatory prose
provides intent. A contradiction is a specification defect and requires an
explicit baseline amendment before affected implementation continues.

## Product profiles

processkit is a composite product with these company-standard profiles:

- CLI application;
- local service or worker for MCP transports;
- schema, protocol, and process package;
- Python library for internal composition and tested extension points; and
- documentation website.

The v1 implementation follows the company standards for configuration,
application output and logging, compatibility, security, verification,
roadmaps, documentation, branching, and spec-driven development.
