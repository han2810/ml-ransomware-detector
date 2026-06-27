# Cuckoo Web

Ứng dụng gồm backend Flask và frontend React/Vite. Backend gửi mẫu tới Cuckoo,
trích xuất 9 nhóm đặc trưng hành vi, tạo Excel và dự đoán bằng model hiện có.

## Cấu trúc

- `backend/app/api`: route HTTP, không chứa logic xử lý.
- `backend/app/services`: điều phối Cuckoo, report, feature, Excel và model.
- `backend/app/parsers`: 9 parser độc lập theo từng nhóm hành vi.
- `backend/app/mappings`: tên đặc trưng đầu vào của model.
- `backend/app/ml`: model và hàm inference.
- `frontend/src`: pages, components và API client.

## Chạy backend

```powershell
cd backend
python -m pip install -r requirements.txt
python -m app.main
```

Sửa `backend/.env`, đặc biệt `CUCKOO_API_URL` và `CUCKOO_API_TOKEN`, cho đúng
máy Cuckoo. Backend mặc định chạy tại `http://127.0.0.1:5000`.

## Chạy frontend

```powershell
cd frontend
npm install
npm run dev
```

Mở `http://127.0.0.1:5173`. Vite proxy `/api` sang backend trong môi trường dev.

## API chính

- `POST /api/upload`: upload multipart với field `file`.
- `GET /api/tasks`: danh sách lịch sử.
- `GET /api/tasks/<task_id>`: trạng thái và kết quả.
- `GET /api/reports/<task_id>`: tải report JSON.
- `GET /api/excels/<task_id>`: tải feature Excel.
- `POST /api/predict/<task_id>`: chạy lại model từ Excel đã tạo.

> Chỉ phân tích file bạn có quyền kiểm thử. Không chạy trực tiếp mẫu trên máy host.
