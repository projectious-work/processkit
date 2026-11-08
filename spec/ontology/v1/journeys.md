# Ontology and content model — acceptance journeys

Each journey runs against the exact release-candidate artifacts in a
temporary Git repository with synthetic content and no ambient credentials.
Each failing step checks the diagnostic code listed in `interfaces.yaml`
`errors`, the file, and the JSON pointer. The diagnostic shape, the result
envelope, and exit categories are those of cli@v1.

No acceptance journey of the baseline release list is specific to this
specification; the journeys below exercise ontology publication, validation,
selectors, and Containers.

## J1 — Read the published ontology registry

Preconditions: processkit is installed from the release candidate; an
initialized governing repository exists.

Steps:

1. Run `processkit version --json`.
2. Run `processkit ontology list --json`.
3. Run `processkit ontology show Container --json` and
   `processkit ontology show WorkItem --json`.
4. Over stdio MCP, call `ontology()` and `ontology(concept="Container")`.
5. Run `processkit ontology show NoSuchConcept --json` and call MCP
   `ontology(concept="NoSuchConcept")`.

Expected results:

- Step 1 reports the ontology version `1.0.0`.
- Step 2 returns a document valid against
  `schemas/ontology-registry.schema.json` with `ontologyVersion` `1.0.0`.
  `concepts` holds exactly 90 entries, sorted by name: 20 of class T, 22
  of class P, 24 of class D, and 24 of class C, matching the inventory
  names in `interfaces.yaml`. Each entry has the side listed there (68
  definition, 22 instance). Every D entry has `parent`, every C entry has
  `parts`, and every T entry has schema form `fragment`. `relationTypes`
  holds the eight relation types of `interfaces.yaml` `relations.types`.
- Step 3 shows Container with side `definition` and schema form
  `closed-schema`, and WorkItem with side `instance` and schema form
  `vocabulary-fragment`.
- Step 4 returns the same registry content as steps 2 and 3.
- Step 5 fails with `ontology.unknown-concept` in CLI and MCP.

Covers: PK-PROD-003, PK-MODEL-001, PK-MODEL-002, PK-MODEL-005,
PK-MODEL-054, PK-MODEL-055, PK-MODEL-056, PK-MODEL-057, PK-MODEL-070

## J2 — Instance concepts are vocabulary, never content

Preconditions: initialized governing repository.

Steps:

1. Pipe a draft item with `"kind": "WorkItem"` and a valid envelope to
   `processkit validate -`.
2. Call MCP `validate(kind="WorkItem", content=...)` with the same draft.
3. Place the same item as a file under the content directory and run
   `processkit list WorkItem` and MCP `list(kind="WorkItem")`.
4. Create a ProcessSpecification that names WorkItem as the type it governs
   and references the instance concepts Event and Outcome by name; run
   `processkit validate`.

Expected results:

- Steps 1 and 2 fail with `ontology.instance-kind` and write no file; CLI
  and MCP report the same code.
- Step 3 serves no WorkItem item.
- Step 4 succeeds; the ProcessSpecification is valid and served.

Covers: PK-PROD-003, PK-MODEL-003, PK-MODEL-061

## J3 — Validate the common envelope

Preconditions: initialized governing repository with one valid Standard
`git-branching` in the root Container.

Steps: run `processkit validate` after each of these separate changes,
reverting the previous one:

1. remove `spec`; then remove `metadata.name`; then remove `apiVersion`;
2. add a second Standard with `metadata.name` `git-branching` in the same
   namespace; then move it to another existing Container;
3. move the `git-branching` file to another path within the declared
   standards location, without changing its content;
4. add 65 labels; then add a label with an invalid key; then a label value
   longer than 63 characters;
5. add label `processkit.projectious.work/x: "y"`; then the same key as an
   annotation;
6. add a top-level `status` object with a content digest;
7. add an unknown field `spec.foo` to a kind whose schema declares no
   extension map at that position;
8. add a Container `engineering` with
   `spec.extensions` `{"example.com/cost-center": "4711"}`; then change the
   key to `title`;
9. run `processkit show Standard git-branching --json` and
   `processkit list Standard --json`.

