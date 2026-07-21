---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260721_1209-FreshBlossom-separate-v0-maintenance-releases-from-v1
  created: '2026-07-21T12:09:35+00:00'
spec:
  title: Separate v0 maintenance releases from v1 development
  state: accepted
  decision: Use main exclusively for the v0 maintenance/release line and v1.0 exclusively
    for v1 development. Preserve v0.27.5 on main and rebuild v1.0 from the divergence
    base with only v1-specific commits.
  context: Post-divergence commits placed the v0.27.5 release on branch v1.0 while
    main continued the v0 maintenance line, making branch names and release provenance
    inconsistent.
  rationale: Release branches must make supported version lines and tag provenance
    unambiguous. Cherry-picking the v0.27.5 release stack onto main preserves its
    history without rewriting the stable branch; a guarded force-with-lease rebuild
    restores v1.0 as a clean major-version development line.
  alternatives:
  - option: Leave the mixed history in place
    rejected_because: Branch names and release provenance would remain misleading.
  - option: Rename branches without moving commits
    rejected_because: This preserves the misplaced v0.27.5 release and does not establish
      clean boundaries.
  - option: Create a replacement v1 branch and retain the mixed v1.0 branch
    rejected_because: It leaves the canonical v1.0 branch misleading and adds avoidable
      migration burden.
  consequences: main receives the v0.27.5 release stack; v1.0 is rewritten with force-with-lease
    and collaborators must reset or rebase local v1.0 checkouts. Existing tags and
    GitHub releases remain immutable.
  deciders:
  - ACTOR-owner
  decided_at: '2026-07-21T12:09:35+00:00'
---
