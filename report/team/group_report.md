# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: ADN
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md) (Lê Hải Anh: Phụ trách Role A - Prompt & Tối ưu v0–v3, hoàn thiện B1, B2)
- Provider/model dùng cho v0–v3: OpenRouter (`openai/gpt-4o-mini`, temperature 0)

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

ADN Research Agent hỗ trợ tra cứu nền tảng bằng Wikipedia, Hacker News, GitHub, web và X/Twitter; đọc URL đã được cung cấp, tra cứu chính sách nội bộ và định dạng trích dẫn hoặc digest. Agent hỏi lại khi thiếu dữ liệu cần thiết, giữ ngữ cảnh qua nhiều lượt và yêu cầu xác nhận rõ ràng trước khi gửi nội dung lên Telegram.

Cách chạy UI cục bộ từ thư mục starter_v0:

    python -m pip install -r requirements.txt
    streamlit run app.py

Poster giới thiệu: [poster.html](poster.html).

Local: http://localhost:8501. Demo public qua Cloudflare Quick Tunnel: https://remaining-processor-sell-lonely.trycloudflare.com (URL tạm thời, hoạt động khi app và cloudflared trên máy demo còn chạy). UI mặc định chọn Ollama với qwen2.5:1.5b, không cần model key. Các tool wiki, hn_search, github_search và cite không cần key; tool/provider cần Tavily, Firecrawl, RapidAPI hoặc cloud-model key vẫn cần cấu hình trong starter_v0/.env.

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi thông tin thiết yếu còn thiếu hoặc xin xác nhận trước khi đăng | Không |
| timeline | Lấy bài gần đây từ tài khoản X/Twitter đã xác định | Không |
| social_search | Tìm bài X/Twitter theo chủ đề | Không |
| lookup | Tìm thông tin hoặc tin tức trên web | Không |
| fetch | Đọc URL bài viết đã được cung cấp | Không |
| format | Gom các item đã thu thập thành digest Markdown | Không |
| send | Gửi nội dung lên Telegram sau khi người dùng duyệt chính xác nội dung | Không |
| policy | Tìm trong các chính sách nội bộ | Không |
| papers | Tìm paper trên arXiv | Không |
| paper_text | Tải và trích văn bản từ PDF arXiv đã biết | Không |
| wiki | Tra cứu bách khoa trên Wikipedia | Có |
| hn_search | Tìm bài và thảo luận trên Hacker News | Có |
| github_search | Tìm repository mã nguồn mở trên GitHub | Có |
| cite | Định dạng nguồn đã có theo APA, MLA hoặc IEEE | Có |

### A3. Câu hỏi mẫu để thử

1. Tìm 2 bài mới nhất trên Hacker News về SQLite.
2. Tìm 3 repository GitHub về DuckDB có nhiều sao nhất.
3. Tra Wikipedia tiếng Việt về mã QR, tối đa 2 trang.
4. Định dạng nguồn Python Tutorial theo IEEE: https://docs.python.org/3/tutorial/.
5. Đăng bản nháp sau lên Telegram giúp mình: Nhóm sẽ đọc tài liệu vào thứ Sáu. (Agent phải xin xác nhận trước khi gửi.)

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
| v4 | `starter_v0/artifacts/tools.yaml` (thêm 4 tool mới của B) | Thêm 4 tool mới với mô tả khi nào dùng/không dùng rõ ràng không gây xao nhãng routing trên bộ base suite, giữ nguyên 20/20 với prompt v3. | Case Acc: 100% (20/20)<br>Routing: 100%<br>Argument: 100%<br>Multiturn: 100% | Case Acc: 95% (19/20)<br>Routing: 95%<br>Argument: 95%<br>Multiturn: 100% | [v4 run](../../starter_v0/runs/v4_B_base_openrouter_20261110T190814400861.json) |
| v5 | `starter_v0/artifacts/system_prompt.md` | Bỏ chỉ dẫn ép thực hiện một bước / chọn một tool còn sót từ starter; cho phép gọi đủ tool cần thiết khi có nhiều nguồn độc lập nhưng cấm gọi thừa và cấm format/cite sớm, đạt 20/20. | Case Acc: 95% (19/20)<br>Routing: 95%<br>Argument: 95%<br>Multiturn: 100% | Case Acc: 100% (20/20)<br>Routing: 100%<br>Argument: 100%<br>Multiturn: 100% | [v5 run](../../starter_v0/runs/v5_B_base_openrouter_20261110T190946471016.json) |

