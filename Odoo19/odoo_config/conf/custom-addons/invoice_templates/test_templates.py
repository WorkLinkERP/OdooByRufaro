#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to verify invoice template functionality
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_template_override():
    """Test if the default invoice report is properly overridden"""
    print("🔍 Testing template override...")
    
    # Check if the override is in place
    report_file = 'report/invoice_report_actions.xml'
    if not os.path.exists(report_file):
        print("❌ Report actions file not found")
        return False
    
    try:
        tree = ET.parse(report_file)
        root = tree.getroot()
        
        # Look for the override record
        override_found = False
        for record in root.findall('.//record[@id="account.account_invoices"]'):
            override_found = True
            # Check if it points to our dynamic template
            for field in record.findall('.//field[@name="report_name"]'):
                if field.text == 'invoice_templates.report_invoice_dynamic':
                    print("✅ Default invoice report properly overridden")
                    return True
        
        if not override_found:
            print("❌ Default invoice report override not found")
            return False
            
    except Exception as e:
        print(f"❌ Error parsing report actions: {e}")
        return False
    
    return False

def test_dynamic_template():
    """Test if the dynamic template exists and is properly configured"""
    print("🔍 Testing dynamic template...")
    
    report_file = 'report/invoice_report_actions.xml'
    try:
        tree = ET.parse(report_file)
        root = tree.getroot()
        
        # Look for the dynamic template
        for template in root.findall('.//template[@id="report_invoice_dynamic"]'):
            # Check if it has the template switching logic
            template_content = ET.tostring(template, encoding='unicode')
            if 'get_invoice_template_report_name' in template_content:
                print("✅ Dynamic template properly configured")
                return True
        
        print("❌ Dynamic template not found or not properly configured")
        return False
        
    except Exception as e:
        print(f"❌ Error checking dynamic template: {e}")
        return False

def test_action_basin_template():
    """Test if the Action Basin template exists"""
    print("🔍 Testing Action Basin template...")
    
    template_file = 'report/invoice_template_action_basin.xml'
    if not os.path.exists(template_file):
        print("❌ Action Basin template file not found")
        return False
    
    try:
        tree = ET.parse(template_file)
        root = tree.getroot()
        
        # Look for the Action Basin template
        for template in root.findall('.//template[@id="report_invoice_action_basin"]'):
            template_content = ET.tostring(template, encoding='unicode')
            if 'action-basin-template' in template_content and 'INVOICE' in template_content:
                print("✅ Action Basin template found and properly structured")
                return True
        
        print("❌ Action Basin template not found or not properly structured")
        return False
        
    except Exception as e:
        print(f"❌ Error checking Action Basin template: {e}")
        return False

def test_template_data():
    """Test if template data records exist"""
    print("🔍 Testing template data records...")
    
    data_file = 'data/invoice_template_data.xml'
    if not os.path.exists(data_file):
        print("❌ Template data file not found")
        return False
    
    try:
        tree = ET.parse(data_file)
        root = tree.getroot()
        
        # Look for Action Basin template record
        action_basin_found = False
        for record in root.findall('.//record[@id="template_action_basin"]'):
            action_basin_found = True
            # Check if it has the correct report_name
            for field in record.findall('.//field[@name="report_name"]'):
                if field.text == 'invoice_templates.report_invoice_action_basin':
                    print("✅ Action Basin template data record properly configured")
                    return True
        
        if not action_basin_found:
            print("❌ Action Basin template data record not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking template data: {e}")
        return False
    
    return False

def test_css_assets():
    """Test if CSS assets are properly configured"""
    print("🔍 Testing CSS assets...")
    
    css_file = 'static/src/css/invoice_templates.css'
    if not os.path.exists(css_file):
        print("❌ CSS file not found")
        return False
    
    try:
        with open(css_file, 'r') as f:
            css_content = f.read()
        
        if '.action-basin-template' in css_content:
            print("✅ CSS assets properly configured")
            return True
        else:
            print("❌ Action Basin CSS classes not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking CSS assets: {e}")
        return False

def main():
    """Run all template tests"""
    print("🚀 Invoice Templates - Template System Test")
    print("=" * 50)
    
    tests = [
        test_template_override,
        test_dynamic_template,
        test_action_basin_template,
        test_template_data,
        test_css_assets
    ]
    
    all_passed = True
    for test in tests:
        if not test():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 ALL TEMPLATE TESTS PASSED!")
        print("📋 Template system is properly configured")
        print("\nNext steps:")
        print("1. Install the module in Odoo")
        print("2. Create an invoice and check the template field")
        print("3. Print the invoice to see the Action Basin template")
        print("4. Go to Accounting > Configuration > Invoice Templates to manage templates")
    else:
        print("❌ SOME TEMPLATE TESTS FAILED!")
        print("Please fix the issues before testing in Odoo")
        sys.exit(1)

if __name__ == "__main__":
    main()
