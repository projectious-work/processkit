# Inheritance across repositories — acceptance journeys

Journey 1 is release acceptance journey 4 of the #197 baseline. The others
exercise failure handling, final items, competing upstreams, upstream
changes, offline operation, and inherited access. Every journey uses
synthetic data, temporary local Git repositories as upstream sources (a
`file://` or local path source stands in for a remote), and no ambient
credentials or user configuration. Commands are those of `cli@v1`; where an
identifier is still open (see `interfaces.yaml`), a journey states the
observable effect, not the identifier.

Common fixture, used unless a journey says otherwise:

- `company` — a governing repository with Standard `secure-coding`
  (version `1.0.0`, rules `SEC-001` level `MUST` and `SEC-002` level `MUST`
  with `final: true`) and Standard `code-review`, tagged `v1.0.0`.
- `platform` — a governing repository whose `processkit.toml` declares
  `[[upstream]] name = "company"` at ref `v1.0.0`, which is locked and
  fetched, and which adds Standard `api-design` (version `2.0.0`, rule
  `API-001` level `MUST`, rule `API-002` level `SHOULD`) and Standard
  `release-notes`, on branch `main`.

## 1. Project inheriting from two governing levels (release journey 4)

Preconditions: processkit installed; the common fixture; an empty Git
repository `payments-api` with one commit.

Steps:

1. Run `processkit init --project` in `payments-api` and declare in
   `processkit.toml` one upstream: `[[upstream]] name = "platform"`, with
   `source` the `platform` repository and `ref = "main"`.
2. Run `processkit lock`; inspect `processkit.lock` and `git status`.
3. Run `processkit list Standard` before fetching.
4. Run `processkit fetch`; inspect `git status` and `.processkit/`.
5. Run `processkit list Standard` and `processkit show Standard api-design`.
6. Add a local Standard `api-design` that declares
   `spec.overrides = {upstream: "platform", name: "api-design",
   version: "2.0.0", reason: "public API must version endpoints"}` and
   raises rule `API-002` from `SHOULD` to `MUST`. Run `processkit validate`.
7. Run `processkit explain Standard api-design --json` and
   `processkit explain Standard secure-coding --json`.
8. Repeat steps 5 and 7 and compare the output byte for byte.
9. Run `git log --all --oneline`, `git status`, and list remotes of
   `payments-api` before and after steps 2 to 8.

Expected results:

- 2: `processkit.lock` exists at the root and has entries for `platform`
  and the transitive upstream `company`, each with an exact commit and a
  content digest; it is an uncommitted file change and nothing was
  committed or staged.
- 3: the command fails as an environment failure naming the unfetched
  upstream and the fix (`processkit fetch`); no network access occurs.
- 4: only the local cache changed; no repository file changed.
- 5: `secure-coding`, `code-review`, `api-design`, and `release-notes` are
  listed as inherited items carrying their upstream identity.
- 6: validation succeeds.
- 7: for `api-design`, provenance names the originating repository
  (`platform`), the locked commit, and the path, and lists the override with
  its upstream, name, version `2.0.0`, and reason; the served rule `API-002`
  has level `MUST`. For `secure-coding`, provenance names `company`, its
  locked commit, and path, and lists no override.
- 8: output is byte-identical.
- 9: no commit, branch, push, remote, or ref was created by processkit;
  the only network-like access happened during `lock` and `fetch`.

Covers: PK-PROD-009, PK-PROD-026, PK-INH-001, PK-INH-002, PK-INH-003,
PK-INH-010, PK-INH-011, PK-INH-012, PK-INH-015, PK-INH-021

## 2. Local item that collides without an override

Preconditions: `payments-api` from journey 1 after step 5.

Steps:

1. Add a local Standard named `code-review` with no `spec.overrides`. Run
   `processkit validate`.
2. Add `spec.overrides` without `reason`. Run `processkit validate`.
3. Complete the override with `upstream`, `name`, `version`, and `reason`.
   Run `processkit validate`.

Expected results:

- 1: validation fails, reporting a conflict between the local and the
  inherited `code-review`.
- 2: validation fails; the override must state a reason.
- 3: validation succeeds.

Covers: PK-INH-011, PK-INH-012

## 3. Final items and final rules

Preconditions: `payments-api` from journey 1 after step 5; in `company`,
Standard `code-review` is changed to `final: true`, tagged, and the change is
propagated by `processkit lock --update` and `processkit fetch` in
`platform` and `payments-api`.

Steps:

1. Add a local override of `secure-coding` that changes rule `SEC-002`
   (marked `final`) from `MUST` to `SHOULD`. Run `processkit validate`.
2. Change the override so that it changes only rule `SEC-001` (not final).
   Run `processkit validate`.
3. Add a local override of `code-review` (marked `final`). Run
   `processkit validate`.

Expected results:

- 1: validation fails, naming the final rule `SEC-002`.
- 2: validation succeeds.
- 3: validation fails, naming the final item `code-review`.

Covers: PK-INH-013

## 4. Two upstreams provide the same item

Preconditions: two governing repositories `team-a` and `team-b`, each
providing Standard `logging`; a project repository declaring both as
upstreams, locked and fetched.

Steps:

1. Run `processkit validate`.
2. Declare in `processkit.toml` that `team-b` wins for `logging`. Run
   `processkit validate` and `processkit explain Standard logging`.
3. Swap the order of the two `[[upstream]]` tables, run `processkit lock`,
   and repeat step 2.

Expected results:

- 1: validation fails, reporting that `logging` is provided by both
  upstreams and no winner is declared; neither is served silently.
- 2: validation succeeds; the served `logging` has provenance in `team-b`.
- 3: the served item and its provenance are unchanged; declaration order
  had no effect.

Covers: PK-INH-014, PK-INH-010

## 5. Upstream changes, change summary, and stale overrides

Preconditions: `payments-api` from journey 1 after step 6, with the lock
committed.

Steps:

1. In `platform` `main`, change `api-design` to version `2.1.0`, add
   Standard `observability`, remove Standard `release-notes`, and add
   Standard `secrets`; `payments-api` already has a local Standard
   `secrets` without an override (which validated before, as no upstream
   provided `secrets`).
2. In `payments-api`, run `processkit lock --update platform --dry-run`.
3. Run `processkit lock --update platform`, then `processkit fetch`.
4. Run `processkit validate`.
5. Run `git diff --stat`.

Expected results:

- 2: the output lists `observability` as added, `api-design` as changed,
  `release-notes` as removed, and `secrets` as newly conflicting;
  `processkit.lock` is byte-identical.
- 3: the same summary is shown before the lock is written; the lock now
  names the new commits and digests.
- 4: the override of `api-design` naming version `2.0.0` is reported as
  stale; `secrets` is reported as a conflict.
- 5: the only repository change is `processkit.lock`, an ordinary
  uncommitted file change for review.

Covers: PK-INH-020, PK-INH-021, PK-INH-016, PK-INH-002

## 6. Missing, unreachable, and tampered upstreams

Preconditions: `payments-api` from journey 1 after step 4 with the lock
committed.

Steps:

1. Change the `ref` of `platform` to a ref that does not exist. Run
   `processkit lock`.
2. Restore the ref; change `source` to a path that does not exist (or an
   unreachable address). Run `processkit lock` and `processkit fetch`.
3. Restore the source. Rewrite the locked commit's content in the `platform`
   source so its content no longer matches the locked digest (for example
   by force-replacing the history), delete `.processkit/`, and run
   `processkit fetch`.
4. After each step, inspect `processkit.lock` and the served items.

Expected results:

- 1: `lock` fails, naming upstream `platform` and the missing ref.
- 2: `lock` and `fetch` fail, naming upstream `platform` and the reason
  (unreachable).
- 3: `fetch` fails, naming upstream `platform` and a digest mismatch.
- 4: the lock is unchanged after every failure, and no other revision of
  `platform` is ever served in place of the locked one.

Covers: PK-INH-004, PK-INH-002

## 7. Offline serving and validation

Preconditions: `payments-api` from journey 1 after step 6; network access
disabled for the processkit process (or Git sources made unreachable).

Steps:

1. Run `processkit validate`, `processkit list Standard`, and
   `processkit explain Standard api-design`.
2. Start `processkit mcp serve --stdio`, connect, and call `get_context`,
   `list`, and `explain`.
3. Meanwhile, push a new commit to `platform` `main` (with the network
   restored only for that push).
4. Repeat step 2; compare `processkit.lock` and `git status` with their
   state before step 1.

Expected results:

- 1, 2: all succeed with no network access attempted.
- 4: served results are unchanged and still name the locked commit;
  `processkit.lock` is byte-identical; no fetch and no lock update occurred
  as a side effect of serving.

Covers: PK-INH-003, PK-INH-021, PK-INH-002, PK-PROD-026

## 8. Inherited access rules and restricted items

Preconditions: a governing repository `company` whose Role and Binding grant
principal `carol` read access to all items, and whose Standard
`incident-runbook` is marked restricted and readable only through Role
`security-team`, granted upstream to `alice` but not to `bob`; a downstream
governing repository `platform` that inherits `company` (locked and fetched)
and is served by the shared server with an authenticator for `alice`,
`bob`, and `carol`; downstream rules grant `alice` and `bob`, but not
`carol`, read access to all items.

Steps:

1. Without importing `company`'s access rules, call `list`, `get`, and
   `get_context` as `alice`, `bob`, and `carol`, including a direct `get`
   of `incident-runbook`.
2. Import `company`'s access rules in the downstream configuration. Repeat
   the calls as `alice` and `bob`.
3. Keep the import and remove `alice`'s downstream grant. Repeat the calls
   as `alice`.

Expected results:

- 1: `carol` receives no item: the upstream Binding grants nothing
  downstream. `incident-runbook` is absent for `alice` and `bob` from every
  result, and a direct `get` does not reveal it.
- 2: `alice` receives `incident-runbook`; `bob` does not.
- 3: `alice` no longer receives `incident-runbook`: both the upstream and
  the downstream rules must allow it.

Covers: PK-INH-030, PK-INH-031

## Verified by component tests only

None. Determinism of resolution (PK-INH-010) is additionally covered by
resolution tests across many inputs (PK-TEST-003), but journeys 1 and 4
observe it directly.