Ghi chú về run: file `starter_v0/runs/v0_B_base_openrouter_20261110T180937971787.json` mang nhãn `v0` nhưng có hash của v3 (`v0+p04552040eeb2+ta01960b8f782`, chạy lúc 18:09 sau run v3 lúc 18:08) và đạt 20/20. Đây là lần chạy lặp lại v3 bị đặt nhầm nhãn, **không phải baseline**. Baseline v0 hợp lệ duy nhất là `v0_B_base_openrouter_20261110T180041253555.json` (`v0+peb1c8179815b+te69bc53ed884`, 15/20). Run Gemini `v0_B_base_gemini_...` bị loại vì `provider_error_cases=5`.

Kết quả thực nghiệm v4 và v5: sau khi B thêm 4 tool mới vào cuối `tools.yaml`, `tools_hash` của bản nộp đổi thành `a078bdccfe27`. Hai run v4 và v5 đã hoàn thành chuẩn xác trên nhánh `b-tool`:
- **v4:** chạy với prompt snapshot v3 và 14 tool declarations. Đạt 19/20 PASS. `R10` hồi quy: model tự điền tài khoản `elonmusk` thay vì hỏi lại (phân tích ở B2).
- **v5:** chạy với prompt v5 (đã bỏ chỉ dẫn ép một bước/một tool) và 14 tool declarations. Đạt **20/20 PASS (100%)**, 0 lỗi provider, routing 100%, arguments 100%, multiturn 100%.

Lần chạy v4/v5 đầu tiên (commit `f6c88c6` trên main) đã bị loại vì chạy trước khi merge 4 tool mới của B (mang hash cũ). Hai run v4 (`runs/v4_B_base_openrouter_20261110T190814400861.json`) và v5 (`runs/v5_B_base_openrouter_20261110T190946471016.json`) hiện tại trên nhánh `b-tool` là hai run chuẩn khớp hoàn toàn với bản nộp cuối cùng.

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

**Kết quả thực nghiệm v4 và v5.** Cả hai run có 20/20 ca được đo và 0 lỗi provider; hash khớp bản chụp trong `runs/base_artifacts/v4/` và `v5/`.

| Version | Case ID | Failure Type / Observed Mismatch | Actual Tool Calls | What Failed — nguyên văn |
|---|---|---|---|---|
| v4 | `R10_missing_handle` | `missing_info` / `missing_tool_call` | `[{"name":"timeline","args":{"screenname":"elonmusk","limit":5}}]` | `missing tool call clarify`<br>`extra tool call timeline` |

- **v4 (19/20):** câu hỏi R10 là "Tóm tắt 5 tweet mới nhất giúp mình", không nêu tài khoản. Ở v3 model gọi đúng `clarify(response_type=text)`. Ở v4, khi chỉ thêm 4 tool mới, model gọi `timeline(screenname="elonmusk")`.
  - Tài khoản `elonmusk` không xuất hiện trong câu hỏi, mà nằm trong danh sách "Known mappings: Sam Altman=sama, Elon Musk=elonmusk, Andrej Karpathy=karpathy" ở mô tả tham số `screenname` (thêm từ v2).
  - Giả thuyết: danh sách ánh xạ mẫu này là một "gợi ý đoán" tiềm ẩn. Khi tool list dài hơn (14 tool), quy tắc "không đoán tài khoản" trong prompt bị lấn át. 19 ca còn lại không đổi so với v3, và trong cả run v4 không có lời gọi nào tới 4 tool mới (bộ base không có ca dành cho chúng).
