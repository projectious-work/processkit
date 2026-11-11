# Inheritance across repositories — acceptance journeys

Journey 1 is release acceptance journey 4 of the #197 baseline. The others
exercise failure handling, final items, competing upstreams, upstream
changes, offline operation, inherited access, the lock file, override
effects, transitive upstreams, and configuration checks. Every journey uses
synthetic data, temporary local Git repositories as upstream sources (an
absolute local path source stands in for a remote), and no ambient
credentials or user configuration. Commands are those of `cli@v1`; codes
are those of `interfaces.yaml` (`errors`). "Fetch, then lock" is the order
of owner decision #213 finding 3: `processkit lock` reads only the local
cache. Unless a step says otherwise, writing commands run with `--yes`.

Common fixture, used unless a journey says otherwise:

- `company` — a governing repository with Standard `secure-coding`
  (version `1.0.0`, rules `SEC-001` level `MUST` and `SEC-002` level `MUST`
  with `final: true`) and Standard `code-review`, tagged `v1.0.0`.
- `platform` — a governing repository whose `processkit.toml` declares
  `[[upstream]] name = "company"` at ref `v1.0.0`, which is fetched, locked,
  and committed, and which adds Standard `api-design` (version `2.0.0`,
  rule `API-001` level `MUST`, rule `API-002` level `SHOULD`) and Standard
  `release-notes`, on branch `main`.

## 1. Project inheriting from two governing levels (release journey 4)

Preconditions: processkit installed; the common fixture; an empty Git
repository `payments-api` with one commit.

Steps:

1. Run `processkit init --project` in `payments-api` and declare in
   `processkit.toml` one upstream: `[[upstream]] name = "platform"`, with
   `source` the `platform` repository and `ref = "main"`.
2. Run `processkit lock -o json` before fetching.
3. Run `processkit fetch -o json`; inspect `git status` and `.processkit/`.
4. Run `processkit lock -o json`; inspect `processkit.lock` and
   `git status`.
5. Delete `.processkit/` and run `processkit get Standard`. Then run
   `processkit fetch` again.
6. Run `processkit get Standard` and `processkit get Standard api-design`.
7. Add a local Standard `api-design` whose `spec` contains only
   `overrides = {upstream: "platform", name: "api-design",
   version: "2.0.0", reason: "public API must version endpoints",
   effect: "amend", ruleLevels: [{rule: "API-002", level: "MUST"}]}`,
   which raises rule `API-002` from `SHOULD` to `MUST`. Run
   `processkit validate`.
8. Run `processkit describe Standard api-design -o json` and
   `processkit describe Standard secure-coding -o json`.
9. Repeat steps 6 and 8 and compare the output byte for byte.
10. Run `git log --all --oneline`, `git status`, and list remotes of
    `payments-api` before and after steps 2 to 9.

Expected results:

- 2: the command fails with `cli.upstream-not-fetched` (exit code 3),
  naming `platform` and the fix `processkit fetch`; no lock is written; no
  network access occurs.
- 3: `data.refs` has one entry for `platform` with the commit of `main`;
  `data.commits` lists that commit and the `company` commit named by
  `platform`'s lock, each with `result` `fetched`; only the local cache
  changed; no repository file changed.
- 4: `processkit.lock` exists at the root, is valid against
  `schemas/lock.schema.json`, and has the entries `platform` and
  `platform/company`, each with a full commit and a content digest; the
  file equals its own re-serialization by `repository-storage@v1`
  PK-STORE-049; `data.added` lists all four Standards; it is an
  uncommitted file change and nothing was committed or staged.
- 5: `get` fails as an environment failure (`cli.upstream-not-fetched`)
  naming the unfetched upstream and the fix; the second fetch reports the
  locked commits with `result` `fetched`.
- 6: `secure-coding`, `code-review`, `api-design`, and `release-notes` are
  listed as inherited items carrying their upstream identity.
