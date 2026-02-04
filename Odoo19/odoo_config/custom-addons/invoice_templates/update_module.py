#!/usr/bin/env python3
"""
Script to help update the invoice_templates module in Odoo
Run this script to ensure the module changes are properly applied
"""

import os
import sys

def main():
    print("🔄 Invoice Templates Module Update Helper")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('__manifest__.py'):
        print("❌ Error: Not in module directory. Please run this from the invoice_templates module root.")
        return False
    
    print("✅ Found module directory")
    
    # Check key files exist
    key_files = [
        'report/invoice_template_action_basin.xml',
        'static/src/css/invoice_templates.css',
        '__manifest__.py'
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"✅ Found {file_path}")
        else:
            print(f"❌ Missing {file_path}")
            return False
    
    print("\n📋 To update the module in Odoo:")
    print("1. Restart your Odoo server")
    print("2. Go to Apps menu in Odoo")
    print("3. Remove the 'Apps' filter and search for 'invoice_templates'")
    print("4. Click 'Upgrade' button on the Invoice Templates module")
    print("5. Clear your browser cache (Ctrl+F5)")
    print("6. Test the invoice generation")
    
    print("\n🔧 Alternative method (if upgrade doesn't work):")
    print("1. Go to Apps > Invoice Templates > Uninstall")
    print("2. Restart Odoo server")
    print("3. Go to Apps > Update Apps List")
    print("4. Install Invoice Templates module again")
    
    print("\n💡 If changes still don't appear:")
    print("1. Check Odoo logs for any errors")
    print("2. Ensure file permissions are correct")
    print("3. Try restarting Odoo with --dev=reload flag")
    
    print("\n✅ Module files are ready for update!")
    return True

if __name__ == "__main__":
    main()
