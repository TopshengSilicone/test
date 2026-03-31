from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, *args, **kwargs):
        email_cc = kwargs.pop("email_cc", False)
        email_bcc = kwargs.pop("email_bcc", False)
        message = super().message_post(*args, **kwargs)
        if email_cc or email_bcc:
            message.sudo().write(
                {
                    "email_cc": email_cc or False,
                    "email_bcc": email_bcc or False,
                }
            )
        return message

    def _notify_by_email_get_final_mail_values(self, *args, **kwargs):
        mail_values = super()._notify_by_email_get_final_mail_values(*args, **kwargs)
        if not mail_values:
            return mail_values

        message = kwargs.get("message")
        if not message and args:
            candidate = args[0]
            if hasattr(candidate, "email_cc"):
                message = candidate
            elif isinstance(candidate, tuple) and candidate and hasattr(candidate[0], "email_cc"):
                message = candidate[0]

        if not message or not hasattr(message, "email_cc"):
            return mail_values

        extra_to = self._merge_recipients(message.email_cc, message.email_bcc)
        for partner_id, values in mail_values.items():
            if message.email_cc:
                values["email_cc"] = self._merge_recipients(values.get("email_cc"), message.email_cc)
            if message.email_bcc:
                values["email_bcc"] = self._merge_recipients(values.get("email_bcc"), message.email_bcc)
            if extra_to:
                values["email_to"] = self._merge_recipients(values.get("email_to"), extra_to)
            mail_values[partner_id] = values
        return mail_values

    def _merge_recipients(self, *sources):
        merged = []
        for source in sources:
            if not source:
                continue
            for email in [item.strip() for item in source.split(",") if item.strip()]:
                if email not in merged:
                    merged.append(email)
        return ", ".join(merged)