- 7: validation succeeds.
- 8: for `api-design`, `status.provenance.origin` has `upstream`
  `platform`, the `platform` source, the locked commit, and the path, and
  `status.provenance.overrides` has one entry with `declaredAt.upstream`
  `null`, upstream `platform`, name `api-design`, version `2.0.0`, the
  reason, effect `amend`, and `stale` `false`; the served item has
  version `2.0.0` and rule `API-002` with level `MUST`. For
  `secure-coding`, `origin.upstream` is `platform/company` with its locked
  commit and path, and `overrides` is empty.
- 9: output is byte-identical.
- 10: no commit, branch, push, remote, or ref was created by processkit;
  network access happened only during `fetch`.

Covers: PK-PROD-009, PK-PROD-026, PK-INH-001, PK-INH-002, PK-INH-003,
PK-INH-010, PK-INH-011, PK-INH-012, PK-INH-015, PK-INH-021, PK-INH-036,
PK-INH-039, PK-INH-040, PK-INH-046, PK-INH-050, PK-INH-055, PK-INH-057

## 2. Local item that collides without an override

Preconditions: `payments-api` from journey 1 after step 6.

Steps:

1. Add a local Standard named `code-review` with no `spec.overrides`. Run
   `processkit validate -o json`.
2. Add `spec.overrides` without `reason`. Run `processkit validate -o json`.
3. Complete the override with `upstream`, `name`, `version`, `reason`,
   and `effect: "replace"`. Run `processkit validate`.
4. Change `spec.overrides.name` to `review-policy`. Run
   `processkit validate -o json`.
5. Restore the name and change `spec.overrides.upstream` to `company`. Run
   `processkit validate -o json`.

Expected results:

- 1: validation fails (exit code 1) with `inheritance.conflict` for
  `Standard/code-review`.
- 2: validation fails with a schema violation of `content-kinds@v1`
  `standard.schema.json` at `/spec/overrides` naming `reason`.
- 3: validation succeeds.
- 4: validation fails with `inheritance.override-name-mismatch`.
- 5: validation fails with `inheritance.override-target-not-found`
  (`company` is not a declared upstream of `payments-api`).

Covers: PK-INH-011, PK-INH-012, PK-INH-050, PK-INH-054

## 3. Final items and final rules

Preconditions: `payments-api` from journey 1 after step 6; in `company`,
Standard `code-review` is changed to `final: true`, tagged `v1.1.0`; in
`platform` the ref is changed to `v1.1.0`, then `processkit fetch` and
`processkit lock` run and the change is committed on `main`; in
`payments-api`, `processkit fetch` and `processkit lock --update` run.

Steps:

1. Add a local `replace` override of `secure-coding` that changes rule
   `SEC-002` (marked `final`) from `MUST` to `SHOULD`. Run
   `processkit validate -o json`.
2. Change the override so that it keeps `SEC-002` and removes the member
   `final` from it. Run `processkit validate -o json`.
3. Change the override so that it keeps `SEC-002` as upstream and changes
   only rule `SEC-001` (not final). Run `processkit validate`.
4. Replace it by an `amend` override with
   `ruleLevels: [{rule: "SEC-002", level: "SHOULD"}]`. Run
   `processkit validate -o json`.
5. Add a local `replace` override of `code-review` (marked `final`). Run
   `processkit validate -o json`.

Expected results:

- 1: validation fails with `inheritance.override-final-rule`, evidence rule
  `SEC-002`.
- 2: validation fails with `inheritance.override-final-rule`: an absent
  `final` equals `false`, so the rule is changed.
- 3: validation succeeds.
- 4: validation fails with `inheritance.override-final-rule`, evidence rule
  `SEC-002`.
- 5: validation fails with `inheritance.override-final-item` naming
  `code-review`.

Covers: PK-INH-013, PK-INH-051, PK-INH-052

## 4. Two upstreams provide the same item

