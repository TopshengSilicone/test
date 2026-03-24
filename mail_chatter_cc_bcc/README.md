# Chatter CC/BCC

Module này thêm trường **CC** và **BCC** vào cửa sổ **Gửi tin nhắn** (wizard `mail.compose.message`) trong Odoo.

## Tính năng
- Thêm người nhận CC (`partner_cc_ids`).
- Thêm người nhận BCC (`partner_bcc_ids`).
- Khi gửi email, module tự động gộp CC/BCC vào `email_cc` và `email_bcc` của email tạo ra.
- Tự động loại bỏ email trùng lặp trong CC/BCC.

## Cài đặt
1. Copy thư mục `mail_chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài app **Chatter CC/BCC**.

## Lưu ý
- Module này mở rộng wizard gửi tin nhắn/email của Odoo (không thay đổi logic follower).
- Nếu bạn muốn thêm CC/BCC trực tiếp trên khung chat inline (OWL composer), cần thêm JS patch riêng theo phiên bản Odoo.
