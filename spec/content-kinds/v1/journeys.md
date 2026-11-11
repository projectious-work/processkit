# Content kinds — acceptance journeys

Each journey runs against a temporary Git repository initialized as a
governing repository (`processkit init --governing`), with synthetic data
and no ambient credentials. "Validates" means `processkit validate -o json`
reports success; "fails validation with C" means it reports a validation
failure (exit code 1) with at least one diagnostic whose `code` is C, with
`file`, `pointer`, and `constraint` set (PK-CONT-017). Field names, codes,
level contents, and section keys are in `interfaces.yaml`.

## 1. Create a standard, a skill, and an MCP server entry from templates

Source: release acceptance journey 2.

Preconditions: an initialized governing repository whose `processkit.toml`
declares the profiles `cli` and `service`.

Steps:

1. Run `processkit create Standard git-branching --yes`,
   `processkit create MCPServer issue-tracker --yes`, and
   `processkit create Skill triage-ticket --yes`.
2. Run `processkit create nosuchkind x`, `processkit create Document x`,
   and `processkit create Standard Bad_Name`.
3. Fill in `triage-ticket/skill.json`: `sideEffects`
   `externally-mutating`, `dependencies` `[Standard/git-branching]`,
   `requiredMcpServers` `[MCPServer/issue-tracker]`, one input, one output,
   one safety constraint, and `parts` with `SKILL.md` normative and
   `reference.md` explanatory; add `reference.md`. Run
   `processkit validate`.
4. Remove, one at a time, each required `spec` field of the three items;
   validate after each; restore.
5. One at a time, validate after each, then restore: set `sideEffects` to
   `externally mutating`; set `requiredMcpServers` to
   `[MCPServer/missing]`; set `dependencies` to `[Skill/missing]`; delete
   `reference.md`; remove `SKILL.md` from `parts`; remove `triggers` from
   `issue-tracker`; remove both the labels and `applicability` from
   `issue-tracker`.
6. Run `processkit get TYPE NAME` for each item with `--level 0` and
   `--level 1`, once with TYPE as the kind name and once as its short
   name (`std`, `mcp`, `sk`).

Expected results:

- Step 1 creates `context/standards/git-branching.json`,
  `context/mcp-servers/issue-tracker.json`, and
  `context/skills/triage-ticket/skill.json` and `SKILL.md`, with
  `metadata.name` (and the `SKILL.md` front matter `name`) set to the given
  name; all three validate.
- Step 2 fails with `content-kinds.unknown-kind`,
  `content-kinds.no-template`, and `content-kinds.invalid-name`, each with
  exit code 2 and no file written.
- Step 3 validates.
- Every removal in step 4 fails validation with
  `content-kinds.missing-field`, whose `pointer` names the removed field.
- Step 5 fails, in order, with `content-kinds.schema-violation`,
  `ontology.unresolved-reference`, `ontology.unresolved-reference`,
  `content-kinds.skill-part-missing`, `content-kinds.schema-violation`,
  `content-kinds.missing-field`, and
  `content-kinds.applicability-missing`.
- Step 6 at level 0 shows exactly the level-0 members of each kind; level 1
  adds the members of `levels` level 1: rules and the section index
  (Standard), `disclosure.body` with the `SKILL.md` body and the file index
  `[{path: reference.md, script: false}]` (Skill), and the server entry
  (MCPServer). No section body appears. The kind name and the short name
  return the same result.

Covers: PK-STD-001, PK-CAT-002, PK-SKILL-001, PK-SKILL-002, PK-SKILL-005,
PK-SKILL-006, PK-SKILL-007, PK-SKILL-008, PK-SKILL-009, PK-SKILL-010,
PK-SKILL-011, PK-SKILL-012, PK-SKILL-013, PK-CONT-001, PK-CONT-002,
PK-CONT-010, PK-CONT-013, PK-CONT-014, PK-CONT-017, PK-CONT-019,
PK-CONT-020, PK-CONT-021.

## 2. Define a ticket-handling process from natural language

Source: release acceptance journey 3.

Preconditions: journey 1 completed; Roles `triager` and `developer` exist in
`context/ontology/`; the worked example
`examples/process-specification.example.json` and the published
ProcessSpecification schema and template.

