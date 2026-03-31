{
    "name": "Mail Composer CC BCC",
    "summary": "Separate To / Cc / Bcc handling in composer, templates and outgoing mail",
    "version": "19.0.1.0.0",
    "category": "Discuss",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["mail", "web"],
    "data": [
        "views/res_company_views.xml",
        "views/mail_template_views.xml",
        "views/mail_message_views.xml",
        "views/mail_mail_views.xml",
        "views/res_config_settings_views.xml",
        "wizards/mail_compose_message_view.xml",
        "wizards/mail_template_preview_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "mail_composer_cc_bcc/static/src/js/chatter_composer_patch.js",
            "mail_composer_cc_bcc/static/src/xml/chatter_composer_patch.xml",
        ],
    },
    "installable": True,
    "application": False,
}
