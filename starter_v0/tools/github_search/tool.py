from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, as_int, err

SORTS = ("stars", "updated", "best_match")
USER_AGENT = "AI20k-Day03-Research-Agent/1.0 (educational lab)"


def github_repo_search(query: str = "", sort: str = "stars", limit: int = 5) -> dict[str, Any]:
    """Search public GitHub repositories (unauthenticated REST API, no key)."""
    try:
        query = (query if isinstance(query, str) else str(query or "")).strip()
        if not query:
            raise ValueError("query must be a non-empty string")
        sort = (sort if isinstance(sort, str) else "").strip().lower() or "stars"
        if sort not in SORTS:
            raise ValueError(f"sort must be one of {list(SORTS)}, got {sort!r}")
        limit = as_int(limit, default=5, lo=1, hi=20)

        params: dict[str, Any] = {"q": query, "per_page": limit}
        if sort != "best_match":
            params.update({"sort": sort, "order": "desc"})
        response = requests.get(
            "https://api.github.com/search/repositories",
            params=params,
            headers={"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        repos = (response.json() or {}).get("items") or []
        items = []
        for repo in repos[:limit]:
            url = repo.get("html_url")
            if not url:
                continue
            items.append({
                "title": repo.get("full_name") or url,
                "url": url,
                "source": "github.com",
                "summary": repo.get("description") or "",
                "date": repo.get("updated_at"),
                "metrics": {
                    "stars": repo.get("stargazers_count"),
                    "forks": repo.get("forks_count"),
                    "language": repo.get("language"),
                },
            })
        return {"tool": "github_repo_search", "query": query, "sort": sort, "items": items}
    except Exception as exc:
        return err("github_repo_search", exc)
