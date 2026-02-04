#!/usr/bin/env python3
"""
Test script for Action Basin Dynamic Template Functionality

This script tests the dynamic features of the Action Basin invoice template
to ensure all customizable fields work correctly.
"""

import os
import sys
import xml.etree.ElementTree as ET

def test_template_model_fields():
    """Test that the invoice template model has all required dynamic fields"""
    print("🧪 Testing Invoice Template Model Fields...")
    
    # Check if the model file exists and has the required fields
    model_path = "models/invoice_template.py"
    if not os.path.exists(model_path):
        print("❌ Invoice template model file not found")
        return False
    
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_fields = [
        'company_name_override',
        'ta_field',
        'show_ta_field',
        'show_subject_field',
        'show_banking_details',
        'usd_banking_title',
        'zig_banking_title',
        'usd_bank_name',
        'usd_account_name',
        'usd_account_number',
        'zig_bank_name',
        'zig_account_name',
        'zig_account_number',
        'ecocash_title',
        'ecocash_number',
        'show_ecocash',
        'terms_conditions',
        'show_terms_conditions',
        'eoe_title',
        'eoe_text',
        'show_eoe',
        'footer_message',
        'show_footer_message'
    ]
    
    missing_fields = []
    for field in required_fields:
        if f"{field} = fields." not in content:
            missing_fields.append(field)
    
    if missing_fields:
        print(f"❌ Missing fields in template model: {', '.join(missing_fields)}")
        return False
    
    print("✅ All required dynamic fields found in template model")
    return True

def test_account_move_subject_field():
    """Test that the account move model has the subject field"""
    print("🧪 Testing Account Move Subject Field...")
    
    model_path = "models/account_move.py"
    if not os.path.exists(model_path):
        print("❌ Account move model file not found")
        return False
    
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "invoice_subject = fields.Char" not in content:
        print("❌ invoice_subject field not found in account move model")
        return False
    
    print("✅ invoice_subject field found in account move model")
    return True

def test_template_xml_dynamic_content():
    """Test that the Action Basin template XML uses dynamic fields"""
    print("🧪 Testing Action Basin Template XML Dynamic Content...")
    
    template_path = "report/invoice_template_action_basin.xml"
    if not os.path.exists(template_path):
        print("❌ Action Basin template XML file not found")
        return False
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for dynamic template variable
        if 't-set="template" t-value="o.invoice_template_id"' not in content:
            print("❌ Template variable not set in XML")
            return False
        
        # Check for dynamic company name
        if 'template.company_name_override' not in content:
            print("❌ Dynamic company name not implemented")
            return False
        
        # Check for dynamic t/a field
        if 'template.show_ta_field' not in content or 'template.ta_field' not in content:
            print("❌ Dynamic t/a field not implemented")
            return False
        
        # Check for dynamic subject field
        if 'template.show_subject_field' not in content or 'o.invoice_subject' not in content:
            print("❌ Dynamic subject field not implemented")
            return False
        
        # Check for dynamic banking details
        if 'template.show_banking_details' not in content:
            print("❌ Dynamic banking details visibility not implemented")
            return False

        if 'template.usd_bank_name' not in content or 'template.zig_bank_name' not in content:
            print("❌ Dynamic banking details fields not implemented")
            return False

        # Check for dynamic banking titles
        if 'template.usd_banking_title' not in content or 'template.zig_banking_title' not in content:
            print("❌ Dynamic banking titles not implemented")
            return False
        
        # Check for dynamic terms & conditions
        if 'template.show_terms_conditions' not in content or 'template.terms_conditions' not in content:
            print("❌ Dynamic terms & conditions not implemented")
            return False
        
        # Check for dynamic E&OE
        if 'template.show_eoe' not in content or 'template.eoe_text' not in content:
            print("❌ Dynamic E&OE not implemented")
            return False

        # Check for dynamic E&OE title
        if 'template.eoe_title' not in content:
            print("❌ Dynamic E&OE title not implemented")
            return False
        
        # Check for dynamic EcoCash
        if 'template.show_ecocash' not in content or 'template.ecocash_number' not in content:
            print("❌ Dynamic EcoCash not implemented")
            return False

        # Check for dynamic EcoCash title
        if 'template.ecocash_title' not in content:
            print("❌ Dynamic EcoCash title not implemented")
            return False
        
        # Check for dynamic footer
        if 'template.show_footer_message' not in content or 'template.footer_message' not in content:
            print("❌ Dynamic footer message not implemented")
            return False
        
        print("✅ All dynamic content implemented in Action Basin template XML")
        return True
        
    except Exception as e:
        print(f"❌ Error reading Action Basin template XML: {e}")
        return False

def test_template_form_view():
    """Test that the template form view has Action Basin specific settings"""
    print("🧪 Testing Template Form View Settings...")
    
    view_path = "views/invoice_template_views.xml"
    if not os.path.exists(view_path):
        print("❌ Invoice template views file not found")
        return False
    
    try:
        with open(view_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for Action Basin specific notebook
        if 'invisible="code != \'action_basin\'"' not in content:
            print("❌ Action Basin specific settings notebook not found")
            return False
        
        # Check for settings pages
        if 'name="header_settings"' not in content:
            print("❌ Header settings page not found")
            return False
        
        if 'name="banking_details"' not in content:
            print("❌ Banking details settings page not found")
            return False
        
        if 'name="terms_footer"' not in content:
            print("❌ Terms & footer settings page not found")
            return False
        
        print("✅ Action Basin specific settings found in template form view")
        return True
        
    except Exception as e:
        print(f"❌ Error reading template views file: {e}")
        return False

def test_invoice_form_view():
    """Test that the invoice form view has the subject field"""
    print("🧪 Testing Invoice Form View Subject Field...")
    
    view_path = "views/account_move_views.xml"
    if not os.path.exists(view_path):
        print("❌ Account move views file not found")
        return False
    
    try:
        with open(view_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'name="invoice_subject"' not in content:
            print("❌ invoice_subject field not found in invoice form view")
            return False
        
        print("✅ invoice_subject field found in invoice form view")
        return True
        
    except Exception as e:
        print(f"❌ Error reading account move views file: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Action Basin Dynamic Template Tests\n")
    
    tests = [
        test_template_model_fields,
        test_account_move_subject_field,
        test_template_xml_dynamic_content,
        test_template_form_view,
        test_invoice_form_view
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Action Basin dynamic template is ready.")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
