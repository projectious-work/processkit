---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260514_0834-AlertShell-adopt-tagged-vocabulary-pools-and-high
  created: '2026-05-14T08:34:18+00:00'
spec:
  title: Adopt tagged vocabulary pools and high-volume three-token ID modes
  state: accepted
  decision: processkit ID generation will evolve from a single small adjective+noun
    pool toward large tagged vocabulary pools with global lexical-token uniqueness
    for human shorthand. The default memorable token remains AdjNoun for normal-volume
    entities. High-volume entities may use AdjAdjNoun as the preferred three-token
    extension, with counted plural forms such as SevenRapidRivers as an optional fallback.
    Verb-based sentence IDs are deferred and, if introduced, limited to narrow event/log-style
    use with operational verbs blocked.
  context: 'The current ID generator uses 120 positive adjectives and 120 concrete
    nouns, yielding 14,400 adjective+noun pairs per kind. Full IDs are collision-checked,
    but bare word-pair references can become ambiguous because resolver paths intentionally
    support shorthand lookup. The accepted design follows research into what3words,
    Diceware, Docker-style names, proquints, and Plus Codes: capacity should come
    from large shared vocabularies and extra token slots, while semantic categories
    should be soft palettes rather than small exclusive pools.'
  rationale: Small category-specific pools make IDs meaningful but reduce capacity
    and increase repeated human shorthand. A tagged-pool design preserves theme and
    kind hints while allowing enough combinations. Double-adjective mode gives a large
    capacity increase without pluralization complexity. Global lexical-token reservation
    protects the way humans actually refer to processkit entities.
  alternatives:
  - option: Keep current two-word pool only
    rationale: Not chosen because the full ID remains safe, but the bare word-pair
      space is too small for durable human shorthand as repositories grow.
  - option: Use small exclusive semantic categories per entity kind
    rationale: Not chosen because this improves thematic meaning but worsens capacity
      and reuse pressure within each category.
  - option: Make three-word numeric-count IDs the default
    rationale: Not chosen because counted IDs are distinctive, but pluralization adds
      complexity and count phrases are heavier than needed for normal volume.
  - option: Use verb sentence IDs broadly
    rationale: Not chosen because verb forms create grammar and command-vocabulary
      ambiguity; they are better deferred to possible log/event experiments.
  consequences: Implementation should add a vocabulary registry with tagged adjectives
    and nouns, palette selection by entity kind and stable subtype, global lexical-token
    reservation or ambiguity detection, and pk-doctor checks for palette occupancy,
    repeated shorthand, confusable words, and invalid counted plural forms. Existing
    IDs remain valid. Category assignments should not encode mutable workflow state
    such as backlog or done.
  decided_at: '2026-05-14T08:34:18+00:00'
---
