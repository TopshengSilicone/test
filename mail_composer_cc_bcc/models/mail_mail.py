from odoo import fields, models
from odoo.tools import email_split


class MailMail(models.Model):
    _inherit = "mail.mail"

    email_bcc = fields.Char(string="Bcc")

    def _prepare_outgoing_list(self):
        outgoing_values = super()._prepare_outgoing_list()
        for values in outgoing_values:
            cc = list(dict.fromkeys(email_split(values.get("email_cc") or self.email_cc or "")))
            bcc = list(dict.fromkeys(email_split(values.get("email_bcc") or self.email_bcc or "")))
            values["email_cc"] = ",".join(cc) or False
            values["email_bcc"] = ",".join([e for e in bcc if e not in cc]) or False
        return outgoing_values
