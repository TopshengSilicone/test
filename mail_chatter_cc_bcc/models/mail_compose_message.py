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

    def _merge_partner_commands(self, current_commands, partners):
        existing_ids = set()
        for command in current_commands or []:
            if isinstance(command, (list, tuple)) and len(command) >= 2 and command[0] == 4:
                existing_ids.add(command[1])
            elif isinstance(command, (list, tuple)) and len(command) >= 3 and command[0] == 6:
                existing_ids.update(command[2] or [])
        merged = list(current_commands or [])
        for partner in partners:
            if partner.id not in existing_ids:
                merged.append((4, partner.id))
                existing_ids.add(partner.id)
        return merged

    def get_mail_values(self, res_ids):
        mail_values = super().get_mail_values(res_ids)

        cc = ", ".join(self.partner_cc_ids.mapped("email"))
        bcc = ", ".join(self.partner_bcc_ids.mapped("email"))
        extra_partners = self.partner_cc_ids | self.partner_bcc_ids

        if not (cc or bcc or extra_partners):
            return mail_values

        for res_id in res_ids:
            values = mail_values.get(res_id, {})
            values["email_cc"] = self._merge_emails(values.get("email_cc"), cc)
            values["email_bcc"] = self._merge_emails(values.get("email_bcc"), bcc)
            values["recipient_ids"] = self._merge_partner_commands(values.get("recipient_ids"), extra_partners)
            # Odoo 19 SMTP envelope may rely primarily on email_to.
            values["email_to"] = self._merge_emails(values.get("email_to"), cc, bcc)
            mail_values[res_id] = values

        return mail_values

    def action_send_mail(self):
        result = super().action_send_mail()
        for wizard in self:
            wizard._send_explicit_cc_bcc_copy()
        return result

    def _send_explicit_cc_bcc_copy(self):
        cc = self._merge_emails(*self.partner_cc_ids.mapped("email"))
        bcc = self._merge_emails(*self.partner_bcc_ids.mapped("email"))
        if not (cc or bcc):
            return

        email_to = self._merge_emails(cc, bcc)
        if not email_to:
            return

        model = self.model or self.env.context.get("default_model")
        res_ids = self.env.context.get("active_ids") or []

        mail_values = {
            "subject": self.subject or "",
            "body_html": self.body or "",
            "email_from": self.email_from,
            "author_id": self.env.user.partner_id.id,
            "email_to": email_to,
            "email_cc": cc or False,
            "email_bcc": bcc or False,
            "auto_delete": False,
        }

        mails = self.env["mail.mail"]
        if model and res_ids:
            for res_id in res_ids:
                mails |= self.env["mail.mail"].sudo().create(
                    {
                        **mail_values,
                        "model": model,
                        "res_id": res_id,
                    }
                )
        else:
            mails = self.env["mail.mail"].sudo().create(mail_values)

        mails.send()
