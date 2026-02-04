# PDF Printing Fixes for Invoice Template

## Problem Analysis

When Odoo generates PDFs from HTML reports, several CSS properties don't translate properly:

### Issues Identified:
1. **Table padding not working** - `padding` on `<table>` elements is ignored in PDF generation
2. **CSS reset conflicts** - Global `margin: 0 !important; padding: 0 !important` overrides intended spacing
3. **Missing print-specific CSS** - No `@media print` rules for PDF-specific styling
4. **Background colors not printing** - Default browser behavior ignores backgrounds in print
5. **Inconsistent spacing approach** - Mix of table padding and cell padding

## Solutions Implemented

### 1. Fixed CSS Reset
**Before:**
```css
* {
    margin: 0 !important;
    padding: 0 !important;
}
```

**After:**
```css
* {
    box-sizing: border-box !important;
    /* Removed global margin/padding reset */
}
```

### 2. Added Print-Specific CSS
```css
@media print {
    .page {
        margin: 0 !important;
        padding: 20px !important;
        width: 100% !important;
        max-width: none !important;
    }
    
    /* Ensure backgrounds print */
    * {
        -webkit-print-color-adjust: exact !important;
        color-adjust: exact !important;
    }
    
    /* Force specific spacing for PDF */
    .invoice-details-section {
        background-color: #f5f5f5 !important;
    }
    
    .invoice-details-cell {
        padding: 20px !important;
        background-color: #f5f5f5 !important;
    }
}
```

### 3. Fixed Invoice Details Section
**Before:**
```html
<table style="background-color: #f5f5f5; padding: 15px;">
    <td style="padding: 15px;">
```

**After:**
```html
<table class="invoice-details-section" style="background-color: #f5f5f5;">
    <td class="invoice-details-cell" style="padding: 20px; background-color: #f5f5f5;">
```

### 4. Added CSS Classes for Better Control
- `.invoice-details-section` - For the gray background table
- `.invoice-details-cell` - For proper cell padding
- `.balance-amount` - For red balance amounts

## Key Principles for PDF-Compatible HTML

1. **Use cell padding, not table padding**
2. **Add background colors to both table AND cells**
3. **Include `@media print` rules**
4. **Use CSS classes for print-specific styling**
5. **Avoid global CSS resets that override spacing**
6. **Include `color-adjust: exact` for background printing**

## Testing

After applying these fixes:
1. Upgrade module to version 17.0.1.5.0
2. Clear browser cache
3. Generate PDF invoice
4. Verify proper spacing and backgrounds in PDF output

## Files Modified

- `report/invoice_template_action_basin.xml` - Main template with CSS fixes
- `__manifest__.py` - Version bump to 17.0.1.5.0
