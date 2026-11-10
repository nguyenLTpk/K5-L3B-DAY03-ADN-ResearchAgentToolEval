# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md) (Lê Hải Anh: Phụ trách Role A - Prompt & Tối ưu v0–v3, hoàn thiện B1, B2)
- Provider/model dùng cho v0–v3: OpenRouter (`openai/gpt-4o-mini`, temperature 0)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

> 1–2 câu mô tả agent dùng để làm gì (cho team khác hiểu nhanh).

Ví dụ: "Research agent: tìm tin theo từ khóa / theo tài khoản, đọc URL, tổng hợp thành digest, và gửi lên Telegram khi được xác nhận."

**Cách chạy UI:**

> Lệnh chạy UI (ví dụ `streamlit run app.py`) và dependency đã thêm vào `starter_v0/requirements.txt`.

**Link dùng thử (deploy):**

> Dán link public để team khác mở thử ngay. Cách deploy nhanh bằng Cloudflare Tunnel xem README. Nếu deploy Vercel/Streamlit Cloud thì dán link đó.
>
> URL:

### A2. Tool agent có

> Liệt kê các tool agent đang dùng (gồm tool mới nhóm tự thêm). Mỗi tool 1 dòng: tên + làm được gì.

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | hỏi lại người dùng khi thiếu thông tin | không |
|  |  |  |
|  |  |  |

### A3. Câu hỏi mẫu để thử

> 3–5 câu hỏi/yêu cầu mẫu để team khác tự thử agent ngay.

1.
2.
3.

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

- **`starter_v0/artifacts/system_prompt.md`**:
  - Bỏ toàn bộ chỉ dẫn xấu từ starter (đoán mò URL, tự ý suy diễn tài khoản nổi tiếng, ép gọi tool trong mọi trường hợp).
  - Bổ sung quy tắc phân loại yêu cầu: câu hỏi về danh tính/năng lực hoặc ngoài phạm vi (như giải toán) trả lời trực tiếp không gọi tool (`no_tool`).
  - Phân tách rõ quy tắc hỏi lại (`clarify` text khi thiếu thông tin cơ bản) và quy tắc xác nhận duyệt đăng (`clarify` yes_no khi chưa có sự đồng ý xuất bản cụ thể).
  - Thiết lập thứ tự ưu tiên (prompt precedence): yêu cầu đăng chưa duyệt phải kích hoạt xác nhận `yes_no` trước khi áp dụng quy tắc thiếu nội dung.
- **`starter_v0/artifacts/tools.yaml` (các tool có sẵn)**:
  - Viết lại toàn bộ description của 10 tool có sẵn, nêu rõ: chức năng, khi nào nên dùng, khi nào KHÔNG được dùng.
  - Tường minh hóa quy ước tham số (arg conventions): `screenname` không chứa ký tự `@`, tách từ khóa chủ đề khỏi `topic=news` và `timeframe=day` trong `lookup`, định dạng enum `Latest`/`Top` trong `social_search`.
  - Thiết lập ranh giới (boundary) nghiêm ngặt cho `send`: chỉ gọi khi đã có nội dung cụ thể và `confirmed=true` sau khi người dùng phê duyệt rõ ràng.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline (unchanged) | Đo lường baseline với prompt và tool declaration ban đầu, chưa chỉnh sửa. | N/A | Case Acc: 75% (15/20)<br>Routing: 80%<br>Argument: 75%<br>Multiturn: 100% | [v0 run](../../starter_v0/runs/v0_B_base_openrouter_20261110T180041253555.json) |
| v1 | `starter_v0/artifacts/system_prompt.md` | Kiểm tra phạm vi (scope), thông tin bắt buộc và quy tắc duyệt đăng trước khi hành động sẽ loại bỏ các lỗi gọi tool sai phạm vi (R08) và đoán mò thông tin (R10, R11). | Case Acc: 75% (15/20)<br>Routing: 80%<br>Argument: 75%<br>Multiturn: 100% | Case Acc: 95% (19/20)<br>Routing: 100%<br>Argument: 95%<br>Multiturn: 100% | [v1 run](../../starter_v0/runs/v1_B_base_openrouter_20261110T180324431405.json) |
| v2 | `starter_v0/artifacts/tools.yaml` (mô tả tool có sẵn) | Hợp đồng mô tả tool và tham số tường minh (tách query khỏi topic/timeframe, chuẩn hóa format handle) giúp chọn đúng đối số (R13) mà không cần đổi schema hay prompt. | Case Acc: 95% (19/20)<br>Routing: 100%<br>Argument: 95%<br>Multiturn: 100% | Case Acc: 95% (19/20)<br>Routing: 100%<br>Argument: 95%<br>Multiturn: 100% | [v2 run](../../starter_v0/runs/v2_B_base_openrouter_20261110T180621384845.json) |
| v3 | `starter_v0/artifacts/system_prompt.md` | Quy định thứ tự ưu tiên trong prompt (prompt precedence): yêu cầu đăng chưa duyệt phải đi qua bước xác nhận (yes_no) trước quy tắc thiếu thông tin (text), giúp sửa lỗi response_type ở R12 mà không gây hồi quy. | Case Acc: 95% (19/20)<br>Routing: 100%<br>Argument: 95%<br>Multiturn: 100% | Case Acc: 100% (20/20)<br>Routing: 100%<br>Argument: 100%<br>Multiturn: 100% | [v3 run](../../starter_v0/runs/v3_B_base_openrouter_20261110T180852592619.json) |