Preconditions: two governing repositories `team-a` and `team-b`, each
providing a different Standard `logging`; a project repository declaring
both as upstreams, fetched and locked.

Steps:

1. Run `processkit validate -o json`.
2. Add `[[winner]] item = "Standard/logging"`, `upstream = "team-b"` to
   `processkit.toml`. Run `processkit validate` and
   `processkit describe Standard logging -o json`.
3. Swap the order of the two `[[upstream]]` tables, run `processkit lock`,
   and repeat step 2.
4. Change the winner's `upstream` to `team-c`. Run
   `processkit validate -o json`.
5. Remove Standard `logging` from `team-a`, commit, run `processkit fetch`,
   restore the winner to `team-b`, and run `processkit lock --update team-a`
   and `processkit validate -o json`.

Expected results:

- 1: validation fails with `inheritance.winner-missing` for
  `Standard/logging`, evidence listing `team-a` and `team-b`; neither is
  served silently.
- 2: validation succeeds; `status.provenance.origin.upstream` of the served
  `logging` is `team-b`.
- 3: `lock` has an empty plan and writes nothing; the served item and its
  provenance are unchanged.
- 4: validation fails with `inheritance.winner-invalid`.
- 5: `lock --update` reports `Standard/logging` in no list (it is still
  provided by `team-b`); validation succeeds and reports
  `inheritance.winner-unused` as a warning (exit code 0).

Covers: PK-INH-014, PK-INH-010, PK-INH-044, PK-INH-049

## 5. Upstream changes, change summary, and stale overrides

Preconditions: `payments-api` from journey 1 after step 7, with the lock
committed.

Steps:

1. In `platform` `main`, change `api-design` to version `2.1.0`, add
   Standard `observability`, remove Standard `release-notes`, and add
   Standard `secrets`; `payments-api` already has a local Standard
   `secrets` without an override (which validated before, as no upstream
   provided `secrets`).
2. In `payments-api`, run `processkit lock --update platform -o json`
   before fetching.
3. Run `processkit fetch`, then
   `processkit lock --update platform --dry-run -o json`.
4. Run `processkit lock --update platform` interactively in a terminal and
   answer `y`.
5. Run `processkit validate -o json`.
6. Run `git diff --stat`.
7. Run `processkit lock --update unknown`.

Expected results:

- 2: the run reports an empty change summary; the newest `main` commit is
  not in the local cache, so nothing changes (the latest fetch still names
  the old commit).
- 3: `data.added` is `["Standard/observability"]`, `data.changed` is
  `["Standard/api-design"]`, `data.removed` is
  `["Standard/release-notes"]`, `data.newlyConflicting` is
  `["Standard/secrets"]`, and `data.upstreams` has entry `platform` with
  `previousCommit` and the new `commit`; `processkit.lock` is
  byte-identical.
- 4: the same summary is printed with the plan before the prompt; the lock
  now names the new commit and digest.
- 5: the override of `api-design` naming version `2.0.0` is reported as
  `inheritance.override-stale` (evidence `2.0.0` and `2.1.0`); `secrets` is
  reported as `inheritance.conflict`.
- 6: the only repository change is `processkit.lock`, an ordinary
  uncommitted file change for review.
- 7: the command fails with `inheritance.unknown-upstream` (exit code 2);
  the lock is unchanged.

Covers: PK-INH-020, PK-INH-021, PK-INH-016, PK-INH-002, PK-INH-043,
PK-INH-053, PK-INH-057

## 6. Missing, unreachable, and tampered upstreams

Preconditions: `payments-api` from journey 1 after step 6 with the lock
committed.

Steps:

1. Change the `ref` of `platform` to a ref that does not exist. Run
   `processkit fetch -o json`, then `processkit lock -o json`.
2. Restore the ref; change `source` to a path that does not exist. Run
   `processkit fetch -o json` and `processkit lock -o json`.
