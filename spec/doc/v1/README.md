# processkit v1.x product specification

Status: **draft for review**

This directory defines the normative baseline for processkit v1 as a
provider-neutral context framework. It replaces the earlier memory-oriented
v1 draft; see [Decisions](12-decisions.md). Existing v0 code and the v1 alpha
are evidence only and do not define this contract.

Normative terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` have the
meanings defined by RFC 2119 and RFC 8174.

## Reading order

1. [Product definition](01-product-definition.md)
2. [Ontology](02-ontology.md)
3. [Repository layout and files](03-repository-and-files.md)
4. [Governance content](04-governance-content.md)
5. [Inheritance across repositories](05-inheritance.md)
6. [Command-line interface](06-cli.md)
7. [MCP server and context assembly](07-mcp-and-context-assembly.md)
8. [Identity and access control](08-identity-and-access.md)
9. [Security, configuration, and output](09-security-configuration-and-output.md)
10. [Architecture and language](10-architecture.md)
11. [Verification, compatibility, and release](11-verification-and-release.md)
12. [Decisions](12-decisions.md)
13. [Roadmap](roadmap.yaml)

## Contract hierarchy

Where documents disagree, published schemas and fixtures govern structure,
numbered requirements govern semantics, and prose explains intent. A
contradiction is a specification defect and requires an explicit amendment
before affected implementation continues.

## Product profiles

processkit is a composite product with these company-standard profiles:

- CLI application;
- MCP server, local over stdio and optionally as an access-controlled shared
  server;
- schema and ontology package; and
- documentation website.

The implementation follows the company standards for configuration, output
and logging, compatibility, security, verification, roadmaps,
documentation, branching, and spec-driven development, and the company
agent-native product-interface standard.
