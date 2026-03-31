from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _merge_emails(self, *email_values):
        emails = []
        email_keys = set()
        for value in email_values:
            if not value:
                continue
            for email in [item.strip() for item in value.split(",") if item.strip()]:
                key = email.lower()
                if key in email_keys:
                    continue
                email_keys.add(key)
                emails.append(email)
        return ", ".join(emails)

    def message_post(self, *args, **kwargs):
        email_cc = kwargs.pop("email_cc", False)
        email_bcc = kwargs.pop("email_bcc", False)

        if email_cc or email_bcc:
            kwargs["email_to"] = self._merge_emails(
                kwargs.get("email_to"),
                email_cc,
                email_bcc,
            )

        return super().message_post(*args, **kwargs)
