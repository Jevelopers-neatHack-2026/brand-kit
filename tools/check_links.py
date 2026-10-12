"""Check local links in Markdown and HTML files.

Default mode is offline and deterministic: local file and Markdown-anchor targets are
resolved against the checkout; http(s) links are only listed as UNCHECKED, never
reported as verified. `--external` additionally sends one HEAD/GET request per external
URL (network, non-deterministic; reachability only, not that the content is correct).
Exit 0 only when no local link is broken (and, with --external, none failed).

    python3 tools/check_links.py [--root DIR] [--external]
"""
from __future__ import annotations

import argparse
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import unquote, urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inventory_lib import ROOT, list_files  # noqa: E402

MD_LINK = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
HTML_ATTR = re.compile(r"""\b(?:src|href|srcset)\s*=\s*["']([^"']+)["']""", re.I)
CSS_URL = re.compile(r"""url\(\s*["']?([^"')]+)["']?\s*\)""", re.I)
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)


def slug(heading: str) -> str:
    h = re.sub(r"<[^>]+>|[`*_]", "", heading).strip().lower()
    h = re.sub(r"[^\w\- ]", "", h)
    return h.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    text = FENCE.sub("", path.read_text(encoding="utf-8"))
    seen: dict[str, int] = {}
    out = set()
    for m in HEADING.finditer(text):
        s = slug(m.group(1))
        n = seen.get(s, 0)
        seen[s] = n + 1
        out.add(s if n == 0 else f"{s}-{n}")
    return out


def extract(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".md":
        text = INLINE_CODE.sub("", FENCE.sub("", text))
        links = MD_LINK.findall(text) + HTML_ATTR.findall(text)
    else:
        links = HTML_ATTR.findall(text) + CSS_URL.findall(text)
    return [u for part in links for u in (part.split(",") if "," in part and " " in part.strip() else [part])]


def check(root: Path) -> tuple[list[str], set[str], int]:
    errors: list[str] = []
    external: set[str] = set()
    local_ok = 0
    for rel in list_files(root):
        if not rel.endswith((".md", ".html")):
            continue
        src = root / rel
        if not src.is_file():
            continue
        for raw in extract(src):
            url = raw.strip().split(" ")[0]
            if not url or url.startswith(("mailto:", "data:", "javascript:")):
                continue
            if url.startswith(("http://", "https://", "//")):
                external.add(url)
                continue
            parts = urlsplit(url)
            target = src if not parts.path else (src.parent / unquote(parts.path)).resolve()
            try:
                target.relative_to(root.resolve())
            except ValueError:
                errors.append(f"{rel}: link '{url}' escapes the repository")
                continue
            if not target.exists():
                errors.append(f"{rel}: broken local link '{url}'")
                continue
            if parts.fragment and target.suffix == ".md" and target.is_file():
                if parts.fragment.lower() not in anchors(target):
                    errors.append(f"{rel}: missing anchor '#{parts.fragment}' in {target.relative_to(root.resolve())}")
                    continue
            local_ok += 1
    return errors, external, local_ok


def probe(url: str) -> str | None:
    if url.startswith("//"):
        url = "https:" + url
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={"User-Agent": "brand-kit-link-check"})
            with urllib.request.urlopen(req, timeout=15):
                return None
        except Exception as exc:  # noqa: BLE001 - report whatever failed
            last = f"{type(exc).__name__}: {exc}"
    return last


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    ap.add_argument("--external", action="store_true", help="also probe external URLs over the network")
    args = ap.parse_args(argv)
    errors, external, ok = check(args.root.resolve())
    for e in errors:
        print(f"FAIL {e}")
    print(f"local links resolved: {ok}; broken: {len(errors)}")
    if args.external:
        failed = 0
        for url in sorted(external):
            err = probe(url)
            print(("OK   " if err is None else "FAIL ") + url + ("" if err is None else f"  ({err})"))
            failed += err is not None
        print(f"external reachable-at-run-time: {len(external) - failed}; failed: {failed} (reachability only)")
        return 1 if errors or failed else 0
    print(f"external links UNCHECKED (offline mode, not verified): {len(external)}")
    for url in sorted(external):
        print(f"UNCHECKED {url}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
