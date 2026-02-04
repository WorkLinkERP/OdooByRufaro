# Invoice Template Settings Separation Fix

## Problem Description

The invoice template settings were appearing in the main Odoo settings page (Accounting > Configuration > Settings), which was overriding or hiding other standard Odoo settings. This happened because the module was extending the main `res.config.settings` model, causing the invoice template fields to be automatically displayed in the main settings form.

## Root Cause

The issue was in `models/invoice_template.py` where the `ResConfigSettings` class inherited from `res.config.settings` and added the `default_invoice_template_id` field. This caused Odoo to automatically include these fields in the main settings page, potentially interfering with other settings.

```python
# PROBLEMATIC CODE (removed):
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_invoice_template_id = fields.Many2one(
        'invoice.template',
        string='Default Invoice Template',
        related='company_id.default_invoice_template_id',
        readonly=False,
        default_model='res.company'
    )
```

## Solution Implemented

### 1. Created Dedicated Settings Model

Replaced the `ResConfigSettings` inheritance with a dedicated model that doesn't interfere with the main settings:

```python
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
```

### 2. Updated Settings View

Modified the settings view in `views/account_move_views.xml` to use the new dedicated model:

```xml
<!-- Changed from res.config.settings to invoice.template.config.settings -->
<record id="view_invoice_template_config_settings" model="ir.ui.view">
    <field name="name">invoice.template.config.settings</field>
    <field name="model">invoice.template.config.settings</field>
    <!-- ... rest of the view remains the same ... -->
</record>
```

### 3. Updated Menu Action

Modified the menu action in `views/menu_views.xml` to use the new model and open in a popup window:

```xml
<record id="action_invoice_template_settings" model="ir.actions.act_window">
    <field name="name">Invoice Template Settings</field>
    <field name="res_model">invoice.template.config.settings</field>
    <field name="view_mode">form</field>
    <field name="view_id" ref="view_invoice_template_config_settings"/>
    <field name="target">new</field>  <!-- Opens in popup instead of inline -->
</record>
```

### 4. Added Security Access Rights

Added access rights for the new model in `security/ir.model.access.csv`:

```csv
access_invoice_template_config_settings_manager,invoice.template.config.settings.manager,model_invoice_template_config_settings,account.group_account_manager,1,1,1,1
```

### 5. Updated Documentation

Updated the README.md to reflect the new location of the settings:

- Changed from: "Go to **Accounting > Configuration > Settings**"
- Changed to: "Go to **Accounting > Configuration > Invoice Templates > Settings**"

## Benefits of This Solution

1. **Separation of Concerns**: Invoice template settings are now completely separate from main Odoo settings
2. **No Interference**: The main Odoo settings page is no longer affected by the invoice template module
3. **Better User Experience**: Settings are logically grouped under the Invoice Templates menu
4. **Cleaner Architecture**: Dedicated model for dedicated functionality
5. **Popup Interface**: Settings open in a popup window for better workflow

## Files Modified

1. `models/invoice_template.py` - Replaced ResConfigSettings with dedicated model
2. `views/account_move_views.xml` - Updated view to use new model
3. `views/menu_views.xml` - Updated action to use new model and popup target
4. `security/ir.model.access.csv` - Added access rights for new model
5. `README.md` - Updated documentation with new settings location

## Testing

After applying these changes:

1. The main Odoo settings page should show all standard settings without interference
2. Invoice template settings should be accessible via: **Accounting > Configuration > Invoice Templates > Settings**
3. The settings should open in a popup window
4. Saving settings should properly update the company's default template
5. All existing functionality should remain intact

## Installation Notes

After updating the module:

1. Update the module in Odoo to apply the new model and views
2. The new settings page will be available immediately
3. Any existing default template settings will be preserved through the company model
4. No data migration is required as the settings are stored in the company model

This fix ensures that the invoice template module plays nicely with other Odoo modules and doesn't interfere with the main settings interface.