3. Restore the source. Replace the `digest` of entry `platform` in
   `processkit.lock` with another valid digest, commit it, delete
   `.processkit/`, and run `processkit fetch -o json` and
   `processkit get Standard`.
4. Restore the lock and run `processkit fetch`. Compute the content digest
   of the locked `platform` commit independently from `git ls-tree -r` and
   the blob bytes, by the manifest of `interfaces.yaml`
   (`content_digest`).
5. After each step, inspect `processkit.lock` and the served items.

Expected results:

- 1: `fetch` fails with `inheritance.upstream-missing` naming `platform`
  and the ref (exit code 3); the locked commits are still `present`;
  `lock` fails with `cli.upstream-not-fetched` naming `platform`.
- 2: `fetch` fails with `inheritance.upstream-unreachable` naming
  `platform`; `lock` fails with `cli.upstream-not-fetched`.
- 3: `fetch` fails with `inheritance.digest-mismatch` naming `platform`
  with the expected and actual digests, and does not keep the commit;
  `get` fails with `cli.upstream-not-fetched`.
- 4: `fetch` succeeds, and the computed digest equals the digest of
  entry `platform` in `processkit.lock`.
- 5: the lock is unchanged after every failure, and no other revision of
  `platform` is ever served in place of the locked one.

Covers: PK-INH-004, PK-INH-002, PK-INH-035, PK-INH-037, PK-INH-038,
PK-INH-039

## 7. Offline serving and validation

Preconditions: `payments-api` from journey 1 after step 7; network access
disabled for the processkit process (or Git sources made unreachable).

Steps:

1. Run `processkit validate`, `processkit get Standard`,
   `processkit describe Standard api-design`, and `processkit lock`.
2. Start `processkit mcp serve --stdio`, connect, and call `get_context`,
   `list`, and `explain`.
3. Meanwhile, push a new commit to `platform` `main` (with the network
   restored only for that push).
4. Repeat step 2; compare `processkit.lock` and `git status` with their
   state before step 1.

Expected results:

- 1, 2: all succeed with no network access attempted; `lock` has an empty
  plan.
- 4: served results are unchanged and still name the locked commit;
  `processkit.lock` is byte-identical; no fetch and no lock update occurred
  as a side effect of serving.

Covers: PK-INH-003, PK-INH-021, PK-INH-002, PK-PROD-026

## 8. Inherited access rules and restricted items

Preconditions: a governing repository `company` whose Role and Binding grant
principal `carol` read access to all items, whose Standard
`incident-runbook` is listed in `[downstream] restricted`, and whose Role
`security-team` (the only rule that allows reading `incident-runbook`) is
granted upstream to `alice` but not to `bob`; a downstream governing
repository `platform` that inherits `company` (fetched and locked) and is
served by the shared server with an authenticator for `alice`, `bob`, and
`carol`; downstream rules grant `alice` and `bob`, but not `carol`, read
access to all items.

Steps:

1. Without importing `company`'s access rules, call `list`, `get`, and
   `get_context` as `alice`, `bob`, and `carol`, including a direct `get`
   of `incident-runbook`.
2. Set the operator key `inheritance.import-access-rules = ["company"]`
   and restart the server. Repeat the calls as `alice` and `bob`.
3. Keep the import and remove `alice`'s downstream grant. Repeat the calls
   as `alice`.
4. Add `"unknown"` to `inheritance.import-access-rules` and restart.
5. Put `[inheritance] import-access-rules = ["company"]` in `platform`'s
   `processkit.toml` and run `processkit validate -o json`.
6. In `platform`, run `processkit get Standard incident-runbook -o json`
   and get it through `processkit mcp serve --stdio`.
7. In `company`, add `"Standard/missing"` to `[downstream] restricted` and
   run `processkit validate -o json` there.

Expected results:

- 1: `carol` receives no item: the upstream Binding grants nothing
  downstream. `incident-runbook` is absent for `alice` and `bob` from every
  result, and a direct `get` is indistinguishable from a missing item.