### B2. Failure Analysis

Nguồn baseline: [run v0 OpenRouter](../../starter_v0/runs/v0_B_base_openrouter_20261110T180041253555.json), model `openai/gpt-4o-mini`: 20/20 ca được đo, 0 lỗi provider, 15 PASS và 5 FAIL. Bảng dưới liệt kê toàn bộ 5 FAIL của v0; `Failure Type` giữ nguyên nhãn dataset/run, còn `Observed Mismatch` mô tả sai lệch thực tế của scorer. Nguyên nhân là giả thuyết phân tích; kết quả v1/v2 được đối chiếu trực tiếp từ run JSON.

| Case ID (v0) | Failure Type | Observed Mismatch | Actual Tool Calls | What Failed — nguyên văn | Nguyên nhân khả dĩ | Thay đổi và kết quả đo |
|---|---|---|---|---|---|---|
| `R08_out_of_scope` | `out_of_scope` | `unexpected_tool_call` | `[{"name":"send","args":{"text":"Nguyên hàm của x^2 là \\( \\frac{x^3}{3} + C \\), trong đó C là hằng số tùy ý."}}]` | `expected no tool call` | Prompt v0 bắt buộc gọi tool và chưa phân định yêu cầu ngoài phạm vi; mô tả send quá chung có thể khiến nó bị dùng để trả lời bài toán. | v1 thêm kiểm tra phạm vi trước hành động; R08 PASS ở v1 và v2. v2 làm rõ send là đăng Telegram, không phải kênh trả lời thông thường. |
| `R10_missing_handle` | `missing_info` | `missing_tool_call` | `[{"name":"timeline","args":{"screenname":"sama"}}]` | `missing tool call clarify`<br>`extra tool call timeline` | Prompt v0 yêu cầu tự chọn tài khoản nổi tiếng khi thiếu người đăng; model chọn sama dù người dùng chưa cung cấp tài khoản. | v1 yêu cầu clarify khi thiếu tài khoản, không đoán; R10 PASS ở v1 và v2. v2 bổ sung điều kiện handle đã xác định trong mô tả timeline. |
| `R11_missing_url` | `missing_info` | `missing_tool_call` | `[{"name":"fetch","args":{"url":"https://example.com/article"}}]` | `missing tool call clarify`<br>`extra tool call fetch` | Prompt v0 cho phép đoán URL khi chỉ có tham chiếu mơ hồ; model tự tạo URL example.com/article. | v1 yêu cầu clarify khi thiếu URL; R11 PASS ở v1 và v2. v2 mô tả fetch chỉ dùng URL có sẵn. |
| `R12_confirm_before_send` | `wrong_boundary` | `missing_tool_call` | `[{"name":"send","args":{"text":"Bản tin này"}}]` | `missing tool call clarify`<br>`extra tool call send` | Prompt v0 yêu cầu gửi ngay, chưa phân biệt yêu cầu đăng với xác nhận nội dung cụ thể; model gọi send thay vì hỏi xác nhận. | v1 và v2 đã chuyển sang clarify nhưng vẫn FAIL vì response_type=text thay vì yes_no. Không có lần gọi send ở R12 trong hai run này; xem bảng chi tiết bên dưới. |
| `R13_parallel_web_and_tweets` | `wrong_tool` | `wrong_arg_value` | `[{"name":"lookup","args":{"query":"AI news","timeframe":"day","max_results":5}},{"name":"social_search","args":{"query":"AI","search_type":"Latest","limit":5}}]` | `query: expected 'AI', got 'AI news'`<br>`topic: expected 'news', got None` | Đã chọn đủ lookup và social_search, nhưng gộp news vào query và bỏ topic. Khi thực thi, lookup dùng mặc định topic=general. | R13 đã PASS ở v1 dù mô tả tool chưa đổi, và tiếp tục PASS ở v2. v2 nêu rõ query theo chủ đề, topic=news và timeframe=day; không thể quy riêng kết quả PASS này cho v2. |

R13 giữ nhãn `wrong_tool` theo dataset, nhưng `routing_correct=true`, `args_correct=false` và `observed_mismatch=wrong_arg_value`: lỗi quan sát được nằm ở đối số. Không đổi nhãn dataset. Phân bố FAIL của v0 theo nhãn gốc: `missing_info=2`, `out_of_scope=1`, `wrong_boundary=1`, `wrong_tool=1`; hai nhóm `wrong_arg_value` và `unnecessary_tool` có 0 ca theo nhãn gốc.

