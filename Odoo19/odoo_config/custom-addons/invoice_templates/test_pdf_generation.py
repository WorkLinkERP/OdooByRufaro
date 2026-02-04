#!/usr/bin/env python3
"""
Test script to diagnose PDF generation issues in Odoo
Run this script to identify the root cause of PDF styling problems
"""

import os
import subprocess
import sys
import tempfile

def test_wkhtmltopdf_version():
    """Test wkhtmltopdf version and capabilities"""
    print("🔍 Testing wkhtmltopdf version...")
    
    try:
        result = subprocess.run(['wkhtmltopdf', '--version'], 
                              capture_output=True, text=True)
        version_output = result.stdout
        print(f"✅ wkhtmltopdf version: {version_output.strip()}")
        
        # Check if it's version 0.12.6 or later (problematic versions)
        if '0.12.6' in version_output or '0.12.7' in version_output or '0.12.8' in version_output:
            print("⚠️  WARNING: This version blocks local file access by default")
            return False
        else:
            print("✅ Version should support local file access")
            return True
            
    except FileNotFoundError:
        print("❌ wkhtmltopdf not found in PATH")
        return False
    except Exception as e:
        print(f"❌ Error checking wkhtmltopdf: {e}")
        return False

def test_local_file_access():
    """Test if wkhtmltopdf can access local files"""
    print("\n🔍 Testing local file access...")
    
    # Create a test HTML file with CSS and image
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                color: red; 
                background-color: #f0f0f0;
            }
            .test-box {
                background-color: blue;
                color: white;
                padding: 20px;
                margin: 20px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>PDF Generation Test</h1>
        <div class="test-box">
            <p>If you can see this blue box with white text, CSS is working!</p>
        </div>
        <p style="color: green; font-size: 18px;">This should be green and large.</p>
    </body>
    </html>
    """
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(test_html)
            html_file = f.name
        
        pdf_file = html_file.replace('.html', '.pdf')
        
        # Test without --enable-local-file-access
        print("  Testing without --enable-local-file-access...")
        result1 = subprocess.run(['wkhtmltopdf', html_file, pdf_file], 
                                capture_output=True, text=True)
        
        if result1.returncode == 0:
            print("  ✅ PDF generated successfully")
            if os.path.exists(pdf_file):
                size1 = os.path.getsize(pdf_file)
                print(f"  📄 PDF size: {size1} bytes")
            os.remove(pdf_file)
        else:
            print(f"  ❌ PDF generation failed: {result1.stderr}")
        
        # Test with --enable-local-file-access
        print("  Testing with --enable-local-file-access...")
        result2 = subprocess.run(['wkhtmltopdf', '--enable-local-file-access', 
                                html_file, pdf_file], 
                                capture_output=True, text=True)
        
        if result2.returncode == 0:
            print("  ✅ PDF generated successfully with local file access")
            if os.path.exists(pdf_file):
                size2 = os.path.getsize(pdf_file)
                print(f"  📄 PDF size: {size2} bytes")
                
                if size2 > size1:
                    print("  ✅ PDF with local file access is larger (likely includes styling)")
                else:
                    print("  ⚠️  PDF sizes are similar (styling may not be applied)")
            os.remove(pdf_file)
        else:
            print(f"  ❌ PDF generation with local file access failed: {result2.stderr}")
        
        # Cleanup
        os.remove(html_file)
        
        return result1.returncode == 0 and result2.returncode == 0
        
    except Exception as e:
        print(f"❌ Error testing local file access: {e}")
        return False

def test_base64_images():
    """Test if base64 embedded images work"""
    print("\n🔍 Testing base64 image embedding...")
    
    # Create a simple base64 image (1x1 red pixel PNG)
    red_pixel_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    test_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .image-test {{ border: 2px solid blue; padding: 10px; }}
        </style>
    </head>
    <body>
        <h1>Base64 Image Test</h1>
        <div class="image-test">
            <p>Base64 embedded image (should show a red pixel):</p>
            <img src="data:image/png;base64,{red_pixel_base64}" 
                 style="width: 50px; height: 50px; border: 1px solid black;" 
                 alt="Red pixel test"/>
        </div>
    </body>
    </html>
    """
    
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            f.write(test_html)
            html_file = f.name
        
        pdf_file = html_file.replace('.html', '.pdf')
        
        result = subprocess.run(['wkhtmltopdf', html_file, pdf_file], 
                              capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(pdf_file):
            size = os.path.getsize(pdf_file)
            print(f"✅ Base64 image test PDF generated ({size} bytes)")
            os.remove(pdf_file)
            success = True
        else:
            print(f"❌ Base64 image test failed: {result.stderr}")
            success = False
        
        os.remove(html_file)
        return success
        
    except Exception as e:
        print(f"❌ Error testing base64 images: {e}")
        return False

def provide_recommendations():
    """Provide recommendations based on test results"""
    print("\n📋 RECOMMENDATIONS:")
    print("=" * 50)
    
    version_ok = test_wkhtmltopdf_version()
    file_access_ok = test_local_file_access()
    base64_ok = test_base64_images()
    
    if not version_ok:
        print("\n🔧 SOLUTION 1: Configure wkhtmltopdf parameters")
        print("   Add to Odoo system parameters:")
        print("   Key: report.wkhtmltopdf.options")
        print("   Value: --enable-local-file-access")
        print("   Then restart Odoo")
    
    if not file_access_ok:
        print("\n🔧 SOLUTION 2: Use inline styles and base64 images")
        print("   - Replace external CSS with inline styles")
        print("   - Use base64 encoded images instead of file references")
        print("   - This approach bypasses file access restrictions")
    
    if base64_ok:
        print("\n✅ Base64 images work - use this for company logos")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Apply the recommended solution")
    print("2. Restart Odoo server")
    print("3. Test PDF generation from an invoice")
    print("4. Verify styling and images appear correctly")

if __name__ == "__main__":
    print("PDF Generation Diagnostic Tool")
    print("=" * 40)
    
    provide_recommendations()
    
    print(f"\n📁 Test completed. Check the results above.")
