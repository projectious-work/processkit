# projectious.work company standards

Engineering and agent-operation standards of projectious.work, vendored from
<https://github.com/projectious-work/standards>. Each file is one standard; its
`## Agent briefing` is the short binding summary.

Do not edit this directory in a consuming repository. Change a standard
upstream, release it, and reinstall; `python3 .standards/standards.py check`
reports local edits and drift. The exact version is recorded in `lock.json`.

## License and attribution

- Standards text: © projectious.work, licensed under
  [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- `standards.py`: MIT License, © projectious.work.
- `sources/i-have-adhd/`: third-party, MIT License, © 2026 Ayoub Ghriss; see
  its `LICENSE` and `UPSTREAM.md`. `agent-communication.md` adapts it.

## Conventions

- Terms in *italics* are [Semantic Anchors](https://github.com/llm-coding/Semantic-Anchors/tree/ccb05b6bd41a663eaf2595e707d98f35d743e61f),
  pinned to catalog commit `ccb05b6b` (2026-10-26): the canonical meaning
  applies, and a standard states only where the company deviates. Adopting a
  later catalog revision is a standards change.
- MUST, MUST NOT, SHOULD, and MAY are used as in RFC 2119; lowercase forms are
  ordinary prose.
- Each standard ends with an `## Agent briefing`, the binding summary loaded
  into agent context: at most six lines, except the always-on communication
  briefing.
