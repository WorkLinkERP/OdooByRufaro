# Invoice Templates Module

A custom Odoo 17 module that provides beautiful, customizable invoice report templates with professional designs.

## Features

- **Multiple Template Designs**: Choose from professionally designed invoice templates
- **Action Basin Template**: Fully dynamic template with customizable header, banking details, terms, and footer
- **Modern Template**: Clean and minimalist design with blue accents
- **Easy Template Selection**: Select templates per invoice or set company defaults
- **Template Preview**: Preview templates with sample invoices before using them
- **Responsive Design**: Templates work well in both screen and print formats

### Action Basin Dynamic Features

The Action Basin template includes comprehensive customization options:

- ✅ **Dynamic Header**: Configurable company name and trading-as field
- ✅ **Per-Invoice Subjects**: Custom subject lines for each invoice
- ✅ **Banking Configuration**: Complete USD/ZIG banking details setup with customizable titles
- ✅ **Terms Management**: Editable terms & conditions and customizable E&OE title/text
- ✅ **Footer Personalization**: Custom footer messages
- ✅ **Visibility Controls**: Show/hide any section as needed
- ✅ **Smart Rendering**: Empty fields automatically hidden

> 📖 **See [ACTION_BASIN_DYNAMIC_GUIDE.md](ACTION_BASIN_DYNAMIC_GUIDE.md) for complete configuration guide**

## Installation

1. Copy this module to your Odoo addons directory
2. Update the app list in Odoo
3. Install the "Invoice Templates" module

## Usage

### How It Works

The module automatically overrides Odoo's default invoice report to use a dynamic template system. When you click "Print" on any invoice, the system:

1. Checks if the invoice has a specific template selected
2. Falls back to the company's default template if none is selected
3. Uses the Action Basin template as the ultimate fallback
4. Renders the invoice using the selected template design

### Setting Default Template

1. Go to **Accounting > Configuration > Invoice Templates > Settings**
2. Select your preferred default template
3. Click "Save"

### Managing Templates

1. Go to **Accounting > Configuration > Invoice Templates > Templates**
2. View available templates in kanban or list view
3. Create new templates or modify existing ones
4. Set templates as default or archive unused ones

### Using Templates on Invoices

1. Create or edit an invoice
2. In the invoice form, select the desired template from the "Invoice Template" field (optional)
3. Generate the PDF using the "Print" button - it will automatically use your selected template!

### Previewing Templates

1. Go to **Accounting > Configuration > Invoice Templates > Preview Templates**
2. Select a template and sample invoice
3. Click "Preview Template" to see how it looks
4. Use "Set as Default" to make it the company default

## Template Customization

### Adding New Templates

1. Create a new QWeb template in the `report/` directory
2. Add the template record in `data/invoice_template_data.xml`
3. Update the dynamic template logic in `report/invoice_report_actions.xml`

### Styling Templates

- Modify `static/src/css/invoice_templates.css` for custom styling
- Each template has its own CSS classes for easy customization
- Use Bootstrap classes for responsive design

## Technical Details

### Models

- **invoice.template**: Manages template definitions
- **account.move**: Extended to include template selection
- **res.company**: Extended to store default template
- **template.preview.wizard**: Handles template previewing

### Templates

- **Action Basin Template**: `invoice_templates.report_invoice_action_basin`
- **Modern Template**: `invoice_templates.report_invoice_modern`
- **Dynamic Template**: `invoice_templates.report_invoice_dynamic`

### Key Files

- `models/invoice_template.py`: Template model and logic
- `models/account_move.py`: Invoice template integration
- `report/invoice_template_action_basin.xml`: Action Basin template
- `report/invoice_template_modern.xml`: Modern template
- `static/src/css/invoice_templates.css`: Template styling

## Configuration

### Company Settings

Set default templates in **Accounting > Configuration > Invoice Templates > Settings**

### Template Management

Manage templates in **Accounting > Configuration > Invoice Templates**

## Troubleshooting

### Template Not Showing

1. **Check if the module is properly installed**: Go to Apps and verify "Invoice Templates" is installed
2. **Verify template is active**: Go to Invoice Templates menu and check if templates are active
3. **Check template data**: Ensure the template's report_name field matches the QWeb template ID
4. **Restart Odoo**: After installation, restart the Odoo server to ensure all changes take effect

### PDF Still Shows Default Template

1. **Clear browser cache**: The old template might be cached
2. **Check module installation**: Ensure the module is installed and not just uploaded
3. **Verify report override**: The default invoice report should be overridden to use our dynamic template
4. **Check invoice template field**: Make sure the invoice has a template selected or company default is set

### PDF Generation Issues

1. Check Odoo logs for QWeb template errors
2. Verify all required fields are available
3. Test with different invoice data
4. Ensure wkhtmltopdf is properly installed

### Styling Issues

1. Clear browser cache
2. Check CSS file is properly loaded in web.report_assets_common
3. Verify Bootstrap classes are available
4. Check for CSS conflicts with other modules

## Key Implementation Details

### Report Override Strategy

The module uses a direct report override approach to ensure the custom templates are used:

1. **Default Report Override**: The module overrides `account.account_invoices` (the default invoice report) to use our dynamic template
2. **Dynamic Template Selection**: The `report_invoice_dynamic` template automatically selects the appropriate template based on:
   - Invoice-specific template selection
   - Company default template
   - System default (Action Basin) as fallback
3. **Seamless Integration**: No need to modify existing workflows - the standard "Print" button automatically uses custom templates

### Template Architecture

```
Standard Print Button
        ↓
account.account_invoices (overridden)
        ↓
report_invoice_dynamic
        ↓
Checks invoice.invoice_template_id
        ↓
Renders selected template (Action Basin, Modern, etc.)
```

This approach ensures that all invoice printing (from any part of Odoo) automatically uses the custom template system.

## Support

For issues or customization requests, please contact your Odoo developer or system administrator.

## License

This module is licensed under LGPL-3.


cd odoo_config/custom-addons/ && unzip -o invoice_templates.zip && cd && cd logipool && docker-compose -f docker-compose.traefik.yml restart odoo && cd