# -*- coding: utf-8 -*-

from odoo import models, fields, api


class TemplatePreviewWizard(models.TransientModel):
    _name = 'template.preview.wizard'
    _description = 'Template Preview Wizard'
    
    template_id = fields.Many2one(
        'invoice.template',
        string='Template',
        required=True,
        domain=[('active', '=', True)]
    )
    invoice_id = fields.Many2one(
        'account.move',
        string='Sample Invoice',
        domain=[('move_type', 'in', ['out_invoice', 'out_refund']), ('state', '!=', 'draft')]
    )
    
    @api.model
    def default_get(self, fields_list):
        """Set default values"""
        res = super().default_get(fields_list)
        
        # Get a sample invoice if available
        if 'invoice_id' in fields_list:
            sample_invoice = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '!=', 'draft')
            ], limit=1)
            if sample_invoice:
                res['invoice_id'] = sample_invoice.id
        
        # Get default template
        if 'template_id' in fields_list:
            default_template = self.env['invoice.template'].get_default_template()
            if default_template:
                res['template_id'] = default_template.id
        
        return res
    
    def action_preview_template(self):
        """Generate preview of the template"""
        self.ensure_one()
        if not self.invoice_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'No Sample Invoice',
                    'message': 'Please select a sample invoice to preview the template.',
                    'type': 'warning',
                }
            }
        
        # Temporarily set the template on the invoice
        original_template = self.invoice_id.invoice_template_id
        self.invoice_id.invoice_template_id = self.template_id
        
        try:
            # Generate the report
            report_action = self.env.ref('invoice_templates.action_report_invoice_dynamic').report_action(self.invoice_id)
            return report_action
        finally:
            # Restore original template
            self.invoice_id.invoice_template_id = original_template
    
    def action_set_as_default(self):
        """Set this template as the default"""
        self.ensure_one()
        self.template_id.write({'is_default': True})
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Default Template Updated',
                'message': f'"{self.template_id.name}" is now the default template.',
                'type': 'success',
            }
        }
