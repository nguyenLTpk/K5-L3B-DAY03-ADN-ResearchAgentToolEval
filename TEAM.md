# Team

## Thông tin nhóm

- Tên nhóm: ADN
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-ADN-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- Demo UI (Quick Tunnel, link tạm thời): https://remaining-processor-sell-lonely.trycloudflare.com (cần giữ app và cloudflared đang chạy).
- URL repo, nhánh nộp, commit chốt: https://github.com/nguyenLTpk/K5-L3B-DAY03-ADN-ResearchAgentToolEval · nhánh main · commit chốt: chưa chốt sau các thay đổi UI/báo cáo.

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Hải Anh | 2A202603986 | lehaianh252005@gmail.com |  | A — Prompt & tối ưu (C1, C2, C3) |
|   2 | Lê Thành Nguyên | 2A202603733 | nguyenngungonvc@gmail.com | nguyenLTpk | B — Tool mới & unit test (C4) |
|   3 | Trần Văn Quang | 2A202604032 |  |  | C — Eval nhóm & live chat (C5, C6 transcript) |
|   4 | Nguyễn Hữu Mạnh | 2A202604015 |  |  | D — UI, demo & tổng hợp báo cáo (C6 UI, C7) |

## Quy ước phân quyền file (tránh conflict)

Mỗi file dùng chung chỉ một người sửa. Ai cần thay đổi file của người khác thì gửi yêu cầu cho chủ file.

| Người | File được sửa |
| ----- | ------------- |
| A — Lê Hải Anh | `starter_v0/artifacts/system_prompt.md`; `starter_v0/artifacts/tools.yaml` (phần tool có sẵn); `starter_v0/artifacts/version_log.csv`; `starter_v0/runs/` (suite base); group report mục B1, B2 |
| B — Lê Thành Nguyên | `starter_v0/tools/<tool_mới>/`; `starter_v0/tools/__init__.py`; `starter_v0/tests/test_tools_todo.py`; khối `# ---- Group tools (B) ----` ở cuối `tools.yaml`; group report mục B5a (phần tool/test), B5 |
| C — Trần Văn Quang | `starter_v0/data/eval_group.json`; `starter_v0/runs/` (suite group); `starter_v0/transcripts/` (từ `chat.py`); group report mục B3, B4 |
| D — Nguyễn Hữu Mạnh | `starter_v0/app.py` (UI); `starter_v0/requirements.txt`; `report/team/poster.html`; phần thông tin chung của `TEAM.md`; group report Phần A, B5a (phần UI), B7, mục 1, 5–8; `version_log.csv` các dòng local (sau khi A chốt version cuối) |

Phối hợp:

- B đã merge 4 tool mới (`wiki`, `hn_search`, `github_search`, `cite`) vào `tools.yaml`. A đã chạy lại v4 (thêm tool) và v5 (bỏ ép một bước) khớp bản nộp.
- C dành đủ case trong 10 case của `eval_group.json` để kiểm tra route tới 4 tool mới của B (≥ 1 case/tool cho bonus).
- Rule routing cho tool mới và boundary xác nhận của `send`: B/C gửi yêu cầu, A sửa `system_prompt.md` (mỗi thay đổi là một version mới, chạy lại base eval).
- Bonus Small Local Model (D) dùng file riêng `system_prompt_local.md`, `tools_local.yaml`, chạy trên bản prompt/tools cuối (v5).

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

## LeHaiAnh-2A202603986

Báo cáo cá nhân: [`report/team/2A202603986_LeHaiAnh.md`](report/team/2A202603986_LeHaiAnh.md)

### Phần việc phụ trách

- Người A — Prompt & tối ưu (C1, C2, C3).
- Chạy baseline v0 (chưa sửa artifact), gán loại lỗi cho từng case FAIL.
- Sửa `artifacts/system_prompt.md` và `artifacts/tools.yaml` (phần tool có sẵn): bỏ chỉ dẫn xấu, thêm rule routing, viết lại description (khi nào dùng/không dùng), convention args, boundary xác nhận của `send`.
- Chạy các version tối ưu (mỗi version một giả thuyết), ghi `artifacts/version_log.csv`.
- Viết mục B1 (Version Evidence), B2 (Failure Analysis) trong group report.

### Đóng góp cụ thể

