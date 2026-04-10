---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1842-SteadyPeak-entity-lookup-by-word-pair
  created: '2026-04-10T18:42:00+00:00'
spec:
  title: "Feature: resolve entities by word-pair alone in get_workitem (and other get_ tools)"
  state: backlog
  type: story
  priority: medium
  description: >
    Agents and humans refer to entities by their word-pair shorthand in
    conversation (e.g. "StoutCrow", "HappyHare"). When slug is enabled the
    canonical ID is KIND-DATETIME-WordPair-slug, making the word-pair alone an
    incomplete key. Agents routinely drop the slug when constructing lookup
    calls, causing silent null returns (see BACK-20260410_1842-SnappyCrane).


    Desired behaviour: if the exact ID is not found, attempt a word-pair
    partial match against the index. If exactly one entity matches, return it.
    If multiple match, return an error listing the candidates.


    Example: get_workitem("StoutCrow") → resolves to
    BACK-20260410_1050-StoutCrow-create-brand-design-skill because the
    word-pair "StoutCrow" is unambiguous in the index.


    Scope: apply consistently across all entity get_ tools (get_workitem,
    get_decision, get_discussion, get_scope, etc.) or implement once in the
    shared index-management layer and call through from each tool.


    Alternative already available: search_entities("StoutCrow") finds the
    entity via full-text search, but agents should not need a full-text search
    just to resolve a known entity by its colloquial name. The resolution
    should be built into the get_ path.
---
