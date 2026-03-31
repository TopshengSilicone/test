# Chatter CC/BCC (Odoo 19.0.1.0.0)

Module thêm 2 ô **CC** và **BCC** trực tiếp ở phần chatter **Send message**.

## Tính năng
- Hiển thị 2 ô nhập CC/BCC ngay trong chatter.
- Không can thiệp luồng gửi chuẩn: vẫn gọi `postMessage` mặc định trước, sau đó mới ghi CC/BCC vào `mail.message`.
- Có fallback backend nếu payload gửi sẵn `cc_emails`/`bcc_emails`.

## Cài đặt nhanh
1. Đặt thư mục `chatter_cc_bcc` trong `custom_addons`.
2. Đảm bảo `addons_path` có `custom_addons` trong `odoo.conf` (phân tách bằng dấu phẩy).
3. Restart Odoo.
4. Vào Apps -> Update Apps List -> cài **Chatter CC/BCC**.

## Lưu ý nếu vẫn không gửi được
- Mở Developer Tools của trình duyệt và kiểm tra lỗi JS trong tab Console.
- Chạy Odoo với log assets để xem lỗi import path nếu có.
- Nếu bản Odoo của bạn dùng path khác cho Chatter component, chỉnh import trong file JS.
