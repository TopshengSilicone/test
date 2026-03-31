from odoo import models
from odoo.tools import email_split


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, *args, **kwargs):
        email_cc = kwargs.pop("email_cc", False)
        email_bcc = kwargs.pop("email_bcc", False)

        message = super().message_post(*args, **kwargs)

        if not (email_cc or email_bcc):
            return message

        message.sudo().write(
            {
                "email_cc": email_cc or False,
                "email_bcc": email_bcc or False,
            }
        )

        # Fallback explicit delivery while preserving proper To/CC/BCC headers in one email.
        self._create_cc_bcc_mail(message, email_cc=email_cc, email_bcc=email_bcc)
        return message

    def _create_cc_bcc_mail(self, message, email_cc=False, email_bcc=False):
        cc_list = self._split_emails(email_cc)
        bcc_list = [email for email in self._split_emails(email_bcc) if email not in cc_list]
        if not cc_list and not bcc_list:
            return

        to_list = self._split_emails(", ".join(message.partner_ids.mapped("email")))
        to_list = [email for email in to_list if email not in cc_list and email not in bcc_list]
        if not to_list and message.email_from:
            # SMTP commonly expects at least one visible recipient.
            to_list = self._split_emails(message.email_from)

        self.env["mail.mail"].sudo().create(
            {
                "mail_message_id": message.id,
                "subject": message.subject or message.record_name or "",
                "body_html": message.body or "",
                "email_from": message.email_from,
                "reply_to": message.reply_to,
                "author_id": message.author_id.id,
                "model": message.model,
                "res_id": message.res_id,
                "attachment_ids": [(6, 0, message.attachment_ids.ids)],
                "auto_delete": False,
                "email_to": ", ".join(to_list),
                "email_cc": ", ".join(cc_list) if cc_list else False,
                "email_bcc": ", ".join(bcc_list) if bcc_list else False,
            }
        )

    def _split_emails(self, emails):
        unique = []
        for email in email_split(emails or ""):
            if email not in unique:
                unique.append(email)
        return unique