Expected results:

- 1: each removal fails with `ontology.missing-field` and the JSON pointer
  of the missing field (`/spec`, `/metadata/name`, `/apiVersion`).
- 2: the duplicate in the same namespace fails with
  `ontology.duplicate-name`; the same name in another Container is valid.
- 3: the item keeps its name and typed identity; validation succeeds.
- 4: the changes fail with `ontology.label-count`, `ontology.label-key`,
  and `ontology.label-value`.
- 5: both fail with `ontology.reserved-key`.
- 6: fails with `ontology.authored-status`; after reverting,
  `processkit explain Standard git-branching --json` reports `status`
  valid against `schemas/status.schema.json`, with
  `status.validation.outcome` `valid`, a `status.digest` that equals
  `sha256:` and the SHA-256 of the file bytes, and `status.source.path`
  equal to the file's repository-relative path.
- 7: fails with `ontology.unknown-field`.
- 8: the namespaced key is valid; the key `title` fails with
  `ontology.extension-field-not-namespaced`.
- 9: the `show` result has `status`; the list items have no `status`.

Covers: PK-MODEL-010, PK-MODEL-012, PK-MODEL-013, PK-MODEL-014,
PK-MODEL-015, PK-MODEL-061, PK-MODEL-062, PK-MODEL-063

## J4 — Containers as namespaces

Preconditions: initialized governing repository.

Steps:

1. Add Containers `company` (no discriminator, no parent), `engineering`
   (discriminator Team, parent `company`), and `payments` (discriminator
   Project, parent `engineering`), each with name, title, owner, and
   lifecycle. Add Standard `git-branching` without `metadata.namespace` and
   Standard `api-style` in namespace `engineering`. Run
   `processkit validate`.
2. Run `processkit list Standard --namespace engineering` and the MCP
   `list(kind="Standard", namespace="engineering")`.
3. Give `api-style` the same `spec` content as an item in another
   namespace and run `processkit show` on both.
4. Add a second Container named `engineering`; validate; revert.
5. Set `company`'s parent to `payments`; validate; revert.
6. Set `payments`' parent to `unknown-unit`; validate; revert.
7. Set `api-style`'s `metadata.namespace` to `nowhere`; run
   `processkit validate`, `processkit list Standard`, and MCP
   `list(kind="Standard")`; revert.
8. Run `processkit list Standard --namespace root`.
9. Add Container `root` with title, owner, and lifecycle and no parent;
   validate. Then give it `spec.parent` `Container/company`; validate;
   revert.
10. Add `metadata.namespace` `engineering` to Container `payments`;
    validate; revert.
11. Add a Container with `spec.discriminator` `Risk`; validate; revert.
12. In a project repository that inherits from this repository through a
    locked and fetched upstream, add Standard `local-style` with
    `metadata.namespace` `engineering` and a Container `squad` with
    `spec.parent` `Container/payments`; validate.

Expected results:

- 1: validation succeeds; `git-branching` belongs to the root Container
  `root`; `company` is a child of `root`.
- 2: CLI and MCP return `api-style` only.
- 3: both items are served with identical content and semantics; only
  their namespace and typed name differ.
- 4: fails with `ontology.duplicate-container`.
- 5: fails with `ontology.container-cycle`.
- 6: fails with `ontology.unknown-parent`.
- 7: validation fails for `api-style` with `ontology.unknown-namespace`;
  the item is not returned by either list, and other valid items still
  are.
- 8: returns `git-branching` and not `api-style`.
- 9: the explicit `root` is valid; with a parent it fails with
  `ontology.root-parent`.
- 10: fails with `ontology.namespace-not-allowed`.
- 11: fails with `ontology.schema-violation` at `/spec/discriminator`.
- 12: validation succeeds; the upstream Containers are known.

Covers: PK-MODEL-011, PK-MODEL-046, PK-MODEL-047, PK-MODEL-048,
PK-MODEL-049, PK-MODEL-064, PK-MODEL-065, PK-MODEL-066

## J5 — Label selectors

