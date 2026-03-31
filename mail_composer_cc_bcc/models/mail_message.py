from odoo import fields, models


class MailMessage(models.Model):
    _inherit = "mail.message"

    recipient_cc_ids = fields.Many2many(
        "res.partner",
        "mail_message_recipient_cc_rel",
        "mail_message_id",
        "partner_id",
        string="Cc Recipients",
        copy=False,
    )
    recipient_bcc_ids = fields.Many2many(
        "res.partner",
        "mail_message_recipient_bcc_rel",
        "mail_message_id",
        "partner_id",
        string="Bcc Recipients",
        copy=False,
    )
