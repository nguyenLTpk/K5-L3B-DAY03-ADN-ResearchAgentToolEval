---
name: cite
track: bonus
kind: local_formatter
provider: none (local)
requires_env: []
inputs: [items, style]
outputs: [citations, markdown, count, skipped]
side_effect: false
---
# cite

Tool mới của nhóm (người B). Định dạng các nguồn **đã thu thập** thành danh sách
tài liệu tham khảo theo chuẩn APA, MLA hoặc IEEE, hỗ trợ `company_policy/source-citation-policy.md`.

- Chạy local, không gọi mạng, không cần key.
- `items[]`: object có `title`, `url`, `source`, `author`, `date`. Thiếu `source` thì lấy domain của `url`.
  Thiếu `date` thì APA ghi `n.d.`. Tool **không bịa** tác giả/ngày/URL.
- Item không phải object, hoặc không có cả `title` lẫn `url`, bị bỏ qua và ghi chỉ số vào `skipped`.
- `style`: `apa` (mặc định), `mla`, `ieee`. Giá trị khác trả error dict.
- APA/MLA sắp xếp theo alphabet; IEEE đánh số `[1]`, `[2]` theo thứ tự đầu vào.
- Tham số nội bộ `accessed` (không khai báo cho model) dùng để cố định ngày truy cập trong unit test.

Không tìm hay kiểm chứng nguồn. Để làm bản tin dùng `format`.