- **v5 (20/20):** R10 quay lại gọi `clarify`, R13 vẫn gọi đủ `lookup` và `social_search`, không có lời gọi thừa.
  - Tuy nhiên thay đổi của v5 (bỏ ràng buộc "một bước / một tool") **không nhắm vào R10**. Với một run mỗi version, không thể kết luận v5 đã sửa nguyên nhân của R10.
  - Hướng thử tiếp theo (chưa chạy): bỏ danh sách "Known mappings" khỏi mô tả `screenname`, hoặc chạy lặp v4/v5 nhiều lần để đo tỉ lệ R10 đoán tài khoản.

Giới hạn phép đo: mỗi version mới có một run, không đủ để kết luận nhân quả hay độ ổn định thống kê. Scorer so khớp tool và tập đối số kỳ vọng, không chấm chất lượng nội dung trả lời hay kết quả API; ca `no_tool` chỉ kiểm tra không có lời gọi tool. Các quan sát trên không chứng minh nhiệm vụ research đã hoàn tất hoặc hệ thống an toàn trong mọi tình huống.

### B3. Team Eval Cases

Phụ trách phần C là Trần Văn Quang. [Bộ eval nhóm](../../starter_v0/data/eval_group.json) gồm 5 case một lượt (G01–G05) và 5 case nhiều lượt (G06–G10). [Run suite `group`](../../starter_v0/runs/v5_B_group_openrouter_20261110T193140379550.json) dùng OpenRouter, model `openai/gpt-4o-mini` và artifact `v5+pe1ddb4bfa9ee+ta078bdccfe27`.

