from odoo import fields, models
from odoo.tools import email_split


class MailTemplate(models.Model):
    _inherit = "mail.template"

    email_bcc = fields.Char(string="Bcc")

    def _mail_cc_bcc_find_or_create_partners(self, emails):
        partners = self.env["res.partner"]
        for email in email_split(emails or ""):
            partner = self.env["res.partner"].search([("email", "=", email)], limit=1)
            if not partner:
                partner = self.env["res.partner"].create({"name": email, "email": email})
            partners |= partner
        return partners

    def generate_email(self, res_ids, fields=None):
        results = super().generate_email(res_ids, fields=fields)
        multi_mode = isinstance(res_ids, (list, tuple, set))
        render_ids = list(res_ids) if multi_mode else [res_ids]

        cc_map = self._render_field("email_cc", render_ids, compute_lang=True)
        bcc_map = self._render_field("email_bcc", render_ids, compute_lang=True)

        for res_id in render_ids:
            values = results[res_id] if multi_mode else results
            cc_value = cc_map.get(res_id) or values.get("email_cc")
            bcc_value = bcc_map.get(res_id) or values.get("email_bcc")
            values["email_cc"] = cc_value or False
            values["email_bcc"] = bcc_value or False

            cc_partners = self._mail_cc_bcc_find_or_create_partners(cc_value)
            bcc_partners = self._mail_cc_bcc_find_or_create_partners(bcc_value)
            values["recipient_cc_ids"] = [(6, 0, cc_partners.ids)]
            values["recipient_bcc_ids"] = [(6, 0, bcc_partners.ids)]

        return results
