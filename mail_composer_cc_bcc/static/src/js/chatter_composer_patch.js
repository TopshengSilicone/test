/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Composer } from "@mail/core/common/composer";

/**
 * Odoo 19 chatter composer is OWL-based. This patch injects explicit To/Cc/Bcc
 * field metadata for send-message mode while keeping log note untouched.
 */
patch(Composer.prototype, {
    get hasCcBcc() {
        return this.composerType === "message";
    },

    get ccFieldName() {
        return "partner_cc_ids";
    },

    get bccFieldName() {
        return "partner_bcc_ids";
    },
});
