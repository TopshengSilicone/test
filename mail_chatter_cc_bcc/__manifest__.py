{
    "name": "Chatter CC/BCC",
    "version": "19.0.1.0.0",
    "summary": "Add Gmail-like CC/BCC in chatter and Send Message composer",
    "category": "Discuss",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["mail"],
    "data": [
        "views/mail_compose_message_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mail_chatter_cc_bcc/static/src/js/composer_cc_bcc_patch.js",
            "mail_chatter_cc_bcc/static/src/xml/composer_cc_bcc.xml",
        ],
    },
    "installable": True,
    "application": False,
}
