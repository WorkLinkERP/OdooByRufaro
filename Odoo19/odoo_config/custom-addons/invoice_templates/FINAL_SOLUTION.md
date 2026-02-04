# FINAL SOLUTION: PDF Styling and Logo Issues

## Problem Identified

The root cause of both CSS styling and company logo not appearing in PDF downloads is **wkhtmltopdf version 0.12.6+** which blocks local file access by default. This affects:

- ❌ External CSS files (styling lost)
- ❌ Local images including company logos
- ❌ Any file-based resources

## Comprehensive Solution Implemented

### 1. Automatic wkhtmltopdf Configuration

**Added system parameters** that will be automatically installed with the module:

```xml
<!-- Enables local file access for wkhtmltopdf -->
<record id="wkhtmltopdf_enable_local_file_access" model="ir.config_parameter">
    <field name="key">report.wkhtmltopdf.options</field>
    <field name="value">--enable-local-file-access</field>
</record>
```

This automatically configures Odoo to pass the `--enable-local-file-access` parameter to wkhtmltopdf.

### 2. Base64 Image Embedding

**Fixed logo display** by using base64 encoding instead of file references:

```xml
<img t-if="o.company_id.logo" 
     t-att-src="'data:image/png;base64,%s' % o.company_id.logo.decode('utf-8')" 
     style="max-height: 80px; max-width: 200px; display: block;" 
     alt="Company Logo"/>
```

This embeds the logo directly in the HTML, bypassing file access restrictions.

### 3. Comprehensive Inline Styling

**Applied inline styles** to all template elements to ensure styling works regardless of CSS file loading:

- Company headers with professional typography
- Styled invoice titles and sections
- Colored table headers and cells
- Highlighted balance due sections
- Green EcoCash payment section
- Professional banking details formatting

### 4. Simplified Template Structure

**Streamlined the report action** to directly use the Action Basin template, eliminating potential complexity issues.

## Installation and Testing

### Step 1: Install/Upgrade Module

1. **Restart Odoo server** to ensure all files are loaded
2. **Upgrade the invoice_templates module**:
   - Go to Apps > Invoice Templates > Upgrade
   - Or use command line: `odoo -u invoice_templates -d your_database`

### Step 2: Verify System Parameters

Check that the wkhtmltopdf configuration was applied:
- Go to **Settings > Technical > Parameters > System Parameters**
- Look for key: `report.wkhtmltopdf.options`
- Value should be: `--enable-local-file-access`

### Step 3: Test PDF Generation

1. Go to any customer invoice
2. Click "Print" or "Download PDF"
3. Verify the PDF includes:
   - ✅ All styling (colors, fonts, spacing)
   - ✅ Company logo (if uploaded in company settings)
   - ✅ Styled table headers (dark background)
   - ✅ Green EcoCash section
   - ✅ Professional layout matching web preview

## Troubleshooting

### If Styling Still Doesn't Work:

1. **Check wkhtmltopdf version:**
   ```bash
   wkhtmltopdf --version
   ```

2. **Manually test wkhtmltopdf:**
   ```bash
   echo '<html><head><style>body{color:red;}</style></head><body><h1>Test</h1></body></html>' > test.html
   wkhtmltopdf --enable-local-file-access test.html test.pdf
   ```

3. **Check Odoo logs:**
   ```bash
   tail -f /var/log/odoo/odoo.log | grep -i wkhtmltopdf
   ```

### If Logo Still Doesn't Appear:

1. **Verify company logo is uploaded:**
   - Settings > Companies > Your Company
   - Ensure logo is uploaded and saved

2. **Check image format:**
   - Use PNG, JPG, or GIF formats
   - Try re-uploading the logo

3. **Test base64 encoding:**
   - The template should show "[Company Logo]" placeholder if no logo is set

### Alternative Solutions:

If the automatic configuration doesn't work:

1. **Manual system parameter:**
   - Settings > Technical > Parameters > System Parameters
   - Create: Key=`report.wkhtmltopdf.options`, Value=`--enable-local-file-access`

2. **Server configuration:**
   Add to `odoo.conf`:
   ```ini
   [options]
   reportgz = False
   ```

3. **Docker/Container users:**
   Ensure wkhtmltopdf is properly installed with correct permissions

## Expected Results

### Before Fix:
- Web preview: ✅ Beautiful styling with logo
- PDF download: ❌ Plain text, no styling, no logo

### After Fix:
- Web preview: ✅ Beautiful styling with logo (unchanged)
- PDF download: ✅ Identical styling with logo

## Technical Details

### Files Modified:
1. `data/wkhtmltopdf_config.xml` - Automatic wkhtmltopdf configuration
2. `report/invoice_template_action_basin.xml` - Base64 logo + inline styling
3. `__manifest__.py` - Added wkhtmltopdf config to data files

### Key Technologies:
- **Base64 encoding**: Embeds images directly in HTML
- **Inline CSS**: Ensures styling without external file dependencies
- **System parameters**: Configures wkhtmltopdf automatically
- **Self-contained templates**: No external resource dependencies

## Diagnostic Tool

Run the included diagnostic script to test your configuration:

```bash
python test_pdf_generation.py
```

This will test:
- wkhtmltopdf version and capabilities
- Local file access functionality
- Base64 image embedding
- Provide specific recommendations

## Support

If issues persist after following this solution:

1. Run the diagnostic tool (`test_pdf_generation.py`)
2. Check your specific Odoo installation type (Docker, native, cloud)
3. Verify wkhtmltopdf version and configuration
4. Consider consulting your system administrator

The solution addresses the root cause and should work for all standard Odoo installations with wkhtmltopdf 0.12.6+.
