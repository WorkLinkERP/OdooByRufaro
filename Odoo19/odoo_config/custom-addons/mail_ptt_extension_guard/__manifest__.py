{
    "name": "Mail PTT Extension Guard",
    "version": "19.0.1.0.0",
    "summary": "Prevents public pages from crashing when chrome.runtime.sendMessage is unavailable.",
    "category": "Hidden",
    "depends": ["mail"],
    "assets": {
        "mail.assets_public": [
            (
                "replace",
                "mail/static/src/discuss/call/common/ptt_extension_service.js",
                "mail_ptt_extension_guard/static/src/discuss/call/common/ptt_extension_service.js",
            ),
        ],
        "web.assets_backend": [
            (
                "replace",
                "mail/static/src/discuss/call/common/ptt_extension_service.js",
                "mail_ptt_extension_guard/static/src/discuss/call/common/ptt_extension_service.js",
            ),
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": True,
    "license": "LGPL-3",
}
