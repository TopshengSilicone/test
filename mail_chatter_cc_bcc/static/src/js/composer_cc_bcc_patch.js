/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Composer as ComposerModel } from "@mail/core/common/composer_model";

function addCc(params, composer) {
    if (composer.ccEmails) {
        params.email_cc = composer.ccEmails;
    }
    return params;
}

patch(ComposerModel.prototype, {
    getMessagePostParams() {
        const params = super.getMessagePostParams(...arguments);
        return addCc(params, this);
    },

    getMessageData() {
        const data = super.getMessageData(...arguments);
        return addCc(data, this);
    },

    clear() {
        super.clear(...arguments);
        this.ccEmails = "";
    },
});
