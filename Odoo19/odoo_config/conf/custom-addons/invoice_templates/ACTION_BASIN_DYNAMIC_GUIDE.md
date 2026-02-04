# Action Basin Dynamic Template Guide

## Overview

The Action Basin invoice template has been enhanced with comprehensive dynamic configuration options. Users can now customize all aspects of the template without modifying code, making it flexible for different business needs while maintaining the professional design.

## Key Features

### ✅ Dynamic Header Configuration
- **Company Name Override**: Customize the company name displayed (defaults to Odoo company name)
- **Trading As (t/a) Field**: Optional field to show "t/a [Your Trading Name]"
- **Dynamic Address**: Automatically pulls company address and contact details from Odoo

### ✅ Flexible Subject Field
- **Per-Invoice Subject**: Add custom subject lines to individual invoices
- **Show/Hide Control**: Template setting to enable/disable subject field display
- **Fallback Support**: Uses invoice reference if no subject is provided

### ✅ Configurable Banking Details
- **Show/Hide Banking Section**: Complete control over banking details visibility
- **Customizable Section Titles**: Configure titles for USD and ZIG banking sections
- **USD Banking Details**: Full configuration (Bank, Account Type, Name, Number, Branch Code, Branch Name, Swift Code)
- **ZIG Banking Details**: Complete ZIG currency banking information
- **EcoCash Integration**: Configurable EcoCash payment details with show/hide option

### ✅ Customizable Terms & Conditions
- **Dynamic Terms Text**: Fully editable terms and conditions content
- **E&OE Configuration**: Customizable title and "Errors and Omissions Excepted" text
- **Professional Formatting**: E&OE title appears bold, text in normal weight
- **Individual Show/Hide**: Separate controls for terms and E&OE sections

### ✅ Personalized Footer
- **Custom Footer Message**: Replace "Thanks for your business" with any message
- **Show/Hide Control**: Option to completely remove footer message

## How to Configure

### 1. Access Template Settings

1. Go to **Accounting > Configuration > Invoice Templates**
2. Find and open the **Action Basin** template
3. The dynamic settings will appear in tabs when the Action Basin template is selected

### 2. Header Settings Tab

**Company Information:**
- **Company Name Override**: Leave empty to use your Odoo company name, or enter a custom name
- **Show Trading As Field**: Check to enable the t/a field
- **Trading As**: Enter your trading name (only visible if "Show Trading As Field" is checked)

**Subject Field:**
- **Show Subject Field**: Check to enable subject lines on invoices

### 3. Banking Details Tab

**General Banking Settings:**
- **Show Banking Details**: Uncheck to hide the entire banking section
- **Show EcoCash Details**: Uncheck to hide EcoCash payment information

**Banking Section Titles:**
- **USD Banking Section Title**: Customize the title for USD banking details (default: "Banking Details (USD)")
- **ZIG Banking Section Title**: Customize the title for ZIG banking details (default: "Banking Details (ZIG)")

**USD Banking Details:**
Configure all USD banking fields:
- Bank Name (default: CBZ)
- Account Type (default: Corporate)
- Account Name
- Account Number
- Branch Code
- Branch Name
- Swift Code

**ZIG Banking Details:**
Configure all ZIG banking fields (same structure as USD)

**EcoCash Details:**
- EcoCash Number (default: 0772 000 000)

### 4. Terms & Footer Tab

**Terms & Conditions:**
- **Show Terms & Conditions**: Check to display terms section
- **Terms & Conditions Text**: Enter your complete terms and conditions

**E&OE:**
- **Show E&OE**: Check to display E&OE section
- **E&OE Title**: Customize the title (default: "E&OE") - appears in bold
- **E&OE Text**: Customize the errors and omissions text - appears in normal weight

**Footer:**
- **Show Footer Message**: Check to display footer message
- **Footer Message**: Customize the closing message (default: "Thanks for your business.")

## Using the Subject Field

### On Individual Invoices

1. Open any customer invoice
2. In the invoice form, you'll see an **Invoice Subject** field
3. Enter a custom subject for that specific invoice
4. The subject will appear on the printed invoice if the template is configured to show subjects

### Subject Display Logic

- If **Show Subject Field** is enabled in template settings:
  - Shows **Invoice Subject** if provided
  - Falls back to **Reference** field if no subject is provided
  - Hides subject line completely if neither field has content
- If **Show Subject Field** is disabled: Subject line never appears

## Template Behavior

### Dynamic Content Rendering

The template intelligently shows/hides sections based on your configuration:

- **Empty fields are automatically hidden** (no blank rows)
- **Sections without content disappear** (e.g., if no banking details are configured)
- **Conditional formatting** maintains professional appearance regardless of configuration

### Fallback Behavior

- **Company Name**: Uses Odoo company name if override is empty
- **Address Details**: Automatically pulls from company settings
- **Banking Details**: Only shows configured fields (empty fields are hidden)
- **Default Values**: Sensible defaults provided for all fields

### Customization Examples

**Banking Section Titles:**
- **"US Dollar Banking Information"** instead of "Banking Details (USD)"
- **"Local Currency Banking"** instead of "Banking Details (ZIG)"
- **"Foreign Currency Account"** and **"Domestic Account"**
- **"USD Payment Details"** and **"ZIG Payment Details"**

**E&OE Customizations:**
- **Title**: "Terms & Conditions" instead of "E&OE"
- **Title**: "Important Notice" instead of "E&OE"
- **Title**: "Legal Disclaimer" instead of "E&OE"
- **Text**: Custom legal text relevant to your business

## Best Practices

### 1. Complete Configuration
- Fill in all banking details for professional appearance
- Provide meaningful terms and conditions
- Test with different configurations to ensure proper display

### 2. Subject Field Usage
- Use descriptive subjects for better invoice organization
- Keep subjects concise (they appear prominently on the invoice)
- Consider using consistent subject formats for different service types

### 3. Banking Details
- Ensure all banking information is accurate
- Consider showing only relevant currency details for your business
- Keep EcoCash details updated if you accept mobile payments

### 4. Terms & Conditions
- Keep terms concise but comprehensive
- Update E&OE text to match your business practices
- Review terms regularly for legal compliance

## Technical Notes

### Template Code
The Action Basin template uses the code `action_basin` - this triggers the display of dynamic settings in the template form.

### Field Storage
All configuration is stored in the `invoice.template` model, making settings persistent and company-specific.

### Backward Compatibility
Existing Action Basin templates will continue to work with default values automatically applied.

## Troubleshooting

### Settings Not Visible
- Ensure you're editing the Action Basin template (code: `action_basin`)
- Check that the template is active
- Refresh the page if settings don't appear immediately

### Content Not Showing
- Verify the "Show [Section]" checkboxes are enabled
- Check that required fields have content
- Ensure the invoice is using the Action Basin template

### Banking Details Missing
- Confirm "Show Banking Details" is checked
- Verify individual banking fields have values
- Empty fields are automatically hidden (this is normal behavior)

## Support

For technical issues or feature requests related to the Action Basin dynamic template, please refer to the module documentation or contact your system administrator.
