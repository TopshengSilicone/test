from odoo import models
from odoo.tools import email_split


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    def build_email(self, *args, **kwargs):
        headers = dict(kwargs.get("headers") or {})
        hidden_bcc = headers.pop("X-Odoo-Bcc", False)
        if hidden_bcc:
            existing_bcc = kwargs.get("email_bcc") or ""
            all_bcc = email_split(existing_bcc) + email_split(hidden_bcc)
            kwargs["email_bcc"] = ",".join(dict.fromkeys(all_bcc))
        kwargs["headers"] = headers
        return super().build_email(*args, **kwargs)