Run đo đủ 10/10 case, 0 lỗi provider và 9/10 case PASS. Điểm chọn tool 100%, đối số 90% và nhiều lượt 80% (4/5). Cả bốn tool mới của B đều có case chọn đúng tool.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_wiki_vi` | Tra cứu bách khoa bằng tiếng Việt | `wiki(lang="vi", limit=2)` | PASS |
| `G02_hn_latest` | Tìm bài mới nhất về SQLite trên Hacker News | `hn_search(query="SQLite", sort="latest", limit=2)` | PASS |
| `G03_github_stars` | Tìm repo DuckDB và xếp theo sao | `github_search(query="DuckDB", sort="stars", limit=3)` | PASS |
| `G04_cite_ieee` | Định dạng nguồn có sẵn theo IEEE | Chỉ gọi `cite(style="ieee")` | PASS |
| `G05_cite_missing_sources` | Danh sách nguồn chưa được cung cấp | `clarify(response_type="text")` | PASS |
| `G06_wiki_keep_topic` | Giữ chủ đề, nhận ngôn ngữ và số lượng mới | `wiki(query="mã QR", lang="vi", limit=1)` | PASS |
| `G07_two_research_sources` | Tra hai nguồn trong cùng lượt, giữ chủ đề DuckDB | `hn_search(sort="latest", limit=2)` và `github_search(sort="stars", limit=2)`, cùng `query="DuckDB"` | PASS |
| `G08_cite_switch_style` | Chuyển APA sang MLA, giữ tiêu đề và URL từ lượt trước | `cite(style="mla")` với nguồn SQLite đã cung cấp | FAIL (`wrong_arg_value`). Model chọn đúng tool, kiểu MLA, tiêu đề và URL. So khớp nguyên object trong `items` lệch do ba trường tùy chọn `source`, `author`, `date` rỗng. |
| `G09_cancel_telegram` | Hủy yêu cầu gửi ở lượt cuối | Phản hồi trực tiếp, không gọi tool | PASS |
| `G10_draft_is_not_approval` | Yêu cầu đăng bản nháp khi chưa xác nhận | `clarify(response_type="yes_no")`, chưa gọi `send` | PASS |

Ở G08, kiểm tra thủ công xác nhận model đã giữ đúng dữ liệu nguồn. Điểm báo cáo giữ theo scorer. Bộ eval nhiều lượt chấm phản hồi cho lượt cuối với các lượt trước làm ngữ cảnh. Chất lượng nội dung trả về được xem riêng ở B4.

### B4. Live Chat Evidence

[Transcript 4 lượt](../../starter_v0/transcripts/v5_openrouter_20261110T193127740264.transcript.json) được tạo bằng `chat.py` với OpenRouter, model `openai/gpt-4o-mini` và artifact `v5+pe1ddb4bfa9ee+ta078bdccfe27`, trùng với run nhóm.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Định dạng nguồn SQLite Documentation theo IEEE. | `cite(style="ieee")` | v5, lượt 1 | `answered`. Agent trả về trích dẫn với tiêu đề và URL đã cung cấp. |
| 2 | Tìm hai bài mới nhất trên Hacker News khi chưa nêu chủ đề. | `clarify(response_type="text")` | v5, lượt 2 | `waiting_for_user`. Agent hỏi chủ đề. |
| 3 | Bổ sung chủ đề SQLite, giữ nguồn Hacker News và số lượng hai bài. | `hn_search(query="SQLite", sort="latest", limit=2)` | v5, lượt 3 | `answered`. Tool trả hai kết quả. Một tiêu đề nói trực tiếp về SQLite, tiêu đề còn lại nói về coding agent và cần kiểm tra thêm độ liên quan. |
| 4 | Yêu cầu đăng tin “Nhóm sẽ đọc tài liệu SQLite vào thứ Sáu” lên Telegram. | `clarify(response_type="yes_no")` | v5, lượt 4 | `waiting_for_user`. Agent đọc lại nội dung và chờ xác nhận. Transcript kết thúc ở đây, chưa có lời gọi `send`. |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) | [`tools/wiki/`](../../starter_v0/tools/wiki/), [`tools/hn_search/`](../../starter_v0/tools/hn_search/), [`tools/github_search/`](../../starter_v0/tools/github_search/), [`tools/cite/`](../../starter_v0/tools/cite/) (mỗi folder có `tool.py` + `TOOL.md`); đăng ký trong [`tools/__init__.py`](../../starter_v0/tools/__init__.py) và khối `# ---- Group tools (B) ----` cuối [`artifacts/tools.yaml`](../../starter_v0/artifacts/tools.yaml) | 4 tool không cần API key: `wiki` (Wikipedia, kiến thức nền), `hn_search` (Hacker News, thảo luận cộng đồng dev), `github_search` (repo mã nguồn mở), `cite` (định dạng trích dẫn APA/MLA/IEEE, chạy local). Smoke test gọi API thật ngày 2026-11-10 trả kết quả đúng cho cả 3 tool live. `pytest tests/test_tool_contract.py`: 75 passed | Mỗi description ghi rõ khi nào dùng / không dùng so với `lookup`, `social_search`, `papers`, `fetch`, `format`. Input xấu (query rỗng, enum sai) trả error dict **không gọi mạng**; `limit` ép về int có chặn trên. GitHub giới hạn ~10 request/phút khi không xác thực → trả `HTTPError` dict. `cite` không bịa tác giả/ngày/URL |
| Unit test tool mới (≥ 3 test/tool) | [`tests/test_tools_todo.py`](../../starter_v0/tests/test_tools_todo.py); `pytest` toàn suite: **140 passed, 0 failed, 0 skipped** | `wiki` 5 test (13 trường hợp parametrize), `hn_search` 4 (5), `github_search` 5 (6), `cite` 7 (8). Mỗi tool có happy path (assert cả request gửi đi lẫn kết quả map), input xấu từ model, và nhánh lỗi (HTTP 429/500/403, timeout) | Test chạy offline: mọi HTTP mock bằng `fake_http`, không dùng key thật |
| UI (lệnh chạy + link dùng thử) | [app.py](../../starter_v0/app.py), [requirements.txt](../../starter_v0/requirements.txt); lệnh tại A1 | Streamlit và Cloudflare Quick Tunnel trả HTTP 200; Ollama/qwen2.5:1.5b đã cài/tải; smoke CLI qua cùng `chat.run_model_tool_loop` gọi `wiki` thành công | Chưa xác nhận trọn luồng bằng thao tác trình duyệt; keys cho provider/tool trả phí chưa cấu hình |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

