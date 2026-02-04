# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    invoice_template_id = fields.Many2one(
        'invoice.template',
        string='Invoice Template',
        help='Template to use for this invoice report',
        domain=[('active', '=', True)]
    )

    invoice_subject = fields.Char(
        string='Invoice Subject',
        help='Subject line to display on the invoice (used by Action Basin template)'
    )

    invoice_representative = fields.Char(
        string='Representative',
        help='Representative name to display on the invoice (used by Action Basin template)'
    )

    @api.model
    def default_get(self, fields_list):
        """Set default invoice template"""
        res = super().default_get(fields_list)
        if 'invoice_template_id' in fields_list:
            # Get company default template
            company_template = self.env.company.default_invoice_template_id
            if company_template and company_template.active:
                res['invoice_template_id'] = company_template.id
            else:
                # Fallback to system default
                default_template = self.env['invoice.template'].get_default_template()
                if default_template:
                    res['invoice_template_id'] = default_template.id
        return res

    def get_invoice_template_report_name(self):
        """Get the report name for the selected template"""
        self.ensure_one()
        if self.invoice_template_id and self.invoice_template_id.active:
            return self.invoice_template_id.report_name
        else:
            # Fallback to default template
            default_template = self.env['invoice.template'].get_default_template()
            if default_template:
                return default_template.report_name
            # Ultimate fallback to Action Basin template
            return 'invoice_templates.report_invoice_action_basin'

    def action_download_template_pdf(self):
        """Download PDF using the selected invoice template"""
        self.ensure_one()

        # Use the direct template report action that bypasses all complexity
        report = self.env.ref('invoice_templates.action_report_invoice_template_direct')

        # Generate and return the PDF
        return report.report_action(self)

    def action_download_action_basin_pdf(self):
        """Download PDF using Action Basin template directly (for testing)"""
        self.ensure_one()

        # Use Action Basin template directly
        report = self.env.ref('invoice_templates.action_report_invoice_action_basin')

        # Generate and return the PDF
        return report.report_action(self)

# The default invoice report is now overridden directly in report_actions.xml
# This ensures the Print button uses our custom template system
