from odoo import models


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def message_post(self, **kwargs):
        """Store CC/BCC coming from chatter composer payload.

        Front-end patch sends `cc_emails` and `bcc_emails` in the same RPC payload
        used by chatter message posting.
        """
        cc_value = kwargs.pop("cc_emails", False) or kwargs.pop("email_cc", False)
        bcc_value = kwargs.pop("bcc_emails", False) or kwargs.pop("email_bcc", False)

        if isinstance(cc_value, (list, tuple)):
            cc_value = ",".join([v for v in cc_value if v])
        if isinstance(bcc_value, (list, tuple)):
            bcc_value = ",".join([v for v in bcc_value if v])

        message = super().message_post(**kwargs)

        vals = {}
        if cc_value:
            vals["email_cc"] = cc_value
        if bcc_value:
            vals["email_bcc"] = bcc_value
        if vals:
            message.sudo().write(vals)

        return message