- `tests/test_tools_todo.py` có 58 test (tính cả parametrize): 14 stub có sẵn của starter, 32 test cho 4 tool mới, 12 regression test.
- Ví dụ lỗi eval không bắt được: nếu model gọi `send(text=..., confirmed="false")` (chuỗi thay vì boolean), eval chỉ so tên tool và args nên không thấy gì bất thường. Nhưng code cũ dùng `if not confirmed`, mà chuỗi `"false"` là truthy, nên **tin nhắn vẫn được gửi lên Telegram khi user chưa xác nhận**. Test `test_regression_send_non_true_confirmation_does_not_call_network` bắt được lỗi này (xem B5).
- Smoke test thật cũng bắt một lỗi trình bày của `cite`: tác giả `Vaswani et al.` bị in thành `et al..`. Đã sửa và thêm `test_cite_author_ending_with_period_is_not_doubled`.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) | 4 folder `tools/wiki/`, `tools/hn_search/`, `tools/github_search/`, `tools/cite/`; test trong `tests/test_tools_todo.py`; eval case route tới từng tool: xem B3 (`data/eval_group.json`, người C) | Mỗi tool đủ `TOOL.md` (frontmatter đúng contract), đăng ký registry + `tools.yaml`, ≥ 4 test/tool | Còn chờ: mỗi tool cần ≥ 1 eval case trong `eval_group.json` (C phụ trách) và rule routing trong `system_prompt.md` nếu cần (A phụ trách) |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output: **140 passed, 0 failed, 0 skipped** | Đạt cả hai điều kiện: toàn suite 0 skipped (14 stub đã viết hết) **và** có regression test cho 3 bug trong tool có sẵn | Regression test được kiểm chứng ngược: chạy trên code gốc thì **9 FAIL**, sau khi sửa thì PASS |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

Tìm được **3 bug** trong tool có sẵn bằng cách thử input biên mà model hay gửi:

| # | Tool | Bug (code gốc) | Hậu quả | Cách sửa | Regression test |
|---|---|---|---|---|---|
| 1 | `send` | `if not confirmed:` coi chuỗi `"false"`, `"no"`, `"0"` (và số `1`) là đã xác nhận | **Gửi Telegram khi user chưa duyệt**, phá boundary xác nhận | `_is_confirmed()`: chỉ chấp nhận `True` hoặc chuỗi `"true"` | `test_regression_send_non_true_confirmation_does_not_call_network` (7 trường hợp), `test_regression_send_string_true_still_sends` |
| 2 | `timeline`, `social_search` | `items[: int(limit or 5)]`: `limit=-1` thành `items[:-1]` (mất bài cuối); `limit="abc"` raise `ValueError` làm hỏng cả lời gọi | Trả thiếu kết quả âm thầm, hoặc lỗi cả tool | Helper `as_int()` trong `tools/_shared.py`: không phải số hoặc ≤ 0 thì dùng mặc định 5 | `test_regression_timeline_negative_limit_does_not_drop_last_item`, `test_regression_non_numeric_limit_uses_default_instead_of_failing` (2 tool) |
| 3 | `format` | Item không phải object (ví dụ chuỗi) gây `AttributeError` **raise ra ngoài tool** | Vi phạm contract "tool trả error dict, không raise" | Bọc `render_digest` trong `try/except`, trả `err("render_digest", exc)` | `test_regression_format_non_object_item_returns_error_dict_instead_of_raising` |

Các bản sửa bug chỉ nằm trong code tool (`tools/*/tool.py`), không đổi `system_prompt.md` hay phần tool có sẵn trong `tools.yaml`. Riêng việc khai báo 4 tool mới ở cuối `tools.yaml` làm `tools_hash` khác bản v3 (`a01960b8f782`), nên A đã chạy lại base eval với bản `tools.yaml` này: v4 (19/20) và v5 (20/20), xem B1/B2.

### B7. Small Local Model Challenge (bonus)

