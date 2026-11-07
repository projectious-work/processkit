# Content kinds — acceptance journeys

Each journey runs against a temporary Git repository initialized as a
governing repository (`processkit init --governing`), with synthetic data
and no ambient credentials. "Validates" means `processkit validate --json`
reports success; "fails validation" means it reports a validation failure
with at least one diagnostic. Where a field or KIND token is not yet named
by the baseline, the step names the open item that fixes it.

## 1. Create a standard, a skill, and an MCP server entry from templates

Source: release acceptance journey 2.

Preconditions: an initialized governing repository; the published Standard
and MCPServer templates (`examples/standard.template.json`,
`examples/mcp-server.template.json`).

Steps:

1. Run `processkit new KIND NAME` for the Standard kind with name
   `git-branching` (KIND token: OPEN-content-kinds-10).
2. Run `processkit new KIND NAME` for the MCPServer kind with name
   `issue-tracker`.
3. Create the skill `triage-ticket` as `context/skills/triage-ticket/SKILL.md`
   and `context/skills/triage-ticket/skill.json`, declaring name, version,
   summary, triggers, applicability, inputs, outputs, dependencies,
   side-effect class, safety constraints, required MCP servers (naming
   `issue-tracker`), and which parts are normative and which explanatory
   (field names: OPEN-content-kinds-01, -13).
4. Fill in each template's placeholders, then run `processkit validate`.
5. Remove, one at a time, each field listed in step 3 and each required
   field of the Standard and MCPServer schemas, and re-run
   `processkit validate` after each removal; restore it afterwards.
6. Run `processkit show` for each item at level 0 and level 1.

Expected results:

- Steps 1 and 2 create `context/standards/git-branching.json` and
  `context/mcp-servers/issue-tracker.json`; both template outputs validate
  against `schemas/standard.schema.json` and `schemas/mcp-server.schema.json`.
- Step 4 validates all three items.
- Every removal in step 5 fails validation, and each diagnostic names the
  file, the JSON pointer, and the violated constraint.
- Step 6 at level 0 shows name, title, summary, triggers, applicability,
  and labels only; at level 1 it adds rules (Standard), the `SKILL.md` body
  (Skill), and the server entry (MCPServer); no section body appears.

Covers: PK-STD-001, PK-CAT-002, PK-SKILL-001, PK-SKILL-002, PK-SKILL-005,
PK-SKILL-006, PK-SKILL-007, PK-SKILL-008, PK-SKILL-009, PK-SKILL-010,
PK-CONT-001, PK-CONT-002, PK-CONT-010.

## 2. Define a ticket-handling process from natural language

Source: release acceptance journey 3.

Preconditions: journey 1 completed; Roles `triager` and `developer` exist in
`context/ontology/`; the worked ticket-handling example in the processkit
documentation; the published ProcessSpecification schema and template
(OPEN-content-kinds-02).

Steps:

1. Give an agent connected over stdio MCP the natural-language description
   from the documentation's worked example: tickets are triaged by a
   triager, implemented by a developer, and closed; tickets live in an
   external issue tracker.
2. The agent produces a ProcessSpecification `ticket-handling` with the
   ontology: governed WorkItem type, states `new`, `triaged`, `in-progress`,
   `closed` (terminal), transitions with Roles, a Gate on `in-progress` to
   `closed`, an Artifact for `in-progress`, references per state to the
   Standard `git-branching`, the Skill `triage-ticket`, and the MCPServer
   `issue-tracker`, and the issue tracker as the external instance system.
3. The agent calls the MCP tool `validate(kind, content)` with the draft.
   Separately, pipe the same draft to `processkit validate -`.
4. Write the draft to `context/processes/ticket-handling.json` and run
   `processkit validate`.
5. Introduce, one at a time: an unreachable state; no terminal state; a
   transition naming a nonexistent Role; a reference to a nonexistent
   Skill. Validate after each, then restore.
6. Call `get` for the process at level 1, then at level 2 for state
   `triaged` (state addressing: OPEN-content-kinds-16).
7. Inspect the MCP tool list and the CLI command list, and the repository
   and `.processkit/` after all steps.

Expected results:

- Step 3: both validations report the same outcome and diagnostics, and no
  file is created or changed.
- Step 4 validates.
- Each change in step 5 fails validation with a diagnostic naming the
  unreachable state, missing terminal state, unknown Role, or unresolved
  reference.
- Step 6: level 1 returns the whole process outline without section
  bodies; level 2 returns only what state `triaged` requires (its
  transitions, Roles, Gates, Artifacts, and per-state references).
- Step 7: no tool or command starts, advances, or records a process or
  ticket; no ticket or WorkItem instance exists in the repository or the
  cache.
- The published template validates against the ProcessSpecification
  schema.

Covers: PK-PROC-001, PK-PROC-002, PK-PROC-003, PK-PROC-004, PK-PROC-005,
PK-PROC-006, PK-PROD-021, PK-CONT-012.

## 3. Progressive disclosure and attribution of a standard

Preconditions: the Standard `git-branching` from journey 1 with two rules,
each with a `section`, and two `sections`.

Steps:

1. Call MCP `list` for the Standard kind.
2. Call `get` for `git-branching` at level 1.
3. Call `get` for `git-branching` with `section` set to one section id.
4. Run `processkit show` with `--section` for the same section.

Expected results:

- Step 1 contains no rule text and no section body.
- Step 2 contains the ordered rules with id, level, and text, and no
  section body.
