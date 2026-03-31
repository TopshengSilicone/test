{
    "name": "Chatter CC/BCC",
    "summary": "Add CC and BCC fields directly in the chatter send message composer",
    "version": "19.0.1.0.0",
    "category": "Discuss",
    "author": "Custom",
    "license": "LGPL-3",
    "depends": ["mail"],
    "data": [
        "security/ir.model.access.csv",
    ],
    "assets": {
        "web.assets_backend": [
            "chatter_cc_bcc/static/src/js/chatter_cc_bcc_patch.js",
            "chatter_cc_bcc/static/src/xml/chatter_cc_bcc.xml",
        ],
    },
    "installable": True,
    "application": False,
}
