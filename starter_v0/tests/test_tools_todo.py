"""CP3: Tool Unit Test Challenge (owner: B - Le Thanh Nguyen).

Sections:
1. Former TODO stubs for the starter tools (clarify, format, send, lookup, fetch,
   timeline, social_search, policy) - all implemented, none skipped.
2. Unit tests for the group's new tools: wiki, hn_search, github_search, cite
   (>= 3 per tool: happy path, bad input from the model, failure path).
3. Regression tests for bugs found in starter tools (see report B5).

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest
import requests

from conftest import FakeResponse
from tools import TOOL_FUNCTIONS

clarify = TOOL_FUNCTIONS["clarify"]
format_tool = TOOL_FUNCTIONS["format"]
send = TOOL_FUNCTIONS["send"]
lookup = TOOL_FUNCTIONS["lookup"]
fetch = TOOL_FUNCTIONS["fetch"]
timeline = TOOL_FUNCTIONS["timeline"]
social_search = TOOL_FUNCTIONS["social_search"]
policy = TOOL_FUNCTIONS["policy"]

wiki = TOOL_FUNCTIONS["wiki"]
hn_search = TOOL_FUNCTIONS["hn_search"]
github_search = TOOL_FUNCTIONS["github_search"]
cite = TOOL_FUNCTIONS["cite"]


def _tweets(count: int, handle: str = "sama") -> list[dict]:
    return [{"tweet_id": str(100 + i), "screen_name": handle, "text": f"post {i}"} for i in range(count)]


# =====================================================================
# 1. Starter tools (former TODO stubs)
# =====================================================================

# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = clarify(question="Bạn muốn xem nguồn nào?", response_type="choice", options=["Web", "X"])

    assert result["options"] == ["Web", "X"]
    assert result["response_type"] == "choice"
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "a1", "url": "https://a.com/1", "section": "A"},
        {"title": "b1", "url": "https://b.com/1", "section": "B"},
        {"title": "a2", "url": "https://a.com/2", "section": "A"},
    ]
    markdown = format_tool(items=items, template="sections")["markdown"]

    assert markdown.count("## A") == 1
    assert markdown.count("## B") == 1
    assert markdown.index("a2") < markdown.index("## B")


def test_format_thread_numbers_items() -> None:
    items = [{"title": f"tin {i}", "url": f"https://x.com/{i}"} for i in range(3)]
    lines = [line for line in format_tool(items=items, template="thread")["markdown"].split("\n") if line]

    assert [line.split(" ")[0] for line in lines] == ["1/", "2/", "3/"]


def test_format_empty_items_does_not_crash() -> None:
    for empty in (None, []):
        result = format_tool(items=empty, template="sections")
        assert result["item_count"] == 0
        assert "error" not in result


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:TESTTOKEN")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send(text="Bản tin AI", confirmed=True)

    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "123:TESTTOKEN" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-1001"
    assert calls[0]["json"]["text"] == "Bản tin AI"
    assert result["status"] == "sent"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))

    result = send(text="Bản tin", confirmed=True)

    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
    calls = fake_http(FakeResponse({"results": []}))

    lookup(query="AI", timeframe=None)

    assert "time_range" not in calls[0]["json"]
    assert calls[0]["json"]["query"] == "AI"


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    calls = fake_http(FakeResponse({"data": {
        "markdown": "# Nội dung",
        "metadata": {"title": "T", "sourceURL": "https://www.example.com/a"},
    }}))

    result = fetch(url="https://www.example.com/a")

    assert calls[0]["url"] == "https://api.firecrawl.dev/v1/scrape"
    assert calls[0]["json"]["url"] == "https://www.example.com/a"
    assert result["items"][0] == {
        "title": "T", "url": "https://www.example.com/a", "source": "example.com", "summary": "# Nội dung",
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    fake_http(FakeResponse({"data": {"markdown": "x" * 5000, "metadata": {}}}))

    summary = fetch(url="https://example.com")["items"][0]["summary"]

    assert len(summary) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rk-test")
    raw = [{"screen_name": "sama", "text": "no id"}, *_tweets(6)]
    calls = fake_http(FakeResponse({"timeline": raw}))

    result = timeline(screenname="sama", limit=3)

    assert calls[0]["params"] == {"screenname": "sama"}
    assert len(result["items"]) == 3
    for item in result["items"]:
        assert item["url"].startswith("https://x.com/sama/status/")
        assert item["summary"] != "no id"


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "rk-test")
    calls = fake_http(FakeResponse({"timeline": _tweets(2, "openai")}))

    result = social_search(query="OpenAI", search_type="Top", limit=5)

    assert calls[0]["url"].endswith("/search.php")
    assert calls[0]["params"] == {"query": "OpenAI", "search_type": "Top"}
    assert calls[0]["headers"]["x-rapidapi-key"] == "rk-test"
    assert result["search_type"] == "Top"
    assert len(result["items"]) == 2


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    for query in ("", "   ", "the of and"):
        assert policy(query=query)["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    results = policy(query="API keys transcript", policy_area="data_privacy", top_k=5)["results"]

    assert results
    assert all(hit["policy_area"] == "data_privacy" for hit in results)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    results = policy(query="injection probe", policy_area="source_citation", top_k=5)["results"]
    probe = next(hit for hit in results if hit["section"] == "Injection probe")

    assert any("citation policy" in line for line in probe["untrusted_text"])
    assert "citation policy" not in probe["facts"]


# =====================================================================
# 2. New group tools (B)
# =====================================================================

# ---------------- wiki ----------------

def test_wiki_sends_expected_request_and_maps_pages(fake_http) -> None:
    calls = fake_http(FakeResponse({"pages": [
        {
            "key": "Transformer_(deep_learning)",
            "title": "Transformer (deep learning)",
            "excerpt": 'A <span class="searchmatch">transformer</span> is a model &amp; architecture',
            "description": "Machine learning architecture",
        },
        {"title": "page without key"},
    ]}))

    result = wiki(query="Transformer", lang="en", limit=2)

    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://en.wikipedia.org/w/rest.php/v1/search/page"
    assert calls[0]["params"] == {"q": "Transformer", "limit": 2}
    assert "User-Agent" in calls[0]["headers"]
    assert result["items"] == [{
        "title": "Transformer (deep learning)",
        "url": "https://en.wikipedia.org/wiki/Transformer_(deep_learning)",
        "source": "en.wikipedia.org",
        "summary": "A transformer is a model & architecture",
        "description": "Machine learning architecture",
    }]


def test_wiki_vietnamese_uses_vi_domain(fake_http) -> None:
    calls = fake_http(FakeResponse({"pages": [{"key": "Hà_Nội", "title": "Hà Nội"}]}))

    result = wiki(query="Hà Nội", lang="vi")

    assert calls[0]["url"].startswith("https://vi.wikipedia.org/")
    assert result["items"][0]["url"] == "https://vi.wikipedia.org/wiki/Hà_Nội"


@pytest.mark.parametrize("bad_args", [
    {"query": ""},
    {"query": "   "},
    {"query": None},
    {"query": "AI", "lang": "fr"},
])
def test_wiki_bad_input_returns_error_without_request(fake_http, bad_args) -> None:
    calls = fake_http(FakeResponse({"pages": []}))

    result = wiki(**bad_args)

    assert result["error"] == "ValueError"
    assert calls == []


@pytest.mark.parametrize("limit, sent", [("abc", 3), ("4", 4), (0, 3), (-2, 3), (99, 10)])
def test_wiki_coerces_limit_from_model(fake_http, limit, sent) -> None:
    calls = fake_http(FakeResponse({"pages": []}))

    wiki(query="AI", limit=limit)

    assert calls[0]["params"]["limit"] == sent


@pytest.mark.parametrize("failure, error", [
    (FakeResponse(status_code=429), "HTTPError"),
    (requests.Timeout("timed out"), "Timeout"),
])
def test_wiki_http_failure_returns_error_dict(fake_http, failure, error) -> None:
    fake_http(failure)

    result = wiki(query="AI")

    assert result["tool"] == "wiki_search"
    assert result["error"] == error


# ---------------- hn_search ----------------

def test_hn_search_popular_maps_hits_and_falls_back_to_discussion_url(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": [
        {"objectID": "1", "title": "Show HN: agent", "url": "https://www.example.com/a",
         "points": 120, "num_comments": 30, "created_at": "2026-11-10T00:00:00Z"},
        {"objectID": "2", "title": "Ask HN: evals?", "url": None, "points": 5, "num_comments": 2},
        {"title": "no id"},
    ]}))

    result = hn_search(query="AI agent", sort="popular", limit=5)

    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search"
    assert calls[0]["params"] == {"query": "AI agent", "tags": "story", "hitsPerPage": 5}
    first, second = result["items"]
    assert first["url"] == "https://www.example.com/a"
    assert first["source"] == "example.com"
    assert first["discussion_url"] == "https://news.ycombinator.com/item?id=1"
    assert first["metrics"] == {"points": 120, "comments": 30}
    assert second["url"] == "https://news.ycombinator.com/item?id=2"
    assert second["source"] == "news.ycombinator.com"


def test_hn_search_latest_uses_search_by_date(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    result = hn_search(query="LLM", sort="latest")

    assert calls[0]["url"] == "https://hn.algolia.com/api/v1/search_by_date"
    assert result["items"] == []


@pytest.mark.parametrize("bad_args", [{"query": ""}, {"query": "AI", "sort": "trending"}])
def test_hn_search_bad_input_returns_error_without_request(fake_http, bad_args) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    result = hn_search(**bad_args)

    assert result["error"] == "ValueError"
    assert calls == []


def test_hn_search_http_error_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=500))

    result = hn_search(query="AI")

    assert result == {"tool": "hacker_news_search", "error": "HTTPError", "message": "HTTP 500"}


# ---------------- github_search ----------------

def test_github_search_sends_sort_and_maps_repos(fake_http) -> None:
    calls = fake_http(FakeResponse({"items": [
        {"full_name": "org/agent-eval", "html_url": "https://github.com/org/agent-eval",
         "description": "Eval harness", "stargazers_count": 900, "forks_count": 40,
         "language": "Python", "updated_at": "2026-11-01T00:00:00Z"},
        {"full_name": "no/url"},
    ]}))

    result = github_search(query="agent evaluation language:python", sort="stars", limit=3)

    assert calls[0]["url"] == "https://api.github.com/search/repositories"
    assert calls[0]["params"] == {"q": "agent evaluation language:python", "per_page": 3, "sort": "stars", "order": "desc"}
    assert calls[0]["headers"]["Accept"] == "application/vnd.github+json"
    assert result["items"] == [{
        "title": "org/agent-eval", "url": "https://github.com/org/agent-eval", "source": "github.com",
        "summary": "Eval harness", "date": "2026-11-01T00:00:00Z",
        "metrics": {"stars": 900, "forks": 40, "language": "Python"},
    }]


def test_github_search_best_match_omits_sort_param(fake_http) -> None:
    calls = fake_http(FakeResponse({"items": []}))

    github_search(query="rag", sort="best_match")

    assert "sort" not in calls[0]["params"]
    assert "order" not in calls[0]["params"]


@pytest.mark.parametrize("bad_args", [{"query": ""}, {"query": "rag", "sort": "forks"}])
def test_github_search_bad_input_returns_error_without_request(fake_http, bad_args) -> None:
    calls = fake_http(FakeResponse({"items": []}))

    result = github_search(**bad_args)

    assert result["error"] == "ValueError"
    assert calls == []


def test_github_search_string_limit_is_coerced(fake_http) -> None:
    calls = fake_http(FakeResponse({"items": []}))

    github_search(query="rag", limit="0")

    assert calls[0]["params"]["per_page"] == 5


def test_github_search_rate_limit_returns_error_dict(fake_http) -> None:
    fake_http(FakeResponse(status_code=403))

    result = github_search(query="rag")

    assert result["tool"] == "github_repo_search"
    assert result["error"] == "HTTPError"


# ---------------- cite ----------------

SOURCES = [
    {"title": "Zeta report", "url": "https://www.zeta.org/r", "author": "Zeta Lab", "date": "2025-03-01"},
    {"title": "Alpha note", "url": "https://alpha.com/n"},
]


def test_cite_apa_sorts_and_never_invents_fields(fake_http) -> None:
    calls = fake_http(FakeResponse({}))

    result = cite(items=SOURCES, style="apa", accessed="2026-11-10")

    assert calls == []
    assert result["count"] == 2
    assert result["citations"] == [
        "alpha.com. (n.d.). *Alpha note*. https://alpha.com/n",
        "Zeta Lab. (2025). *Zeta report*. zeta.org. https://www.zeta.org/r",
    ]
    assert result["markdown"].startswith("- alpha.com.")


def test_cite_ieee_numbers_in_input_order_with_access_date() -> None:
    result = cite(items=SOURCES, style="ieee", accessed="2026-11-10")

    first, second = result["citations"]
    assert first.startswith('[1] Zeta Lab, "Zeta report,"')
    assert "(accessed 2026-11-10)" in first
    assert second.startswith('[2] "Alpha note,"')


def test_cite_mla_includes_accessed_date() -> None:
    result = cite(items=SOURCES[:1], style="mla", accessed="2026-11-10")

    assert result["citations"] == [
        'Zeta Lab. "Zeta report." *zeta.org*, 2025-03-01, https://www.zeta.org/r. Accessed 2026-11-10.'
    ]


def test_cite_author_ending_with_period_is_not_doubled() -> None:
    item = {"title": "Attention Is All You Need", "url": "https://arxiv.org/abs/1706.03762",
            "author": "Vaswani et al.", "date": "2017-06-12"}

    citation = cite(items=[item], style="apa")["citations"][0]

    assert citation.startswith("Vaswani et al. (2017).")
    assert ".." not in citation


def test_cite_skips_unusable_items_and_reports_indexes() -> None:
    result = cite(items=[SOURCES[0], "plain string", {}, {"source": "only source"}], style="apa")

    assert result["count"] == 1
    assert result["skipped"] == [1, 2, 3]


@pytest.mark.parametrize("bad_args, error", [
    ({"items": SOURCES, "style": "harvard"}, "ValueError"),
    ({"items": "not a list"}, "TypeError"),
])
def test_cite_bad_input_returns_error_dict(bad_args, error) -> None:
    result = cite(**bad_args)

    assert result["tool"] == "format_citations"
    assert result["error"] == error


def test_cite_empty_items_returns_empty_list() -> None:
    result = cite(items=None)

    assert result["count"] == 0
    assert result["markdown"] == ""


# =====================================================================
# 3. Regression tests for bugs found in starter tools (report B5)
# =====================================================================

@pytest.mark.parametrize("flag", ["false", "False", "no", "0", "", 1, None])
def test_regression_send_non_true_confirmation_does_not_call_network(monkeypatch, fake_http, flag) -> None:
    # Bug: `if not confirmed` treated the string "false" as confirmed and posted to Telegram.
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:TESTTOKEN")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001")
    calls = fake_http(FakeResponse({"ok": True}))

    result = send(text="Bản tin", confirmed=flag)

    assert result["status"] == "needs_confirmation"
    assert calls == []


def test_regression_send_string_true_still_sends(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:TESTTOKEN")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001")
    calls = fake_http(FakeResponse({"ok": True}))

    assert send(text="Bản tin", confirmed="true")["status"] == "sent"
    assert len(calls) == 1


def test_regression_timeline_negative_limit_does_not_drop_last_item(monkeypatch, fake_http) -> None:
    # Bug: limit=-1 became items[:-1] and silently dropped the last post.
    monkeypatch.setenv("RAPIDAPI_KEY", "rk-test")
    fake_http(FakeResponse({"timeline": _tweets(3)}))

    result = timeline(screenname="sama", limit=-1)

    assert len(result["items"]) == 3


@pytest.mark.parametrize("tool", [timeline, social_search])
def test_regression_non_numeric_limit_uses_default_instead_of_failing(monkeypatch, fake_http, tool) -> None:
    # Bug: int("abc") raised inside the tool, so the whole call returned an error dict.
    monkeypatch.setenv("RAPIDAPI_KEY", "rk-test")
    fake_http(FakeResponse({"timeline": _tweets(7)}))

    result = tool("sama", limit="abc")

    assert "error" not in result
    assert len(result["items"]) == 5


def test_regression_format_non_object_item_returns_error_dict_instead_of_raising() -> None:
    # Bug: a plain string item raised AttributeError out of the tool.
    result = format_tool(items=["plain string"], template="bullets")

    assert result["tool"] == "render_digest"
    assert result["error"] == "AttributeError"
