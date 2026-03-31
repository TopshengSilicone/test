from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, *args, **kwargs):
        email_cc = kwargs.pop("email_cc", False)
        kwargs.pop("email_bcc", False)

        message = super().message_post(*args, **kwargs)
        if email_cc:
            message.sudo().write({"email_cc": email_cc})
        return message
