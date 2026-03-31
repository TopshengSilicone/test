from odoo import fields, models


class MailTemplatePreview(models.TransientModel):
    _inherit = "mail.template.preview"

    email_bcc = fields.Char(readonly=True)

    def _compute_record_fields(self):
        super()._compute_record_fields()
        for wizard in self:
            wizard.email_bcc = wizard.mail_template_id.email_bcc
