# Chatter CC/BCC (Odoo 19)

Module thêm **CC** và **BCC** theo kiểu Gmail ở 2 nơi:
1. Wizard **Send Message** (`mail.compose.message`).
2. Composer ngoài Chatter (ngay dưới dòng `To:`).

## Tính năng
- Trường `CC` + `BCC` trong wizard gửi tin nhắn.
- Trường `CC` + `BCC` hiển thị trực tiếp trên khung gửi message ngoài Chatter.
- Dữ liệu được truyền vào luồng gửi email qua `email_cc` và `email_bcc`.
- Khử trùng email không phân biệt hoa/thường.

## Cài đặt
1. Copy `mail_chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài app **Chatter CC/BCC**.
4. Hard refresh trình duyệt để nạp lại assets JS/XML.

## Cách dùng
- Ở chatter, nhập email vào CC/BCC, phân tách bằng dấu phẩy.
- Ở wizard Send Message, chọn partner có email tại CC/BCC.
- BCC được gửi ẩn (đúng logic thông dụng như Gmail: người nhận không thấy danh sách BCC).
