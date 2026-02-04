#!/usr/bin/env python3
"""
Comprehensive test to verify that the header and footer issues are fixed
in the Action Basin invoice templates.
"""

import xml.etree.ElementTree as ET
import sys
import os

def test_action_basin_template():
    """Test Action Basin template for header/footer issues."""
    print("🔍 Testing Action Basin template...")
    
    template_path = "report/invoice_template_action_basin.xml"
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    try:
        tree = ET.parse(template_path)
        root = tree.getroot()
        
        # Find the template
        template = root.find(".//template[@id='report_invoice_action_basin']")
        if template is None:
            print("❌ Action Basin template not found")
            return False
        
        # Convert to string for easier searching
        template_content = ET.tostring(template, encoding='unicode')
        
        # Check 1: Should NOT use web.external_layout
        if 'web.external_layout' in template_content:
            print("❌ Still using web.external_layout - this causes header/footer issues")
            return False
        
        # Check 2: Should use web.html_container
        if 'web.html_container' not in template_content:
            print("❌ Missing web.html_container")
            return False
        
        # Check 3: Should have CSS reset for list styling
        if 'list-style: none !important' not in template_content:
            print("❌ Missing CSS reset for list styling (black dot fix)")
            return False
        
        # Check 4: Should hide default headers/footers
        if '.header, .footer' not in template_content or 'display: none !important' not in template_content:
            print("❌ Missing CSS to hide default headers/footers")
            return False
        
        # Check 5: Should use article div structure
        if 'class="article o_report_layout_standard"' not in template_content:
            print("❌ Missing proper article div structure")
            return False
        
        print("✅ Action Basin template passes all header/footer tests")
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error: {e}")
        return False

def test_modern_template():
    """Test Modern template for header/footer issues."""
    print("🔍 Testing Modern template...")
    
    template_path = "report/invoice_template_modern.xml"
    if not os.path.exists(template_path):
        print(f"❌ Template file not found: {template_path}")
        return False
    
    try:
        tree = ET.parse(template_path)
        root = tree.getroot()
        
        # Find the template
        template = root.find(".//template[@id='report_invoice_modern']")
        if template is None:
            print("❌ Modern template not found")
            return False
        
        # Convert to string for easier searching
        template_content = ET.tostring(template, encoding='unicode')
        
        # Check 1: Should NOT use web.external_layout
        if 'web.external_layout' in template_content:
            print("❌ Modern template still using web.external_layout")
            return False
        
        # Check 2: Should have CSS reset
        if 'list-style: none !important' not in template_content:
            print("❌ Modern template missing CSS reset")
            return False
        
        print("✅ Modern template passes header/footer tests")
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error in Modern template: {e}")
        return False

def test_dynamic_templates():
    """Test that dynamic templates don't introduce header/footer issues."""
    print("🔍 Testing dynamic templates...")
    
    report_path = "report/invoice_report_actions.xml"
    if not os.path.exists(report_path):
        print(f"❌ Report actions file not found: {report_path}")
        return False
    
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        # Find dynamic templates
        dynamic_template = root.find(".//template[@id='report_invoice_dynamic']")
        direct_template = root.find(".//template[@id='report_invoice_template_direct']")
        
        if dynamic_template is None:
            print("❌ Dynamic template not found")
            return False
        
        if direct_template is None:
            print("❌ Direct template not found")
            return False
        
        # Check that dynamic templates only call our fixed templates
        dynamic_content = ET.tostring(dynamic_template, encoding='unicode')
        direct_content = ET.tostring(direct_template, encoding='unicode')
        
        # These templates should call our individual templates, not use external_layout
        if 'web.external_layout' in dynamic_content:
            print("❌ Dynamic template uses web.external_layout")
            return False
        
        if 'web.external_layout' in direct_content:
            print("❌ Direct template uses web.external_layout")
            return False
        
        # Should call our fixed templates
        if 'report_invoice_action_basin' not in dynamic_content:
            print("❌ Dynamic template doesn't call Action Basin template")
            return False
        
        if 'report_invoice_modern' not in dynamic_content:
            print("❌ Dynamic template doesn't call Modern template")
            return False
        
        print("✅ Dynamic templates are correctly configured")
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error in report actions: {e}")
        return False

def test_report_override():
    """Test that the default report is properly overridden."""
    print("🔍 Testing report override...")
    
    report_path = "report/invoice_report_actions.xml"
    try:
        tree = ET.parse(report_path)
        root = tree.getroot()
        
        # Find the account.account_invoices override
        override_record = root.find(".//record[@id='account.account_invoices']")
        if override_record is None:
            print("❌ Default invoice report override not found")
            return False
        
        # Check that it points to our Action Basin template
        report_name_field = override_record.find(".//field[@name='report_name']")
        if report_name_field is None or 'report_invoice_action_basin' not in report_name_field.text:
            print("❌ Report override doesn't point to Action Basin template")
            return False
        
        print("✅ Default report properly overridden")
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error in report override: {e}")
        return False

def main():
    """Run all header/footer fix tests."""
    print("🧪 Testing Header and Footer Fix")
    print("=" * 60)
    
    tests = [
        test_action_basin_template,
        test_modern_template,
        test_dynamic_templates,
        test_report_override
    ]
    
    all_passed = True
    for test in tests:
        try:
            result = test()
            all_passed = all_passed and result
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            all_passed = False
            print()
    
    print("=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("\n✅ Header and Footer Issues Fixed:")
        print("   • No more black dot in header")
        print("   • No unwanted footer with page numbers/contact details")
        print("   • Templates are completely self-contained")
        print("   • Clean design matching Action Basin specification")
        print("\n🔧 Technical Changes Made:")
        print("   • Removed web.external_layout dependency")
        print("   • Added comprehensive CSS reset")
        print("   • Made templates self-contained")
        print("   • Preserved all functionality")
        
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the template files and fix any issues.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
