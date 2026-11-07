# Ontology and content model — acceptance journeys

Each journey runs against the exact release-candidate artifacts in a
temporary Git repository with synthetic content and no ambient credentials.
Diagnostic codes, registry field names, and the selector error position
format are open (see `interfaces.yaml` `open`); until they are fixed, a
journey checks the outcome, the file, the JSON pointer, and the violated
constraint that the diagnostic reports.

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

Expected results:

- Step 1 reports an ontology version.
- Step 2 lists exactly 90 concepts: 20 of class T, 22 of class P, 24 of
  class D, and 24 of class C, matching the inventory names in
  `interfaces.yaml`; every concept has a class, a side (definition or
  instance), a description, relations, and a schema or fragment location,
  and every D concept names its parent primitive.
- Step 3 shows Container with side definition and WorkItem with side
  instance; WorkItem's location is a vocabulary fragment, Container's a
  closed schema.
- Step 4 returns the same registry content as steps 2 and 3.

Covers: PK-PROD-003, PK-MODEL-001, PK-MODEL-002, PK-MODEL-005,
PK-MODEL-054

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

- Steps 1 and 2 report a failure that the kind is an instance concept and
  write no file; CLI and MCP report equivalent diagnostics.
- Step 3 serves no WorkItem item.
- Step 4 succeeds; the ProcessSpecification is valid and served.

Covers: PK-PROD-003, PK-MODEL-003

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
8. add a namespaced extension field where the owning schema declares an
   extension map, and then one that uses an ontology field name.

Expected results:

- 1: each removal fails with the JSON pointer of the missing field.
- 2: the duplicate in the same namespace fails; the same name in another
  Container is valid.
- 3: the item keeps its name and typed identity; validation succeeds.
- 4: each change fails naming the bound that was exceeded.
- 5: both fail as reserved keys.
- 6: fails because `status` is derived; `processkit explain Standard
  git-branching` reports validation result, content digest, source path,
  and provenance as derived facts.
- 7: fails as an unknown field.
- 8: the namespaced extension field is valid; the redefinition fails.

Covers: PK-MODEL-010, PK-MODEL-012, PK-MODEL-013, PK-MODEL-014,
PK-MODEL-015

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
   `list(kind="Standard")`.

Expected results:

- 1: validation succeeds; `git-branching` belongs to the root Container.
- 2: CLI and MCP return `api-style` only.
- 3: both items are served with identical content and semantics; only
  their namespace and typed name differ.
- 4: fails as a duplicate Container name.
- 5: fails as a Container cycle.
- 6: fails as an unknown parent.
- 7: validation fails for `api-style` with an unknown Container; the item
  is not returned by either list, and other valid items still are.

Covers: PK-MODEL-011, PK-MODEL-046, PK-MODEL-047, PK-MODEL-048,
PK-MODEL-049

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

Expected results:

- 1: `a`, `c`. 3: `a`, `b`. 5: `a`, `b`. 6: `c`. 7: `a`.
- 2 and 4: include `b` and exclude `a`; whether `c` is included is
  OPEN-ontology-06.
- 8: no item; annotations are not selectable.
- 9 and 10: rejected as invalid selectors; the error reports the exact
  position of the fault, and CLI and MCP report the same position.
- For every S, CLI and MCP return the same items.

Covers: PK-MODEL-012, PK-MODEL-044, PK-MODEL-045

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
  lock and the results carry the upstream identity.
- 2: the path is not accepted as a reference.
- 3: validation fails for the required reference; `processkit show`
  reports the reference as unresolved rather than omitting it.

Covers: PK-MODEL-021, PK-MODEL-022, PK-MODEL-023

## J7 — Visibility only through labels and access control

Preconditions: shared server with two principals; Role `reader-all` with
`get`/`list` on Standard and Role `reader-internal` with selector
`sensitivity notin (confidential)`, each granted by a `grants-role`
Binding scoped to the root Container; the Standards from J5.

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

1. Under `context/ontology/`, add a namespaced concept and a namespaced
   relation type with a declared namespace owner; validate.
2. Remove the namespace owner; validate; revert.
3. Add an extension that redefines the published concept `Container`;
   validate; revert.
4. In a project repository inheriting from this one, use the upstream
   extension concept in an item; validate and run `processkit explain`.

Expected results:

- 1: valid against the published extension metaschemas.
- 2 and 3: fail.
- 4: valid; the namespace owner reported is the upstream repository.

Covers: PK-MODEL-040, PK-MODEL-041

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

## Verified by component tests only

- **PK-MODEL-004** — drift between registry, schemas, and generated
  documentation is a build-time regeneration check on the source tree.
- **PK-MODEL-016** — absent, null, empty, and default distinctions are
  per-schema properties checked by schema fixtures.
- **PK-MODEL-020** — relation and relation-type declarations are checked
  against the relation registry by schema and fixture tests.
- **PK-MODEL-030** — a recommendation verified by schema review against
  Dublin Core Terms and W3C PROV mappings.
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
