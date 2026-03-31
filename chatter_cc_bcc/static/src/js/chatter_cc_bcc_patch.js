/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { Chatter } from "@mail/chatter/web/chatter";

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        this.ccBccState = useState({ cc: "", bcc: "" });
    },

    onInputCc(ev) {
        this.ccBccState.cc = (ev.target.value || "").trim();
    },

    onInputBcc(ev) {
        this.ccBccState.bcc = (ev.target.value || "").trim();
    },

    async postMessage(...args) {
        const result = await super.postMessage(...args);

        const cc = this.ccBccState.cc;
        const bcc = this.ccBccState.bcc;
        if (!cc && !bcc) {
            return result;
        }

        // Keep send flow untouched, then persist CC/BCC on the newly-created message.
        const messageId =
            result?.id ||
            result?.message_id ||
            this.thread?.messages?.[this.thread.messages.length - 1]?.id;

        if (messageId && this.env?.services?.orm) {
            await this.env.services.orm.write("mail.message", [messageId], {
                email_cc: cc,
                email_bcc: bcc,
            });
        }

        this.ccBccState.cc = "";
        this.ccBccState.bcc = "";
        return result;
    },
});
