from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, **kwargs):
        """Backward-compatible support if payload contains CC/BCC directly."""
        cc_value = kwargs.pop("cc_emails", False) or kwargs.pop("email_cc", False)
        bcc_value = kwargs.pop("bcc_emails", False) or kwargs.pop("email_bcc", False)

        if isinstance(cc_value, (list, tuple)):
            cc_value = ",".join([v for v in cc_value if v])
        if isinstance(bcc_value, (list, tuple)):
            bcc_value = ",".join([v for v in bcc_value if v])

        message = super().message_post(**kwargs)

        if cc_value or bcc_value:
            message.sudo().write(
                {
                    "email_cc": cc_value or False,
                    "email_bcc": bcc_value or False,
                }
            )
        return message
