# wkhtmltopdf Configuration Fix for PDF Styling and Images

## Root Cause Identified

The issue where both CSS styling and company logos don't appear in PDF downloads is caused by **wkhtmltopdf version 0.12.6+** which has `--disable-local-file-access` enabled by default. This prevents wkhtmltopdf from loading:

- External CSS files
- Local images (including company logos)
- Any other local resources

## Symptoms

- ✅ Web preview shows perfect styling and images
- ❌ PDF download shows plain text without styling
- ❌ Company logo doesn't appear in PDF
- ❌ All CSS formatting is lost in PDF

## Solution Options

### Option 1: Configure wkhtmltopdf Parameters (Recommended)

Add the `--enable-local-file-access` parameter to wkhtmltopdf configuration.

#### For System-wide Installation:

1. **Check current wkhtmltopdf version:**
   ```bash
   wkhtmltopdf --version
   ```

2. **If version 0.12.6+, configure Odoo system parameters:**
   - Go to **Settings > Technical > Parameters > System Parameters**
   - Create or modify the parameter:
     - **Key**: `report.wkhtmltopdf.options`
     - **Value**: `--enable-local-file-access`

#### For Docker/Container Installations:

Add to your Odoo configuration file (`odoo.conf`):
```ini
[options]
reportgz = False
```

And ensure wkhtmltopdf is called with proper parameters.

### Option 2: Downgrade wkhtmltopdf (Alternative)

If you can't modify the configuration, downgrade to version 0.12.5:

```bash
# Ubuntu/Debian
sudo apt-get remove wkhtmltopdf
wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.5-1/wkhtmltox_0.12.5-1.bionic_amd64.deb
sudo dpkg -i wkhtmltox_0.12.5-1.bionic_amd64.deb
```

### Option 3: Use Base64 Embedded Images (Implemented)

I've already implemented this approach in the template:

```xml
<img t-if="o.company_id.logo" 
     t-att-src="'data:image/png;base64,%s' % o.company_id.logo.decode('utf-8')" 
     style="max-height: 80px; max-width: 200px; display: block;" 
     alt="Company Logo"/>
```

This embeds the image directly in the HTML as base64 data, bypassing file access restrictions.

## Testing the Fix

### Step 1: Apply wkhtmltopdf Configuration

Choose one of the solution options above and apply it.

### Step 2: Restart Odoo

After making configuration changes:
```bash
sudo systemctl restart odoo
# or for Docker
docker-compose restart odoo
```

### Step 3: Test PDF Generation

1. Go to any invoice
2. Click "Print" or "Download PDF"
3. Verify that:
   - ✅ All styling appears (colors, fonts, spacing)
   - ✅ Company logo is visible
   - ✅ Table headers are styled
   - ✅ EcoCash section is green

## Verification Commands

### Check wkhtmltopdf Configuration:
```bash
# Test with a simple HTML file
echo '<html><head><style>body{color:red;}</style></head><body><h1>Test</h1></body></html>' > test.html
wkhtmltopdf test.html test.pdf
# If styling appears in test.pdf, wkhtmltopdf is working correctly
```

### Check Odoo System Parameters:
```sql
-- Connect to Odoo database and check
SELECT key, value FROM ir_config_parameter WHERE key LIKE '%wkhtmltopdf%';
```

## Advanced Troubleshooting

### If Option 1 Doesn't Work:

1. **Check Odoo logs** for wkhtmltopdf errors:
   ```bash
   tail -f /var/log/odoo/odoo.log | grep -i wkhtmltopdf
   ```

2. **Test wkhtmltopdf directly:**
   ```bash
   wkhtmltopdf --enable-local-file-access https://www.google.com test.pdf
   ```

3. **Verify system parameters are loaded:**
   - Restart Odoo after adding system parameters
   - Check that parameters appear in Settings > Technical > System Parameters

### If Images Still Don't Work:

The base64 approach should work regardless of wkhtmltopdf configuration. If logos still don't appear:

1. **Check if company has a logo set:**
   - Go to Settings > Companies > Your Company
   - Verify logo is uploaded

2. **Check image format:**
   - Ensure logo is in PNG, JPG, or GIF format
   - Try re-uploading the logo

## Expected Results After Fix

### Before Fix:
- Web preview: ✅ Styled with logo
- PDF download: ❌ Plain text, no logo

### After Fix:
- Web preview: ✅ Styled with logo (unchanged)
- PDF download: ✅ Fully styled with logo

## Technical Notes

- **wkhtmltopdf 0.12.6+**: Blocks local file access by default for security
- **Base64 Images**: Bypass file access restrictions by embedding data directly
- **System Parameters**: Odoo's way to pass custom parameters to wkhtmltopdf
- **Container Considerations**: Docker installations may need volume mounts for file access

## Support

If the issue persists after trying these solutions:

1. Check your specific Odoo installation type (Docker, native, cloud)
2. Verify wkhtmltopdf version and configuration
3. Test with a minimal HTML file to isolate the issue
4. Consider consulting your system administrator for wkhtmltopdf configuration changes