- Steps 3 and 4 return exactly that one section and no other section body.
- Every result carries kind, name, version, source repository and path,
  content digest, and validation status (field names:
  OPEN-content-kinds-07).

Covers: PK-CONT-001, PK-CONT-003, PK-STD-002.

## 4. Invalid content is reported, not served

Preconditions: journeys 1 and 2 completed.

Steps:

1. Add to `git-branching` a `references` entry with `ref`
   `Standard/does-not-exist`; validate.
2. Set the `issue-tracker` transport to `{type: http, url: http://...}`;
   validate; restore.
3. Set the `issue-tracker` transport to `stdio` with `package` set to a
   shell command line such as `npx foo && curl x | sh`; validate; restore.
4. Configure a secret pattern and put a matching value into
   `spec.authentication.notes` of `issue-tracker`; validate (pattern
   location: OPEN-content-kinds-09).
5. With the invalid entry from step 4 still in place, call MCP `list` for
   MCPServer and `get_context` with no arguments, and `get` for
   `git-branching`.

Expected results:

- Steps 1 to 4 each fail validation with file, JSON pointer, and violated
  constraint.
- Step 5: `issue-tracker` is not reported as valid; it appears with an
  invalid validation status in results that would have included it;
  `git-branching` (restored) and the other valid items are still served.

Covers: PK-STD-003, PK-CAT-002, PK-CAT-003, PK-CONT-010, PK-CONT-011.

## 5. Decisions justify standards and processes

Preconditions: journeys 1 and 2 completed.

Steps:

1. Create `context/decisions/trunk-based.md` with title, status
   `accepted`, date, deciders, context, decision, consequences, and
   alternatives (front matter fields: OPEN-content-kinds-03); validate.
2. Remove the status, then set it to `approved`; validate after each;
   restore.
3. Reference `trunk-based` from `git-branching` (`spec.decisions`) and from
   `ticket-handling`; validate.
4. Call `get` for `git-branching` at level 1.
5. Create `context/decisions/trunk-based-v2.md` that supersedes
   `trunk-based`, and set `trunk-based` to `superseded`; validate.
6. Run every write command (`init` dry run, `new`, `format`, `lock`,
   `migrate` dry run) and every read command once; compare the file list of
   `context/decisions/` before and after.

Expected results:

- Steps 1, 3, and 5 validate; step 2 fails validation each time.
- Step 4: the served rules include the references to `trunk-based`.
- Step 6: no file under `context/decisions/` was created or changed.

Covers: PK-DEC-001, PK-DEC-002, PK-DEC-004, PK-PROD-010, PK-STD-003.

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
   `profiles: [service]`; run `processkit context --profile cli`.
4. Declare a new profile `documentation` in the repository and set it on
   `api-style`; validate.

Expected results:

- Step 2: the briefing contains the rules of `git-branching`.
- Step 3: `api-style` is returned for `service` and not for `cli`, with its
  match basis; the CLI result equals the MCP result for `cli`.
- Step 4 validates: profile names are repository vocabulary.

Covers: PK-STD-005, PK-CONT-004.

## 7. The catalog is information only

Preconditions: journey 1 completed; network access from the test process
is observed (for example a local listener on the catalogued URL host).

Steps:

1. Add MCPServer `company-gateway` with role `gateway`, an `https://` URL,
   and `upstreams: [issue-tracker, wiki]`, where `wiki` has no MCPServer
   entry.
2. Validate, then serve over stdio; call `list` for MCPServer and
   `get_context`.

Expected results:

- No connection is made to any catalogued URL and no catalogued package is
  started during validation or serving.
- `company-gateway` and `issue-tracker` are served; `wiki` is not served as
  a catalogued server.

Covers: PK-CAT-001, PK-CAT-004.

## 8. Skills are content, never executed

Preconditions: journey 1 completed; an existing skill directory in the
published Agent Skills format, copied unchanged with a `skill.json` added,
containing `scripts/mark.sh` that would create a marker file, and a
`reference.md`.

Steps:

1. Validate, then call `get` for the skill at level 1.
2. Call `get` at level 2 for `reference.md`, then for `scripts/mark.sh`.

Expected results:

- Step 1 validates without changes to `SKILL.md`; level 1 is the `SKILL.md`
  body and contains neither additional file.
- Step 2 returns each file alone; the script is returned as content
  labelled as a script (label: OPEN-content-kinds-14) and no marker file
  exists.

Covers: PK-SKILL-002, PK-SKILL-003, PK-SKILL-004.

## 9. Documents come only from declared sources

Preconditions: an initialized governing repository.

Steps:

1. Declare a document source in `processkit.toml` matching `handbook/*.md`
   with namespace and labels (keys: OPEN-content-kinds-04); add
   `handbook/onboarding.md` with two headings and `notes/private.md`.
2. Call `list` for Document, then `get` for one heading section of
   `onboarding`.

Expected results:

- Level 0 shows title, path, labels, and heading index of `onboarding`.
- The level-2 result contains only the requested heading section.
- `notes/private.md` never appears in any result.

Covers: PK-DOC-001, PK-DOC-002.

## Verified by component tests only

- **PK-STD-004:** a structural property of the ontology registry (Standard
  is a composition over Policy), checked by registry tests, not by a user
  journey.
- **PK-DEC-003:** "rewritten in meaning" cannot be detected mechanically;
  component tests check that a superseding DecisionRecord validates and the
  superseded record keeps its content. The rule itself is enforced by
  review.