Preconditions: repository with Standards `a` (labels `area=delivery`,
`sensitivity=internal`), `b` (labels `area=security`,
`sensitivity=confidential`), and `c` (label `area=delivery`, no
`sensitivity`), and annotation `example.com/review-cycle: yearly` on `a`.

Steps: run `processkit list Standard --selector S --json` and MCP
`list(kind="Standard", selector=S)` for each S:

1. `area=delivery`
2. `area!=delivery`
3. `sensitivity in (internal,confidential)`
4. `sensitivity notin (confidential)`
5. `sensitivity`
6. `!sensitivity`
7. `area=delivery,sensitivity`
8. `example.com/review-cycle=yearly`
9. `area=delivery,sensitivity in (internal` (missing parenthesis)
10. `area==delivery`
11. `` (empty) and `   ` (three spaces)
12. ` area = delivery , sensitivity  in ( internal , confidential ) `
13. `area="delivery"`
14. `sensitivity in ()`
15. `! sensitivity`

Expected results:

- 1: `a`, `c`. 2: `b`. 3: `a`, `b`. 4: `a`, `c`. 5: `a`, `b`. 6: `c`.
  7: `a`.
- 8: no item; annotations are not selectable.
- 9, 10, 13, and 14: rejected with `ontology.invalid-selector` and
  `offset` 38, 5, 5, and 16; CLI and MCP report the same offset.
- 11: `a`, `b`, `c`. 12: `a`. 15: `c`.
- For every S, CLI and MCP return the same items.

Covers: PK-MODEL-012, PK-MODEL-044, PK-MODEL-045, PK-MODEL-067,
PK-MODEL-068, PK-MODEL-069

## J6 — Typed references and unresolved references

Preconditions: a project repository that inherits from a locked and fetched
upstream governing repository containing Standard `git-branching` and
DecisionRecord `adopt-github-flow`; a local Container `engineering`.

Steps:

1. Add a local Standard that references `Standard/git-branching`,
   `DecisionRecord/adopt-github-flow`, and `Container/engineering`; run
   `processkit validate` and `processkit explain` on it.
2. Replace one reference with the file path
   `standards/git-branching.json`; validate.
3. Replace one reference with `Standard/does-not-exist` in a field the
   owning schema requires; validate and run `processkit show`.

Expected results:

- 1: validation succeeds; the inherited references resolve through the
  lock; in `status.references` of the explain result, each inherited
  reference has `resolved` true and an `origin` that names the upstream.
- 2: fails with `ontology.invalid-reference`.
- 3: validation fails with `ontology.unresolved-reference` (severity
  error); `processkit show` lists the reference in `status.references`
  with `resolved` false.

Covers: PK-MODEL-021, PK-MODEL-022, PK-MODEL-023, PK-MODEL-071

## J7 — Visibility only through labels and access control

Preconditions: shared server with two principals; Role `reader-all` with
`get`/`list` on Standard and Role `reader-internal` with selector
`sensitivity notin (confidential)`, each granted by a `grants-role`
Binding scoped to `Container/root`; the Standards from J5.

Steps:

1. As each principal, call MCP `list(kind="Standard")`.
2. Run `processkit access can-i list Standard b --as` each principal.
3. Inspect `processkit config show` and the published schemas for any
   other setting or field that hides items.

Expected results:

- 1: `reader-all` receives `a`, `b`, `c`; `reader-internal` receives `a` and
  `c` only.
- 2: the decision and granting Binding match step 1.
- 3: no setting or field other than labels and access rules hides items.

Covers: PK-MODEL-050, PK-MODEL-012

## J8 — Extensions

Preconditions: initialized governing repository.

Steps:

1. Under `context/ontology/`, add the OntologyExtension
   `incident-management` of `interfaces.yaml` `extensions.example`, with
   one relation type `escalates-to` added; validate; run
   `processkit ontology show Incident --json`.
2. Remove `spec.namespaceOwner`; validate; revert.
3. Add a concept named `container` to the extension; validate; revert.
4. Set `spec.namespace` to `processkit.projectious.work`; validate;
   revert.
5. Add a second OntologyExtension `other` that adds a concept `Incident`;
   validate; revert.
