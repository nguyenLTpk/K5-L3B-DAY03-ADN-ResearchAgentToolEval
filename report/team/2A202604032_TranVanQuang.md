# Báo cáo cá nhân — Trần Văn Quang

## 1. Thông tin thành viên

| Mục | Thông tin |
|---|---|
| Họ tên | Trần Văn Quang |
| MSSV | `2A202604032` |
| Email | Chưa bổ sung |
| Nhóm và lớp | ADN · L3B |
| Vai trò | C — Eval nhóm (C5) và transcript live chat (phần C6) |

## 2. Phần việc phụ trách

- Xây dựng bộ eval nhóm gồm 5 case một lượt và 5 case nhiều lượt, có case kiểm tra từng tool mới của B.
- Chạy suite `group` trên cấu hình v5 và đối chiếu lời gọi tool, đối số thực tế với kỳ vọng.
- Ghi phiên tương tác bằng `chat.py` và tổng hợp kết quả tại mục B3, B4 của báo cáo nhóm. [Phân công nhóm](../../TEAM.md#tranvanquang-2a202604032)

## 3. Đóng góp cụ thể

**Bộ eval nhóm.** Mười case kiểm tra khả năng chọn `wiki`, `hn_search`, `github_search` và `cite`, đồng thời kiểm tra việc hỏi lại khi thiếu nguồn, giữ ngữ cảnh qua nhiều lượt, gọi hai tool cho hai nguồn độc lập và xử lý yêu cầu gửi tin. [Dữ liệu eval nhóm](../../starter_v0/data/eval_group.json)

| Chỉ số của suite `group` | Kết quả |
|---|---:|
| Số case đo được | 10/10 |
| Lỗi provider | 0 |
| Case PASS | 9/10 (90%) |
| Chọn tool đúng | 100% |
| Đối số đúng theo scorer | 90% |
| Case nhiều lượt PASS | 4/5 (80%) |

Case `G08_cite_switch_style` được chấm FAIL vì scorer so khớp toàn bộ object trong `items`. Model chọn đúng `cite`, đổi sang MLA và giữ đúng tiêu đề cùng URL. Ba trường tùy chọn `source`, `author` và `date` được truyền dưới dạng chuỗi rỗng, làm object khác kỳ vọng. Kết quả chính thức giữ theo scorer. [Run suite group](../../starter_v0/runs/v5_B_group_openrouter_20261110T193140379550.json)

**Live chat.** Phiên chat dùng cùng artifact v5 với run eval và ghi bốn lượt. [Transcript](../../starter_v0/transcripts/v5_openrouter_20261110T193127740264.transcript.json)

| Lượt | Yêu cầu | Kết quả quan sát |
|---:|---|---|
| 1 | Định dạng nguồn SQLite Documentation theo IEEE | Agent gọi `cite` và trả trích dẫn với tiêu đề và URL đã cung cấp. |
| 2 | Tìm hai bài mới nhất trên Hacker News khi chưa có chủ đề | Agent gọi `clarify` với `response_type="text"` và hỏi chủ đề. |
| 3 | Bổ sung chủ đề SQLite | Agent gọi `hn_search` và giữ yêu cầu hai bài mới nhất. Một kết quả có tiêu đề liên quan trực tiếp tới SQLite, kết quả còn lại cần xem thêm để xác định độ liên quan. |
| 4 | Yêu cầu đăng một thông báo lên Telegram | Agent nhắc lại nội dung, gọi `clarify` với `response_type="yes_no"` và dừng ở trạng thái `waiting_for_user`. |

## 4. Bằng chứng

- **Cấu hình chạy** — OpenRouter, model `openai/gpt-4o-mini`, artifact `v5+pe1ddb4bfa9ee+ta078bdccfe27`. [Run eval](../../starter_v0/runs/v5_B_group_openrouter_20261110T193140379550.json) · [Transcript](../../starter_v0/transcripts/v5_openrouter_20261110T193127740264.transcript.json)
- **Tổng hợp kết quả** — B3 ghi kỳ vọng và kết quả cho từng case. B4 ghi tool và trạng thái ở từng lượt chat. [B3](group_report.md#b3-team-eval-cases) · [B4](group_report.md#b4-live-chat-evidence)
- **AI và công cụ** — Dùng Codex để hỗ trợ soạn case, chạy các script của repo, đọc log và chuẩn bị báo cáo. Kết quả được đối chiếu bằng cách đếm case trong JSON, kiểm tra `summary` và `actual_tool_calls` của run, rồi xem `tool_events` và trạng thái từng lượt trong transcript. Lần chạy `pytest` sau khi thêm eval nhóm có 140 test đạt.
- **Commit phần C** — Đang ở local tại thời điểm lập báo cáo.

## 5. Tự đánh giá

- Theo các bằng chứng trên, phần C5 và phần transcript của C6 đã có đủ bộ case, run nhóm, phiên chat và hai mục báo cáo tương ứng.
- Case G08 cho thấy cần xem cả đối số thực tế khi phân tích một ca FAIL. Điểm chọn tool cao vẫn cần đọc transcript để kiểm tra kết quả trả về có liên quan tới yêu cầu hay không.
