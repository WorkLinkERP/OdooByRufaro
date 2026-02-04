# -*- coding: utf-8 -*-

from odoo import models, fields, api
import json


class InvoiceTemplate(models.Model):
    _name = 'invoice.template'
    _description = 'Invoice Template'
    _order = 'sequence, name'

    name = fields.Char(string='Template Name', required=True)
    code = fields.Char(string='Template Code', required=True)
    description = fields.Text(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    report_name = fields.Char(
        string='Report Name',
        required=True,
        help='Technical name of the QWeb template'
    )
    preview_image = fields.Binary(string='Preview Image')
    is_default = fields.Boolean(string='Default Template', default=False)

    # Action Basin Template Specific Fields
    # Header Configuration
    company_name_override = fields.Char(
        string='Company Name Override',
        help='Override the company name displayed in the header. Leave empty to use company name.'
    )
    ta_field = fields.Char(
        string='Trading As (t/a)',
        help='Optional trading as name to display below company name'
    )
    show_ta_field = fields.Boolean(
        string='Show Trading As Field',
        default=False,
        help='Whether to display the t/a field in the header'
    )

    # Subject Field Configuration
    show_subject_field = fields.Boolean(
        string='Show Subject Field',
        default=True,
        help='Whether to display the subject field on invoices'
    )

    # Banking Details Configuration
    show_banking_details = fields.Boolean(
        string='Show Banking Details',
        default=True,
        help='Whether to display banking details section'
    )

    # Banking Details Section Titles
    usd_banking_title = fields.Char(
        string='Banking Details 1 Title',
        default='Banking Details 1',
        help='Title for the first banking details section'
    )
    zig_banking_title = fields.Char(
        string='Banking Details 2 Title',
        default='Banking Details 2',
        help='Title for the second banking details section'
    )

    # Banking Details 1 (formerly USD)
    usd_bank_name = fields.Char(string='Bank Name 1', default='CBZ')
    usd_account_type = fields.Char(string='Account Type 1', default='Corporate')
    usd_account_name = fields.Char(string='Account Name 1')
    usd_account_number = fields.Char(string='Account Number 1')
    usd_branch_code = fields.Char(string='Branch Code 1')
    usd_branch_name = fields.Char(string='Branch Name 1')
    usd_swift_code = fields.Char(string='Swift Code 1')

    # Banking Details 2 (formerly ZIG)
    zig_bank_name = fields.Char(string='Bank Name 2', default='CBZ')
    zig_account_type = fields.Char(string='Account Type 2', default='Corporate')
    zig_account_name = fields.Char(string='Account Name 2')
    zig_account_number = fields.Char(string='Account Number 2')
    zig_branch_code = fields.Char(string='Branch Code 2')
    zig_branch_name = fields.Char(string='Branch Name 2')
    zig_swift_code = fields.Char(string='Swift Code 2')

    # Mobile Details
    ecocash_title = fields.Char(
        string='Mobile banking section Title',
        default='MOBILE',
        help='Title/label for the mobile payment section'
    )
    ecocash_number = fields.Char(string='Mobile Code', default='0772 000 000')
    show_ecocash = fields.Boolean(
        string='Show Mobile Details',
        default=True,
        help='Whether to display Mobile payment details'
    )

    # Terms & Conditions
    terms_conditions = fields.Text(
        string='Terms & Conditions',
        default='These rates are inclusive of 3x FREE amendment sessions, after which a $25 hourly rate will come into effect. All values are in USD. ZIG payments accepted at agreed prevailing rates at date of transfer. A downpayment of 50% is required upon acceptance of brief with the difference payable upon completion of a job.',
        help='Terms and conditions text to display on invoices'
    )
    show_terms_conditions = fields.Boolean(
        string='Show Terms & Conditions',
        default=True,
        help='Whether to display terms and conditions section'
    )

    # E&OE
    eoe_title = fields.Char(
        string='E&OE Title',
        default='E&OE',
        help='Title for the Errors and Omissions Excepted section'
    )
    eoe_text = fields.Char(
        string='E&OE Text',
        default='All invoices in ZIG subject to weekly reviews.',
        help='Errors and Omissions Excepted text'
    )
    show_eoe = fields.Boolean(
        string='Show E&OE',
        default=True,
        help='Whether to display E&OE text'
    )

    # Footer Configuration
    footer_message = fields.Char(
        string='Footer Message',
        default='Thanks for your business.',
        help='Message to display at the bottom of the invoice'
    )
    show_footer_message = fields.Boolean(
        string='Show Footer Message',
        default=True,
        help='Whether to display footer message'
    )
    
    @api.model
    def create(self, vals):
        # Ensure only one default template
        if vals.get('is_default'):
            self.search([('is_default', '=', True)]).write({'is_default': False})
        return super().create(vals)
    
    def write(self, vals):
        # Ensure only one default template
        if vals.get('is_default'):
            self.search([('is_default', '=', True), ('id', 'not in', self.ids)]).write({'is_default': False})
        return super().write(vals)
    
    @api.model
    def get_default_template(self):
        """Get the default invoice template"""
        default_template = self.search([('is_default', '=', True)], limit=1)
        if not default_template:
            default_template = self.search([('active', '=', True)], limit=1)
        return default_template


class ResCompany(models.Model):
    _inherit = 'res.company'
    
    default_invoice_template_id = fields.Many2one(
        'invoice.template',
        string='Default Invoice Template',
        help='Default template to use for invoice reports'
    )


class InvoiceTemplateConfigSettings(models.TransientModel):
    """Dedicated settings model for invoice templates that doesn't interfere with main settings"""
    _name = 'invoice.template.config.settings'
    _description = 'Invoice Template Configuration Settings'

    default_invoice_template_id = fields.Many2one(
        'invoice.template',
        string='Default Invoice Template',
        help='Default template to use for invoice reports'
    )

    @api.model
    def default_get(self, fields_list):
        """Load current company's default template"""
        res = super().default_get(fields_list)
        company = self.env.company
        if 'default_invoice_template_id' in fields_list and company.default_invoice_template_id:
            res['default_invoice_template_id'] = company.default_invoice_template_id.id
        return res

    def execute(self):
        """Save the settings to the current company"""
        company = self.env.company
        company.default_invoice_template_id = self.default_invoice_template_id
        return {'type': 'ir.actions.client', 'tag': 'reload'}

    def cancel(self):
        """Cancel the settings dialog"""
        return {'type': 'ir.actions.act_window_close'}