- Phân tích 5 case FAIL của baseline v0 (`R08`, `R10`, `R11`, `R12`, `R13`).
- Kết quả qua 6 version (case accuracy):

  | Version | Case accuracy | Thay đổi |
  |---|---|---|
  | v0 | 75% | Baseline, chưa sửa gì |
  | v1 | 95% | Kiểm tra phạm vi, thông tin thiếu, duyệt trước khi đăng |
  | v2 | 95% | Mô tả tool tường minh |
  | v3 | 100% | Thứ tự ưu tiên trong prompt cho xác nhận đăng |
  | v4 | 95% | Thêm 4 tool của B |
  | v5 | 100% | Bỏ chỉ dẫn ép một bước / một tool |

### Bằng chứng

- `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv` (v0–v5).
- Run hợp lệ: `starter_v0/runs/v0_…180041…json`, `v1_…180324…`, `v2_…180621…`, `v3_…180852…`, `v4_…190814…`, `v5_…190946…`.
- Kế hoạch thí nghiệm: `starter_v0/runs/base_experiment_plan.md`; snapshot `starter_v0/runs/base_artifacts/v0`–`v5`.
- Commit: `59b5b8c` (CP1–3), `189e1c8`, `4a1082a` (v4, v5).

## LeThanhNguyen-2A202603733

Báo cáo cá nhân: [`report/team/2A202603733_LeThanhNguyen.md`](report/team/2A202603733_LeThanhNguyen.md)

### Phần việc phụ trách

- Người B — Tool mới & unit test (C4).
- Viết tool mới trong `tools/<tên>/` (`tool.py` + `TOOL.md`), đăng ký trong `tools/__init__.py` và khối Group tools ở cuối `artifacts/tools.yaml`.
- Viết ≥ 3 unit test/tool trong `tests/test_tools_todo.py` (happy path, input xấu, nhánh lỗi); giữ `pytest` 0 failed.
- Bonus: ≥ 4 tool mới, test challenge (0 skipped hoặc regression test).
- Viết mục B5a (phần tool/test), B5 trong group report.

### Đóng góp cụ thể

- 4 tool mới, đều không cần API key:
  - `wiki`: tra cứu Wikipedia.
  - `hn_search`: tìm bài trên Hacker News.
  - `github_search`: tìm repo GitHub.
  - `cite`: định dạng trích dẫn APA/MLA/IEEE.
- 58 test trong `tests/test_tools_todo.py`: 32 test cho 4 tool mới, 14 stub của starter, 12 regression test.
- Sửa 3 bug trong tool có sẵn:
  - `send`: `confirmed="false"` vẫn gửi Telegram.
  - `timeline` / `social_search`: `limit` âm hoặc không phải số gây sai kết quả hoặc lỗi.
  - `format`: raise exception thay vì trả error dict.

### Bằng chứng

- `starter_v0/tools/wiki/`, `hn_search/`, `github_search/`, `cite/`; `starter_v0/tools/__init__.py`; `starter_v0/tests/test_tools_todo.py`.
- `pytest`: 140 passed, 0 failed, 0 skipped. 9 regression test FAIL trên code gốc và PASS sau khi sửa.
- Commit: `bba92d1` (tool + test + bug fix).

## TranVanQuang-2A202604032

Báo cáo cá nhân: `report/team/2A202604032_TranVanQuang.md`

### Phần việc phụ trách

- Người C — Eval nhóm & live chat (C5, transcript của C6).
- Viết đúng 10 case trong `data/eval_group.json` (5 single turn + 5 multi turn), ≥ 1 case route tới mỗi tool mới; chạy `--suite group`.
- Chạy `chat.py` ≥ 3 lượt live (yêu cầu thường, thiếu thông tin rồi bổ sung, yêu cầu gửi/đăng), lưu `transcripts/`.
- Bonus: gửi Telegram thật sau khi user xác nhận.
- Viết mục B3 (Team Eval Cases), B4 (Live Chat Evidence) trong group report.

### Đóng góp cụ thể

-

### Bằng chứng

-

## NguyenHuuManh-2A202604015

Báo cáo cá nhân: `report/team/2A202604015_NguyenHuuManh.md`

### Phần việc phụ trách

- Người D — UI, demo & tổng hợp báo cáo (UI của C6, C7).
- Làm UI Streamlit (`app.py`), thêm dependency vào `requirements.txt`, mở link dùng thử (Cloudflare Tunnel) cho Team showdown.
- Viết Phần A của group report trước 16:30 (+ poster tùy chọn); tổng hợp mục 1, 5–8 và phần UI của B5a.
- Bonus: Small Local Model Challenge (sau khi A chốt version cuối), viết mục B7.

### Đóng góp cụ thể

-

### Bằng chứng

-