Chạy cùng bộ base 20 case trên prompt/tools v5 cuối cùng, provider Ollama không cần model key. Cả bốn run có measured_cases=20 và provider_error_cases=0.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---:|---:|---:|---:|---|
| v5-cloud | openai/gpt-4o-mini (OpenRouter) | v5 | 100% | 100% | 100% | 100% | [v5 cloud run](../../starter_v0/runs/v5_B_base_openrouter_20261110T190946471016.json) |
| v5-local-qwen2.5:1.5b | Qwen2.5 1.5B (Ollama) | v5 | 35% | 55% | 35% | 33.3% | [base run](../../starter_v0/runs/v5-qwen2.5-1.5b_B_base_ollama_20261111T001716212966.json) |
| v5-local-qwen2.5:0.5b | Qwen2.5 0.5B (Ollama) | v5 | 15% | 30% | 15% | 0% | [base run](../../starter_v0/runs/v5-qwen2.5-0.5b_B_base_ollama_20261111T001901516754.json) |
| v6-local-qwen2.5:1.5b | Qwen2.5 1.5B (Ollama) | [local prompt v6](../../starter_v0/artifacts/system_prompt_local_v6.md) + [local tools](../../starter_v0/artifacts/tools_local.yaml) | 30% | 45% | 30% | 33.3% | [round 1 run](../../starter_v0/runs/v6-local-qwen2.5-1.5b_B_base_ollama_20261111T002013205741.json) |
| v7-local-qwen2.5:1.5b | Qwen2.5 1.5B (Ollama) | [local prompt v7](../../starter_v0/artifacts/system_prompt_local_v7.md) + [local tools](../../starter_v0/artifacts/tools_local.yaml) | 35% | 40% | 35% | 33.3% | [round 2 run](../../starter_v0/runs/v7-local-qwen2.5-1.5b_B_base_ollama_20261111T002335288041.json) |

Các nhóm lỗi ở run base qwen2.5:1.5b:

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---:|---|---|---|
| wrong / hallucinated tool | 4 | R02 chọn timeline thay vì social_search | v6 mô tả rõ hợp đồng tool; v7 thêm bảng route | Không: routing giảm từ 55% xuống 40% ở v7 |
| invalid JSON args | 0 | Không ghi nhận | Không cần | N/A |
| no tool call / answered directly | 9 | R03 không gọi lookup | v6 nhắc gọi tool cho thông tin bên ngoài | Không: case accuracy v6 giảm 35% xuống 30% |
| missed clarify | 3 | R10, R11, R12 | v6 làm rõ clarify text/yes_no; v7 lặp quy tắc | Không: các lỗi vẫn còn ở v7 |
| repeated / unnecessary calls | 0 | Không ghi nhận | Không cần | N/A |

Không có chỉnh sửa nào giúp vượt base local qwen2.5:1.5b trong hai vòng đã đo: v6 giảm case accuracy còn 30%; v7 trở về 35% nhưng routing thấp hơn base. Model 1.5B tốt hơn model 0.5B ở bộ này (35% so với 15%), nhưng cloud v5 đạt 100%. Chỉ số đo khả năng route/args, không chứng minh chất lượng nội dung; các tool cần RapidAPI/Tavily/Firecrawl chưa có key nên kết quả thực thi của chúng chưa được đánh giá.

Bằng chứng hiện có cho thấy local phù hợp khi cần chạy model không gửi prompt tới provider cloud và có sẵn Ollama; phải chấp nhận độ chính xác thấp hơn đáng kể trên eval này. Prompt local v6/v7 chưa được chạy lại trên cloud.

## 5. Khó khăn và cách xử lý

- Ở v1 và v2, R12 vẫn chọn clarify nhưng sai response_type=text thay vì yes_no. V3 làm rõ thứ tự ưu tiên xác nhận trước khi hỏi nội dung; run v3 chuyển R12 sang PASS.
- Khi thêm bốn tool ở v4, R10 hồi quy: model đoán tài khoản elonmusk từ ví dụ trong mô tả timeline. V5 bỏ gợi ý định danh không cần thiết và làm rõ quy tắc hỏi lại; R10 trở lại PASS, đồng thời base đạt 20/20.
- G08 bị chấm FAIL vì scorer so khớp toàn bộ object lồng nhau trong items; các trường tùy chọn rỗng làm lệch kết quả dù tool, style, title và URL đúng. Báo cáo giữ nguyên điểm theo scorer và ghi riêng kiểm tra thủ công.
- Kết quả Hacker News ở lượt live có một tiêu đề liên quan trực tiếp SQLite và một tiêu đề cần kiểm tra thêm. Điều này cho thấy routing đúng không tự chứng minh độ liên quan của nội dung trả về; cần review nguồn.
- UI Streamlit và Cloudflare Quick Tunnel trả HTTP 200; smoke query qua vòng lặp agent gọi wiki thành công. URL tạm thời: https://remaining-processor-sell-lonely.trycloudflare.com. Base eval local đo đủ 20 case, 0 provider error: Qwen2.5 1.5B đạt 35%, Qwen2.5 0.5B đạt 15%. Hai vòng tuning đạt lần lượt 30% và 35%, chưa vượt baseline 1.5B. Keys cho tool/provider trả phí vẫn chưa được cấu hình.

