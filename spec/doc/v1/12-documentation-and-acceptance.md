# Documentation and acceptance

## Documentation system

- **PK-DOC-001:** public documentation MUST describe shipped behavior for the
  selected version line and label planned behavior explicitly.
- **PK-DOC-002:** source, schemas, examples, CLI/MCP reference, and development
  notes MUST evolve in the same change as the behavior they describe.
- **PK-DOC-003:** CLI, MCP, configuration, schema, package, and event references
  MUST be generated or mechanically checked against canonical contracts.
- **PK-DOC-004:** the documentation site MUST build locally and publish static
  output from `gh-pages` without project-authored GitHub Actions.
- **PK-DOC-005:** versioned documentation MUST preserve supported v0 material
  during v1 development and clearly distinguish stable from prerelease lines.
- **PK-DOC-006:** maintained examples are product contracts and MUST run or
  validate in release gates.
- **PK-DOC-007:** existing public documentation MUST be retained in its
  applicable versioned archive. v1 documentation MUST be rewritten from the
  accepted specification and shipped behavior, not edited as though historical
  pages already described the new product.

The public information architecture covers overview, getting started,
concepts, how-to guides, reference, troubleshooting, roadmap, releases and
migration, contributing, and security. The README remains a concise entry
point, not a second specification.

## Development evidence

- **PK-DOC-010:** every non-trivial roadmap phase maintains a development note
  recording implementation, boundaries, decisions, deviations, tests,
  security, compatibility, documentation, and owned follow-up work.
- **PK-DOC-011:** `roadmap.yaml` is the canonical roadmap and validates against
  the company-compatible roadmap schema.
- **PK-DOC-012:** an item becomes `shipped` only when it names a release and
  development note and its conformance evidence is accepted.

## Specification conformance

Implementation follows the company spec-driven development-cycle standard.
The accepted baseline consists of every file in this directory, its schemas,
examples, governing decisions, and applicable company standards.

- **PK-ACCEPT-001:** planning MUST inventory every normative requirement and
  map it to implementation work, tests, documentation, and evidence.
- **PK-ACCEPT-002:** an independent reviewer MUST review both the plan and the
  integrated result against every applicable requirement and executable
  contract.
- **PK-ACCEPT-003:** specification defects stop affected implementation and
  require an explicit corrective amendment and plan revision.
- **PK-ACCEPT-004:** implementation convenience MUST NOT silently redefine the
  contract, and existing behavior MUST NOT be grandfathered without an
  explicit compatibility decision.
- **PK-ACCEPT-005:** final conformance classifies every requirement as
  satisfied, accepted not-applicable, authorized deferral, or blocker; unknown
  and partially satisfied are not completion.

## Final acceptance journeys

1. Install an exact authenticated release into an empty temporary repository
   on every supported platform.
2. Verify the installed profile and inspect effective configuration.
3. Start MCP over stdio, then reuse the same capability catalog through an
   authenticated local daemon and stdio proxy; prove equivalent operations,
   root isolation, refresh, and shutdown behavior.
4. List installed skills, ontology concepts, packages, profiles, and MCP
   servers in both text and machine form and reconcile the result with package
   manifests and MCP discovery.
5. Create, query, transition, relate, and supersede representative entities;
   verify equivalent CLI and MCP outcomes, events, and index state without an
   implicit Git commit.
6. Generate and validate coverage for all 89 canonical ontology concepts,
   exercise every persistent P and C schema, every D discriminator, and every
   T fragment through at least one consuming contract.
7. Assemble bounded, attributed agent context through lexical, semantic, and
   hybrid retrieval; delete every derived index, rebuild it from canonical Git
   files, and obtain functionally equivalent sources without memory loss.
8. Install one canonical skill and MCP capability, project them into two
   supported harness formats in one reviewed adapter plan, and prove equivalent
   discovery, safety metadata, invocation, provenance, and conflict handling.
9. Run a durable process with a gate, evidence, interruption, and resumption.
10. Add and validate a namespaced extension package without core modification.
11. Preview and apply an update with unchanged, locally modified, mergeable,
   conflicting, generated, and project-owned files.
12. Recover from injected interruption at each mutation boundary.
13. Import representative v0 and earlier-v1-alpha corpora with preservation
   reports and explicit manual blockers.
14. Export a sanitized cross-repository handoff and receive it as local state.
15. Conservatively uninstall processkit while preserving modified and
    project-owned content.
16. Build documentation and verify the exact published release artifacts.
17. Run two independently indexed clones as different TeamMembers, integrate
    their proposed context changes through an ordinary reviewed Git merge,
    rebuild both indexes, and verify that canonical state converges without a
    shared processkit database.
18. Confirm that one repository supports human, permanent-agent, and
    ephemeral-agent participants while TeamMember state remains project-local
    and runtime memory remains outside canonical entities.
19. Add a newly installed harness target to declarative project configuration,
    preview and apply the adapter reconciliation, verify convergence, and then
    obtain an empty plan from the same desired state without a harness-specific
    imperative command.

## Definition of v1.0.0 complete

v1.0.0 is complete only when all normative requirements and acceptance
journeys are evidenced; security, migration, compatibility, documentation,
and platform support are published; no required check has an unexplained skip;
and the exact release artifacts pass independent post-publication verification.
