# -*- coding: utf-8 -*-
{
    'name': 'Invoice Templates',
    'version': '17.0.1.6.0',
    'category': 'Accounting/Accounting',
    'summary': 'Custom invoice report templates with beautiful designs',
    'description': """
        This module provides custom invoice report templates with beautiful designs.
        Users can select from multiple template designs for their invoice PDFs.
        
        Features:
        - Multiple beautiful invoice template designs
        - Easy template selection interface
        - Action Basin inspired template
        - Professional and modern layouts
        - Customizable company branding
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'depends': [
        'base',
        'account',
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/wkhtmltopdf_config.xml',
        'report/invoice_template_action_basin.xml',
        'report/invoice_template_modern.xml',
        'report/invoice_report_actions.xml',
        'data/invoice_template_data.xml',
        'views/template_preview_wizard_views.xml',
        'views/invoice_template_views.xml',
        'views/account_move_views.xml',
        'views/menu_views.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'invoice_templates/static/src/css/invoice_templates.css',
        ],
        'web.assets_common': [
            'invoice_templates/static/src/css/invoice_templates.css',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