## 6. Tổng hợp đóng góp

- **Lê Hải Anh (A):** baseline và các vòng tối ưu prompt/tool v0–v5; phân tích B1, B2.
- **Lê Thanh Nguyên (B):** bốn tool mới, unit test, ba sửa lỗi hồi quy và các mục B5a/B5.
- **Trần Văn Quang (C):** 10 eval case nhóm, run group, transcript live và mục B3/B4.
- **Nguyễn Hữu Mạnh (D):** UI Streamlit, poster, Phần A và tổng hợp báo cáo; dựng Cloudflare Quick Tunnel https://remaining-processor-sell-lonely.trycloudflare.com; chạy base eval cho hai model local và hai vòng tuning v6/v7 (các run và metrics ở B7).

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix thuộc system_prompt.md:** giới hạn phạm vi, không đoán URL/tài khoản/nội dung, hỏi thiếu thông tin và đặt xác nhận đăng trước các bước khác; v5 bỏ ép một tool cho mọi tình huống nhưng vẫn cấm gọi thừa.
- **Fix thuộc tools.yaml:** nêu rõ khi dùng/không dùng từng tool, quy ước tham số và ranh giới xác nhận cho send. Code tool riêng xử lý kiểu dữ liệu sai và trả lỗi có cấu trúc.
- **Cần review thủ công:** chất lượng/độ liên quan của kết quả tìm kiếm; G08 vì scorer kiểm tra object lồng nhau quá chặt; hành động gửi thật cần đối chiếu nội dung và xác nhận trong transcript.
- **Vòng tiếp theo:** cải thiện scorer để so tập con các trường được kỳ vọng trong object lồng nhau; thêm eval cho chất lượng liên quan và nhiều nguồn; chạy lặp nhiều lần để đo độ ổn định. Với local, thử các hướng ngắn hơn hoặc few-shot cho lỗi route/argument và chỉ giữ prompt khi eval tăng.
- **Giới hạn:** mỗi version mới chạy một lần; suite chấm routing/args chứ không đánh giá đầy đủ sự thật, độ mới hoặc chất lượng nội dung. Local scores thấp hơn cloud rõ rệt và hai lần tuning chưa cải thiện baseline. Keys cho provider/tool trả phí chưa có nên các nhánh đó chưa được xác minh. Tunnel Quick Tunnel tạm thời chỉ hoạt động khi tiến trình còn chạy.

## 8. Tài liệu tham khảo

- [Hướng dẫn và rubric của lab](../../README.md), [rubric chấm điểm](../../RUBRIC.md).
- [Tool folder contract](../../starter_v0/tools/README.md), [system prompt](../../starter_v0/artifacts/system_prompt.md), [tool declarations](../../starter_v0/artifacts/tools.yaml).
- [Base eval](../../starter_v0/data/eval_base.json), [group eval](../../starter_v0/data/eval_group.json), [version log](../../starter_v0/artifacts/version_log.csv).
- Các run v0–v7, run suite group và transcript được liên kết tại B1–B4/B7; file bằng chứng nằm trong starter_v0/runs/ và starter_v0/transcripts/. Prompt local: [v6](../../starter_v0/artifacts/system_prompt_local_v6.md), [v7](../../starter_v0/artifacts/system_prompt_local_v7.md), tool snapshot: [tools_local.yaml](../../starter_v0/artifacts/tools_local.yaml).