Steps:

1. Give an agent connected over stdio MCP the natural-language description
   of the worked example: tickets are triaged by a triager, implemented by
   a developer, and closed after a review gate; tickets live in an
   external issue tracker.
2. The agent produces a ProcessSpecification `ticket-handling` with the
   members of the worked example: `workItemType` `ticket`, states `new`,
   `triaged`, `in-progress`, `closed` (terminal), transitions with Roles,
   the Gate `review-approved` on `in-progress` to `closed`, the produced
   artifact `pull-request`, per-state references to `Standard/git-branching`,
   `Skill/triage-ticket`, and `MCPServer/issue-tracker`, and
   `instanceSystem`.
3. The agent calls the MCP tool `validate(kind, content)` with the draft.
   Separately, pipe the same draft to
   `processkit validate ProcessSpecification -f - -o json`.
4. Write the draft to `context/processes/ticket-handling.json` and run
   `processkit validate`.
5. Introduce, one at a time, and validate after each, then restore: an
   unreachable state; no terminal state; a transition naming `Role/tester`;
   a reference to `Skill/missing`; a transition from `closed` to `new`; a
   transition to state `done`; two states with id `triaged`.
6. Call `get` for the process at level 1, then with `section` `triaged`,
   then with `section` `nonexistent`.
7. Run `processkit create ProcessSpecification example-process --yes` and
   validate.
8. Inspect the MCP tool list and the CLI command list, and the repository
   and `.processkit/` after all steps.

Expected results:

- Step 3: both validations report the same outcome and the same
  diagnostics, each diagnostic with `file` `-`; no file is created or
  changed.
- Step 4 validates.
- Step 5 fails, in order, with `content-kinds.process-unreachable-state`,
  `content-kinds.process-no-terminal-state`,
  `ontology.unresolved-reference` (pointer to the role),
  `ontology.unresolved-reference` (pointer to the reference),
  `content-kinds.process-terminal-transition`,
  `content-kinds.process-unknown-state`, and `content-kinds.duplicate-id`.
- Step 6: level 1 lists the states with only `id`, `title`, and
  `terminal`, the transitions with gate `id` and `title` only, and no
  `guidance`; the `triaged` section contains that state in full (with its
  `guidance`, inputs, and references) and its outgoing transition, and no
  other state; `nonexistent` fails with `content-kinds.unknown-section`.
- Step 7 validates: the template has one terminal state and needs no Role.
- Step 8: no tool or command starts, advances, or records a process or
  ticket; no ticket or WorkItem instance exists in the repository or the
  cache.
- The published template and the worked example validate against the
  ProcessSpecification schema.

Covers: PK-PROC-001, PK-PROC-002, PK-PROC-003, PK-PROC-004, PK-PROC-005,
PK-PROC-006, PK-PROC-007, PK-PROD-021, PK-CONT-012, PK-CONT-015,
PK-CONT-022.

## 3. Progressive disclosure and attribution

Preconditions: the Standard `git-branching` from journey 1 with two rules,
each with a `section`, and two `sections`; the MCPServer `issue-tracker`.

Steps:

1. Call MCP `list` for kind `Standard`.
2. Call `get` for `git-branching` at level 1.
3. Call `get` for `git-branching` with `section` set to one section id.
4. Run `processkit get Standard git-branching --section <id> -o json`.
5. Call `get` for `issue-tracker` at level 1.

Expected results:

- Step 1 contains no rule text and no section body.
- Step 2 contains the ordered rules with id, level, and text,
  `disclosure.index` with each section's id and title, and no section
  body.
- Steps 3 and 4 return the level-0 members and `disclosure.section` with
  exactly that one section; no other section body appears.
- Every item in steps 2 to 5 carries `kind`, `metadata.name`,
  `status.source.path`, `status.digest`, `status.provenance`, and
  `status.validation.outcome` `valid`. The version of `git-branching` is
  its `spec.version`; the version of `issue-tracker` is its
  `status.digest`.

Covers: PK-CONT-001, PK-CONT-003, PK-CONT-013, PK-CONT-016, PK-STD-002.

## 4. Invalid content is reported, not served

Preconditions: journeys 1 and 2 completed.

Steps:

