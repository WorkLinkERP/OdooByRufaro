#!/usr/bin/env python3
"""
Installation test script for Invoice Templates module
Run this script to verify the module is ready for installation
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_module_structure():
    """Test if all required files exist"""
    print("🔍 Testing module structure...")
    
    required_files = [
        '__manifest__.py',
        '__init__.py',
        'models/__init__.py',
        'models/invoice_template.py',
        'models/account_move.py',
        'models/template_preview_wizard.py',
        'security/ir.model.access.csv',
        'data/invoice_template_data.xml',
        'views/invoice_template_views.xml',
        'views/account_move_views.xml',
        'views/template_preview_wizard_views.xml',
        'views/menu_views.xml',
        'report/invoice_report_actions.xml',
        'report/invoice_template_action_basin.xml',
        'report/invoice_template_modern.xml',
        'static/src/css/invoice_templates.css'
    ]
    
    missing = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print("❌ Missing files:")
        for f in missing:
            print(f"   - {f}")
        return False
    
    print("✅ All required files present")
    return True

def test_manifest_syntax():
    """Test manifest file syntax"""
    print("🔍 Testing manifest syntax...")
    
    try:
        with open('__manifest__.py', 'r') as f:
            content = f.read()
        
        # Test if it's valid Python
        compile(content, '__manifest__.py', 'exec')
        print("✅ Manifest syntax valid")
        return True
    except Exception as e:
        print(f"❌ Manifest error: {e}")
        return False

def test_xml_syntax():
    """Test XML file syntax"""
    print("🔍 Testing XML syntax...")
    
    xml_files = [
        'data/invoice_template_data.xml',
        'views/invoice_template_views.xml',
        'views/account_move_views.xml',
        'views/template_preview_wizard_views.xml',
        'views/menu_views.xml',
        'report/invoice_report_actions.xml',
        'report/invoice_template_action_basin.xml',
        'report/invoice_template_modern.xml'
    ]
    
    for xml_file in xml_files:
        try:
            ET.parse(xml_file)
        except ET.ParseError as e:
            print(f"❌ {xml_file}: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ {xml_file}: File not found")
            return False
    
    print("✅ All XML files valid")
    return True

def test_odoo17_compatibility():
    """Test Odoo 17 compatibility"""
    print("🔍 Testing Odoo 17 compatibility...")
    
    xml_files = [
        'views/invoice_template_views.xml',
        'views/account_move_views.xml',
        'views/template_preview_wizard_views.xml'
    ]
    
    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            # Check for deprecated attributes
            for elem in root.iter():
                if 'attrs' in elem.attrib:
                    print(f"❌ {xml_file}: Found deprecated 'attrs' attribute")
                    return False
                if 'states' in elem.attrib:
                    print(f"❌ {xml_file}: Found deprecated 'states' attribute")
                    return False
        except Exception as e:
            print(f"❌ {xml_file}: {e}")
            return False
    
    print("✅ Odoo 17 compatible")
    return True

def main():
    """Run all tests"""
    print("🚀 Invoice Templates Module - Installation Test")
    print("=" * 50)
    
    tests = [
        test_module_structure,
        test_manifest_syntax,
        test_xml_syntax,
        test_odoo17_compatibility
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("📦 Module is ready for installation in Odoo 17")
        print("\nInstallation steps:")
        print("1. Copy module to Odoo addons directory")
        print("2. Restart Odoo server")
        print("3. Update Apps List")
        print("4. Install 'Invoice Templates' module")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please fix the issues before installation")
        sys.exit(1)

if __name__ == "__main__":
    main()
