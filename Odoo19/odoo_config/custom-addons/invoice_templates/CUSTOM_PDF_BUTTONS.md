# Custom PDF Download Buttons Solution

## Problem Addressed

Since the standard PDF generation wasn't working properly due to wkhtmltopdf configuration issues, I've added **dedicated PDF download buttons** that bypass the default system and directly use the invoice templates.

## New Features Added

### 1. Template PDF Download Button

**Location**: Invoice form header (blue button)
**Label**: "📄 Download Template PDF"
**Function**: Downloads PDF using the selected invoice template

**How it works**:
- Checks the `invoice_template_id` field on the invoice
- Uses the selected template (Action Basin, Modern, etc.)
- Falls back to company default template if none selected
- Uses Action Basin as ultimate fallback

### 2. Action Basin PDF Download Button

**Location**: Invoice form header (gray button)
**Label**: "🎨 Download Action Basin PDF"
**Function**: Downloads PDF using Action Basin template directly (for testing)

**How it works**:
- Bypasses all template selection logic
- Directly uses the Action Basin template
- Useful for testing and troubleshooting

### 3. Stat Button

**Location**: Invoice form button box (top right area)
**Label**: "Template PDF"
**Function**: Same as Template PDF Download button

## Technical Implementation

### New Methods Added

#### `action_download_template_pdf()`
```python
def action_download_template_pdf(self):
    """Download PDF using the selected invoice template"""
    self.ensure_one()
    
    # Use the direct template report action that bypasses all complexity
    report = self.env.ref('invoice_templates.action_report_invoice_template_direct')
    
    # Generate and return the PDF
    return report.report_action(self)
```

#### `action_download_action_basin_pdf()`
```python
def action_download_action_basin_pdf(self):
    """Download PDF using Action Basin template directly (for testing)"""
    self.ensure_one()
    
    # Use Action Basin template directly
    report = self.env.ref('invoice_templates.action_report_invoice_action_basin')
    
    # Generate and return the PDF
    return report.report_action(self)
```

### New Report Action

#### `action_report_invoice_template_direct`
- **Purpose**: Dedicated report action for custom buttons
- **Template**: `report_invoice_template_direct`
- **Benefit**: Completely separate from default invoice report system

## Button Visibility

The buttons are only visible when:
- ✅ Invoice type is customer invoice (`out_invoice`) or refund (`out_refund`)
- ✅ Invoice is not in draft state
- ❌ Hidden for vendor bills and draft invoices

## Usage Instructions

### Step 1: Install/Upgrade Module
1. Restart Odoo server
2. Upgrade the `invoice_templates` module
3. The new buttons will appear automatically

### Step 2: Test the Buttons

#### Testing Template PDF Button:
1. Go to any customer invoice (not draft)
2. Select a template in the "Invoice Template" field (optional)
3. Click "📄 Download Template PDF" button
4. PDF should download with proper styling

#### Testing Action Basin PDF Button:
1. Go to any customer invoice (not draft)
2. Click "🎨 Download Action Basin PDF" button
3. PDF should download using Action Basin template with styling

### Step 3: Verify Results

The downloaded PDFs should include:
- ✅ All styling (colors, fonts, spacing)
- ✅ Company logo (if uploaded)
- ✅ Professional layout
- ✅ Styled tables and sections

## Troubleshooting

### If Buttons Don't Appear:
1. **Check invoice type**: Buttons only show for customer invoices
2. **Check invoice state**: Buttons hidden for draft invoices
3. **Clear browser cache**: Force refresh the page
4. **Verify module upgrade**: Ensure module was properly upgraded

### If PDFs Still Don't Have Styling:
1. **Try Action Basin button first**: This bypasses all template logic
2. **Check Odoo logs**: Look for wkhtmltopdf errors
3. **Run diagnostic script**: Use `python test_pdf_generation.py`
4. **Verify wkhtmltopdf**: Check if `--enable-local-file-access` is working

### If Buttons Cause Errors:
1. **Check Odoo logs**: Look for Python errors
2. **Verify report references**: Ensure all report actions exist
3. **Test with simple invoice**: Use invoice with minimal data

## Advantages of This Approach

### 1. **Bypasses Default System**
- No interference from Odoo's default invoice report
- No conflicts with other modules
- Clean, dedicated PDF generation path

### 2. **Multiple Options**
- Template-aware button (uses selected template)
- Direct Action Basin button (for testing)
- Stat button (alternative access)

### 3. **Easy Testing**
- Action Basin button provides consistent test case
- Template button tests dynamic selection
- Clear separation of functionality

### 4. **User-Friendly**
- Prominent buttons in header
- Clear labels and icons
- Helpful tooltips

## Files Modified

1. **`models/account_move.py`**:
   - Added `action_download_template_pdf()` method
   - Added `action_download_action_basin_pdf()` method

2. **`views/account_move_views.xml`**:
   - Added header buttons
   - Added stat button
   - Configured visibility rules

3. **`report/invoice_report_actions.xml`**:
   - Added `action_report_invoice_template_direct` report action
   - Added `report_invoice_template_direct` template

## Expected Results

### Before Adding Buttons:
- Only standard "Print" button available
- PDF generation issues due to wkhtmltopdf configuration
- No way to test specific templates

### After Adding Buttons:
- Multiple PDF download options available
- Direct access to template-specific PDFs
- Easy testing and troubleshooting
- Bypass default system issues

## Next Steps

1. **Test both buttons** on different invoices
2. **Verify styling appears** in downloaded PDFs
3. **Check logo display** in generated PDFs
4. **Compare results** between buttons
5. **Use Action Basin button** as baseline for troubleshooting

The custom buttons provide a reliable way to generate styled PDFs regardless of any issues with the default Odoo report system or wkhtmltopdf configuration.
