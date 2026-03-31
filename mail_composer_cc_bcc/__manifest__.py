{
    "name": "Mail Composer CC BCC",
    "summary": "Separate To / Cc / Bcc handling in composer, templates and outgoing mail",
    "version": "19.0.1.0.0",
    "category": "Discuss",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["mail"],
    "data": [
        "views/res_company_views.xml",
        "views/mail_template_views.xml",
        "views/mail_message_views.xml",
        "views/mail_mail_views.xml",
        "wizards/mail_compose_message_view.xml",
        "wizards/mail_template_preview_view.xml",
    ],
    "installable": True,
    "application": False,
}
