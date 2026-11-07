---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260721_1830-WildPath-promote-v1-general-availability-through-v1
  created: '2026-07-21T18:30:28+00:00'
spec:
  title: Promote v1 general availability through v1.x-release
  state: accepted
  decision: For a v1 general-availability release, create v1.x-release from the selected
    v1.x-pre-release state. Validate and tag the stable v1.x.y release on v1.x-release,
    then merge v1.x-release into main. Continue to create prerelease tags only on
    v1.x-pre-release.
  context: The accepted release-line policy defines v1.x-dev and v1.x-pre-release
    for prereleases but needed an explicit, durable rule for promoting v1 to general
    availability.
  rationale: A dedicated GA integration branch gives v1 the same explicit release
    authority as v0, preserves a final validation gate, and keeps main limited to
    finalized published releases.
  alternatives:
  - option: Merge v1.x-pre-release directly to main for GA
    rejected_because: Rejected because it bypasses a dedicated GA validation and tagging
      branch.
  - option: Tag stable v1 releases on v1.x-dev
    rejected_because: Rejected because the development branch is not the release authority.
  consequences: Create and protect v1.x-release only when preparing the first v1 GA
    release. Stable v1 tags must originate there and be merged to main immediately
    after tagging. v1.x-pre-release remains the sole source of v1 prerelease tags.
  decided_at: '2026-07-21T18:30:28+00:00'
---
