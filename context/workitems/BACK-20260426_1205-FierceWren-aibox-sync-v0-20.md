---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260426_1205-FierceWren-aibox-sync-v0-20
  created: '2026-04-26T12:05:59+00:00'
spec:
  title: aibox sync v0.20.0 content-diff overwrites locally-added schema/entity content
    with upstream baseline (RoyalFern wipe)
  state: backlog
  type: bug
  priority: high
  description: 'aibox v0.20.0 sync (run 2026-04-26 ~13:55 against processkit pin v0.22.0)
    silently rewrote 36 already-tracked files in /workspace/context/, stripping ALL
    of the RoyalFern Model schema additions that had been committed earlier the same
    day at 4a0e1d6.


    Files mutated (now reverted via `git checkout --`):

    - context/schemas/model.yaml — entire RoyalFern block (jurisdiction, data_privacy,
    knowledge_cutoff, vendor_model_id, latency_p50_ms) deleted (-97 lines)

    - context/models/MODEL-*.md — all 34 backfilled model entities had their RoyalFern
    fields stripped (-15..-19 lines each)

    - context/skills/processkit/model-recommender/SKILL.md — Governance dimension
    structured-fields block + 4 query_models filter examples deleted (-28 lines)


    Total: -734 / +93 lines. RoyalFern is preserved in the commit graph at 4a0e1d6
    + 8e914d7, so no permanent data loss; risk was that the next `git add . && git
    commit` would have silently undone the morning''s work.


    ROOT CAUSE HYPOTHESIS:

    aibox sync''s content-diff feature (per v0.20.0 release notes: "content-diff classifies
    upstream-removed-stale skills") compares /workspace/context/ against the new template
    baseline at /workspace/context/templates/processkit/v0.22.0/. The v0.22.0 release
    tag predates the RoyalFern commits (which sit on main, awaiting v0.22.1/v0.23.0).
    So the baseline legitimately lacks RoyalFern, but sync interprets local additions
    as "drift to remove" instead of "user changes on top of baseline" — and rewrites
    the live files.


    This is a DIFFERENT class of bug from CleverRiver (BACK-20260425_1711) which was
    about same-version migrations producing empty baselines. CleverRiver was a baseline-resolution
    bug; this is a downstream-application bug where, even with a correct baseline,
    the sync nukes local additions.


    LEGITIMATE v0.20.0 SYNC OUTPUT (kept):

    - aibox.lock bump 0.19.2 → 0.20.0; mcp_config_hash → processkit_install_hash rename

    - .claude/settings.json: WildGrove Phase B preauth merge (18 perms, 18 servers)
    — verified by pk-doctor preauth_applied INFO

    - .claude/commands/pk-doctor.md: minor wording update from upstream

    - New baselines: context/templates/aibox-home/0.20.0/, context/templates/processkit/v0.22.0/,
    context/.processkit-provenance.toml


    ACCEPTANCE / FIX:

    - aibox sync content-diff must distinguish "file present in baseline but user
    added fields" (preserve) from "file removed upstream and stale locally" (offer
    to remove via the migration plan, never silent rewrite).

    - For schema-bearing entity files (Model, Decision, etc.), additive local edits
    are a first-class workflow — the sync must never overwrite them silently.

    - Cross-project: filed against processkit because that''s where the affected entities
    live and where the regression was first observed; aibox should pick up and fix
    on their side.


    WORKAROUND IN PLACE:

    Run `git status` after every `aibox sync`. If untracked content/* files appear
    or tracked entity files show large deletions matching baseline-shape, revert with
    `git checkout -- <paths>` before any commit. Migration plans at context/migrations/
    are safe to keep (read-only).


    LINKAGE:

    - Closely related to BACK-20260425_1711-CleverRiver (other aibox sync defect —
    same-version migrations).

    - Not a regression of WildGrove (just closed); preauth merge piece of v0.20.0
    sync was clean.'
---
