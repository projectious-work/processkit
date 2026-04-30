---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260426_1646-RapidSpruce-processkit-13-provenance-freshness
  created: '2026-04-26T16:46:04+00:00'
  updated: '2026-04-26T17:28:27+00:00'
spec:
  title: processkit#13 — provenance freshness build-time guard (PROVENANCE.toml stale-tag
    fix)
  state: done
  type: bug
  priority: low
  description: |
    ## Symptom (per GH issue #13)

    `processkit` v0.23.0 shipped `PROVENANCE.toml` with `generated_for_tag = "v0.21.0"` — stale by two minor releases. Downstream `aibox sync` warns but continues; non-blocking but the field lies. Filed by owner from aibox v0.21.1 integration cycle, 2026-04-26.

    ## Root cause

    The release-semver SKILL.md flow already documents the stamp step:
    ```
    3. Regenerate provenance / transitive artifacts — for processkit,
       `scripts/stamp-provenance.sh vX.Y.Z`.
    ```
    But it is human-driven and was skipped (or run with the wrong arg) for v0.22.0 and v0.23.0. There is no machine guard.

    ## Fix

    Add a build-time provenance freshness guard to `scripts/build-release-tarball.sh`, mirroring the existing `check-src-context-drift.sh` guard pattern:

    ```bash
    echo "running provenance guard: stamp-provenance --check $VERSION" >&2
    if ! "$REPO_ROOT/scripts/stamp-provenance.sh" --check "$VERSION"; then
        echo "" >&2
        echo "error: provenance guard failed — src/PROVENANCE.toml is stale." >&2
        echo "Run 'scripts/stamp-provenance.sh $VERSION' to regenerate," >&2
        echo "review the diff, and commit before re-running this script." >&2
        exit 1
    fi
    ```

    `stamp-provenance.sh --check` already exists; this just wires it into the tarball build so a stale stamp aborts the build with a clear remediation message. Releases that don't go through `build-release-tarball.sh` (currently the GitHub Release flow doesn't always upload a tarball) are not covered, but the script is the natural choke point for the published artifact.

    ## Scope

    - `scripts/build-release-tarball.sh` only (no src/ mirror — scripts/ is repo-root tooling, not shipped).
    - Local file `src/PROVENANCE.toml` is already at `generated_for_tag = "v0.23.0"` (verified) — the stale value only ever existed in the published v0.23.0 release tarball.
    - Ships in v0.23.1 alongside the BACK-20260426_1622-FierceOwl release-audit cleanup.

    ## Verification

    After edit, run `scripts/stamp-provenance.sh --check v0.23.0` from repo root. With `src/PROVENANCE.toml` already stamped at v0.23.0, this should exit 0. Then run with a wrong tag (e.g. `--check v9.9.9`) to confirm exit 3.

    ## Closes

    GH issue projectious-work/processkit#13.
  started_at: '2026-04-26T17:28:15+00:00'
  completed_at: '2026-04-26T17:28:27+00:00'
---

## Transition note (2026-04-26T17:28:20+00:00)

Implementation complete in working tree: scripts/build-release-tarball.sh provenance guard added; scripts/stamp-provenance.sh --check fixed to ignore generated_at timestamp. Verified positive (v0.23.0 → exit 0) and negative (v9.9.9 → exit 3) cases.


## Transition note (2026-04-26T17:28:27+00:00)

Closed by owner directive ("fix immediately"). Ships in v0.23.1 alongside FierceOwl release-audit cleanup. Owner to comment + close projectious-work/processkit#13 after v0.23.1 publishes.
