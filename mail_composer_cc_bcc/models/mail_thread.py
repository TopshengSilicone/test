from odoo import models
from odoo.tools import email_split


class MailThread(models.AbstractModel):
    _inherit = "mail.thread"

    def _message_create(self, values_list):
        cc_ids = self.env.context.get("partner_cc_ids") or []
        bcc_ids = self.env.context.get("partner_bcc_ids") or []
        for values in values_list:
            if cc_ids and not values.get("recipient_cc_ids"):
                values["recipient_cc_ids"] = [(6, 0, cc_ids)]
            if bcc_ids and not values.get("recipient_bcc_ids"):
                values["recipient_bcc_ids"] = [(6, 0, bcc_ids)]
        return super()._message_create(values_list)

    def _notify_by_email_get_base_mail_values(self, message, additional_values=None):
        mail_values = super()._notify_by_email_get_base_mail_values(
            message, additional_values=additional_values
        )
        if self.env.context.get("mail_notify_no_cc_bcc"):
            return mail_values

        to_emails = set(email_split(mail_values.get("email_to") or ""))
        cc_emails = [email for email in message.recipient_cc_ids.mapped("email") if email]
        bcc_emails = [email for email in message.recipient_bcc_ids.mapped("email") if email]

        cc_emails = [e for e in dict.fromkeys(email_split(",".join(cc_emails))) if e and e not in to_emails]
        bcc_emails = [e for e in dict.fromkeys(email_split(",".join(bcc_emails))) if e and e not in to_emails and e not in cc_emails]

        if cc_emails:
            mail_values["email_cc"] = ",".join(cc_emails)
        if bcc_emails:
            mail_values["email_bcc"] = ",".join(bcc_emails)

        return mail_values
