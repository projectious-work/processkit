---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-latex-authoring
  name: latex-authoring
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "LaTeX authoring with LuaLaTeX — document classes, math, TikZ, BibLaTeX."
  category: language
  layer: null
  when_to_use: "Use when writing or editing LaTeX documents, setting up preambles, typesetting math, building TikZ diagrams, or managing bibliographies."
---

# LaTeX Authoring

## Level 1 — Intro

Prefer LuaLaTeX for new documents — native Unicode, system fonts
via `fontspec`, and better TikZ performance. Use modern packages
(`tabularray`, `siunitx`, `biblatex`, `cleveref`) and structure
documents for reviewable diffs: one sentence per line, sections in
their own files.

## Level 2 — Overview

### Document classes

| Class         | Use for                                              |
|---------------|------------------------------------------------------|
| `article`     | Papers, short documents (no chapters)                |
| `book`        | Books, theses (chapters, front/back matter)          |
| `report`      | Technical reports (chapters, no front/back matter)   |
| `extarticle`  | Articles needing 8pt–20pt font sizes                 |
| `memoir`      | Flexible class combining book and article features  |
| `beamer`      | Presentations and slides                             |
| `standalone`  | Single figures or TikZ diagrams for inclusion        |

### LuaLaTeX vs pdfLaTeX

Prefer LuaLaTeX for new projects — native Unicode, OpenType/TrueType
fonts via `fontspec`, Lua scripting, better TikZ performance on
complex diagrams, and packages like `fontspec` and `emoji` require
it. Stick with pdfLaTeX only when a legacy project or publisher
requires it, or when compile speed matters on trivial documents.

Build with `latexmk -lualatex main.tex` (or `-pdf` for pdfLaTeX).
`latexmk` runs biber and reruns the engine as needed.

### Essential packages

**Layout and typography:** `geometry` (margins), `fancyhdr`
(headers/footers), `fontspec` (system fonts, LuaLaTeX only),
`babel` (multilingual), `enumitem` (custom lists).

**Math and science:** `amsmath` (environments and commands),
`siunitx` (units and number formatting).

**Tables and figures:** `tabularray` (modern tables, replaces
`tabular`/`booktabs`), `graphicx` (images), `svg` (SVG inclusion,
requires Inkscape).

**Graphics and color:** `tikz` (programmatic vector graphics),
`pgfkeys` (key-value interface), `xcolor` (extended color),
`tcolorbox` (colored boxes, theorems, code listings).

**Bibliography:** `biblatex` with the Biber backend — modern
replacement for `bibtex` and `natbib`.

**Specialty:** `bytefield` (protocol diagrams), `xskak` (chess),
`emoji` (LuaLaTeX only).

See `references/packages.md` for detailed usage and configuration
of each package.

### Document structure

Write one sentence per line — it produces cleaner git diffs and
makes review much easier. Split large documents with
`\input{sections/introduction}` per section. Keep the preamble in
a separate `preamble.tex` so you can reuse it. Put `\label{}` on
every float, section, and equation, and reference with `\cref{}`
(from `cleveref`) rather than bare `\ref{}`.

### Bibliography with BibLaTeX

```latex
\usepackage[backend=biber, style=authoryear]{biblatex}
\addbibresource{references.bib}

% In text:
\textcite{Knuth1984} writes that...     % Knuth (1984) writes that...
As shown before \autocite{Knuth1984}    % As shown before (Knuth, 1984)

% At end:
\printbibliography
```

Build with `latexmk -lualatex main.tex` — it handles biber runs
automatically.

### Math

Inline math uses `$...$` or `\(...\)`; display math uses `\[...\]`
(never `$$...$$`). Use `align`, `gather`, and `cases` from
`amsmath` for multi-line equations. Define reusable commands in
the preamble (`\newcommand{\vect}[1]{\mathbf{#1}}`). Use `siunitx`
for all units: `\qty{9.8}{m/s^2}`, `\num{1.23e4}`. See
`references/math-reference.md` for a symbol and environment
reference.

### TikZ

Load with `\usepackage{tikz}` plus `\usetikzlibrary{...}`. Common
libraries: `arrows.meta`, `positioning`, `calc`, `shapes`, `fit`.
Use the `standalone` class for diagrams you want to include from
multiple documents. Define styles once in the preamble to keep
picture bodies readable. See `references/tikz-reference.md` for
drawing patterns.

## Level 3 — Full reference

### Minimal LuaLaTeX preamble

```latex
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{tabularray}
\usepackage{tikz}
\usepackage{xcolor}
\usepackage[backend=biber, style=authoryear]{biblatex}
\usepackage{cleveref}
\addbibresource{references.bib}
```

### Common mistakes

- Using `$$...$$` for display math — it is not plain-TeX in
  LaTeX. Use `\[...\]` or an `equation` environment.
- Manual spacing with `\,` and `~` instead of proper environments.
- Forgetting `\label` immediately after `\caption` inside a float
  — the label must come after the caption, or it references the
  enclosing section instead.
- Including bitmap images where vector (PDF or SVG) would produce
  crisper output at no cost.
- Forgetting to run biber when the bibliography does not appear —
  use `latexmk` and it is handled automatically.
- Using `\ref{}` alone when `\cref{}` would produce "Figure 3"
  instead of just "3".
- Writing multi-sentence lines, which makes git diffs unreadable.
- Building with pdfLaTeX when the preamble loads `fontspec`,
  `unicode-math`, or `emoji`.

### Tables with tabularray

`tabularray` replaces the older `tabular`/`booktabs` combo with a
key-value interface and saner defaults. Use `tblr` for tables in a
`table` float and the `booktabs` library for rules.

### Standalone diagrams

When a TikZ diagram will be reused or is complex enough to warrant
its own file, build it with the `standalone` class so it produces a
cropped PDF you can `\includegraphics` from the main document. This
keeps the main compile fast and lets you iterate on diagrams
independently.

### Further reading

- `references/packages.md` — per-package usage and configuration
- `references/math-reference.md` — math symbols, environments, and
  formulas
- `references/tikz-reference.md` — TikZ drawing commands and
  patterns
