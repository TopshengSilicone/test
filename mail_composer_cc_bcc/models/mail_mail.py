from odoo import fields, models
from odoo.tools import email_split


class MailMail(models.Model):
    _inherit = "mail.mail"

    email_bcc = fields.Char(string="Bcc")

    def _prepare_outgoing_list(self):
        outgoing_values = super()._prepare_outgoing_list()
        if not self.env.context.get("is_from_composer"):
            return outgoing_values

        bcc_ids = self.env.context.get("partner_bcc_ids") or []
        bcc_partners = self.env["res.partner"].browse(bcc_ids).exists()
        bcc_emails = [email for email in bcc_partners.mapped("email") if email]

        for values in outgoing_values:
            headers = dict(values.get("headers") or {})
            current_bcc = values.get("email_bcc") or self.email_bcc
            all_bcc = email_split(current_bcc or "") + bcc_emails
            dedup_bcc = list(dict.fromkeys([e for e in all_bcc if e]))
            values["email_bcc"] = ",".join(dedup_bcc) or False
            if dedup_bcc:
                headers["X-Odoo-Bcc"] = ",".join(dedup_bcc)
            values["headers"] = headers
        return outgoing_values
