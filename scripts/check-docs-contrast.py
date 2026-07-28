#!/usr/bin/env python3
"""Check the built stylesheet's text surfaces against WCAG AA, in both modes.

    check-docs-contrast.py <docs-site/public>

Dark-on-dark text has reached the published site twice, both times the same
way: the colour and the background behind it are decided by *different* rules,
so nothing objects when one of them moves. The worst case was overriding
`--td-pre-bg` to force an always-dark code surface — that variable also backs
inline code and tab bodies, whose text colour stayed on the body colour, so
inline code became near-black on near-black in light mode.

Checking the palette alone does not catch that: the intended pair stays fine
while the rule that would have applied it loses the cascade. So this does two
things:

  PALETTE   the token pairs the theme intends to use.
  CASCADE   for a handful of real elements, works out which rules actually win
            — by specificity, then source order — and checks the colour and
            background that result.

The cascade half is what catches a project rule being outranked by a theme
rule, which is how both incidents happened.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# --------------------------------------------------------------------------
# PALETTE: (label, foreground expression, background expression, minimum)
# --------------------------------------------------------------------------
# 4.5:1 is the AA floor for normal-size text. Nothing here is large enough to
# qualify for the 3:1 exception.
PAIRS = [
    ("body text",            "var(--bs-body-color)",  "var(--bs-body-bg)",        4.5),
    ("code block text",      "#c5daf0",               "#131e2b",                  4.5),
    ("code block comment",   "#72889d",               "#131e2b",                  4.5),
    ("code block keyword",   "#8aacc8",               "#131e2b",                  4.5),
    ("code block string",    "#ea7558",               "#131e2b",                  4.5),
    ("code block operator",  "#97a8b8",               "#131e2b",                  4.5),
    ("sidebar link",         "var(--pj-slate-11)",    "var(--bs-body-bg)",        4.5),
    ("sidebar link active",  "var(--pj-midnight-11)", "var(--bs-body-bg)",        4.5),
    ("sidebar link hover",   "var(--pj-orange-10)",   "var(--bs-body-bg)",        4.5),
    ("breadcrumb",           "var(--pj-text-muted)",  "var(--bs-body-bg)",        4.5),
    ("table header",         "var(--pj-text-muted)",  "var(--pj-surface-subtle)", 4.5),
    ("h6 / overline",        "var(--pj-text-muted)",  "var(--bs-body-bg)",        4.5),
    ("banner text",          "var(--bs-body-color)",  "var(--pj-orange-2)",       4.5),
    ("banner tag",           "var(--pj-orange-2)",    "var(--pj-orange-11)",      4.5),
    ("banner link",          "var(--pj-orange-11)",   "var(--pj-orange-2)",       4.5),
    ("accent button label",  "#ffffff",               "#cc4528",                  4.5),
    ("navbar brand",         "#c5daf0",               "#132440",                  4.5),
    ("navbar link",          "#97a8b8",               "#132440",                  4.5),
    ("footer text",          "#c5daf0",               "#132440",                  4.5),
]

# --------------------------------------------------------------------------
# CASCADE: elements whose colour and background come from competing rules.
# --------------------------------------------------------------------------
# Each element is an ancestor chain, outermost first. A chain entry is
# (tag, {classes}).
CASCADE = [
    ("inline code in a list item", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-content"}),
        ("ul", set()), ("li", set()), ("code", set())]),
    ("inline code in a paragraph", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-content"}),
        ("p", set()), ("code", set())]),
    ("inline code in a table cell", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-content"}),
        ("table", set()), ("tbody", set()), ("tr", set()), ("td", set()),
        ("code", set())]),
    ("tabbed panel body", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-content"}),
        ("div", {"tab-body"})]),
    ("active table-of-contents entry", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-toc"}),
        ("nav", {"TableOfContents"}), ("ul", set()), ("li", set()),
        ("a", {"active"})]),
    ("version menu release entry", 4.5, [
        ("html", set()), ("body", set()), ("div", {"td-version-menu"}),
        ("ul", {"dropdown-menu"}), ("li", set()),
        ("div", {"pk-version-line"}), ("ul", {"pk-version-line__releases"}),
        ("li", set()), ("a", {"dropdown-item", "pk-version-release"})]),
]

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
VAR = re.compile(r"var\(\s*(--[\w-]+)\s*(?:,([^)]*))?\)")
RULE = re.compile(r"([^{}@]+)\{([^{}]*)\}")

# Pseudo-classes that describe a resting state we want to evaluate, or that do
# not narrow what the element is. Anything else (:hover, :disabled, …) is a
# state we are not checking, so rules carrying it are skipped.
INERT_PSEUDO = {":root", ":not", ":first-child", ":last-child", ":only-child"}


def custom_properties(css: str, mode: str) -> dict[str, str]:
    """Custom properties in effect for one colour mode.

    Root-scoped declarations win. Component-scoped ones (Bootstrap sets a
    number of these on `.dropdown-menu`, `.btn`, and friends) are collected as
    a fallback so a value defined only there still resolves.
    """
    scoped: dict[str, str] = {}
    fallback: dict[str, str] = {}
    for match in RULE.finditer(css):
        selector = match.group(1)
        target = (scoped
                  if ":root" in selector or f"[data-bs-theme={mode}]" in selector
                  else fallback)
        for name, value in re.findall(r"(--[\w-]+)\s*:\s*([^;}]+)", match.group(2)):
            if target is fallback and name in fallback:
                # Keep the first component-scoped definition. Bootstrap emits
                # the base component before its variants, so last-wins would
                # resolve `.dropdown-menu` through `.dropdown-menu-dark`.
                continue
            target[name] = value.strip()
    return {**fallback, **scoped}


def resolve(value: str, props: dict[str, str], depth: int = 0):
    if depth > 8:
        return None
    match = VAR.search(value)
    if match:
        referent = props.get(match.group(1))
        if referent is None:
            referent = match.group(2)
        if referent is None:
            return None
        return resolve(referent, props, depth + 1)
    match = HEX.search(value)
    if not match:
        return None
    digits = match.group(1)
    if len(digits) == 3:
        digits = "".join(c * 2 for c in digits)
    return tuple(int(digits[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb) -> float:
    def channel(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(fg, bg) -> float:
    low, high = sorted((luminance(fg), luminance(bg)))
    return (high + 0.05) / (low + 0.05)


def hexstr(rgb) -> str:
    return "#%02x%02x%02x" % rgb


# --------------------------------------------------------------------------
# A deliberately small selector matcher.
# --------------------------------------------------------------------------
# It understands descendant and child combinators, tags, classes, and ids, and
# treats `:not(...)` as a negative compound. That covers the selectors Docsy
# and this project actually write for these elements. A selector using
# anything it does not understand is skipped rather than guessed at.

COMPOUND = re.compile(r"^(?:([\w-]+|\*)?)((?:[.#][\w-]+|\[[^\]]*\]|:not\([^)]*\))*)$")


def parse_compound(text: str):
    match = COMPOUND.match(text)
    if not match:
        return None
    tag = match.group(1)
    classes, ids, negatives = set(), set(), []
    rest = match.group(2) or ""
    for token in re.finditer(r"\.([\w-]+)|#([\w-]+)|\[([^\]]*)\]|:not\(([^)]*)\)", rest):
        cls, ident, attr, neg = token.groups()
        if cls:
            classes.add(cls)
        elif ident:
            ids.add(ident)
        elif attr is not None:
            return None          # attribute selectors: not modelled
        elif neg is not None:
            inner = parse_compound(neg.strip())
            if inner is None:
                return None
            negatives.append(inner)
    return {"tag": tag if tag not in (None, "*") else None,
            "classes": classes, "ids": ids, "negatives": negatives}


def compound_matches(compound, node) -> bool:
    tag, classes = node
    if compound["tag"] and compound["tag"] != tag:
        return False
    if not compound["classes"] <= classes:
        return False
    if compound["ids"] and not (compound["ids"] <= classes):
        return False
    for negative in compound["negatives"]:
        if compound_matches(negative, node):
            return False
    return True


def selector_matches(selector: str, chain) -> bool | None:
    """True/False, or None when the selector uses something not modelled."""
    selector = selector.strip()
    if not selector or "," in selector:
        return None
    if re.search(r"::|:(?!not\()[\w-]+", selector):
        pseudo = set(re.findall(r"::?[\w-]+", selector))
        if not pseudo <= INERT_PSEUDO:
            return False          # a state we are not evaluating
    if "~" in selector or "+" in selector:
        return None

    parts = [p for p in re.split(r"\s*(>)\s*|\s+", selector) if p]
    parsed = []
    for part in parts:
        if part == ">":
            parsed.append(">")
            continue
        compound = parse_compound(part)
        if compound is None:
            return None
        parsed.append(compound)

    # Match right to left against the ancestor chain.
    index = len(chain) - 1
    position = len(parsed) - 1
    if not isinstance(parsed[position], dict):
        return None
    if not compound_matches(parsed[position], chain[index]):
        return False
    position -= 1
    index -= 1
    while position >= 0:
        child_combinator = parsed[position] == ">"
        if child_combinator:
            position -= 1
            if position < 0:
                return None
        compound = parsed[position]
        if child_combinator:
            if index < 0 or not compound_matches(compound, chain[index]):
                return False
            index -= 1
        else:
            while index >= 0 and not compound_matches(compound, chain[index]):
                index -= 1
            if index < 0:
                return False
            index -= 1
        position -= 1
    return True


def specificity(selector: str) -> tuple[int, int, int]:
    ids = len(re.findall(r"#[\w-]+", selector))
    classes = len(re.findall(r"\.[\w-]+|\[[^\]]*\]|:(?!not\()[\w-]+", selector))
    tags = len(re.findall(r"(?:^|[\s>+~])([a-zA-Z][\w-]*)", selector))
    return ids, classes, tags


def winning_declarations(css: str, chain):
    """The colour and background-color that win for one element."""
    best = {"color": None, "background-color": None}
    for order, match in enumerate(RULE.finditer(css)):
        body = match.group(2)
        for selector in match.group(1).split(","):
            verdict = selector_matches(selector, chain)
            if verdict is not True:
                continue
            spec = specificity(selector)
            for prop in ("color", "background-color"):
                found = re.findall(
                    rf"(?:^|;)\s*{prop}\s*:\s*([^;}}]+)", body)
                if not found:
                    continue
                value = found[-1].strip()
                important = "!important" in value
                key = (important, spec, order)
                if best[prop] is None or key > best[prop][0]:
                    best[prop] = (key, value.replace("!important", "").strip())
    return ({k: (v[1] if v else None) for k, v in best.items()})


def main() -> int:
    public = Path(sys.argv[1] if len(sys.argv) > 1 else "docs-site/public")
    sheets = sorted(public.glob("scss/main*.css"))
    if not sheets:
        print(f"error: no compiled stylesheet under {public}/scss", file=sys.stderr)
        return 1
    css = sheets[0].read_text(encoding="utf-8")

    failures: list[str] = []
    warnings: list[str] = []

    for mode in ("light", "dark"):
        props = custom_properties(css, mode)
        body_colour = resolve("var(--bs-body-color)", props)
        body_bg = resolve("var(--bs-body-bg)", props)

        for label, fg_expr, bg_expr, minimum in PAIRS:
            fg, bg = resolve(fg_expr, props), resolve(bg_expr, props)
            if fg is None or bg is None:
                warnings.append(f"{mode}: unresolved palette pair {label}")
                continue
            ratio = contrast(fg, bg)
            if ratio < minimum:
                failures.append(
                    f"{mode}: {label} is {ratio:.2f}:1, needs {minimum}:1 "
                    f"({hexstr(fg)} on {hexstr(bg)})")

        for label, minimum, chain in CASCADE:
            won = winning_declarations(css, chain)
            fg_expr = won["color"]
            bg_expr = won["background-color"]
            # `inherit`, or nothing at all, means the value comes from an
            # ancestor. For these elements that resolves to the page defaults.
            fg = (body_colour if fg_expr in (None, "inherit")
                  else resolve(fg_expr, props))
            bg = (body_bg if bg_expr in (None, "inherit", "transparent")
                  else resolve(bg_expr, props))
            if fg is None or bg is None:
                warnings.append(
                    f"{mode}: unresolved cascade for {label} "
                    f"(color={fg_expr!r} background={bg_expr!r})")
                continue
            ratio = contrast(fg, bg)
            if ratio < minimum:
                failures.append(
                    f"{mode}: {label} resolves to {ratio:.2f}:1, needs "
                    f"{minimum}:1 ({hexstr(fg)} on {hexstr(bg)}); "
                    f"winning rules set color={fg_expr!r} "
                    f"background-color={bg_expr!r}")

    for item in warnings:
        print(f"warning: {item}", file=sys.stderr)
    if failures:
        print("documentation contrast check failed:", file=sys.stderr)
        for item in failures:
            print(f"  {item}", file=sys.stderr)
        return 1

    print(f"documentation contrast checked: {len(PAIRS)} palette pairs and "
          f"{len(CASCADE)} resolved elements, both modes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
