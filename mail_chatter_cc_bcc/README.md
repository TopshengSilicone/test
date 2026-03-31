# Chatter CC/BCC (Odoo 19)

Module thêm ô nhập **CC** và **BCC** kiểu Gmail ở 2 nơi:
1. Wizard **Send Message** (`mail.compose.message`).
2. Composer ngoài Chatter (ngay dưới dòng `To:`).

## Tính năng
- Có ô `CC` + `BCC` để nhập/chọn người nhận.
- Khi gửi mail sẽ **gộp chung To + CC + BCC** thành một danh sách người nhận duy nhất (`email_to`).
- Không gửi tách riêng header CC/BCC.
- Khử trùng email không phân biệt hoa/thường.

## Cài đặt
1. Copy `mail_chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài app **Chatter CC/BCC**.
4. Hard refresh trình duyệt để nạp lại assets JS/XML.

## Cách dùng
- Ở chatter, nhập email vào CC/BCC, phân tách bằng dấu phẩy.
- Ở wizard Send Message, chọn partner có email tại CC/BCC.
- Hệ thống sẽ tự động gộp tất cả người nhận vào To khi gửi.
