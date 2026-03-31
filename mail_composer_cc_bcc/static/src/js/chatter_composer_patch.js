/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Composer } from "@mail/core/common/composer";

patch(Composer.prototype, {
    get isSendMessageMode() {
        return this.composerType === "message";
    },
});
