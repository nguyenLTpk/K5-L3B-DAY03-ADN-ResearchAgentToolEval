from __future__ import annotations

import re
from datetime import date
from typing import Any

from tools._shared import domain, err

STYLES = ("apa", "mla", "ieee")


def _clean(value: Any) -> str:
    return str(value).strip() if value is not None else ""


def _year(raw: str) -> str:
    match = re.search(r"(19|20)\d{2}", raw)
    return match.group(0) if match else "n.d."


def _fields(item: dict[str, Any]) -> dict[str, str]:
    url = _clean(item.get("url"))
    source = _clean(item.get("source")) or domain(url)
    return {
        "title": _clean(item.get("title")) or url,
        "url": url,
        "source": source,
        # "Vaswani et al." -> "Vaswani et al" so the style's own period does not double up.
        "author": _clean(item.get("author")).rstrip("."),
        "date": _clean(item.get("date")),
    }


def _apa(f: dict[str, str], accessed: str) -> str:
    who = f["author"] or f["source"] or "Unknown"
    parts = [f"{who}. ({_year(f['date'])}).", f"*{f['title']}*."]
    if f["source"] and f["source"] != who:
        parts.append(f"{f['source']}.")
    if f["url"]:
        parts.append(f["url"])
    return " ".join(parts)


def _mla(f: dict[str, str], accessed: str) -> str:
    parts = []
    if f["author"]:
        parts.append(f"{f['author']}.")
    parts.append(f"\"{f['title']}.\"")
    tail = ", ".join(x for x in [f"*{f['source']}*" if f["source"] else "", f["date"], f["url"]] if x)
    if tail:
        parts.append(f"{tail}.")
    parts.append(f"Accessed {accessed}.")
    return " ".join(parts)


def _ieee(f: dict[str, str], accessed: str, number: int) -> str:
    who = f"{f['author']}, " if f["author"] else ""
    text = f"[{number}] {who}\"{f['title']},\""
    if f["source"]:
        text += f" {f['source']},"
    if f["date"]:
        text += f" {f['date']}."
    if f["url"]:
        text += f" [Online]. Available: {f['url']} (accessed {accessed})."
    return text


def format_citations(items: list[dict[str, Any]] | None = None, style: str = "apa", accessed: str | None = None) -> dict[str, Any]:
    """Format already-collected source items as a reference list. Local, no network, never invents fields."""
    try:
        style = (style if isinstance(style, str) else "").strip().lower() or "apa"
        if style not in STYLES:
            raise ValueError(f"style must be one of {list(STYLES)}, got {style!r}")
        if items is None:
            items = []
        if not isinstance(items, list):
            raise TypeError("items must be a list of source objects")
        accessed = accessed or date.today().isoformat()

        citations: list[str] = []
        skipped: list[int] = []
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                skipped.append(index)
                continue
            fields = _fields(item)
            if not fields["title"] and not fields["url"]:
                skipped.append(index)
                continue
            if style == "apa":
                citations.append(_apa(fields, accessed))
            elif style == "mla":
                citations.append(_mla(fields, accessed))
            else:
                citations.append(_ieee(fields, accessed, len(citations) + 1))

        if style == "ieee":
            markdown = "\n".join(citations)
        else:
            citations.sort(key=str.lower)
            markdown = "\n".join(f"- {c}" for c in citations)
        return {
            "tool": "format_citations",
            "style": style,
            "citations": citations,
            "markdown": markdown,
            "count": len(citations),
            "skipped": skipped,
        }
    except Exception as exc:
        return err("format_citations", exc)
