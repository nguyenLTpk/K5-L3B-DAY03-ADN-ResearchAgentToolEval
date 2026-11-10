from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, as_int, domain, err

ENDPOINTS = {
    "popular": "https://hn.algolia.com/api/v1/search",
    "latest": "https://hn.algolia.com/api/v1/search_by_date",
}


def hacker_news_search(query: str = "", sort: str = "popular", limit: int = 5) -> dict[str, Any]:
    """Search Hacker News stories via the public Algolia API (no API key)."""
    try:
        query = (query if isinstance(query, str) else str(query or "")).strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        sort = (sort if isinstance(sort, str) else "").strip().lower() or "popular"
        if sort not in ENDPOINTS:
            raise ValueError(f"sort must be one of {list(ENDPOINTS)}, got {sort!r}")
        limit = as_int(limit, default=5, lo=1, hi=20)

        response = requests.get(
            ENDPOINTS[sort],
            params={"query": query, "tags": "story", "hitsPerPage": limit},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        hits = (response.json() or {}).get("hits") or []
        items = []
        for hit in hits[:limit]:
            story_id = hit.get("objectID")
            if not story_id:
                continue
            discussion_url = f"https://news.ycombinator.com/item?id={story_id}"
            url = hit.get("url") or discussion_url
            items.append({
                "title": hit.get("title") or "",
                "url": url,
                "source": domain(url) or "news.ycombinator.com",
                "summary": hit.get("title") or "",
                "discussion_url": discussion_url,
                "date": hit.get("created_at"),
                "metrics": {"points": hit.get("points"), "comments": hit.get("num_comments")},
            })
        return {"tool": "hacker_news_search", "query": query, "sort": sort, "items": items}
    except Exception as exc:
        return err("hacker_news_search", exc)
