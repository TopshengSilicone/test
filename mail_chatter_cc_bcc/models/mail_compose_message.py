from odoo import fields, models


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    partner_cc_ids = fields.Many2many(
        "res.partner",
        "mail_compose_message_cc_rel",
        "wizard_id",
        "partner_id",
        string="CC",
        domain="[(\"email\", \"!=\", False)]",
        help="Partners that will be added in carbon copy (CC).",
    )
    partner_bcc_ids = fields.Many2many(
        "res.partner",
        "mail_compose_message_bcc_rel",
        "wizard_id",
        "partner_id",
        string="BCC",
        domain="[(\"email\", \"!=\", False)]",
        help="Partners that will be added in blind carbon copy (BCC).",
    )

    def _merge_emails(self, *email_values):
        emails = []
        for value in email_values:
            if not value:
                continue
            for email in [item.strip() for item in value.split(",") if item.strip()]:
                if email not in emails:
                    emails.append(email)
        return ", ".join(emails)

    def get_mail_values(self, res_ids):
        mail_values = super().get_mail_values(res_ids)

        cc = ", ".join(self.partner_cc_ids.mapped("email"))
        bcc = ", ".join(self.partner_bcc_ids.mapped("email"))

        if not (cc or bcc):
            return mail_values

        for res_id in res_ids:
            values = mail_values.get(res_id, {})
            values["email_cc"] = self._merge_emails(values.get("email_cc"), cc)
            values["email_bcc"] = self._merge_emails(values.get("email_bcc"), bcc)
            mail_values[res_id] = values

        return mail_values
