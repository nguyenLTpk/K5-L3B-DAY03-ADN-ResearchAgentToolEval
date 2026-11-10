---
name: wiki
track: bonus
kind: live_api
provider: Wikipedia REST API
requires_env: []
inputs: [query, lang, limit]
outputs: [items]
side_effect: false
---
# wiki

Tool mới của nhóm (người B). Tìm trang Wikipedia để lấy kiến thức nền về một
thực thể, khái niệm hoặc thuật ngữ ("X là gì", "ai là Y", lịch sử của Z).

- API: `GET https://{lang}.wikipedia.org/w/rest.php/v1/search/page?q=...&limit=...`, không cần key.
- `lang`: `en` hoặc `vi`. Giá trị khác trả error dict để model tự sửa args.
- `limit`: ép về int trong khoảng 1–10. Chuỗi rỗng/âm/không phải số thì dùng mặc định 3.
- Output: `items[]` gồm `title`, `url`, `source`, `summary` (excerpt đã bỏ thẻ HTML), `description`.
- Lỗi (query rỗng, sai `lang`, HTTP lỗi, timeout) trả `{"tool", "error", "message"}`, không raise.

Không dùng cho tin tức/sự kiện mới (dùng `lookup`), paper (dùng `papers`) hay đọc một URL cụ thể (dùng `fetch`).