6. In a project repository inheriting from this one, run
   `processkit ontology show Incident --json` and
   `processkit explain OntologyExtension incident-management --json`.
7. In that project repository, add an OntologyExtension with
   `spec.namespace` `example.com`; validate.

Expected results:

- 1: valid against `schemas/ontology-extension.schema.json`; the entry
  has `namespace` `example.com`, `namespaceOwner` `Platform team`, and
  `extension` `OntologyExtension/incident-management`.
- 2: fails with `ontology.extension-missing-owner`.
- 3: fails with `ontology.extension-redefines-concept`.
- 4: fails with `ontology.reserved-key`.
- 5: fails with `ontology.extension-duplicate-name`.
- 6: the entry is listed; the explain provenance names the upstream
  repository.
- 7: fails with `ontology.extension-namespace-taken`.

Covers: PK-MODEL-040, PK-MODEL-041, PK-MODEL-057, PK-MODEL-072,
PK-MODEL-073, PK-MODEL-074

## J9 — Scaling-framework concepts are optional

Preconditions: processkit installed from the release candidate.

Steps:

1. Initialize a governing repository and create one item of every
   processkit content kind from its published template; validate.
2. Add a Container with discriminator ART and a WSJFEstimate reference in
   a ProcessSpecification; validate.

Expected results:

- 1: succeeds without any ART, ValueStream, ProgramIncrement, or
  WSJFEstimate content or default.
- 2: succeeds; the concepts are usable.

Covers: PK-MODEL-006

## J10 — Relations as Bindings

Preconditions: initialized governing repository with the Containers of J4
and the Standards of J5.

Steps: add each Binding below, run `processkit validate`, and revert:

1. `spec.relation` `dependency`, subject `Standard/a`, target
   `Standard/b`.
2. `spec.relation` `depends-on`, same subject and target.
3. `spec.relation` `hierarchy`, subject `Container/payments`, target
   `Container/company`.
4. Two Bindings with `spec.relation` `ownership-link` and subject
   `Standard/a`, targets `Container/company` and `Container/engineering`.
5. `spec.relation` `related-to` with `spec.scope` `Container/engineering`.

Expected results:

- 1: valid.
- 2: fails with `ontology.unknown-relation-type`.
- 3: fails with `ontology.relation-endpoint`.
- 4: fails with `ontology.relation-cardinality`.
- 5: fails with `ontology.relation-endpoint`.

Covers: PK-MODEL-020, PK-MODEL-070

## Verified by component tests only

- **PK-MODEL-004** — drift between registry, schemas, and generated
  documentation is a build-time regeneration check on the source tree.
- **PK-MODEL-016** — absent, null, empty, and default distinctions are
  per-schema properties checked by schema fixtures.
- **PK-MODEL-020** — beyond J10, relation-type declarations (direction,
  cardinality, endpoints, inverse) are checked against the registry by
  schema and fixture tests.
- **PK-MODEL-030** — a recommendation verified by schema review against
  Dublin Core Terms and W3C PROV mappings.
- **PK-MODEL-075** — a fixture item with a
  `v0.processkit.projectious.work/` key validates, and one with a
  `processkit.projectious.work/` key fails; a schema-fixture test.
- **PK-MODEL-031** — optional; no projection ships in v1. If one is added,
  a generation test proves it derives from the registry.
- **PK-MODEL-042** — a review criterion for changes to the published
  ontology, checked on registry change proposals, not at runtime.
- **PK-MODEL-043** — a repository-level check that processkit's own
  repositories declare no private concepts.
- **PK-MODEL-051** — generation failure conditions need malformed ontology
  sources, which only the build-time generator accepts.
- **PK-MODEL-052** — T-concept fragment coverage and consumption is a
  generator check.
- **PK-MODEL-053** — discriminator positive and negative fixtures run in the
  schema test suite.
- **PK-MODEL-058** — generator failure codes need malformed ontology
  sources, which only the build-time generator accepts.
- **PK-MODEL-059** and **PK-MODEL-060** — coverage of discriminators and
  rejection of invalid mixing are checked on the release fixtures by the
  schema test suite.