- 2: `alice` receives `incident-runbook`; `bob` does not.
- 3: `alice` no longer receives `incident-runbook`: both the upstream and
  the downstream rules must allow it.
- 4: the server starts and reports `inheritance.import-unknown-upstream`
  as a warning; access decisions are unchanged.
- 5: validation fails with `cli.config-unknown-key`: project configuration
  cannot import access rules.
- 6: both return `incident-runbook` with `status.provenance.restricted`
  `true` and `restrictedBy` `company`.
- 7: `inheritance.restricted-unknown-item` is reported as a warning; exit
  code 0.

Covers: PK-INH-030, PK-INH-031, PK-INH-059, PK-INH-060, PK-INH-061,
PK-INH-062

## 9. The lock file and plain lock

Preconditions: `payments-api` from journey 1 after step 6, with the lock
committed; `platform` `main` has a newer commit than the locked one.

Steps:

1. Run `processkit fetch`, then `processkit lock -o json`.
2. Declare a second upstream `[[upstream]] name = "tools"` (a governing
   repository without upstreams, ref `v1`) and run
   `processkit validate -o json` and `processkit get Standard -o json`.
3. Run `processkit fetch` and `processkit lock -o json`.
4. Edit `processkit.lock` so that it misses `apiVersion`, and run
   `processkit validate -o json` and `processkit get Standard -o json`.
5. Restore the lock of step 3 without committing it; change the `ref` of
   `tools` and run `processkit fetch` and `processkit lock`.
6. Remove the `tools` declaration, commit the lock, and run
   `processkit lock -o json`.

Expected results:

- 1: the plan is empty and the lock is byte-identical: plain `lock` keeps
  entries whose `source` and `ref` are unchanged.
- 2: `validate` fails with `inheritance.lock-outdated`; `get` succeeds,
  reports `inheritance.lock-outdated` as a warning, and serves the items
  of the existing lock.
- 3: the lock gains the entry `tools` with the fetched commit; `platform`
  and `platform/company` are unchanged; entries are sorted by name.
- 4: both fail with `inheritance.lock-invalid`; `get` serves no inherited
  item.
- 5: `lock` is refused with `storage.target-not-committed` (exit code 4)
  and writes nothing.
- 6: the entry `tools` is removed, `data.upstreams` lists `tools` with a
  `null` commit, and `data.removed` lists its items.

Covers: PK-INH-040, PK-INH-042, PK-INH-044, PK-INH-045, PK-INH-057

## 10. Override effects

Preconditions: `payments-api` from journey 1 after step 6.

Steps:

1. Add a local `api-design` `amend` override with
   `addRules: [{id: "API-003", level: "MAY", text: "..."}]`. Run
   `processkit validate` and `processkit get Standard api-design -o json`.
2. Add `ruleLevels: [{rule: "API-001", level: "SHOULD"}]` to the same
   override. Run `processkit get Standard api-design -o json`.
3. Change the `ruleLevels` entry to rule `API-009`. Run
   `processkit validate -o json`.
4. Restore it and change the added rule's id to `API-001`. Run
   `processkit validate -o json`.
5. Replace the override by a complete `replace` override whose `summary`
   and rule texts differ from the upstream item. Run `processkit validate`
   and `processkit describe Standard api-design -o json`.

Expected results:

- 1: validation succeeds; the served item has the upstream title,
  summary, and version `2.0.0` and the rules `API-001`, `API-002`,
  `API-003` in this order.
- 2: rule `API-001` is served with level `SHOULD`; every other member is
  unchanged.
- 3: validation fails with `content-kinds.override-unknown-rule`.
- 4: validation fails with `content-kinds.override-duplicate-rule`.
- 5: validation succeeds; the served item is the local item; the
  override's `effect` in provenance is `replace`, and `origin` still names
  `platform`.

