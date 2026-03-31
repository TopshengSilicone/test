from odoo.tests import common


class TestMailComposerCcBcc(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner_to = cls.env["res.partner"].create(
            {"name": "To", "email": "to@example.com"}
        )
        cls.partner_cc = cls.env["res.partner"].create(
            {"name": "Cc", "email": "cc@example.com"}
        )
        cls.partner_bcc = cls.env["res.partner"].create(
            {"name": "Bcc", "email": "bcc@example.com"}
        )
        cls.env.company.write(
            {
                "default_partner_cc_ids": [(6, 0, cls.partner_cc.ids)],
                "default_partner_bcc_ids": [(6, 0, cls.partner_bcc.ids)],
            }
        )
        cls.template = cls.env["mail.template"].create(
            {
                "name": "CC BCC Template",
                "model_id": cls.env.ref("base.model_res_partner").id,
                "subject": "Test",
                "body_html": "<p>Hello</p>",
                "email_to": "{{ object.email }}",
                "email_cc": "cc@example.com",
                "email_bcc": "bcc@example.com",
            }
        )

    def _new_composer(self):
        return self.env["mail.compose.message"].with_context(
            default_model="res.partner",
            default_res_ids=[self.partner_to.id],
            default_composition_mode="comment",
        ).create({"partner_ids": [(6, 0, self.partner_to.ids)]})

    def test_company_defaults_loaded_in_composer(self):
        wizard = self._new_composer()
        self.assertEqual(wizard.partner_cc_ids, self.partner_cc)
        self.assertEqual(wizard.partner_bcc_ids, self.partner_bcc)

    def test_template_applies_cc_bcc_partners(self):
        wizard = self._new_composer()
        wizard.template_id = self.template
        wizard._onchange_template_id_cc_bcc()
        self.assertIn(self.partner_cc, wizard.partner_cc_ids)
        self.assertIn(self.partner_bcc, wizard.partner_bcc_ids)

    def test_template_placeholders_resolve(self):
        email_values = self.template.generate_email(self.partner_to.id)
        self.assertIn("to@example.com", email_values.get("email_to"))
        self.assertIn("cc@example.com", email_values.get("email_cc"))
        self.assertIn("bcc@example.com", email_values.get("email_bcc"))

    def test_no_duplicate_when_template_reselected(self):
        wizard = self._new_composer()
        wizard.template_id = self.template
        wizard._onchange_template_id_cc_bcc()
        wizard._onchange_template_id_cc_bcc()
        self.assertEqual(len(wizard.partner_cc_ids), 1)
        self.assertEqual(len(wizard.partner_bcc_ids), 1)

    def test_cc_not_merged_into_main_recipients(self):
        wizard = self._new_composer()
        wizard.email_to = "to@example.com"
        recipients = wizard._get_mail_recipients()
        self.assertIn(self.partner_to, recipients)
        self.assertNotIn(self.partner_cc, recipients)

    def test_send_without_cc_bcc(self):
        wizard = self._new_composer()
        wizard.partner_cc_ids = [(5, 0, 0)]
        wizard.partner_bcc_ids = [(5, 0, 0)]
        values_by_res_id = wizard._prepare_mail_values([self.partner_to.id])
        mail_values = values_by_res_id[self.partner_to.id]
        self.assertFalse(mail_values.get("email_cc"))
        self.assertFalse(mail_values.get("email_bcc"))
