---
name: hn_search
track: bonus
kind: live_api
provider: Hacker News (Algolia API)
requires_env: []
inputs: [query, sort, limit]
outputs: [items]
side_effect: false
---
# hn_search

Tool mới của nhóm (người B). Tìm story trên Hacker News để xem cộng đồng
developer/tech đang thảo luận gì về một chủ đề.

- API: `GET https://hn.algolia.com/api/v1/search` (`sort=popular`) hoặc
  `/search_by_date` (`sort=latest`), luôn lọc `tags=story`, không cần key.
- `sort`: `popular` hoặc `latest`. Giá trị khác trả error dict.
- `limit`: ép về int trong khoảng 1–20, mặc định 5.
- Output: `items[]` gồm `title`, `url` (story không có link ngoài thì dùng link thảo luận),
  `source`, `summary`, `discussion_url`, `date`, `metrics.points`, `metrics.comments`.
- Lỗi trả error dict, không raise.

Không dùng cho bài đăng X/Twitter (dùng `social_search`) hay tin tức web chung (dùng `lookup`).
