/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { useState } from "@odoo/owl";
import { Chatter } from "@mail/chatter/web_portal/chatter";

function splitEmails(value) {
    return (value || "")
        .split(/[;,\n]/)
        .map((v) => v.trim())
        .filter(Boolean);
}

patch(Chatter.prototype, {
    setup() {
        super.setup(...arguments);
        this.ccBccState = useState({
            cc: "",
            bcc: "",
        });
    },

    onInputCc(ev) {
        this.ccBccState.cc = ev.target.value || "";
    },

    onInputBcc(ev) {
        this.ccBccState.bcc = ev.target.value || "";
    },

    async postMessage(...args) {
        if (this.composer) {
            this.composer.cc_emails = splitEmails(this.ccBccState.cc);
            this.composer.bcc_emails = splitEmails(this.ccBccState.bcc);
        }
        const result = await super.postMessage(...args);
        this.ccBccState.cc = "";
        this.ccBccState.bcc = "";
        return result;
    },
});
