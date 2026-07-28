#!/usr/bin/env python3
"""Check generated Hugo HTML for broken local links without network access."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []
        self.has_h1 = False
        self.has_main = False
        self.images_without_alt = 0
        # Hugo emits an `aliases:` entry as a bare meta-refresh stub with no
        # <main> and no <h1>. Those are redirects, not pages, so the landmark
        # and heading checks do not apply to them.
        self.is_alias_redirect = False

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        if tag == "meta" and any(
            name == "http-equiv" and (value or "").lower() == "refresh"
            for name, value in attrs
        ):
            self.is_alias_redirect = True
        if tag == "h1":
            self.has_h1 = True
        if tag == "main":
            self.has_main = True
        if tag == "img" and not any(
            name == "alt" and value is not None for name, value in attrs
        ):
            self.images_without_alt += 1
        if tag not in {"a", "img", "script", "link"}:
            return
        key = "href" if tag in {"a", "link"} else "src"
        for name, value in attrs:
            if name == key and value:
                self.values.append(value)


def target_for(public: Path, page: Path, raw: str, base_path: str) -> Path | None:
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc or raw.startswith(("#", "mailto:", "data:")):
        return None
    path = unquote(parsed.path)
    absolute = path.startswith("/")
    if not path:
        return None
    if path.startswith(base_path):
        path = path[len(base_path) :]
        absolute = True
    if absolute:
        candidate = public / path.lstrip("/")
    else:
        candidate = page.parent / path
    if path.endswith("/"):
        return candidate / "index.html"
    if candidate.suffix:
        return candidate
    return candidate if candidate.is_file() else candidate / "index.html"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("public", type=Path)
    parser.add_argument("--base-path", default="/processkit/")
    args = parser.parse_args()
    public = args.public.resolve()
    failures: list[str] = []
    for page in sorted(public.rglob("*.html")):
        if "_print" in page.relative_to(public).parts:
            continue
        links = Links()
        links.feed(page.read_text(encoding="utf-8"))
        relative_page = page.relative_to(public)
        if relative_page.name != "404.html" and not links.is_alias_redirect:
            if not links.has_main:
                failures.append(f"{relative_page}: missing main landmark")
            if not links.has_h1:
                failures.append(f"{relative_page}: missing h1")
        if links.images_without_alt:
            failures.append(
                f"{relative_page}: {links.images_without_alt} image(s) "
                "lack alt text"
            )
        for raw in links.values:
            target = target_for(public, page, raw, args.base_path)
            if target is not None and not target.exists():
                failures.append(
                    f"{page.relative_to(public)}: {raw} -> "
                    f"{target.relative_to(public)}"
                )
    if failures:
        print("broken generated documentation links:")
        for failure in failures:
            print(f"- {failure}")
        return 1
    print("generated documentation links are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
