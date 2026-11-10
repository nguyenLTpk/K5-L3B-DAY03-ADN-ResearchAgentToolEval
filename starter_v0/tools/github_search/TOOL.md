---
name: github_search
track: bonus
kind: live_api
provider: GitHub REST API (unauthenticated)
requires_env: []
inputs: [query, sort, limit]
outputs: [items]
side_effect: false
---
# github_search

Tool mới của nhóm (người B). Tìm repository công khai trên GitHub: thư viện,
code mẫu, implementation mã nguồn mở về một chủ đề.

- API: `GET https://api.github.com/search/repositories`, không cần key. GitHub giới hạn
  khoảng 10 request/phút khi không xác thực; khi bị giới hạn (HTTP 403/429) tool trả error dict.
- `sort`: `stars` (mặc định), `updated`, hoặc `best_match` (không gửi tham số sort lên API).
- `limit`: ép về int trong khoảng 1–20, mặc định 5.
- Output: `items[]` gồm `title` (`owner/repo`), `url`, `source`, `summary` (description),
  `date` (updated_at), `metrics.stars`, `metrics.forks`, `metrics.language`.

Không dùng cho paper (dùng `papers`), bài viết/tin tức (dùng `lookup`) hay đọc một URL repo cụ thể (dùng `fetch`).
