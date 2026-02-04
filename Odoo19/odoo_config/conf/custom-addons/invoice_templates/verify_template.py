#!/usr/bin/env python3
"""
Script to verify the Action Basin template has been updated correctly
"""

import xml.etree.ElementTree as ET
import os

def verify_template():
    print("🔍 Verifying Action Basin Template Structure")
    print("=" * 50)
    
    template_file = "report/invoice_template_action_basin.xml"
    
    if not os.path.exists(template_file):
        print(f"❌ Template file not found: {template_file}")
        return False
    
    try:
        tree = ET.parse(template_file)
        root = tree.getroot()
        
        # Read the file content to check for key elements
        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        checks = [
            ("Full page layout (no max-width)", "width: 100%" in content),
            ("No box-shadow", "box-shadow" not in content),
            ("Table-based header", "Header Section - Table Layout" in content),
            ("Gray background invoice details", "background-color: #f5f5f5" in content),
            ("Dark table headers", "background: #555" in content),
            ("Red balance amount", "color: #dc3545" in content),
            ("Banking details tables", "Banking Details (USD)" in content),
            ("Mobile banking section", "ECOCASH" in content),
            ("Terms & Conditions", "Terms &amp; Conditions" in content),
        ]
        
        all_passed = True
        for check_name, condition in checks:
            if condition:
                print(f"✅ {check_name}")
            else:
                print(f"❌ {check_name}")
                all_passed = False
        
        if all_passed:
            print("\n🎉 Template structure looks correct!")
            print("\nNext steps:")
            print("1. Run: python update_module.py")
            print("2. Follow the module update instructions")
            print("3. Test invoice generation")
        else:
            print("\n⚠️  Some template elements may need attention")
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error parsing template: {e}")
        return False

if __name__ == "__main__":
    verify_template()
