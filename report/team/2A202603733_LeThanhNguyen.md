# Báo cáo cá nhân — LeThanhNguyen-2A202603733

## 1. Thông tin thành viên

- Họ tên: Lê Thành Nguyên
- MSSV: 2A202603733
- Email: nguyenngungonvc@gmail.com

## 2. Phần việc phụ trách

Người B — Tool mới và unit test (C4), cùng bonus "Hơn 3 tool mới" và "Test challenge".

- Viết tool mới trong `starter_v0/tools/<tên>/` (`tool.py` + `TOOL.md`), đăng ký trong `starter_v0/tools/__init__.py` và khối `# ---- Group tools (B) ----` cuối `starter_v0/artifacts/tools.yaml`.
- Viết unit test trong `starter_v0/tests/test_tools_todo.py`, giữ `pytest` 0 failed.
- Viết mục B5a (phần tool/test) và B5 trong `report/team/group_report.md`.

## 3. Đóng góp cụ thể

**4 tool mới, đều không cần API key:**

| Tool | Hàm | Làm gì | Khi nào agent nên gọi |
|---|---|---|---|
| `wiki` | `wiki_search` | Tìm trang Wikipedia (en/vi), trả tiêu đề, mô tả, excerpt, link | "X là gì", "Y là ai", định nghĩa, lịch sử một khái niệm |
| `hn_search` | `hacker_news_search` | Tìm story Hacker News (popular/latest), trả link, điểm, số comment, link thảo luận | Khi user hỏi cộng đồng dev / Hacker News / HN nói gì về một chủ đề |
| `github_search` | `github_repo_search` | Tìm repo GitHub (stars/updated/best_match), trả tên repo, mô tả, sao, ngôn ngữ | Khi user cần repo, thư viện, code mã nguồn mở |
| `cite` | `format_citations` | Định dạng nguồn đã có thành trích dẫn APA/MLA/IEEE, chạy local | Khi user cần danh sách tài liệu tham khảo cho nguồn đã thu thập |

Nguyên tắc chung của 4 tool:

- Input xấu (query rỗng, enum sai, `items` không phải list) trả error dict và **không gọi mạng**.
- `limit` từ model được ép về int có chặn trên (helper `as_int` trong `tools/_shared.py`).
- Lỗi HTTP hoặc timeout trả error dict, không raise.
- `cite` không bịa tác giả, ngày hay URL.

**Unit test (`tests/test_tools_todo.py`, 58 test):**

- 32 test cho 4 tool mới (≥ 4 test/tool), gồm happy path (assert cả request gửi đi lẫn kết quả map), input xấu từ model, và nhánh lỗi.
- Viết hết 14 stub `pytest.skip(TODO)` của starter (clarify, format, send, lookup, fetch, timeline, social_search, policy).
- 12 regression test cho 3 bug tìm được trong tool có sẵn.

**3 bug đã sửa trong tool có sẵn (chi tiết ở B5):**

1. `send` coi `confirmed="false"` là đã xác nhận, nên có thể gửi Telegram khi chưa được duyệt.
2. `timeline` và `social_search`: `limit=-1` làm mất bài cuối, `limit="abc"` làm hỏng cả lời gọi.
3. `format` raise `AttributeError` khi gặp item không phải object, thay vì trả error dict.

## 4. Bằng chứng

- File:
  - `starter_v0/tools/wiki/`, `starter_v0/tools/hn_search/`, `starter_v0/tools/github_search/`, `starter_v0/tools/cite/`
  - `starter_v0/tools/__init__.py`, `starter_v0/tools/_shared.py` (`as_int`)
  - `starter_v0/artifacts/tools.yaml` (khối Group tools)
  - `starter_v0/tools/send/tool.py`, `timeline/tool.py`, `social_search/tool.py`, `format/tool.py` (sửa bug)
  - `starter_v0/tests/test_tools_todo.py`
- Kết quả `pytest` (chạy trong `starter_v0/`): `140 passed, 0 failed, 0 skipped`. Riêng `tests/test_tool_contract.py`: 75 passed.
- Kiểm chứng ngược: chạy 12 regression test trên code tool gốc thì 9 FAIL, sau khi sửa thì 12 PASS.
- Smoke test API thật (2026-11-10): `wiki` (en, vi), `hn_search` (popular, latest), `github_search` đều trả kết quả hợp lệ.
- Commit/PR: `bba92d1` (tool, test, sửa bug) trên nhánh `b-tool`. Base eval sau khi thêm tool: v4 19/20, v5 20/20 (người A chạy).
- AI/công cụ đã dùng và cách tự kiểm tra kết quả: Dùng Claude Code (Claude) hỗ trợ viết code tool, test và đọc code tool có sẵn để tìm bug. Tự kiểm tra bằng 4 cách:
  - Chạy toàn bộ `pytest` offline.
  - Chạy regression test trên code gốc để xác nhận test thật sự bắt được bug.
  - Gọi API thật để xác nhận endpoint và cách map dữ liệu.
  - Đọc lại từng description trong `tools.yaml` để chắc mỗi tool có ranh giới dùng/không dùng rõ ràng.

## 5. Tự đánh giá

- Đã hoàn thành C4 (tool mới + ≥ 3 test/tool, `pytest` 0 failed) và phần code của bonus "Hơn 3 tool mới" và "Test challenge" (0 skipped và có regression test).
- Phụ thuộc còn lại:
  - Bonus "Hơn 3 tool mới" cần mỗi tool có ≥ 1 eval case trong `data/eval_group.json` (người C).
  - Có thể cần thêm rule routing cho tool mới trong `system_prompt.md` (người A).
- Hạn chế: `github_search` dùng API không xác thực nên bị giới hạn khoảng 10 request/phút. `wiki` chỉ hỗ trợ `en` và `vi`.
