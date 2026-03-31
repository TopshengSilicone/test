# Chatter CC/BCC (Odoo 19.0.1.0.0)

Module này thêm 2 ô **CC** và **BCC** trực tiếp ở phần chatter "Send message" (ngoài màn hình, không cần mở popup).

## Tính năng
- Hiển thị 2 ô nhập CC/BCC ngay dưới vùng nhập tin nhắn.
- Hỗ trợ nhập nhiều email, phân tách bằng `;`, `,` hoặc xuống dòng.
- Lưu giá trị CC/BCC vào `mail.message` (`email_cc`, `email_bcc`) khi gửi message.

## Cài đặt
1. Copy thư mục `chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài module **Chatter CC/BCC**.

## Lưu ý kỹ thuật
- Vì Odoo 19 có thể thay đổi cấu trúc JS/XML của mail/chatter theo build cụ thể, nếu không hiển thị thì cần chỉnh lại:
  - Import path component `Chatter` trong JS.
  - XPath kế thừa template `mail.Chatter` trong XML.
