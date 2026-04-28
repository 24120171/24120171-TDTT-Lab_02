1.Thông tin sinh viên
    Họ và tên: Nguyễn Khánh Đăng
    Mã số sinh viên: 24120171
    Lớp: 24CTT3
    Khoa: Công nghệ Thông tin - ĐH Khoa học Tự nhiên TP.HCM
2.Tính năng chính
    Xác thực người dùng: Đăng ký, Đăng nhập/Đăng xuất bằng Firebase Authentication (Email/Password & Google Login).
    Quản lý Task: Thêm công việc mới kèm mô tả và hạn chót (Deadline).
    Cập nhật: Đánh dấu hoàn thành công việc ngay trên giao diện.
    Xóa: Loại bỏ các công việc không còn cần thiết.
    Lưu trữ: Dữ liệu được đồng bộ hóa thời gian thực trên Cloud Firestore theo từng tài khoản riêng biệt.
3.Hướng dẫn cài đặt thư viện.
    pip install -r requirements.txt
4.Cách chạy ứng dụng
    Mở một terminal và chạy lệnh: uvicorn backend.app.main:app --reload
        API sẽ khả dụng tại: http://127.0.0.1:8000
    Mở một terminal khác và chạy lệnh: streamlit run frontend/app.py
        Ứng dụng sẽ tự động mở tại: http://localhost:8501

https://github.com/user-attachments/assets/015e1080-12e9-4005-9b9f-f2f6eba357ff





