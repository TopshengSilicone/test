from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, *args, **kwargs):
        email_cc = kwargs.pop("email_cc", False)
        email_bcc = kwargs.pop("email_bcc", False)

        message = super().message_post(*args, **kwargs)
        vals = {}
        if email_cc:
            vals["email_cc"] = email_cc
        if email_bcc:
            vals["email_bcc"] = email_bcc
        if vals:
            message.sudo().write(vals)
        return message
