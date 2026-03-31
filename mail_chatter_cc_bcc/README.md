# Chatter CC/BCC

Module thêm trường **CC** ở 2 nơi:
1. Wizard **Send Message** (`mail.compose.message`).
2. Composer ngoài Chatter (ngay dưới dòng `To:`).

## Tính năng
- Trường `CC` trong wizard gửi tin nhắn.
- Trường `CC` hiển thị trực tiếp trên khung gửi message ngoài Chatter.
- Giá trị CC được lưu vào `mail.message` và đẩy vào header `email_cc`.
- Tự động loại bỏ email trùng.

## Cài đặt
1. Copy `mail_chatter_cc_bcc` vào addons path.
2. Update Apps List.
3. Cài app **Chatter CC/BCC**.
4. Hard refresh trình duyệt để nạp lại assets JS/XML.

## Lưu ý
- Nhập CC theo dạng email, phân tách bởi dấu phẩy.
- Module đã bỏ BCC theo yêu cầu để tránh lệch hiển thị giữa người nhận To và CC.