1. Add to `git-branching` a `references` entry with `ref`
   `Standard/does-not-exist`; validate; restore.
2. Set the `issue-tracker` transport to `{type: http, url: http://...}`;
   validate; restore.
3. Set the `issue-tracker` transport to `stdio` with `package` set to
   `npx foo && curl x | sh`; validate; restore.
4. Put `Bearer abcdefghijklmnopqrstuvwxyz` into
   `spec.authentication.notes` of `issue-tracker`; validate. Then replace
   it by `corp-secret-0042`, write an operator configuration with
   `redaction.patterns = ["corp-secret-[0-9]+"]`, and validate with
   `--config` naming that file.
5. With the invalid entry from step 4 still in place, call MCP `list` for
   `MCPServer`, `get_context` with no arguments, and `get` for
   `issue-tracker` and `git-branching`.

Expected results:

- Step 1 fails with `ontology.unresolved-reference`; step 2 with
  `content-kinds.transport-not-https`; step 3 with
  `content-kinds.package-not-coordinate`.
- Step 4 fails both times with `content-kinds.secret-in-catalog-entry`,
  pointer `/spec/authentication/notes`, and `evidence.pattern`
  `bearer-token`, then `operator-0`. Neither secret value appears in
  stdout or stderr.
- Step 5: `issue-tracker` appears only with kind, name, namespace, and
  attribution, with validation outcome `invalid`, its diagnostics, and no
  `spec` members; `git-branching` and the other valid items are served.

Covers: PK-STD-003, PK-CAT-002, PK-CAT-003, PK-CAT-005, PK-CONT-010,
PK-CONT-011, PK-CONT-018.

## 5. Decisions justify standards and processes

Preconditions: journeys 1 and 2 completed.

Steps:

1. Run `processkit create DecisionRecord trunk-based --yes`; fill in the
   front matter with status `accepted`, date `2026-11-08`, deciders,
   summary, triggers, context, decision, consequences, and two
   alternatives; add a Markdown body; validate.
2. One at a time, validate after each, then restore: remove `status`; set
   it to `approved`; set `date` to `08.11.2026`.
3. Reference `trunk-based` from `git-branching` (`spec.decisions`) and from
   `ticket-handling` (`spec.decisions`); validate.
4. Call `get` for `git-branching` at level 1, and `get` for `trunk-based`
   at level 1 and with `section` `context`, `alternatives`, and `notes`.
5. Create `trunk-based-v2` with `supersedes: [DecisionRecord/trunk-based]`;
   validate. Set `trunk-based` to `superseded`; validate. Remove the
   `supersedes` entry from `trunk-based-v2`; validate; restore.
6. Run every write command (`init` dry run, `create Standard other`,
   `apply -f` with a Standard document, `format`, `lock`, `migrate` dry
   run) and every read command once; compare the file list of
   `context/decisions/` before and after.

Expected results:

- Steps 1 and 3 validate. Step 2 fails with `content-kinds.missing-field`,
  then `content-kinds.schema-violation` twice.
- Step 4: the served rules of `git-branching` include `spec.decisions`
  with `trunk-based`, resolved in `status.references`. `trunk-based` at
  level 1 has `decision` and `consequences` and no `context`, alternatives,
  or body; each section request returns only that section; `notes` is the
  Markdown body.
- Step 5: the first validation fails with
  `content-kinds.supersession-status`; the second validates; the third
  validates with the warning `content-kinds.supersession-missing` (exit
  code 0).
- Step 6: no file under `context/decisions/` was created or changed.

Covers: PK-DEC-001, PK-DEC-002, PK-DEC-004, PK-DEC-005, PK-DEC-006,
PK-PROD-010, PK-STD-003.

## 6. Always-on rules and applicability

Preconditions: journey 1 completed; the repository declares profiles `cli`
and `service`.

Steps:

1. Set `alwaysOn: true` on `git-branching`; add a second standard
   `api-style` with `applicability.profiles: [service]` and a label
   `area: api`.
2. Connect a harness with `processkit mcp serve --stdio` and no instruction
   or skill files; read the connection briefing.
3. Call `get_context` with `profiles: [cli]`, then with
   `profiles: [service]`; run `processkit get context --profile cli`.
4. Set `applicability.profiles: [documentation]` on `api-style`; validate.
   Then declare the profile `documentation` in the repository; validate.

