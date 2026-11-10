# Team

## Thông tin nhóm

- Tên nhóm:
- Lớp: L3A / L3B
- Repo nhóm: `K5-L3A-DAY03-TenNhom-ResearchAgentToolEval` hoặc `K5-L3B-DAY03-TenNhom-ResearchAgentToolEval` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Lê Hải Anh |      |       |        | Role A (Prompt & tối ưu v0–v3: C1, C2, C3) |
|   2 |        |      |       |        |         |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## LeHaiAnh-MSSV

### Phần việc phụ trách

- Phụ trách Role A (Prompt và tối ưu v0–v3, C1, C2, C3):
  - Chạy baseline v0, gán loại lỗi và phân tích 5 case FAIL.
  - Tối ưu `artifacts/system_prompt.md` và viết lại mô tả tool có sẵn trong `artifacts/tools.yaml`.
  - Thực nghiệm chu trình giả thuyết v1 -> v2 -> v3 trên base suite, ghi log `version_log.csv`.
  - Hoàn thiện mục B1 (Version Evidence) và B2 (Failure Analysis) trong `report/team/group_report.md`.

### Đóng góp cụ thể

- Phân tích nguyên nhân gốc của 5 ca FAIL ở baseline v0 (`R08`, `R10`, `R11`, `R12`, `R13`).
- Thiết lập ranh giới tool, viết lại description tường minh khi nào dùng/không dùng và quy ước tham số (`lookup`, `social_search`, `timeline`, `send`).
- Cải thiện qua 3 phiên bản đạt độ chính xác tuyệt đối: v0 (75%) -> v1 (95%) -> v2 (95%) -> v3 (100% case accuracy, 100% routing, 100% args, 100% multiturn).
- Đảm bảo 55/55 tool contract tests xanh (`pytest tests/test_tool_contract.py`).

### Bằng chứng

- Artifacts: `starter_v0/artifacts/system_prompt.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/artifacts/version_log.csv`.
- Runs: `starter_v0/runs/v0_B_base_openrouter_20261110T180041253555.json` đến `starter_v0/runs/v3_B_base_openrouter_20261110T180852592619.json`.
- Báo cáo: Mục B1, B2 trong `report/team/group_report.md`.
