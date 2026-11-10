# Báo cáo cá nhân — Nguyen Huu Manh

## 1. Thông tin thành viên

| Mục | Thông tin |
|---|---|
| Họ tên | Nguyen Huu Manh |
| MSSV | 2A202604015 |
| Email | Chưa cung cấp |
| Nhóm và lớp | ADN — L3B |
| Vai trò | D — UI, demo và tổng hợp báo cáo |

## 2. Phần việc phụ trách

- Bổ sung giao diện Streamlit cho research agent, dependency và hướng dẫn chạy local.
- Hoàn thiện Phần A và các mục báo cáo tổng hợp còn thiếu theo mẫu.
- Demo public: https://remaining-processor-sell-lonely.trycloudflare.com. Đã chạy base eval trên Qwen2.5 1.5B/0.5B và hai vòng tuning local v6/v7; kết quả tại B7.

## 3. Đóng góp cụ thể

- Tạo starter_v0/app.py để chat nhiều lượt, chọn provider/model, xem tool events và ghi transcript JSON.
- Thêm Streamlit vào starter_v0/requirements.txt; lệnh chạy được ghi ở A1 trong báo cáo nhóm và trên poster.
- Hoàn thiện giới thiệu agent, bảng tool, câu hỏi demo, mục UI B5a, khó khăn, tổng hợp đóng góp, reflection và tài liệu tham khảo trong report/team/group_report.md.
- Tạo báo cáo này theo mẫu. Email chưa được điền vì không có trong repo.

## 4. Bằng chứng

- File: starter_v0/app.py, starter_v0/requirements.txt, report/team/poster.html, report/team/group_report.md.
- Commit/PR: commit D được tạo local; chưa push lên nhánh nộp.
- AI/công cụ: Codex hỗ trợ đọc cấu trúc repo, tạo UI và tổng hợp báo cáo. Streamlit và URL public trả HTTP 200; smoke query gọi model Ollama qwen2.5:1.5b cùng tool wiki thành công. Hai local models và hai vòng tuning đã có run JSON ở starter_v0/runs/. Các provider/tool cần key trả phí phải được cấu hình trong starter_v0/.env.

## 5. Tự đánh giá

Phần giao diện và tài liệu chạy local đã được bổ sung theo cấu trúc hiện có của chat.py và transcript JSON. UI và tunnel đang hoạt động; một truy vấn thật qua agent đã gọi wiki thành công. Base eval đo đủ 20 case cho hai model local; hai vòng tuning được ghi ở B7. Các tool cần key trả phí chưa được xác minh.