Expected results:

- Step 2: the briefing contains the rules of `git-branching`.
- Step 3: `api-style` is returned for `service` and not for `cli`, with its
  match basis; the CLI result equals the MCP result for `cli`.
- Step 4: the first validation fails with
  `content-kinds.undeclared-profile`; the second validates, because
  profile names are repository vocabulary.

Covers: PK-STD-005, PK-CONT-004, PK-CONT-021.

## 7. The catalog is information only

Preconditions: journey 1 completed; network access from the test process
is observed (for example a local listener on the catalogued URL host).

Steps:

1. Add MCPServer `company-gateway` with role `gateway`, an `https://` URL,
   and `upstreams: [issue-tracker, wiki]`, where `wiki` has no MCPServer
   entry.
2. Validate, then serve over stdio; call `list` for `MCPServer` and
   `get_context`.
3. Add `upstreams: [wiki]` to `issue-tracker` (role `server`); validate;
   restore.

Expected results:

- Step 2 validates with the warning `content-kinds.upstream-not-catalogued`
  for `wiki` (exit code 0). No connection is made to any catalogued URL and
  no catalogued package is started during validation or serving.
  `company-gateway` and `issue-tracker` are served; `wiki` is not served as
  a catalogued server.
- Step 3 fails with `content-kinds.upstreams-not-allowed`.

Covers: PK-CAT-001, PK-CAT-004, PK-CAT-006.

## 8. Skills are content, never executed

Preconditions: journey 1 completed; an existing skill directory
`fixture-skill` in the Agent Skills format (`SKILL.md` with front matter
`name` and `description`), copied unchanged, with a `skill.json` added
whose `parts` lists `SKILL.md`; it contains `scripts/mark.sh` that would
create a marker file, `references/guide.md`, `tools/run` whose content
starts with `#!`, and the binary file `assets/logo.png`. `skill.json`
declares `agent` with `persona` `Document/company-persona` (a Document from
a declared source), `modelClass` `deep`, and one evaluation case.

Steps:

1. Validate, then call `get` for the skill at level 1.
2. Call `get` with `section` `references/guide.md`, `scripts/mark.sh`,
   `tools/run`, `assets/logo.png`, and `SKILL.md`.

Expected results:

- Step 1 validates without changes to `SKILL.md`. Level 1 has
  `disclosure.body` with the `SKILL.md` body, the `agent` members, and an
  index of the four files with `script` true for `scripts/mark.sh` and
  `tools/run`; it contains no file content.
- Step 2 returns each file alone with `path`, `script`, `encoding`, and
  `content`: `utf-8` for the text files and `base64` for `logo.png`;
  `SKILL.md` fails with `content-kinds.unknown-section`. No marker file
  exists, and no process or network connection was started for the
  scripts or the evaluation case.

Covers: PK-SKILL-002, PK-SKILL-003, PK-SKILL-004, PK-SKILL-014,
PK-SKILL-015, PK-SKILL-016.

## 9. Documents come only from declared sources

Preconditions: an initialized governing repository.

Steps:

1. Declare in `processkit.toml` a `[[document-sources]]` table with
   `pattern = "handbook/*.md"`, `namespace = "root"`,
   `labels = { area = "handbook" }`, and `triggers`; add
   `handbook/onboarding.md` with front matter `summary`, the headings
   `# Onboarding`, `## First day`, and `## First day`, and
   `notes/private.md`. Validate.
2. Call `list` for `Document`, then `get` for `onboarding` with `section`
   `first-day-1`.
3. Remove the `summary` from `onboarding.md`; validate; restore.
4. Add a second source with `pattern = "handbook/**/*.md"`; validate;
   remove it.
5. Add `handbook/archive/onboarding.md` and a source
   `pattern = "handbook/archive/*.md"` with the same namespace, labels,
   `summary`, and `triggers`; validate.

Expected results:

- Step 1 validates. Level 0 of `onboarding` shows title `Onboarding`,
  `status.source.path` `handbook/onboarding.md`, the labels, and the
  heading index with ids `onboarding`, `first-day`, and `first-day-1`.
- Step 2 returns only the second `First day` section, from its heading to
  the end of the file.