Covers: PK-INH-012, PK-INH-051, PK-INH-055

## 11. Transitive upstreams and diamonds

Preconditions: the common fixture; a governing repository `security` that
declares `company` at `v1.0.0`, fetched, locked, and committed; a project
repository declaring `platform` and `security`.

Steps:

1. Run `processkit fetch`, `processkit lock`, and `processkit validate`.
2. In `company`, tag `v1.1.0` with a changed `code-review`; move
   `security` to `v1.1.0` (fetch, lock, commit). In the project, run
   `processkit fetch`, `processkit lock --update security`, and
   `processkit validate -o json`.
3. Add `[[winner]] item = "Standard/code-review"`, `upstream = "security"`
   and run `processkit validate` and
   `processkit describe Standard code-review -o json`.
4. In a new governing repository `loose`, declare an upstream but commit
   no lock. Declare `loose` in the project and run `processkit fetch -o json`.
5. In `platform`, add a local Standard `code-review` without override and
   commit it. In the project, run `processkit fetch`,
   `processkit lock --update platform`, and `processkit validate -o json`.

Expected results:

- 1: the lock has `platform`, `platform/company`, `security`, and
  `security/company`, both `company` entries at one commit; validation
  succeeds: identical candidates are one item.
- 2: validation fails with `inheritance.winner-missing` for
  `Standard/code-review` and `Standard/secure-coding`: the two paths reach
  `company` at two commits.
- 3: `code-review` validates and `origin.upstream` is `security/company`;
  `secure-coding` still fails with `inheritance.winner-missing`.
- 4: `fetch` reports `inheritance.upstream-lock-invalid` for `loose` with
  reason `absent`.
- 5: validation fails with `inheritance.upstream-invalid` for `platform`,
  evidence code `inheritance.conflict`.

Covers: PK-INH-041, PK-INH-046, PK-INH-047, PK-INH-048, PK-INH-010,
PK-INH-014

## 12. Upstream declarations and credentials

Preconditions: an initialized project repository; a process environment
without a Git credential helper, SSH agent, or home directory
configuration.

Steps:

1. Declare two `[[upstream]]` tables with the same `name`. Run
   `processkit validate -o json`.
2. Declare one upstream with `source = "http://git.example.com/x.git"`.
   Run `processkit validate -o json`.
3. Declare one upstream with
   `source = "https://user:s3cret-token@git.example.com/x.git"`. Run
   `processkit validate -o json` and `processkit config view -o json`, and
   collect every log line.
4. Declare one upstream with an absolute local path source of a public
   repository and run `processkit fetch`, recording the argument vectors of
   every child process.

Expected results:

- 1, 2: validation fails with `cli.config-invalid-value`.
- 3: validation fails with `cli.config-forbidden-key`; the text
  `s3cret-token` appears in no output, diagnostic, or log line.
- 4: `fetch` succeeds without any credential configuration; no argument
  vector contains a credential value.

Covers: PK-INH-001, PK-INH-032, PK-INH-033, PK-INH-034

## Verified by component tests only

- PK-INH-035 (ref resolution order): the tag-before-branch order and full
  commit IDs need a source with a tag and a branch of the same name;
  component tests drive the Git port with such a repository. Journey 6
  covers a missing ref.
- PK-INH-054 (code, category, and scope of every condition): checked by a
  component test over the diagnostic registry against `interfaces.yaml`
  (`errors`); the journeys exercise most codes.
- PK-INH-056 (PROV mapping): documentation only in v1; checked by review of
  the published mapping, as no PROV serialization is emitted.
- PK-INH-058 (previous lock unavailable): needs a lock whose commit is
  missing from the cache while the new commits are present; component tests
  arrange the cache through the cache port.

Determinism of resolution (PK-INH-010) is additionally covered by
resolution tests across many inputs (PK-TEST-003), but journeys 1 and 4
observe it directly.