Kiểm tra `tool_results` của cả 20 ca v0: không có kết quả chứa `error`. Hai lần gọi `send` ở R08 và R12 đều bỏ qua đối số `confirmed`, nên mặc định `false` trả về `status=needs_confirmation`; không có lần gửi Telegram thực tế trong baseline. Đây là lỗi chọn hành động của model, còn lớp chặn trong implementation đã hoạt động ở hai lần gọi này.

**Kết quả sau v1 và v2.** [Run v1](../../starter_v0/runs/v1_B_base_openrouter_20261110T180324431405.json) và [run v2](../../starter_v0/runs/v2_B_base_openrouter_20261110T180621384845.json) đều có 20/20 ca được đo, 0 lỗi provider, 19 PASS và 1 FAIL; routing đạt 20/20, argument đạt 19/20, multi-turn đạt 6/6. R08, R10, R11 và R13 chuyển từ FAIL ở v0 sang PASS ở v1 và giữ PASS ở v2. Không có ca hồi quy quan sát được trong hai lần chạy này. V2 không tăng điểm so với v1; lỗi duy nhất vẫn là R12, với lời gọi và thông báo lỗi giống nhau:

| Version | Case ID | Failure Type / Observed Mismatch | Actual Tool Calls | What Failed — nguyên văn |
|---|---|---|---|---|
| v1 | `R12_confirm_before_send` | `wrong_boundary` / `wrong_arg_value` | `[{"name":"clarify","args":{"question":"Bạn có thể cung cấp nội dung cụ thể của bản tin mà bạn muốn đăng lên Telegram không?","response_type":"text"}}]` | `response_type: expected 'yes_no', got 'text'` |
| v2 | `R12_confirm_before_send` | `wrong_boundary` / `wrong_arg_value` | `[{"name":"clarify","args":{"question":"Bạn có thể cung cấp nội dung cụ thể của bản tin mà bạn muốn đăng lên Telegram không?","response_type":"text"}}]` | `response_type: expected 'yes_no', got 'text'` |

Ở R12 của v1/v2, `routing_correct=true` nhưng `args_correct=false`: model hỏi xin nội dung bản tin bằng `clarify(response_type=text)`, tool trả `awaiting_user=true`, và **không gọi send**. Cách hỏi này giữ hành động đăng ở trạng thái chờ nhưng không đáp ứng quy ước `yes_no` của case. Vì vậy nhãn dataset `wrong_boundary` ở đây không phải bằng chứng đã gửi khi chưa được duyệt.

Giả thuyết cho lỗi còn lại: quy tắc chung “thiếu thông tin → text” trong prompt chồng lấn với quy tắc “yêu cầu đăng chưa được duyệt → yes_no” khi bản tin cũng chưa có nội dung. V2 đã nêu thứ tự ưu tiên trong mô tả clarify, nhưng hai run v1/v2 vẫn cho cùng kết quả R12; chưa có bằng chứng mô tả đã giải quyết được chồng lấn này.

**Kết quả thực nghiệm v3.** Theo [bản kế hoạch và phần amendment](../../starter_v0/runs/base_experiment_plan.md), v3 chỉ sửa prompt nhằm giải quyết chồng lấn giữa quy tắc xác nhận duyệt đăng và quy tắc hỏi thông tin còn thiếu: yêu cầu đăng chưa được duyệt phải đi qua bước xác nhận (`yes_no`) trước; quy tắc hỏi `text` chỉ áp dụng cho yêu cầu không phải đăng. Toàn bộ mô tả tool v2 giữ nguyên.

[Run v3](../../starter_v0/runs/v3_B_base_openrouter_20261110T180852592619.json) ghi nhận kết quả: 20/20 ca được đo, 0 lỗi provider, **20 PASS (100%)**, 0 FAIL; routing đạt 20/20 (1.0), argument đạt 20/20 (1.0), multi-turn đạt 6/6 (1.0).
- Case `R12_confirm_before_send` đã chuyển từ FAIL sang **PASS**: model gọi đúng `clarify` với `question="Bạn có thể cung cấp nội dung cụ thể của bản tin mà bạn muốn đăng lên Telegram không?"` và `response_type="yes_no"`.
- 19 ca còn lại đều giữ vững trạng thái PASS, xác nhận không có bất kỳ ca hồi quy (regression) nào phát sinh.

Thử nghiệm nhiều nguồn được hoãn sang vòng sau. Chỉ dẫn chọn một tool vẫn được giữ để tách riêng cơ chế của v3; đây là hạn chế đã biết, dù R13 gọi đủ hai tool ở v0/v1/v2/v3. Không gán cải thiện nhiều nguồn cho v3 hoặc thêm thay đổi xử lý ngữ cảnh khi cả 6 ca multi-turn hiện đều PASS.

Giới hạn phép đo: mỗi version mới có một run, không đủ để kết luận nhân quả hay độ ổn định thống kê. Scorer so khớp tool và tập đối số kỳ vọng, không chấm chất lượng nội dung trả lời hay kết quả API; ca `no_tool` chỉ kiểm tra không có lời gọi tool. Các quan sát trên không chứng minh nhiệm vụ research đã hoàn tất hoặc hệ thống an toàn trong mọi tình huống.

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/*.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
|  |  |  |  |  |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
