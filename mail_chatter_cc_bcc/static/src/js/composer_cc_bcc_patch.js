/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Composer as ComposerModel } from "@mail/core/common/composer_model";

function addCcBcc(params, composer) {
    if (composer.ccEmails) {
        params.email_cc = composer.ccEmails;
    }
    if (composer.bccEmails) {
        params.email_bcc = composer.bccEmails;
    }
    return params;
}

patch(ComposerModel.prototype, {
    getMessagePostParams() {
        const params = super.getMessagePostParams(...arguments);
        return addCcBcc(params, this);
    },

    getMessageData() {
        const data = super.getMessageData(...arguments);
        return addCcBcc(data, this);
    },

    clear() {
        super.clear(...arguments);
        this.ccEmails = "";
        this.bccEmails = "";
    },
});
