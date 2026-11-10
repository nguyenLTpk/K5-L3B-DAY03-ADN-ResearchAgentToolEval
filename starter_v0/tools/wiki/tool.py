from __future__ import annotations

import html
import re
from typing import Any

import requests

from tools._shared import TIMEOUT, as_int, err

LANGS = ("en", "vi")
USER_AGENT = "AI20k-Day03-Research-Agent/1.0 (educational lab)"


def _clean_excerpt(raw: str) -> str:
    text = re.sub(r"<[^>]+>", "", raw or "")
    return html.unescape(text).strip()


def wiki_search(query: str = "", lang: str = "en", limit: int = 3) -> dict[str, Any]:
    """Search Wikipedia pages (no API key) and return title, description, excerpt and link."""
    try:
        query = (query if isinstance(query, str) else str(query or "")).strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        lang = (lang if isinstance(lang, str) else "").strip().lower() or "en"
        if lang not in LANGS:
            raise ValueError(f"lang must be one of {list(LANGS)}, got {lang!r}")
        limit = as_int(limit, default=3, lo=1, hi=10)

        response = requests.get(
            f"https://{lang}.wikipedia.org/w/rest.php/v1/search/page",
            params={"q": query, "limit": limit},
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        pages = (response.json() or {}).get("pages") or []
        items = []
        for page in pages[:limit]:
            key = page.get("key")
            if not key:
                continue
            items.append({
                "title": page.get("title") or key,
                "url": f"https://{lang}.wikipedia.org/wiki/{key}",
                "source": f"{lang}.wikipedia.org",
                "summary": _clean_excerpt(page.get("excerpt", "")),
                "description": page.get("description"),
            })
        return {"tool": "wiki_search", "query": query, "lang": lang, "items": items}
    except Exception as exc:
        return err("wiki_search", exc)
