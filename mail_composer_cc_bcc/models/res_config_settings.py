from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    default_partner_cc_ids = fields.Many2many(
        related="company_id.default_partner_cc_ids",
        readonly=False,
        string="Default Cc Recipients",
    )
    default_partner_bcc_ids = fields.Many2many(
        related="company_id.default_partner_bcc_ids",
        readonly=False,
        string="Default Bcc Recipients",
    )