- Step 3 fails with `content-kinds.document-missing-field`; step 4 with
  `content-kinds.document-source-overlap`; step 5 with
  `content-kinds.document-name-collision` for both files.
- `notes/private.md` never appears in any result.

Covers: PK-DOC-001, PK-DOC-002, PK-DOC-003, PK-DOC-004, PK-DOC-005.

## 10. Gates and linear processes

Preconditions: journey 2 completed; a Role `release-manager` exists.

Steps:

1. Add the ProcessSpecification `release-checklist` with `shape`
   `linear`, states `draft`, `review`, `published` (terminal) in this
   order, transitions `draft` to `review` and `review` to `published`; in
   `draft` a produced artifact `notes` and an input of class `instruction`
   with `ref` `Standard/git-branching`; in `review` an input of class
   `working` with `artifact` `notes`; on `review` to `published` a Gate
   with kind `approval`, a validator description, authority
   `[Role/release-manager]`, evidence naming artifact `notes`, and a
   waiver with authority `[Role/release-manager]`. Validate.
2. One at a time, validate after each, then restore: add a transition
   `draft` to `published`; set the `review` input's `artifact` to
   `missing`; set the Gate authority to `[Role/missing]`; remove the Gate's
   `validator`.
3. Call `get` for `release-checklist` with `section` `review`.
4. Inspect every CLI command and MCP tool for an argument that records a
   gate outcome or waiver; inspect the repository and `.processkit/`.

Expected results:

- Step 1 validates.
- Step 2 fails, in order, with `content-kinds.process-not-linear`,
  `content-kinds.process-unknown-artifact`,
  `ontology.unresolved-reference`, and `content-kinds.missing-field`.
- Step 3 returns the `review` state with its outgoing transition and the
  full Gate (kind, validator, authority, blocking `true` by default,
  evidence, waiver).
- Step 4: no command or tool accepts or records a gate outcome or waiver;
  no such file exists.

Covers: PK-PROC-009, PK-PROC-010, PK-PROC-011, PK-PROC-012.

## 11. Overriding inherited items

Preconditions: an upstream governing repository `company`, locked and
fetched as `inheritance@v1` defines, with the Standard `git-branching`
(version `1.0.0`; rules `GB-001` MUST and `GB-002` MUST with
`final: true`) and the ProcessSpecification `ticket-handling` from
journey 2; a downstream project repository that inherits from `company`.

Steps:

1. In the downstream repository, add `standards/git-branching.json` whose
   `spec` contains only `overrides` with `upstream` `company`, `name`
   `git-branching`, `version` `1.0.0`, a reason, `effect` `amend`,
   `ruleLevels: [{rule: GB-001, level: SHOULD}]`, and one `addRules` rule
   `LOCAL-001`. Validate, then call `get` at level 1.
2. One at a time, validate after each, then restore: set `ruleLevels` rule
   to `GB-009`; give the added rule the id `GB-001`; add `title` to the
   amending `spec`; remove both `addRules` and `ruleLevels`.
3. Replace the file by a complete Standard with `effect` `replace`;
   validate.
4. Add `processes/ticket-handling.json`, a complete ProcessSpecification
   with `overrides` `effect` `replace`; validate. Change its `effect` to
   `amend`; validate.

Expected results:

- Step 1 validates; the served `git-branching` has the upstream rules with
  `GB-001` at level `SHOULD`, followed by `LOCAL-001`, and every other
  member from the upstream item.
- Step 2 fails, in order, with `content-kinds.override-unknown-rule`,
  `content-kinds.override-duplicate-rule`,
  `content-kinds.schema-violation`, and `content-kinds.schema-violation`.
- Step 3 validates, and the served item is the local Standard.
- Step 4 validates with `replace` and fails with
  `content-kinds.schema-violation` with `amend`.

Covers: PK-STD-006, PK-STD-007, PK-CONT-023.

## Verified by component tests only

- **PK-STD-004:** a structural property of the ontology registry (Standard
  is a composition over Policy), checked by registry tests, not by a user
  journey.
- **PK-DEC-003:** "rewritten in meaning" cannot be detected mechanically;
  component tests check that a superseding DecisionRecord validates and the
  superseded record keeps its content. The rule itself is enforced by
  review.
