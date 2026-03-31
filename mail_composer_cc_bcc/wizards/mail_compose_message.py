from odoo import api, fields, models
from odoo.tools import email_split


class MailComposeMessage(models.TransientModel):
    _inherit = "mail.compose.message"

    partner_cc_ids = fields.Many2many(
        "res.partner",
        "mail_compose_message_cc_rel",
        "wizard_id",
        "partner_id",
        string="Cc",
    )
    partner_bcc_ids = fields.Many2many(
        "res.partner",
        "mail_compose_message_bcc_rel",
        "wizard_id",
        "partner_id",
        string="Bcc",
    )

    @api.model
    def default_get(self, fields_list):
        values = super().default_get(fields_list)
        company = self.env.company
        if "partner_cc_ids" in fields_list and not values.get("partner_cc_ids"):
            values["partner_cc_ids"] = [(6, 0, company.default_partner_cc_ids.ids)]
        if "partner_bcc_ids" in fields_list and not values.get("partner_bcc_ids"):
            values["partner_bcc_ids"] = [(6, 0, company.default_partner_bcc_ids.ids)]
        return values

    def _mail_composer_find_or_create_partners_from_emails(self, emails):
        partners = self.env["res.partner"]
        for email in email_split(emails or ""):
            partner = self.env["res.partner"].search([("email", "=", email)], limit=1)
            if not partner:
                partner = self.env["res.partner"].create({"name": email, "email": email})
            partners |= partner
        return partners

    def _mail_composer_set_partners_from_email_string(self, field_name, email_value):
        partners = self._mail_composer_find_or_create_partners_from_emails(email_value)
        self[field_name] = [(6, 0, partners.ids)]

    def _mail_composer_render_template_cc_bcc(self):
        self.ensure_one()
        if not self.template_id or not self.model or not self.res_id:
            return

        template = self.template_id
        render_ids = [self.res_id]
        cc_value = template._render_field("email_cc", render_ids, compute_lang=True).get(self.res_id)
        bcc_value = template._render_field("email_bcc", render_ids, compute_lang=True).get(self.res_id)
        self._mail_composer_set_partners_from_email_string("partner_cc_ids", cc_value)
        self._mail_composer_set_partners_from_email_string("partner_bcc_ids", bcc_value)

    @api.onchange("template_id")
    def _onchange_template_id_cc_bcc(self):
        for wizard in self:
            if wizard.template_id:
                wizard._mail_composer_render_template_cc_bcc()
            else:
                wizard.partner_cc_ids = [(6, 0, wizard.env.company.default_partner_cc_ids.ids)]
                wizard.partner_bcc_ids = [(6, 0, wizard.env.company.default_partner_bcc_ids.ids)]

    def _get_mail_recipients(self):
        self.ensure_one()
        partners = self.partner_ids
        if self.email_to:
            partners |= self._mail_composer_find_or_create_partners_from_emails(self.email_to)
        return partners

    def _prepare_mail_values(self, res_ids):
        values_by_res_id = super()._prepare_mail_values(res_ids)
        cc_commands = [(6, 0, self.partner_cc_ids.ids)]
        bcc_commands = [(6, 0, self.partner_bcc_ids.ids)]

        for res_id in res_ids:
            values = values_by_res_id.get(res_id, {})
            values["recipient_cc_ids"] = cc_commands
            values["recipient_bcc_ids"] = bcc_commands
            values["email_cc"] = ",".join(self.partner_cc_ids.mapped("email")) or False
            values["email_bcc"] = ",".join(self.partner_bcc_ids.mapped("email")) or False
            values_by_res_id[res_id] = values
        return values_by_res_id

    def _action_send_mail(self, auto_commit=False):
        self.ensure_one()
        return super(
            MailComposeMessage,
            self.with_context(
                is_from_composer=True,
                partner_cc_ids=self.partner_cc_ids.ids,
                partner_bcc_ids=self.partner_bcc_ids.ids,
            ),
        )._action_send_mail(auto_commit=auto_commit)

    def action_send_mail(self):
        self.ensure_one()
        return super(
            MailComposeMessage,
            self.with_context(
                is_from_composer=True,
                partner_cc_ids=self.partner_cc_ids.ids,
                partner_bcc_ids=self.partner_bcc_ids.ids,
            ),
        ).action_send_mail()
