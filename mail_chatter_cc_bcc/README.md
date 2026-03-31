# Chatter CC/BCC

Module thêm **CC/BCC** ở cả 2 nơi:
1. Wizard **Send Message** (`mail.compose.message`).
2. Composer ngoài Chatter (ngay dưới dòng `To:` như ảnh bạn gửi).

## Tính năng
- Trường `CC` và `BCC` trong wizard gửi tin nhắn.
- Trường `CC` và `BCC` hiển thị trực tiếp trên khung gửi message ngoài Chatter.
- Giá trị CC/BCC được lưu vào `mail.message` và module tạo thêm `mail.mail` với header To/CC/BCC chuẩn để đảm bảo luôn gửi được đúng vai trò người nhận.
- Tự động loại bỏ email trùng.

## Cài đặt
1. Copy `mail_chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài app **Chatter CC/BCC**.
4. Hard refresh trình duyệt để nạp lại assets JS/XML.

## Lưu ý
- Nhập CC/BCC theo dạng email, phân tách bởi dấu phẩy.
- Nếu bạn đang custom mạnh module `mail`, có thể cần điều chỉnh xpath/template theo phiên bản.
